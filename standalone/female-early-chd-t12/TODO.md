# T12 audit follow-up To Do

Updated: 2026-09-13

The 718-case production, 255-case evidence-retention pass and 12-case resource
micro-run are complete and frozen in separate namespaces. No further paid Colab
run is currently indicated. The planned local CPU analyses are also complete; the
definitive T12 gate now requires blinded human anatomical adjudication.

## 2026-09-13 current priority gate

- [x] Complete and preserve the 255-case selective run: 151 SUCCESS, 104 QC_ERROR,
      0 process errors; 1,275 masks passed hash/readability checks.
- [x] Complete and preserve notebook v1.2.1's frozen 12-case resource run: 8
      SUCCESS, 4 QC_ERROR, 0 process errors. Case `10394779` reached 16.25 GiB PSS
      and 14.21 GiB USS, supporting local earlyoom host-memory intervention rather
      than CUDA OOM.
- [x] Reconcile muscle assets by ID, provenance, readability and labels. Historical
      explicit bilateral masks plus Stage2-v2 cover 718/718; no broad GPU rerun is
      warranted.
- [x] Complete the generated 255-case blinded panel/form package and its D-drive
      checksum mirror; human anatomical reading remains a manual gate.
- [x] Freeze and QC the local CPU corrected-slice muscle sidecar. Legacy Stage2
      masks are thin-series geometry and must be sampled by physical-coordinate
      mapping from the thick audit slice, never by copying the slice index.
- [x] Run the pre-adjudication VFA agreement and identical-complete-case Paper1G
      refit: 612 positive pairs, ICC(2,1)=0.9796; paired M3 TSH OR 1.374 old vs
      1.375 corrected. Do not promote corrected values until reader adjudication.
- [ ] After reader adjudication, freeze the definitive VFA field/dispositions and
      rerun all VFA-dependent models. This is the remaining scientific gate.

## Cold-start handoff after closing the 2026-09-12 session

This handoff has been superseded by the verified 2026-09-13 completion below. At
21:51 Asia/Shanghai, the active Colab selective run had 109/255 terminal rows
(66 `SUCCESS`, 43 `QC_ERROR`) and was processing ordinal 110. Drive held 110
minimal-mask directories, consistent with 109 completed cases plus the active case.
Mean completed-case time was 67.3 seconds and the snapshot ETA was about 2.7 hours.
This is a timestamped snapshot, not a completion claim.

On the next Codex cold start, do these actions first, in order:

1. Query Drive `selective_qc_20260912/results.csv`, the last task event, current
   minimal-mask directory count and the session telemetry timestamp. Do not use the
   known-bad v1.2.0 telemetry `checkpoint_rows` field.
2. If fewer than 255 terminal rows and events are still advancing, leave Colab alone
   and report the new ETA. If progress is stale, inspect the final task event and
   Colab runtime state before deciding whether checkpoint resume is required.
3. If 255/255 is complete, immediately freeze the selective checkpoint, events,
   provenance, telemetry, resource summary and minimal-mask tree to a new local
   gitignored snapshot; generate hashes; then mirror and checksum-verify it on D drive.
4. Reconcile row IDs, mask-directory IDs and the frozen 255-row manifest; classify
   SUCCESS/QC/PROCESS_ERROR, missing archives and termination signals. Only after
   this integrity gate should anatomical review material or downstream work begin.
5. Start §5a's conditional serial closeout queue: first the 6-12 case explicit
   local-interruption resource micro-run, then ID/checksum/readability/task-map
   reconciliation of existing muscle assets, and only then a missing-only GPU
   manifest if any true gap remains. Do not create a broad erector rerun by default.

## 0. Done 2026-09-11 — runner no longer needs a public repository

- [x] Upload `run_t12_audit.py` to `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/assets/` (md5 `263a5317eb506084ec5f604c80db2380`, verified against the repository copy).
- [x] Notebook v1.1.2 reads the runner from that Drive asset and prints source plus sha256; the GitHub raw URL is now only a fallback.
- [x] Correct the README, which still described the runner as coming from Drive after v1.1.1 had moved it to GitHub.
- [x] Re-upload v1.2.0 `run_t12_audit.py` to Drive (2026-09-12; md5 `6494df1a94f94158b9134b5287ecb49c`, verified after upload). The active v1.1.0 Cell 6 continues from its already-loaded `/content` copy; the new runner applies only after reconnect/restart.

The batch that was active when this change was made is unaffected: its Cell 1 had already downloaded the runner to `/content`, and Cell 6 launches that local path without touching the network. The change takes effect on the next Cell 1 run.

