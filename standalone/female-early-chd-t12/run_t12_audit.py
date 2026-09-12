#!/usr/bin/env python3
"""Checkpointed T12 midpoint audit with terminal QC and retryable process errors."""

import argparse, csv, hashlib, json, os, shutil, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import SimpleITK as sitk
from scipy import ndimage as ndi

TS = Path(os.environ.get("TOTALSEG_BIN", shutil.which("TotalSegmentator") or "TotalSegmentator"))
LEVELS = [f"vertebrae_T{i}" for i in range(1, 13)] + [f"vertebrae_L{i}" for i in range(1, 6)]
FIELDS = ["patientingroupid", "case_id", "status", "error", "cohort_source", "stenosis_group", "required_reason", "old_slice", "new_slice", "shift_mm", "old_vfa_mm2", "new_vfa_mm2", "relative_vfa_change", "body_voxels", "body_overlap_fraction", "body_components", "second_component_ratio", "pp_overlap_label", "pp_centroid_label", "pp_t12_agreement", "input_bytes", "input_size_xyz", "input_spacing_xyz", "stage_seconds", "measurement_seconds", "cleanup_seconds", "case_seconds"]

def now(): return datetime.now(timezone.utc).isoformat()
def arr(path): return sitk.GetArrayFromImage(sitk.ReadImage(str(path))) > 0

def event(path, **values):
    if not path: return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps({"timestamp_utc": now(), **values}, sort_keys=True) + "\n"); f.flush(); os.fsync(f.fileno())

def active_state(path, **values):
    if not path: return
    path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({"timestamp_utc": now(), **values}, sort_keys=True))
    os.replace(tmp, path)

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()

