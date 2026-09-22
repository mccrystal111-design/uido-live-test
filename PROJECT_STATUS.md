# UiDo — Project Source of Truth

**Last updated:** 2026-09-22  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, completed work, current blockers, exact next step, and what must not be rebuilt.

## Current state

**Overstone data foundation: READY, but Stage 1 Step 1 is not yet closed.** The authoritative OSM capture and deterministic normalised source remain locked and present in the UiDo Library. The GitHub provider-neutral v0.1 model remains canonical. EA aerial, LiDAR and terrain acquisition/assembly are proven. A successful combined build (`35608919741`) produced the offline course package and human-review bundle.

The repository is now at commit `7e7fca3f6889bbecd3aa52ded6575efdbd01530f` (`Reconcile source of truth with latest course-model QA`). This commit is a source-of-truth reconciliation only; it does not change the authoritative course data or claim a new successful Overstone package build. Its parent was `4c097a8ad0b9e835df6fda94cee6eb72c0617a1c` (`Run Poult Wood full-course wireframe QA`). Recent course-model work refactored the Poult Wood skeleton to align with the Overstone source model and fixed single-line fairway relation unions.

The latest known Overstone builder regression remains run `35627704315` on commit `9ca6c0974a3928eba3d9b7aadf4d97254ef673ea`: EA aerial, LiDAR, compact aerial rendering and terrain all complete; the run fails only at **Acquire Overstone OSM golf source** with Overpass HTTP 406. Do not replace the authoritative OSM source because of this acquisition regression.

## Recent course-model findings

### F/M/B derivation — corrected and still under investigation

`course-models/FMB_DERIVATION.md` is now corrected to the proper historical association: the recovered historical F/M/B test belongs to **Overstone hole 2**, not hole 1. The OSM green/route relationship and Front/Back source vertices are proven, but the exact historical point-selection algorithm is **not** proven. The earlier exact-centroid claim has been discarded. fileciteturn5file0L1-L6

Required next validation: analyse all 18 Overstone greens to identify the common F/B/M construction rule before testing Poult Wood. Do not promote a universal F/M/B derivation yet.

### Hole orientation / OpenYardage sense check

`course-models/HOLE_ORIENTATION_SENSE_CHECK.md` now defines the intended local frame: Y = forward along play, X = left/right, while preserving underlying geospatial geometry. OpenYardage is an independent golf-useful sense check only; large discrepancies become QA warnings, not automatic geometry edits. fileciteturn10file0L1-L6

### Poult Wood — source identity confirmed; QA work active

`course-models/POULT_WOOD_SOURCE_MANIFEST.json` records an identity PASS for the 18-hole Poult Wood target and retains the raw OSM source without invented geometry. It identifies 18 target hole refs and 24 hole routes in the facility source, with 6 additional routes outside the target 18-hole set. OpenYardage is explicitly a sense-check, not UiDo source geometry. fileciteturn11file0L1-L6

The latest Poult Wood workflow commit changes the QA pass to render the **complete 18-hole footprint on one consistent map**. This is QA/source inspection work, not permission to overwrite course geometry. fileciteturn7file0L3-L11

## Authoritative Overstone source

### Raw OSM — authoritative

Do not ask the user to re-upload the OSM capture.

- Library: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
- Library file id: `file_00000000e32481f4a00f707344416e79`
- SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- GitHub identity lock: `course-models/OVERSTONE_OSM_SOURCE_LOCK.json`
- GitHub manifest: `course-models/OVERSTONE_SOURCE_MANIFEST.json`

Library search on 2026-09-22 reconfirms the authoritative OSM capture is present. fileciteturn12file1L156-L163

### Normalised source — authoritative derived artifact

- Library: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
- Library file id: `file_0000000052948210969af327286d4488`
- Schema: `uido.course.source-normalized.v0.1`
- SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
- Status: **complete**; source geometry unchanged.

Library search on 2026-09-22 reconfirms this file is present. fileciteturn12file0L1-L8

### Library v0.4 discrepancy

A previously recorded `/UiDo/UiDo_Overstone_Course_Model_v0.4.json` is still not surfaced by the current Library search. Treat v0.4 as **unlocated/not verified**, not deleted. Do not recreate it or silently promote it over the GitHub v0.1 model.

## Overstone model-generation fix

`tools/course-model/build_overstone_model.py` now builds provider-neutral course geometry from the authoritative OSM capture plus existing green anchors. It preserves source geometry/provenance, records deterministic association evidence and hard-fails unless all 18 holes have routing, tee and fairway geometry.

The fix is **present but not proven in a successful post-fix package build** because the latest builder run is blocked before model generation by Overpass HTTP 406. The older successful package predates this fix and therefore cannot be used as proof that the fix is incorporated.

## Successful combined Overstone build