## 0b. Pending — make this repository private once the batch finishes

Decided 2026-09-11 by 诸嵘. Policy: everything private except the personal site and pyobfus.

- [x] Confirm the 718-case batch has finished and its Drive records are preserved (§1 first item; local + D-drive checksum-verified copies completed 2026-09-12).
- [ ] Flip `zhurong2020/claude-colab-projects` to private.
- [ ] In Colab, authorise GitHub private-repository access before reopening this notebook. The `colab.research.google.com/github/...` links do not work on a private repo until that is granted.
- [ ] Re-run Cell 1 once and confirm it prints `Runner from Drive ...`, not the GitHub fallback.

The blocker that made this unsafe was cleared in §0: the runner now comes from Drive. Flipping earlier would have left a mid-batch reconnect unable to resume.

Open question, not a blocker: this repository also holds a general Colab integration guide under an MIT licence, which has reuse value outside this research. Making the whole repository private gives that up. Splitting the research `standalone/` tasks into a private repo would keep both, at the cost of more setup. Recorded in `home/archives/project_docs/GITHUB_VISIBILITY_INVENTORY.md`.

## 1. Close and validate the active audit

- [x] Preserve `results.csv`, all logs, session provenance, resource telemetry, active runner and manifest from Drive in the local gitignored final snapshot; generate SHA-256 inventory.
- [x] Confirm 718 unique manifest IDs: 614 `SUCCESS`, 104 terminal `QC_ERROR`, 0 retryable `PROCESS_ERROR`.
- [x] Confirm there are no `PROCESS_ERROR` cases to retry. Deterministic `QC_ERROR` cases enter the selective mask/adjudication workflow instead of blind retry.
- [x] Add a deterministic case-level QC/rerun manifest builder covering QC errors, T12 identity disagreement, >=20% change tails and stratified controls. Generate the actual manifest from the frozen final snapshot before the next Colab run.
- [x] Re-run representative QC and prior local-earlyoom cases with 1-5 second RSS/PSS/GPU sampling and retained minimal masks (v1.2.1 resource micro-run).
- [x] Launch the frozen 255-record selective run and verify independent checkpoint,
      events, five-mask archive plus per-case logs/checksums, and 5-second telemetry
      on Drive (verified after nine terminal records on 2026-09-12).
- [x] After the active run, create a separate immutable micro-manifest for explicit
      local interruption/resource-reproduction cases. The current 255-row manifest
      contains no explicit `prior_interruption` reason and excludes `10394779`; do
      not edit a running manifest.
- [x] Fix v1.2.0 telemetry `checkpoint_rows`: v1.2.1 uses the active mode checkpoint
      checkpoint during selective mode. The selective checkpoint itself is correct;
      only this monitor field is wrong. Use selective `results.csv` as progress SoT.

### 1c. Selective closeout completed 2026-09-13

- [x] Freeze and checksum the 255-case result, events, provenance, telemetry and
      minimal-mask archive locally and on D drive (2,048 matches; zero differences).
- [x] Reconcile 255 manifest/result/archive IDs and verify all 1,275 declared masks'
      hashes and NIfTI readability.
- [x] Summarise the 4.99-hour resource trace and preserve the raw 3,503 samples.
- [x] Fix the monitor checkpoint pointer before any future notebook version.
- [x] Run the separate 12-case local-interruption micro-experiment. It remains
      into the completed 255-case evidence set.
- [x] Build and freeze the 12-case resource manifest, including `10394779` plus
      high-PSS/long-runtime/large-input/long-z strata. Local SHA-256:
      `c3fdaddd3b9547f98a2f8f3ec1cf9aa6569ed6c8c05c794e0a53ef74348a7980`;
      Drive MD5 verified as `1d1f3c34f48620da34eda25f3546e5da`.
- [x] Add notebook v1.2.1 `resource_micro` mode with a separate checkpoint/events/
      minimal-mask namespace. Preparation is complete; no paid job was launched.

### 1a. Refined evidence design (decided 2026-09-12; do not interrupt the active batch)

The active v1.1.0 process already has its runner and monitor loaded in memory. Do
not restart it merely to improve telemetry. Its 30-second process-tree RSS series
remains an operational record, but RPR-01 has shown that RSS sums can double-count
shared pages and that this interval can miss short peaks. It is not a memory gold
standard.

- [x] For the selective post-run reruns, sample every **1-5 seconds** and record,
      side by side: process count, root RSS, process-tree RSS sum, process-tree PSS
      sum, process-tree USS sum, system available RAM, GPU utilisation/allocated
      memory, scratch usage and checkpoint count. Preserve the metric definitions.