def midpoint(mask):
    z = np.flatnonzero(mask.any(axis=(1, 2)))
    if not len(z): raise ValueError("empty T12 mask")
    return int(z[len(z)//2])

def body_midpoint(level_path, body_path):
    level = arr(level_path); overlap = level & arr(body_path)
    cc, n = ndi.label(overlap); sizes = np.bincount(cc.ravel())[1:]
    if not len(sizes): raise ValueError("no T12/body overlap")
    order = np.argsort(sizes)[::-1]; ratio = sizes[order[1]] / sizes[order[0]] if len(order) > 1 else 0
    if ratio >= .25: raise ValueError(f"ambiguous body components ratio={ratio:.3f}")
    body = cc == order[0] + 1; z = np.flatnonzero(body.any(axis=(1, 2)))
    return int(np.floor(z[0] + .5*(z[-1]-z[0]) + .5)), int(body.sum()), float(body.sum()/level.sum()), int(n), float(ratio)

def pp_arbitrate(old, pp_dir):
    oz = float(np.where(old)[0].mean()); scores = []
    for name in LEVELS:
        p = pp_dir / f"{name}.nii.gz"
        if p.exists():
            x = arr(p)
            if x.any(): scores.append((name, int((old & x).sum()), abs(float(np.where(x)[0].mean())-oz)))
    if not scores: return "NONE", "NONE", False
    by_overlap = max(scores, key=lambda x: x[1])[0]; by_centroid = min(scores, key=lambda x: x[2])[0]
    return by_overlap, by_centroid, by_overlap == by_centroid == "vertebrae_T12"

def run_task(cmd, events, state, session_id, patient, case, task, log_dir):
    started = time.monotonic(); active_state(state, session_id=session_id, patientingroupid=patient, case_id=case, task=task, phase="inference")
    event(events, event="task_start", session_id=session_id, patientingroupid=patient, case_id=case, task=task)
    log_dir.mkdir(parents=True, exist_ok=True); task_log = log_dir/f"{task}.log"
    with task_log.open("w") as logf:
        proc = subprocess.run(cmd, stdout=logf, stderr=subprocess.STDOUT, text=True)
    rc = proc.returncode
    event(events, event="task_end", session_id=session_id, patientingroupid=patient, case_id=case, task=task, returncode=rc, termination_signal=(-rc if rc < 0 else None), elapsed_seconds=round(time.monotonic()-started, 3))
    print(f"  {task}: {time.monotonic()-started:.1f}s rc={rc}", flush=True)
    if rc:
        tail = task_log.read_text(errors="replace").splitlines()[-40:]
        raise RuntimeError(f"{task} rc={rc}; log_tail={' | '.join(tail)}")

def archive_minimal(case_out, old_level, archive_root, case):
    if not archive_root: return
    dst = archive_root/case; dst.mkdir(parents=True, exist_ok=True)
    wanted = [(old_level, "historical_vertebrae_T12.nii.gz"),
              (case_out/"vertebrae_body/vertebrae_body.nii.gz", "vertebrae_body.nii.gz")]
    for level in ("T11", "T12", "L1"):
        wanted.append((case_out/f"vertebrae_pp/vertebrae_{level}.nii.gz", f"vertebrae_pp_T{level[1:]}.nii.gz" if level.startswith("T") else "vertebrae_pp_L1.nii.gz"))
    for src, name in wanted:
        if src.is_file(): shutil.copy2(src, dst/name)
    if (case_out/"logs").is_dir(): shutil.copytree(case_out/"logs", dst/"logs", dirs_exist_ok=True)
    manifest = {p.name: {"bytes": p.stat().st_size, "sha256": sha256(p)} for p in dst.iterdir() if p.is_file()}
    (dst/"checksums.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))

def atomic_upsert(result, rec):
    prior = []
    if result.exists(): prior = [r for r in csv.DictReader(result.open()) if r["patientingroupid"] != rec["patientingroupid"]]
    tmp = result.with_suffix(result.suffix + ".tmp")
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(prior); w.writerow(rec); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, result)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--manifest", type=Path, required=True); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--checkpoint", type=Path, required=True); ap.add_argument("--events", type=Path); ap.add_argument("--active-state", type=Path); ap.add_argument("--session-id", default="unknown"); ap.add_argument("--minimal-archive", type=Path); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--keep-work", action="store_true")
    a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True); a.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(a.manifest.open()))[:a.limit or None]
    terminal = set()
    if a.checkpoint.exists(): terminal = {r["patientingroupid"] for r in csv.DictReader(a.checkpoint.open()) if r.get("status") in {"SUCCESS", "QC_ERROR"}}
    for i, row in enumerate(rows, 1):
        patient, case = row["patientingroupid"], row["case_id"]
        if patient in terminal: continue
        case_out = a.out/case; case_out.mkdir(exist_ok=True); local_ct = case_out/"input.nii.gz"
        case_started = time.monotonic(); rec = {k: row.get(k, "") for k in FIELDS}; rec.update(status="PROCESS_ERROR", error="")
        active_state(a.active_state, session_id=a.session_id, patientingroupid=patient, case_id=case, task="", phase="staging")
        event(a.events, event="case_start", session_id=a.session_id, patientingroupid=patient, case_id=case, ordinal=i, total=len(rows))
        try:
            stage_started = time.monotonic()
            if not local_ct.exists(): shutil.copy2(row["image_path"], local_ct)
            rec["stage_seconds"] = round(time.monotonic()-stage_started, 3); rec["input_bytes"] = local_ct.stat().st_size
            header = sitk.ReadImage(str(local_ct)); rec["input_size_xyz"] = "x".join(map(str, header.GetSize())); rec["input_spacing_xyz"] = "x".join(f"{x:.6g}" for x in header.GetSpacing())
            for task in ("vertebrae_body", "vertebrae_pp"):
                task_out = case_out/task; sentinel = task_out/("vertebrae_body.nii.gz" if task == "vertebrae_body" else "vertebrae_T12.nii.gz")
                if not sentinel.exists(): run_task([str(TS), "-i", str(local_ct), "-o", str(task_out), "-ta", task, "--device", "gpu"], a.events, a.active_state, a.session_id, patient, case, task, case_out/"logs")
            measure_started = time.monotonic(); active_state(a.active_state, session_id=a.session_id, patientingroupid=patient, case_id=case, task="", phase="measurement_qc")
            level = Path(row["label_dir"])/"vertebrae_T12.nii.gz"; torso = Path(row["label_dir"])/"tissue_4types_torso_fat.nii.gz"
            old = arr(level); oldz = midpoint(old)
            newz, bvox, frac, ncomp, ratio = body_midpoint(level, case_out/"vertebrae_body/vertebrae_body.nii.gz")
            ct_img = sitk.ReadImage(str(local_ct)); ct = sitk.GetArrayFromImage(ct_img); fat = arr(torso); area = ct_img.GetSpacing()[0]*ct_img.GetSpacing()[1]
            def vat(z): return float((fat[z] & (ct[z] >= -150) & (ct[z] <= -50)).sum()*area)
            ov, nr, agree = pp_arbitrate(old, case_out/"vertebrae_pp"); vo, vn = vat(oldz), vat(newz)
            rec.update(status="SUCCESS", old_slice=oldz, new_slice=newz, shift_mm=(newz-oldz)*ct_img.GetSpacing()[2], old_vfa_mm2=vo, new_vfa_mm2=vn, relative_vfa_change=((vn-vo)/vo if vo else np.nan), body_voxels=bvox, body_overlap_fraction=frac, body_components=ncomp, second_component_ratio=ratio, pp_overlap_label=ov, pp_centroid_label=nr, pp_t12_agreement=int(agree))
            rec["measurement_seconds"] = round(time.monotonic()-measure_started, 3)
        except (ValueError, IndexError) as exc:
            rec.update(status="QC_ERROR", error=repr(exc))
        except Exception as exc:
            rec.update(status="PROCESS_ERROR", error=repr(exc))
        rec["case_seconds"] = round(time.monotonic()-case_started, 3)
        atomic_upsert(a.checkpoint, rec)
        event(a.events, event="case_checkpoint", session_id=a.session_id, patientingroupid=patient, case_id=case, status=rec["status"], error=rec["error"], case_seconds=rec["case_seconds"])
        print(f"[{i}/{len(rows)}] {case} {rec['status']} shift={rec.get('shift_mm','')} rel={rec.get('relative_vfa_change','')}", flush=True)
        archive_minimal(case_out, Path(row["label_dir"])/"vertebrae_T12.nii.gz", a.minimal_archive, case)
        cleanup_started = time.monotonic(); active_state(a.active_state, session_id=a.session_id, patientingroupid=patient, case_id=case, task="", phase="cleanup")
        local_ct.unlink(missing_ok=True)
        if not a.keep_work: shutil.rmtree(case_out, ignore_errors=True)
        rec["cleanup_seconds"] = round(time.monotonic()-cleanup_started, 3); rec["case_seconds"] = round(time.monotonic()-case_started, 3)
        atomic_upsert(a.checkpoint, rec); event(a.events, event="case_end", session_id=a.session_id, patientingroupid=patient, case_id=case, status=rec["status"], error=rec["error"], cleanup_seconds=rec["cleanup_seconds"], case_seconds=rec["case_seconds"])

    active_state(a.active_state, session_id=a.session_id, patientingroupid="", case_id="", task="", phase="finished")

if __name__ == "__main__": main()
