#!/usr/bin/env python3
"""Build a deterministic selective T12 QC rerun manifest after the full pass."""

import argparse, csv, hashlib
from pathlib import Path

def number(value):
    try: return float(value)
    except (TypeError, ValueError): return None

def stable_key(seed, patient):
    return hashlib.sha256(f"{seed}|{patient}".encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results",type=Path,required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--controls",type=int,default=40)
    ap.add_argument("--seed",default="t12-qc-20260912")
    ap.add_argument("--prior-cases",type=Path)
    a=ap.parse_args()
    results={r["patientingroupid"]:r for r in csv.DictReader(a.results.open())}
    manifest=list(csv.DictReader(a.manifest.open()))
    prior=set()
    if a.prior_cases and a.prior_cases.exists():
        prior={x.strip() for x in a.prior_cases.read_text().splitlines() if x.strip() and not x.startswith("#")}
    reasons={}
    def add(pid,reason): reasons.setdefault(pid,[]).append(reason)
    controls=[]
    for row in manifest:
        pid=row["patientingroupid"]; r=results.get(pid,{})
        if r.get("status")=="QC_ERROR": add(pid,"qc_error")
        if r.get("status")=="SUCCESS" and r.get("pp_t12_agreement") in {"0","0.0"}: add(pid,"pp_disagreement")
        rel=number(r.get("relative_vfa_change"))
        if r.get("status")=="SUCCESS" and rel is not None and abs(rel)>=.20: add(pid,"absolute_relative_vfa_change_ge_20pct")
        if pid in prior or row.get("case_id") in prior: add(pid,"prior_local_interruption_case")
        if r.get("status")=="SUCCESS" and r.get("pp_t12_agreement") in {"1","1.0"} and rel is not None and abs(rel)<.20:
            stratum=(row.get("cohort_source",""),row.get("stenosis_group","")); controls.append((stratum,stable_key(a.seed,pid),pid))
    # Round-robin over strata after deterministic within-stratum hashing.
    pools={}
    for stratum,key,pid in controls: pools.setdefault(stratum,[]).append((key,pid))
    for pool in pools.values(): pool.sort()
    while sum("hash_stratified_control" in x for x in reasons.values())<a.controls and any(pools.values()):
        for stratum in sorted(pools):
            if pools[stratum] and sum("hash_stratified_control" in x for x in reasons.values())<a.controls:
                _,pid=pools[stratum].pop(0); add(pid,"hash_stratified_control")
    selected=[]
    for row in manifest:
        pid=row["patientingroupid"]
        if pid in reasons:
            out=dict(row); out["rerun_reason"]=";".join(sorted(set(reasons[pid]))); out["selection_seed"]=a.seed; selected.append(out)
    assert len({r["patientingroupid"] for r in selected})==len(selected)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    fields=list(manifest[0])+["rerun_reason","selection_seed"]
    with a.output.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(selected)
    print(f"selected={len(selected)} controls={sum('hash_stratified_control' in r['rerun_reason'] for r in selected)} output={a.output}")

if __name__=="__main__": main()