- [x] Add `session_id`, monotonic elapsed time, active `case_id`, active task and
      sample sequence to telemetry so samples can be joined deterministically to
      `case_task_events.jsonl` across Colab reconnects.
- [x] Write high-frequency samples to Colab local disk first and atomically mirror
      them to Drive every 30-60 seconds plus at every task/case boundary. This limits
      Drive-FUSE overhead while bounding telemetry loss after runtime reclamation.
- [x] Extend task events with input shape, voxel spacing, input bytes, CT staging
      seconds, inference seconds, measurement/QC seconds, cleanup seconds, return
      code and termination signal where available. Derive per-case resource peaks
      by timestamp join; do not estimate them from console text.
- [x] Record explicitly that Colab dashboard/system RAM and PSS are feasible
      telemetry, not cgroup kernel gold standards. Do not use this production run
      as an independent accuracy-validation arm in RPR-01.

### 1b. Prespecified mask/QC retention sample

Because v1.1.0 deletes case work directories, create the review archive by a
selective rerun after the scalar checkpoint is complete:

**Why 255 cases are run again:** every one of the 255 is a subset of the already
completed 718-case cohort. The first pass computed and checkpointed scalar audit
fields but deliberately removed the new per-case TotalSegmentator work directories
to control Drive storage. The selective pass repeats inference only for cases with
high review value so it can retain T12-relevant masks, task logs, checksums and
5-second resource telemetry. It is not filling 255 unprocessed cases and must not
be added to 718 as a new denominator.

- [x] Freeze all `QC_ERROR` cases, all `pp_t12_agreement=0` cases, all positive
      pairs with absolute relative VFA change >=20%, and 40 controls (255 unique;
      one overlap). Explicit local earlyoom cases were not supplied and remain a
      separate micro-run TODO.
- [ ] Before inspecting images, select a deterministic hash-based stratified sample
      of apparently concordant cases across cohort source, scanner/geometry strata,
      stenosis group and scan-length bands. Freeze its manifest and hash.
- [x] Archive only the source T12 label, `vertebrae_body.nii.gz`, the relevant
      `vertebrae_pp` T11/T12/L1 masks, compact task logs, review image and checksums;
      do not upload every C1-L5 output by default.
- [ ] Have the anatomical reader adjudicate level identity and midpoint suitability
      without seeing coronary group or old/new VFA change. Use this as the reference
      for the T12 methods study; model agreement alone is not ground truth.
- [ ] Report failure and disagreement denominators separately. A successfully
      executed task is not automatically an anatomically valid measurement.

## 2. Reconcile muscle assets before any new segmentation

- [x] Reconcile the 718 Paper1G IDs against Drive/local
      `stage2_v2_abdominal_muscles_thin`. Result: 716/718 current IDs have readable,
      provenance-backed masks; Drive and D copies match. The apparent 718 count
      included two unrelated extras and omitted `10304520`, `11412977`.
- [ ] Reconcile against the existing `total` multilabel masks. The validated mapping records `autochthon_left/right` as labels 86/87; verify that these correspond to the intended Paper1A/Paper5 paraspinal definition before calling them erector spinae.
- [x] Generate a machine-readable reconciliation table under gitignored
      `720cases/t12_audit/muscle_asset_reconciliation_20260913.csv` plus aggregate
      JSON. It includes historical explicit-mask availability, Stage-2 presence,
      provenance, checksum, readability and labels 15-18.
- [x] Reject a 43-case broad rerun. The 43 historical gaps are all recovered by
      Stage-2-v2, and its two absent current IDs both have historical bilateral
      explicit masks: union coverage is 718/718. A two-case rerun is optional only
      if uniform model/version becomes a prespecified requirement; do not launch it
      automatically.

## 3. Recompute muscle measurements at the corrected T12 slice

- [x] Use the audit `new_slice`, not the historical whole-vertebra midpoint.
- [x] Recompute total skeletal-muscle area/density where an adjudicable corrected slice exists.
- [ ] After semantic sign-off, select erector labels 15/16 alone versus the broader paraspinal 15-18 union for Paper1A/Paper5 promotion. Both candidate sets are already in the sidecar.
- [x] Keep old and corrected-slice variables side by side; never overwrite V5.2-V5.2.4.
- [x] Freeze a dated pre-adjudication derived table, provenance and QC report. Final promotion remains reader/signoff gated.

## 4. Mask-retention policy

