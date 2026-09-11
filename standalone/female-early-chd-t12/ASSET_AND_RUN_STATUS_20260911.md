# Paper1G T12 Colab asset and run status

Last verified: 2026-09-11

## Scope and cohort

- The active manifest contains 718 analysis-eligible records derived from `female_baseline_wide_table_V5.2.4_FINAL_720_20260911__his_dates_confirmed.csv`.
- The 720-source versus 718-analysis distinction reflects the locked malignancy disposition and must be retained in downstream tables and manifests.
- The active computation is the Paper1G T12 vertebral-body-midpoint VFA audit. It does not recompute muscle measurements.

## Historical and current T12 methods

- The historical pipeline used TotalSegmentator v2.12.0 tasks `total`, `tissue_4_types`, and `abdominal_muscles`.
- The current audit uses TotalSegmentator v2.18.0 `vertebrae_body` plus `vertebrae_pp` to derive a body-centered slice and independently arbitrate T12 identity.
- Paper1G currently uses corrected T12 visceral-fat area as an adjustment variable. Muscle is not a required covariate in the current Paper1G model.

## Muscle asset findings

- In the V5.2.4 720-row wide table, the standard total/paraspinal muscle area and density fields have 636/720 non-missing values.
- Across the active 718-case manifest, `tissue_4types_skeletal_muscle.nii.gz` exists for 718/718 cases.
- The old per-case label trees contain explicit `erector_spinae_left/right.nii.gz` files for 675/718 cases.
- The 43 explicit-mask gaps comprise 42 `female_new` and one `original_735` case. All 43 also lack old VFA and standard total-muscle density values; this pattern is an incomplete historical processing branch, not a research exclusion.
- A separate Stage 2 v2 `abdominal_muscles` mask inventory was completed at 718/718 on 2026-05-29 and is mirrored on Drive and local disk (about 720 MiB). Existing `total` multilabel masks also support the validated `autochthon_left/right` labels 86/87 for 717 valid cases.
- `autochthon`, erector-spinae and the manuscripts' broader paraspinal compartment must not be treated as interchangeable until a task-map and anatomical-definition review is signed off.

## Active Colab behavior

- Notebook v1.1.0 was used to start the active long batch. It stages CTs on Colab local scratch and atomically updates the Drive checkpoint after every completed case.
- `SUCCESS` and deterministic `QC_ERROR` records are terminal; `PROCESS_ERROR` is retryable.
- The active v1.1.0 runner deletes successful and QC per-case scratch directories after checkpointing. Newly generated `vertebrae_body` and `vertebrae_pp` masks are therefore not retained on Drive.
- This does not prevent corrected-slice fat or muscle measurement because the scalar `new_slice`, original CT and existing tissue masks are sufficient. Mask-level review cases must be rerun selectively with retention enabled.
- Notebook v1.1.1 fixes Drive telemetry durability by closing the telemetry file after every 30-second sample. It applies to future sessions and does not alter the already-running v1.1.0 process.

## Confirmed local earlyoom incident

- On the local 18 GiB host, `earlyoom` crossed its 20% available-memory threshold on 2026-09-11 at 18:48.
- It sent SIGTERM to multiple TotalSegmentator/nnU-Net processes reporting about 7.3-7.7 GiB RSS while instantaneous available RAM fell as low as about 2.25 GiB.
- The earlier 60-second monitor missed the short peaks. This was an `earlyoom` termination, not a demonstrated CUDA OOM.

## Persistent Colab records

Drive root: `MyDrive/cardiac_colab/t12_midpoint_audit_20260911/`

- `output/results.csv`
- `logs/case_task_events.jsonl`
- `logs/session_provenance.json`
- `logs/resource_telemetry.csv` when the telemetry writer is visible/closed
- `logs/RESOURCE_SUMMARY.md` after a v1.1.x run completes Cell 7

## Evidence pointers

- Female_Early_CHD: `papers/paper1G/t12_audit/T12_PILOT_AUDIT_SUMMARY_20260911.md`
- Female_Early_CHD: `papers/paper5/docs/MUSCLE_HU_MYOSTEATOSIS_QC_20260604.md`
- cardiac-ml-research: `docs/project/MEMORY_MEASUREMENT_FINDINGS_20260910.md`
- cardiac-ml-research: `docs/project/sessions/2026-09/2026-09-02_patent_portfolio_full_audit.md`
- cardiac-ml-research: `docs/project/sessions/2026-09/2026-09-05_radiomics_thoracic_label_mapping_incident.md`
- vbca: `docs/RADIOMICS_AND_MULTI_ROI_ASSET_INDEX.md`
- vbca: `docs/sessions/2026-05/20260529_stage2_v2_abd_complete_and_pull.md`

Pending work is maintained separately in [`TODO.md`](TODO.md).