Workflow run `35608919741` / commit `2c4697c77fbceeec2d8789245570668f1a513f7e` completed:

1. EA aerial acquisition;
2. EA LiDAR acquisition;
3. compact aerial render;
4. terrain layer;
5. UiDo offline course package;
6. human-review bundle;
7. artifact uploads.

Known unexpired artifacts (verified 2026-09-22) include `overstone-uido-course-package`, `overstone-course-review`, `overstone-ea-lidar-capture` and `overstone-ea-aerial-capture`, all expiring 2026-10-05. Their existence is verified; their contents still require deliberate inspection before the package → loader contract is declared verified.

## Issue #2 / build sequence

GitHub Issue #2 remains the active vertical-slice build contract: Overstone course loader → player position → shot situation model → SmartPoint → SmartShot → Caddie → shot lifecycle → playable hole → 18-hole round → live course testing.

Engineering rules: deterministic fixtures before live sensors; test each component before integration; do not change two layers simultaneously while debugging; keep Parking Lot features out of this phase. The immediate Overstone hand-off remains package → course-loader contract → one real populated hole.

## Registration / refinement

Measured OSM-to-raster registration remains a separate stage. `course-models/OVERSTONE_REGISTRATION_CONTROL_POINTS.json` is the control-point template. Do not invent/reuse a transform or use validation GPS as candidate-generation geometry.

## UI / product state

The Library remains the UI source of truth: premium golf instrument aesthetic, light/dark system, persistent navigation icon language and the GPS/Yardage/Wind/Lie/Start Line/Shape/Strike live shot flow. Strategy remains out of the live flow until SmartShot is ready. fileciteturn3file0L11-L33 fileciteturn3file1L62-L70

The committed `assets/Lo_Flag_Icon.svg` remains an asset addition only and does not replace the UI blueprints or change course-data authority.

## Beta discrepancy

`beta/catalog.json` still carries generic `Second course` metadata with no package URL while later repository work names Poult Wood as the second beta course. Treat the catalogue as stale beta metadata, not proof of a published second-course package.

## Outstanding work

1. **Inspect the successful Overstone package/review artifacts from run `35608919741` and define the exact package → UiDo course-loader contract.**
2. Repair only the Overpass HTTP 406 acquisition step; then run the existing model-generation fix and prove a populated 18-hole post-fix package.
3. Build/test the Overstone course-loader vertical slice and render one real hole with populated routing/tee/fairway geometry.
4. Complete F/M/B rule analysis across all 18 Overstone greens; only then test Poult Wood and consider promotion.
5. Continue Poult Wood full-course wireframe QA and identify OSM fairway coverage gaps; use EA imagery for refinement rather than importing third-party geometry.
6. Establish measured OSM-to-raster control points and registration metrics.
7. Locate/reconcile Library v0.4 before any model-version promotion.
8. Align beta metadata once an approved second-course package exists.

## EXACT NEXT STEP

**Inspect the existing successful Overstone course-package and review artifacts, define the package → UiDo course-loader contract, and use the deterministic package fixture for the first loader test. Separately, repair only the Overpass 406 so the post-fix Overstone model can be built and compared. Continue F/M/B analysis as a validation task, not as permission to rewrite source geometry.**

## DO NOT REBUILD

1. Do not ask for or recreate the authoritative Overstone OSM capture.
2. Do not recreate the complete normalised source; it is present and authoritative.
3. Do not recreate or promote Library v0.4 without locating and comparing the actual artifact.
4. Do not rebuild the entire Overstone pipeline because of Overpass HTTP 406; repair only the failing acquisition step.
5. Do not treat the old terrain `find` failure as current; terrain assembly is proven.
6. Do not replace EA aerial/LiDAR acquisition with manual portal steps.
7. Do not invent an OSM-to-raster transform or reuse an unmeasured one.
8. Do not use validation GPS as candidate-generation geometry.
9. Do not generate PNGs merely to demonstrate progress.
10. Do not treat screenshots/diagnostics as source of truth when underlying data exists.
11. Do not silently overwrite verified/source geometry with derived geometry.
12. Do not treat the old successful package as proof that the new model-generation fix is incorporated.
13. Do not promote the F/M/B derivation to a universal rule; the exact point-selection algorithm is still under investigation.
14. Do not treat OpenYardage as UiDo source geometry; it is an independent sense check only.
15. Do not treat Poult Wood wireframe QA as a replacement for the Overstone Stage 1 contract.
16. Do not treat stale beta catalogue metadata as evidence of a published second-course package.
17. If a GitHub artifact appears missing, check artifact history and Library/conversation sources before declaring it missing.
18. Do not ask the user to repeat information already recorded here or in the source manifests/locks/course model/Library.

## Change discipline

Whenever meaningful UiDo work changes project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite source data.
