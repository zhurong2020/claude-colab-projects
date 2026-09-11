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
6. Use a T4 GPU with High-RAM and run all cells in Chrome.

The notebook reads its runner, manifest, historical masks and checkpoint from the authenticated user's `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/` tree. No patient-level manifest, mask, checkpoint or CT volume is stored in this repository.

### Runner source and repository visibility

From notebook v1.1.2, Cell 1 copies the runner from `assets/run_t12_audit.py` on Drive and prints the source and its sha256. It falls back to the GitHub raw URL only when that asset is absent.

This matters because v1.1.1 fetched the runner from an unauthenticated `raw.githubusercontent.com` URL. That call returns 404 the moment this repository stops being public, so a runtime reconnect part way through a long batch would have been unable to resume. **The notebook no longer depends on this repository being public.**

Keep the two copies in step. When `run_t12_audit.py` changes here, upload it to Drive as well, or Cell 1 will silently keep using the older asset. The printed sha256 is how you tell which one ran.

Each pending CT is copied just in time from Drive to Colab local scratch before TotalSegmentator runs, then removed after the patient result is checkpointed. The 718-case historical-mask archive is extracted once to `/content`, so inference does not repeatedly read large NIfTI inputs directly through Drive FUSE.

The batch writes an atomic per-case checkpoint to Drive. `SUCCESS` and deterministic `QC_ERROR` records are terminal on resume; `PROCESS_ERROR` records are retried. A 30-second resource sampler writes host RAM, process-tree RSS, GPU utilization/VRAM and scratch space directly to Drive and closes the file after every sample, while a JSONL event stream records case/task boundaries and return codes. This preserves useful evidence even if the Colab runtime is later reclaimed.

Persistent run records are written under `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/`: `output/results.csv`, `logs/resource_telemetry.csv`, `logs/case_task_events.jsonl`, `logs/session_provenance.json`, and the final `logs/RESOURCE_SUMMARY.md`. TotalSegmentator progress bars are suppressed from the notebook display; concise per-task durations and per-case status remain visible.

Verified cohort, muscle-asset, mask-retention and earlyoom findings are recorded in [`ASSET_AND_RUN_STATUS_20260911.md`](ASSET_AND_RUN_STATUS_20260911.md). Post-run asset reconciliation, corrected-slice muscle work, selective mask retention and CU-efficient scheduling are tracked separately in [`TODO.md`](TODO.md).

The runtime is pinned to TotalSegmentator 2.18.0, matching the locally validated environment. Startup checks require both `vertebrae_body` and `vertebrae_pp` before the smoke test begins; older releases such as 2.11.0 do not expose `vertebrae_pp`.

The Drive inventory was checked before transfer. Existing cohort CT files were reused; only one genuinely missing CT and the task-specific mask archive were uploaded.
