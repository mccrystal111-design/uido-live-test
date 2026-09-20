# UiDo — Project Source of Truth

**Last updated:** 2026-09-21  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, completed work, current blockers, exact next step, and what must not be rebuilt.

## Current state

**Course data foundation: READY.** Overstone's authoritative OSM capture has been recovered, identity-locked and deterministically normalised. The provider-neutral course model and measured-registration tooling exist. Public EA source resolution is complete. **Raw EA raster/LAZ acquisition is still the remaining source-data gate.**

**Do not start another visual prototype.** The immediate priority is the public-source data/model pipeline.

## Core pipeline

`source capture -> deterministic normalisation -> provider-neutral course model -> measured OSM/satellite registration -> satellite refinement -> LiDAR enrichment -> verification/fusion -> phone/watch/renderers`

Data policy: **source preserved -> derived explicit -> verified -> never silently replaced**.

## Authoritative Overstone source

### Raw OSM — authoritative

Do not ask the user to re-upload the OSM capture.

- Library: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
- Library file id: `file_00000000e32481f4a00f707344416e79`
- SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- GitHub identity lock: `course-models/OVERSTONE_OSM_SOURCE_LOCK.json`
- GitHub manifest: `course-models/OVERSTONE_SOURCE_MANIFEST.json`

Source counts: 18 holes, 18 pins, 20 greens, 30 tees, 17 fairways, 31 bunkers, 23 rough, 17 paths, 2 water hazards, 1 driving range; 177 features total.

Only `golf=hole` features carry explicit `ref=1..18`. Other feature classes are not hole-numbered at source. Preserve them as source geometry; hole association must be spatial/derived, never inferred from feature order.

### Normalised source — authoritative derived artifact

- Library: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
- Library file id: `file_0000000052948210969af327286d4488`
- Schema: `uido.course.source-normalized.v0.1`
- SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
- Status: **complete**; source geometry unchanged; no invented hole assignments.

## Course model state

### GitHub canonical model

- `course-models/overstone-park-v0.1.json`
- Schema: `uido.course.v0.1`
- Contains all 18 green F/M/B anchors.
- Registration transform/metrics remain null until measured control points are used.

### Library discrepancy to preserve, not overwrite

Library contains a newer generated artifact:

- `/UiDo/UiDo_Overstone_Course_Model_v0.4.json`
- Schema/capture version: `0.4.0`
- Model status: `STRUCTURAL_MODEL_READY_IMAGERY_REFINEMENT_GATED`
- It contains source-preserving geometry plus derived hole associations and registration/refinement gates.

This v0.4 Library artifact is **not yet promoted as the GitHub canonical course model**. Do not delete or recreate it, and do not silently replace the GitHub v0.1 model with it. Reconcile the two explicitly when the next model promotion is undertaken.

## Existing tooling / work already completed

- `tools/course-model/build_overstone_model.py` — deterministic source normalisation.
- `tools/course-model/register_affine.py` — measured affine registration; reports residuals/RMS/max error.
- `tools/course-model/ea_source_acquisition.py` — EA catalogue resolver/acquisition adapter scaffold.
- `tools/course-model/resolve_overstone_public_sources.py` — public-source catalogue resolution.
- `course-models/OVERSTONE_ACQUISITION_MANIFEST.json` — acquisition manifest.
- `course-models/OVERSTONE_PUBLIC_SOURCE_RESOLUTION.json` — exact resolved EA source records.
- `docs/OVERSTONE_DATASET_PROCESSING.md` — dataset processing rules.
- `docs/UI_DO_COURSE_MODEL_V0.1.md` and related extraction/pixel/provenance docs.
- Whole-course satellite viewer and historical Earth Studio/Hole 1/Hole 2 experiments exist. Do not rebuild them merely because a fresh chat cannot see an old conversation.

### New EA acquisition runner — implemented, not yet proven

`.github/workflows/build-overstone-ea.yml` is now the active manual acquisition runner. It:

- discovers the actual EA aerial product/tiles for the fixed Overstone footprint through the EA survey catalogue;
- requests the discovered ZIP packages using the EA survey download endpoint and public survey key;
- validates ZIP integrity and raster members;
- retries failed downloads;
- records URLs, byte counts and SHA-256 hashes in `uido.course.ea-acquisition.v0.2` manifest output;
- uploads the captured source package as a GitHub Actions artifact when successful.

A manual run of the earlier implementation failed before producing an artifact. The failure was an acquisition-path assumption, not evidence that the EA data is absent. The runner was then changed to catalogue discovery plus retries in commit `95409ef365371972eff35a9b2f8db3e54ffbfaed`.

**Important:** no successful end-to-end raw EA aerial capture has yet been recorded after this fix. Do not mark acquisition complete until a successful artifact is inspected.

## Public-source acquisition state

### EA catalogue resolution — COMPLETE

The EA Vertical Aerial Photography and National LiDAR catalogue services are machine-queryable in EPSG:27700. Exact Overstone source coverage is resolved.

**Aerial:** four 1 km 2013 25 cm RGB tiles:
- SP8064 — `Ortho_NightTime_P00055683_20130218_20130218_25cm_res.ecw`
- SP8065 — `Ortho_NightTime_P00055670_20130218_20130218_25cm_res.ecw`
- SP8164 — `Ortho_NightTime_P00055697_20130218_20130218_25cm_res.ecw`
- SP8165 — `Ortho_NightTime_P00055618_20130218_20130218_25cm_res.ecw`

