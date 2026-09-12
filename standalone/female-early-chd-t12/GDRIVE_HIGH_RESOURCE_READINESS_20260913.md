# Google Drive high-resource readiness inventory

Verified: 2026-09-13 via the configured `rclone` `gdrive:` remote

## Decision summary

Do not upload or launch a broad 718-case muscle batch. The principal CT and mask
assets already exist on Drive, and the expensive reusable mask collections should
be consumed locally/serially. Only a frozen missing-only or controlled resource
micro-run should return to a paid GPU runtime.

| Needed work | Drive asset | Observed inventory | Disposition |
|---|---|---:|---|
| Paper1G thin CT, new branch | `cardiac_colab/data/female_new_thin/` | 372 objects, 32.26 GiB; manifest uses 371 cases | present; no upload |
| Paper1G legacy thin CT | `cardiac_colab/data/sr_training/` | 8,279 objects, 406.08 GiB shared source tree | present; use manifest/files-from; no bulk upload |
| Corrected-slice skeletal muscle | existing `tissue_4types` collections plus D mirror | 718/718 reported for active manifest | local CPU extraction; no inference upload |
| Erector/transversospinalis | `cardiac_colab/output/stage2_v2_abdominal_muscles_thin/` | 724 objects, 715.62 MiB | Drive/D checksum-identical; ID audit is 716/718, not 718/718 |
| Alternative thin muscle masks | `muscle_female_new_thin/` + `muscle_legacy_thin/` | 377 + 353 objects; 365.17 + 346.33 MiB | existing 371+346 scientific line; no repeat upload |
| Thoracic/shoulder muscle | `stage2_v2_thigh_shoulder_thin/` | 724 objects, 488.49 MiB | already present; do not rerun without a new scientific endpoint |
| Legacy tissue-4-types subset | `q1_legacy_tissue4types_thin/` | 191 objects, 411.19 MiB | partial legacy cache; use canonical local/Drive manifest rather than count alone |
| T12 selective review evidence | `t12_midpoint_audit_20260911/selective_qc_20260912/` | 255 cases complete | backed up locally and to D; no upload |

## Exact gaps and duplicates

The Stage-2-v2 directory has 718 mask IDs, but it is not an exact match to the
current 718-record Paper1G manifest. Current IDs `10304520` and `11412977` are
missing, while `10950884` and `7219352` are extra for this cohort. Thus directory
counts alone concealed a two-for-two membership substitution. All 716 matched masks
are readable, have matching provenance task text, and contain nonzero labels 15-18
(`erector_spinae_right/left`, `transversospinalis_right/left`).

Both Stage-2-v2-missing cases retain historical bilateral explicit erector masks;
conversely, all 43 historical explicit-mask gaps have readable Stage-2-v2 masks.
The union is 718/718, so there is no genuine missing-mask queue. Before any optional
two-case version-harmonisation run, verify that each input is the intended thin CT,
that each remains eligible, and that a uniform segmentation version is a
prespecified requirement. Existing extra masks are retained with provenance; they
are not silently renamed or substituted.

## Economical serial queue

1. Complete the 6-12-case resource micro-experiment only after its immutable
   manifest and lower-tier comparison are ready.
2. Omit muscle inference by default. Consider the two Stage-2-v2 version gaps only
   if scientific analysis requires a uniform mask model across all 718.
3. Copy only selected inputs to Colab scratch just in time; keep TotalSegmentator
   inference serial and reuse the existing model cache.
4. Return small checkpoints/masks/logs to Drive at case boundaries. Perform
   corrected-slice scalar extraction and radiomics locally on CPU from the retained
   masks.
5. Do not append North, Older-PCI, NLST, ZAL or training workloads merely to use an
   active runtime. Their manifests, eligibility and scientific priorities are
   separate decision gates.

This is an inventory/readiness assessment, not authorization to start a paid Colab
job or to delete apparent duplicate assets.