- [x] Record that the full-pass notebook deletes successful per-case scratch masks; the selective and micro namespaces retain minimal evidence instead.
- [x] Treat the scalar `new_slice` and audit fields as sufficient for routine corrected-slice tissue measurement using existing tissue/muscle masks.
- [x] For QC errors, T12-disagreement cases and representative controls, retain T12-relevant masks, task logs and checksums in the frozen 255-case package.
- [x] Add and exercise opt-in minimal-mask archive mode; it retains historical T12, body and PP T11/T12/L1 rather than all C1-L5 outputs.

## 5. Compute-unit and session strategy

- [ ] Batch compatible work into one Colab session so environment installation, model-cache restore, Drive enumeration and CT staging occur once.
- [ ] Keep TotalSegmentator inference serial on a single GPU. Do not run concurrent cases without telemetry-supported evidence of lower CU per completed case.
- [ ] Run mask-only scalar extraction serially on standard CPU/RAM when no inference is required.
- [ ] Use T4 High-RAM for `abdominal_muscles` inference until peak telemetry proves a cheaper tier safe; use A100 only if a timed pilot shows lower total CU per successful case.
- [ ] Compare configurations using `CU per successful case`, wall time, peak PSS and failure rate, rather than GPU/RAM utilization alone.
- [ ] Reuse the existing TotalSegmentator weight cache and use just-in-time local scratch copies; retain atomic per-case checkpoints on Drive.

### 5a. Conditional serial closeout queue after the 255-case run

Do not build or launch another broad segmentation notebook until the active selective
run is complete, backed up and reconciled. The next notebook, if still needed, must
be generated from the verified missing-work set rather than from historical TODO
counts.

1. **Close the active run:** freeze selective results, events, session provenance,
   telemetry, minimal masks and checksums; mirror them locally and to D drive.
2. **Run a 6-12 case resource micro-experiment:** include explicit local interruption
   cases such as `10394779` plus representative long/thin, thick and high-voxel
   scans. Compare only prespecified TotalSegmentator 2.18 muscle configurations and
   keep inference serial. This is a separate immutable manifest, not an amendment
   to the 255 cases.
3. **Reconcile before inference:** match all 718 Paper1G IDs against Drive and D-drive
   `stage2_v2_abdominal_muscles_thin`, the 717 thin muscle collection, existing
   `total` masks and provenance. Verify readability, non-empty labels and anatomical
   semantics. The historical 43 explicit-mask gaps are not evidence that 43 new
   segmentations are still missing.
4. **Generate a missing-only manifest:** run `abdominal_muscles` only for IDs proven
   absent, corrupt or semantically unusable after step 3. If the verified count is
   zero, omit this GPU stage entirely.
5. **Move downstream extraction off the GPU:** compute corrected-slice total muscle,
   erector, transversospinalis/paraspinal, HU and myosteatosis measures on standard
   CPU/local storage, retaining old and new variables side by side.
6. **Stop at decision gates:** Older-PCI no-coverage records, missing source NIfTI,
   thoracic visual-QC failures and dormant NLST batches are separate projects. Do
   not append them merely to consume a live High-RAM runtime; each needs a current
   scientific priority, complete input manifest and its own output namespace.

Current readiness snapshot: the 718 T12 CT inputs and 718 tissue masks are available;
Drive records 718 Stage-2-v2 `abdominal_muscles` masks, while the thin muscle/radiomics
line has 371 female_new + 346 legacy = 717 cases. These counts establish that broad
erector re-segmentation is probably unnecessary, but they do not replace the ID-level
checksum/readability/task-map reconciliation in step 3.

## 6. Paper boundaries

- [ ] Paper1G: complete corrected T12 VFA audit/refit gate; muscle is not a required current-model covariate.
- [ ] Paper1A/Paper5/radiomics: require corrected-slice muscle reconciliation before using a new unified body-composition dataset.
- [ ] Preserve the 720-source/718-analysis distinction and the malignancy-lock exclusions in every derived manifest.
- [ ] T12 methods paper may cite RPR-01 for memory-measurement limitations; RPR-01
      may use this campaign as a disclosed real-world workload. Shared run records
      must not be counted as independent validation in both papers.

## 7. Documentation closeout

- [x] Update `ASSET_AND_RUN_STATUS_20260911.md` with final outcome counts, backup locations, resource record summary and artifact checksums. Exact Colab CU consumption is not exposed in the exported run artifacts and must not be invented.
- [ ] Record the selected muscle-mask definition and rejected alternatives after semantic review.
- [ ] Mark completed checklist items with dated evidence links; do not delete historical decisions.
