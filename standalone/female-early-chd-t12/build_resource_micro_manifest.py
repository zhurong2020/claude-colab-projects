#!/usr/bin/env python3
"""Build an immutable 6-12 case resource-reproduction manifest.

Selection is deterministic and combines named prior interruptions with high-PSS,
long-runtime, large-input and long-z cases from the completed production records.
The output must be reviewed and hashed before any paid runtime is started.
"""

import argparse
import csv
from pathlib import Path

import pandas as pd


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--telemetry", type=Path, required=True)
    p.add_argument("--prior-interruption", action="append", default=[])
    p.add_argument("--count", type=int, default=12, choices=range(6, 13))
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    manifest = pd.read_csv(args.manifest, dtype={"case_id": str})
    results = pd.read_csv(args.results, dtype={"case_id": str})
    tele = pd.read_csv(args.telemetry, dtype={"active_case_id": str})
    peaks = tele.groupby("active_case_id", dropna=True)["tree_pss_gib"].max()
    data = manifest.merge(results[["case_id", "case_seconds", "input_bytes", "input_size_xyz", "input_spacing_xyz"]], on="case_id", how="left")
    data["peak_tree_pss_gib"] = data.case_id.map(peaks)
    data["z_slices"] = pd.to_numeric(data.input_size_xyz.str.rsplit("x").str[-1], errors="coerce")

    selected = {}
    def take(ids, reason, quota=None):
        if len(selected) >= args.count:
            return
        added = 0
        for case_id in ids:
            if case_id in set(data.case_id) and case_id not in selected:
                selected[case_id] = reason
                added += 1
                if len(selected) >= args.count:
                    return
                if quota is not None and added >= quota:
                    return

    take(args.prior_interruption, "prior_local_interruption")
    for column, reason in [
        ("peak_tree_pss_gib", "high_observed_pss"),
        ("case_seconds", "long_runtime"),
        ("input_bytes", "large_input"),
        ("z_slices", "long_z"),
    ]:
        take(data.sort_values([column, "case_id"], ascending=[False, True]).case_id, reason, quota=3)
    take(data.sort_values(["peak_tree_pss_gib", "case_id"], ascending=[False, True]).case_id,
         "high_observed_pss_fill")
    chosen = data[data.case_id.isin(selected)].copy()
    chosen["required_reason"] = chosen.case_id.map(selected)
    chosen["micro_manifest_version"] = "1.0.0"
    chosen = chosen.sort_values("case_id")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    chosen.to_csv(args.out, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"wrote {args.out}: {len(chosen)} cases")
    print(chosen[["case_id", "required_reason", "peak_tree_pss_gib", "case_seconds", "input_size_xyz"]].to_string(index=False))


if __name__ == "__main__":
    main()
