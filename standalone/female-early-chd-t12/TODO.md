# T12 audit follow-up To Do

Updated: 2026-09-11

This list starts after the active 718-case Paper1G T12 midpoint audit finishes. Do not interrupt the active batch to perform these items.

## 0. Done 2026-09-11 — runner no longer needs a public repository

- [x] Upload `run_t12_audit.py` to `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/assets/` (md5 `263a5317eb506084ec5f604c80db2380`, verified against the repository copy).
- [x] Notebook v1.1.2 reads the runner from that Drive asset and prints source plus sha256; the GitHub raw URL is now only a fallback.
- [x] Correct the README, which still described the runner as coming from Drive after v1.1.1 had moved it to GitHub.
- [ ] When `run_t12_audit.py` changes, re-upload it to Drive. Cell 1 prefers the Drive asset and will otherwise keep running the older copy.

The batch that was active when this change was made is unaffected: its Cell 1 had already downloaded the runner to `/content`, and Cell 6 launches that local path without touching the network. The change takes effect on the next Cell 1 run.

## 0b. Pending — make this repository private once the batch finishes

Decided 2026-09-11 by 诸嵘. Policy: everything private except the personal site and pyobfus.

- [ ] Confirm the 718-case batch has finished and its Drive records are preserved (§1 first item).
- [ ] Flip `zhurong2020/claude-colab-projects` to private.
- [ ] In Colab, authorise GitHub private-repository access before reopening this notebook. The `colab.research.google.com/github/...` links do not work on a private repo until that is granted.
- [ ] Re-run Cell 1 once and confirm it prints `Runner from Drive ...`, not the GitHub fallback.

The blocker that made this unsafe was cleared in §0: the runner now comes from Drive. Flipping earlier would have left a mid-batch reconnect unable to resume.

Open question, not a blocker: this repository also holds a general Colab integration guide under an MIT licence, which has reuse value outside this research. Making the whole repository private gives that up. Splitting the research `standalone/` tasks into a private repo would keep both, at the cost of more setup. Recorded in `home/archives/project_docs/GITHUB_VISIBILITY_INVENTORY.md`.

## 1. Close and validate the active audit

- [ ] Preserve `results.csv`, `case_task_events.jsonl`, session provenance and resource telemetry from Drive.
- [ ] Confirm 718 unique manifest IDs and classify outcomes as `SUCCESS`, terminal `QC_ERROR`, or retryable `PROCESS_ERROR`.
- [ ] Re-run only `PROCESS_ERROR` cases. Do not repeatedly run deterministic `QC_ERROR` cases.
- [ ] Produce a case-level QC queue for empty historical T12 masks, ambiguous body components and T12 identity disagreement.
- [ ] Re-run representative QC and prior local-earlyoom cases with 1-5 second RSS/PSS/GPU sampling and `--keep-work`.

## 2. Reconcile muscle assets before any new segmentation

- [ ] Reconcile the 718 Paper1G IDs against the existing Drive/local `stage2_v2_abdominal_muscles_thin` inventory (reported 718/718, 727 MB) and its provenance sidecars.
- [ ] Reconcile against the existing `total` multilabel masks. The validated mapping records `autochthon_left/right` as labels 86/87; verify that these correspond to the intended Paper1A/Paper5 paraspinal definition before calling them erector spinae.
- [ ] Generate a PHI-free machine-readable reconciliation table for the 43 historical explicit-mask gaps, including cohort branch, availability in each alternative mask inventory and final disposition.
- [ ] Do not launch a 43-case `abdominal_muscles` rerun unless the two existing mask inventories fail checksum/readability/task-map QC.

## 3. Recompute muscle measurements at the corrected T12 slice

- [ ] Use the audit `new_slice`, not the historical whole-vertebra midpoint.
- [ ] Recompute total skeletal-muscle area/density from the existing 718/718 `tissue_4types_skeletal_muscle` masks.
- [ ] After semantic sign-off, recompute left/right paraspinal area, combined area, HU, LAM/NAM and myosteatosis measures from an existing validated mask source.
- [ ] Keep old and corrected-slice variables side by side; never overwrite V5.2-V5.2.4.
- [ ] Freeze a dated derived table, data dictionary, mask provenance and QC report before Paper1A/Paper5/radiomics reuse.

## 4. Mask-retention policy

- [ ] Record that the active notebook v1.1.0 deletes successful per-case `vertebrae_body` and `vertebrae_pp` scratch directories after checkpointing; it does not persist newly generated masks to Drive.
- [ ] Treat the scalar `new_slice` and audit fields as sufficient for routine corrected-slice tissue measurement using existing tissue/muscle masks.
- [ ] For QC errors, T12-disagreement cases and a representative validation sample, rerun with `--keep-work` and archive `vertebrae_body.nii.gz`, `vertebrae_pp/vertebrae_T12.nii.gz`, task logs and checksums.
- [ ] Before any future full inference, add an opt-in minimal-mask archive mode that retains only the two T12-relevant masks. Do not upload all C1-L5 `vertebrae_pp` files unless a defined analysis requires them.

## 5. Compute-unit and session strategy

- [ ] Batch compatible work into one Colab session so environment installation, model-cache restore, Drive enumeration and CT staging occur once.
- [ ] Keep TotalSegmentator inference serial on a single GPU. Do not run concurrent cases without telemetry-supported evidence of lower CU per completed case.
- [ ] Run mask-only scalar extraction serially on standard CPU/RAM when no inference is required.
- [ ] Use T4 High-RAM for `abdominal_muscles` inference until peak telemetry proves a cheaper tier safe; use A100 only if a timed pilot shows lower total CU per successful case.
- [ ] Compare configurations using `CU per successful case`, wall time, peak PSS and failure rate, rather than GPU/RAM utilization alone.
- [ ] Reuse the existing TotalSegmentator weight cache and use just-in-time local scratch copies; retain atomic per-case checkpoints on Drive.

## 6. Paper boundaries

- [ ] Paper1G: complete corrected T12 VFA audit/refit gate; muscle is not a required current-model covariate.
- [ ] Paper1A/Paper5/radiomics: require corrected-slice muscle reconciliation before using a new unified body-composition dataset.
- [ ] Preserve the 720-source/718-analysis distinction and the malignancy-lock exclusions in every derived manifest.

## 7. Documentation closeout

- [ ] Update `ASSET_AND_RUN_STATUS_20260911.md` with final outcome counts, elapsed time, CU estimate, resource peaks and Drive artifact checksums.
- [ ] Record the selected muscle-mask definition and rejected alternatives after semantic review.
- [ ] Mark completed checklist items with dated evidence links; do not delete historical decisions.