**LiDAR:** 1 m survey `P_10738`, flown 2020-01-29 and 2020-03-06, requiring 5 km tiles SP8060 and SP8065. Required DSM, DTM, FZ DSM, intensity, LAZ and VOM filenames are recorded in `course-models/OVERSTONE_PUBLIC_SOURCE_RESOLUTION.json`.

Course footprint: EPSG:27700 E 480137.49–481451.93 / N 264803.28–266016.15.

### Automated acquisition — aerial runner awaiting proof

The GitHub main branch contains both the catalogue connectivity test and the new manual acquisition runner. The catalogue path is proven in code, but **raw raster/LAZ acquisition is not yet proven end-to-end**.

The earlier direct-download implementation was manually triggered and failed in 12 seconds with exit code 1 and no artifact. The failure was recorded before the runner was changed to discover the product/tiles from the EA catalogue. The corrected runner is commit `95409ef365371972eff35a9b2f8db3e54ffbfaed` and is awaiting a fresh manual run.

Draft PR #1 (`test/ea-machine-acquisition`) is open and unmerged. Do not treat the PR as production acquisition.

A headless Selenium EA Survey Download workaround remains available as fallback if the corrected direct survey endpoint fails. It has not yet been adapted/tested against the Overstone Vertical Aerial Photography product.

### Production architecture decision

Do not make the phone download raw EA/OSM/LiDAR data. Central UiDo acquisition/processing should build a compact provider-neutral course package; phone/watch clients consume that package.

Provider-agnostic architecture:

`course footprint -> provider adapter -> source catalogue -> source download -> raw source archive -> processing -> UiDo course package -> API/CDN -> phone/watch`

Manual EA portal downloads may be a development fallback, but are **not** production-approved.

## Registration state

Measured OSM-to-raster registration is a separate stage.

Do not invent a transform, reconstruct one from screenshots, use validation GPS as candidate-generation geometry, or silently reuse an old/unmeasured transform.

`course-models/OVERSTONE_REGISTRATION_CONTROL_POINTS.json` is the control-point template. The next registration step is to obtain/locate real measured control points against the fixed acquired raster, then run `register_affine.py` and record residuals/registration version.

## Feature refinement / LiDAR

Established refinement approach is two-pass:

1. Whole-course maintained-surface discovery.
2. Hole-specific refinement constrained by OSM/source ROIs.

Use feature-specific local signatures and retain provenance/confidence. Do not turn visual experiments into authoritative geometry without validation.

LiDAR has **not** yet been ingested into the canonical GitHub course model. Its intended role is terrain/elevation, vegetation/tree structure, height/visibility context and ambiguous geometry refinement.

## UI / product state

The Library contains current UI source-of-truth documents, including the revised premium-golf aesthetic, light/dark system, tile navigation language and agreed live-test round flow. The current primary path is GPS/course recognition -> Yardage -> Wind -> Lie -> Start Line -> Shape -> Strike -> Shot Recorded -> Score/round review. The live-test flow deliberately keeps SmartShot strategy out until the engine is ready. Do not redesign screens from memory; use the current Library blueprint for each screen.

## EXACT NEXT STEP

**Run the corrected `.github/workflows/build-overstone-ea.yml` manually for Overstone Park / 2013 / 0.25 m and inspect the resulting job/artifact.**

1. Trigger the workflow with the existing defaults.
2. If it succeeds, inspect the artifact contents and manifest; verify the four required aerial tiles, raster members, hashes and georeferencing.
3. If it fails, capture the exact catalogue/download response and fix the runner; do not switch to manual downloads merely to make the status green.
4. Once aerial acquisition is proven, add/prove the corresponding LiDAR acquisition for SP8060/SP8065.
5. Only after fixed raster acquisition succeeds: establish measured control points, run `register_affine.py`, record residuals, then proceed to refinement/LiDAR fusion.

## DO NOT REBUILD

1. **Do not ask for `export (1).geojson` again.** It is recovered and persisted.
2. Do not recreate the Overstone OSM capture from screenshots or memory.
3. Do not recreate the normalised source; it is complete and persisted.
4. Do not invent an 18th fairway or collapse the 30 tee polygons to force symmetry.
5. Do not replace source geometry with derived geometry or silently overwrite verified/source features.
6. Do not invent/reuse an unmeasured OSM-to-satellite transform.
7. Do not use validation GPS as candidate-generation geometry.
8. Do not generate PNGs merely to demonstrate progress.
9. Do not treat screenshots/diagnostics as the source of truth when underlying data exists.
10. Do not ask the user to repeat information already recorded in this document, the source manifests/locks, the course model or the Library.
11. If an artifact appears missing from GitHub, check the Library/conversation sources before declaring it lost.
12. Do not silently promote Library v0.4 to replace GitHub v0.1; reconcile and version the promotion explicitly.
13. Do not treat EA catalogue connectivity as equivalent to successful raw-data acquisition.
14. Do not treat the failed pre-fix EA workflow run as proof that the EA source is unavailable.
15. Do not replace the corrected acquisition runner with manual portal steps unless the automated route has been conclusively tested and documented as blocked.

## Change discipline

Whenever meaningful UiDo work changes the project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite.
