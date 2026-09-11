# Female Early CHD T12 midpoint audit

This directory is the GitHub launch point for the full-cohort T12 vertebral-body midpoint audit.

## Open in Colab

[Open the T12 audit notebook in Colab](https://colab.research.google.com/github/zhurong2020/claude-colab-projects/blob/main/standalone/female-early-chd-t12/20260911_t12_midpoint_audit_colab.ipynb)

Manual selection:

1. In Colab, choose **File > Open notebook > GitHub**.
2. Enter `zhurong2020/claude-colab-projects`.
3. Select branch `main`.
4. Open `standalone/female-early-chd-t12/20260911_t12_midpoint_audit_colab.ipynb`.
5. In Colab's Secrets panel, add `TOTALSEG_LICENSE`, paste the academic license number and enable notebook access.
6. Use a T4 GPU with High-RAM and run all cells in Chrome.

The notebook reads its runner, manifest, historical masks and checkpoint from the authenticated user's `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/` tree. No patient-level manifest, mask, checkpoint or CT volume is stored in this public repository.

Each pending CT is copied just in time from Drive to Colab local scratch before TotalSegmentator runs, then removed after the patient result is checkpointed. The 718-case historical-mask archive is extracted once to `/content`, so inference does not repeatedly read large NIfTI inputs directly through Drive FUSE.

The runtime is pinned to TotalSegmentator 2.18.0, matching the locally validated environment. Startup checks require both `vertebrae_body` and `vertebrae_pp` before the smoke test begins; older releases such as 2.11.0 do not expose `vertebrae_pp`.

The Drive inventory was checked before transfer. Existing cohort CT files were reused; only one genuinely missing CT and the task-specific mask archive were uploaded.
