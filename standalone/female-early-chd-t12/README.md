# Female Early CHD T12 midpoint audit

This directory is the GitHub launch point for the full-cohort T12 vertebral-body midpoint audit.

## Open in Colab

[Open the T12 audit notebook in Colab](https://colab.research.google.com/github/zhurong2020/claude-colab-projects/blob/main/standalone/female-early-chd-t12/20260911_t12_midpoint_audit_colab.ipynb?flush_cache=true)

Manual selection:

1. In Colab, choose **File > Open notebook > GitHub**.
2. Enter `zhurong2020/claude-colab-projects`.
3. Select branch `main`.
4. Open `standalone/female-early-chd-t12/20260911_t12_midpoint_audit_colab.ipynb`.
5. In Colab's Secrets panel, add `TOTALSEG_LICENSE`, paste the academic license number and enable notebook access.
6. In Cell 2 select `RUN_MODE`. Keep `full_resume` for the frozen full checkpoint;
   use `resource_micro` only for the reviewed 12-case experiment. Then select the
   intended runtime and run the cells in Chrome.

The notebook reads its runner, manifest, historical masks and checkpoint from the authenticated user's `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/` tree. No patient-level manifest, mask, checkpoint or CT volume is stored in this repository.

### Runner source and repository visibility

From notebook v1.1.2, Cell 1 copies the runner from `assets/run_t12_audit.py` on Drive and prints the source and its sha256. It falls back to the GitHub raw URL only when that asset is absent.

This matters because v1.1.1 fetched the runner from an unauthenticated `raw.githubusercontent.com` URL. That call returns 404 the moment this repository stops being public, so a runtime reconnect part way through a long batch would have been unable to resume. **The notebook no longer depends on this repository being public.**

Keep the two copies in step. When `run_t12_audit.py` changes here, upload it to Drive as well, or Cell 1 will silently keep using the older asset. The printed sha256 is how you tell which one ran.

Each pending CT is copied just in time from Drive to Colab local scratch before TotalSegmentator runs, then removed after the patient result is checkpointed. The 718-case historical-mask archive is extracted once to `/content`, so inference does not repeatedly read large NIfTI inputs directly through Drive FUSE.

The batch writes an atomic per-case checkpoint to Drive. `SUCCESS` and deterministic `QC_ERROR` records are terminal on resume; `PROCESS_ERROR` records are retried. Notebook v1.2.1 samples host RAM, process count, root/process-tree RSS, process-tree PSS/USS, GPU utilization/VRAM and scratch space every 5 seconds on local scratch. It atomically mirrors a session-specific CSV to Drive every 30 seconds and at case/task state changes. A JSONL event stream records session/case/task boundaries, timings, return codes and available termination signals. PSS/USS are sampled estimates, not a cgroup kernel gold standard.

Persistent full-run records are written under `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/`: `output/results.csv`, session-specific resource/provenance/summary files, and `logs/case_task_events.jsonl`. Selective reruns use the separate `selective_qc_20260912/` checkpoint, events, summaries and `minimal_masks/` tree. Smoke events and telemetry are also session-specific, so a new run does not overwrite or append to the completed-run evidence. TotalSegmentator progress bars are suppressed from the notebook display; concise per-task durations and per-case status remain visible.

The frozen selective cohort completed all 255 unique records (104 QC, 76 >=20% VFA-change,
36 PP-disagreement and 40 control memberships, with one overlapping membership).
It did not explicitly include local interruption case `10394779`. Notebook v1.2.1
adds an isolated `resource_micro` namespace and uses the frozen 12-case manifest in
Drive; it does not amend or overwrite the completed 255-case evidence. The v1.2.0
selective telemetry's stale `checkpoint_rows=718` field is retained as historical
evidence; v1.2.1 passes each selected mode's checkpoint to the monitor.

Verified cohort, muscle-asset, mask-retention and earlyoom findings are recorded in [`ASSET_AND_RUN_STATUS_20260911.md`](ASSET_AND_RUN_STATUS_20260911.md). Drive readiness and no-duplicate-upload decisions are in [`GDRIVE_HIGH_RESOURCE_READINESS_20260913.md`](GDRIVE_HIGH_RESOURCE_READINESS_20260913.md). Completed corrected-slice work, conditional future adjudication and the still-open RPR-01 positioning decision are tracked in [`TODO.md`](TODO.md).

The runtime is pinned to TotalSegmentator 2.18.0, matching the locally validated environment. Startup checks require both `vertebrae_body` and `vertebrae_pp` before the smoke test begins; older releases such as 2.11.0 do not expose `vertebrae_pp`.

The Drive inventory was checked before transfer. Existing cohort CT files were reused; only one genuinely missing CT and the task-specific mask archive were uploaded.
