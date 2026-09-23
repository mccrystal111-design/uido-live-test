# UiDo — Project Source of Truth

**Last updated:** 2026-09-23  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, verified work, current blockers, exact next step, and what must not be rebuilt.

## CURRENT STATE

**Poult Wood course acquisition → Course Packet → packet-driven wireframe: VALIDATED.**
**GolfCourseAPI discovery/registration: IMPLEMENTED; Northampton registry metadata is complete and identity validation is GREEN.**
**Northampton physical acquisition: BLOCKED by incomplete OSM hole coverage.**

Current `main` head: `60836d469270b30506cad8bfc98cefa15d3914dd` (`Allow standalone fairways in packet QA`).

The latest master run is `35895454637` (2026-09-23). It was a **Northampton** test. Physical source preparation generated and identity-validated the Northampton boundary, but the OSM query ultimately returned hole refs **1–3 and 5–18; hole 4 was absent**, so acquisition failed closed. Stages 2–4 were correctly skipped. This is now the active blocker; it is not evidence that the course is missing or that source data should be recreated.

The run also exercised the new resilient Overpass endpoint list. The first endpoint returned 504/timeouts, after which the query progressed far enough to produce OSM data but failed the required 18-hole identity check. Do not treat this as a generic Overpass outage without checking the returned course data.

## VERIFIED RECENT WORK

- `ed0dc127…` added resilient Overpass endpoint fallback.
- `60836d469…` relaxed packet QA so a course may use standalone fairway ways when no fairway relations exist; it still requires fairway source data.
- Poult Wood master run `35851974870` remains the verified end-to-end reference: Stage 1 acquisition, Stage 2 packet QA, Stage 3 packet-driven wireframe, Stage 4 summary all succeeded.
- The wireframe renderer treats fairway relations as authoritative features and member ways as reconstruction inputs only, preventing duplicate rendering/counting and failing closed if all 18 target hole routes are not present.
- GolfCourseAPI discovery/import and registry workflows are implemented. Northampton metadata now contains a valid provider identity and an OSM identity match; the remaining Northampton proof is physical acquisition → packet → wireframe.

## AUTHORITATIVE OVERSTONE SOURCE

Raw OSM and normalised source are still authoritative and present in the UiDo Library; they must not be recreated or replaced.

- Raw OSM: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
  - Library file id: `file_00000000e32481f4a00f707344416e79`
  - SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- Normalised: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
  - Library file id: `file_0000000052948210969af327286d4488`
  - SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
  - Schema: `uido.course.source-normalized.v0.1`

Library retrieval still confirms the normalised source retains 18 hole features and preserves source geometry exactly. fileciteturn9file0

### Library v0.4 discrepancy

Previously recorded `/UiDo/UiDo_Overstone_Course_Model_v0.4.json` remains **unlocated/not verified**. Do not recreate it or assume deletion. Do not promote it over the verified GitHub model without locating and comparing the actual artifact.

## OVERSTONE BUILDER STATUS

The earlier Overstone acquisition regression remains a separate, contained issue: run `35627704315` failed at Overpass HTTP 406 after EA aerial, LiDAR, compact aerial and terrain completed. The successful combined run `35608919741` remains the known-good fixture for those acquisition/downstream stages.

The newer model-generation fix is still not proven in a successful post-fix Overstone package build. Repair the acquisition issue only when returning to that track.

## COURSE PIPELINE CONTRACT

The architecture is modular:

- `.github/workflows/build-course-ea.yml` — reusable/manual physical acquisition.
- `.github/workflows/build-course.yml` — master orchestration.
- `course-models/COURSE_PIPELINE.md` — Course Packet hand-off contract.
- `PROJECT_STATUS.md` — source of truth.

Once acquired and QA'd, the **Course Packet is the persisted hand-off layer**. Downstream stages must consume the packet and must not silently re-query or recapture OSM/EA data.

Poult Wood run `35851974870` is the proof that this packet-driven wireframe path works end-to-end. The Library wireframe artifact also exists as QA output; it is not source geometry. fileciteturn9file4

## COURSE-MODEL FINDINGS

### F/M/B

`course-models/FMB_DERIVATION.md` is correctly associated with historical **Overstone hole 2**. The OSM green/route relationship and source F/B vertices are proven; the exact historical point-selection algorithm is not. Analyse all 18 Overstone greens before promoting a universal F/M/B rule.

### Hole orientation

`course-models/HOLE_ORIENTATION_SENSE_CHECK.md`: Y = direction of play, X = left/right. OpenYardage is an independent sense check only; discrepancies are QA warnings, not automatic geometry edits.

### Poult Wood

`course-models/POULT_WOOD_SOURCE_MANIFEST.json` remains the source identity record. Preserve existing fairway multipolygon reconstruction and hole association logic. Do not invent, smooth, move or replace source geometry.

## NORTHAMPTON — ACTIVE NEW-COURSE TEST

Registry identity is GREEN: provider `golfcourseapi`, provider id `51sjdksg`, OSM candidate `way/472178757`, similarity `1.0`, ~176.5 m from provider coordinates. The physical-source manifest was generated successfully.

The current failure is precise: the OSM `golf=hole` query returned **17 target refs and omitted hole 4**. The acquisition workflow correctly stopped before EA/LiDAR and before packet publication. This must be resolved by inspecting why hole 4 is absent from the physical OSM query/boundary/identity selection; do not invent hole 4 geometry.

## UI / PRODUCT STATE

Library UI source of truth remains the premium golf-instrument direction, with light/dark system, persistent navigation icon language and the live flow GPS/Yardage → Wind → Lie → Start Line → Shape → Strike. The UI blueprint explicitly calls for shared theme tokens, one icon family, reusable tile shell, then tile migration and radial navigation. fileciteturn10file2 fileciteturn10file4

Strategy remains outside the live capture flow until SmartShot is ready.

## JOBS TO DO — FRESH-CHAT HANDOVER

### 1. Northampton one-ping course test
**STATUS: BLOCKED AT PHYSICAL OSM ACQUISITION**

Fix only the Northampton OSM acquisition/identity problem that causes hole 4 to be absent. Re-run the existing `test-new-course.yml` path only after the failure mode is understood. The intended chain remains:
**GolfCourseAPI discovery → registration → physical acquisition → Course Packet → packet QA → packet-driven wireframe.**

API budget rule remains: first clean provider run = one `/v1/search` + one `/v1/courses/{provider_id}` request; do not enable provider refresh. Cached provider data must be reused thereafter.

### 2. Northampton downstream proof
After physical acquisition succeeds, prove Course Packet QA and packet-driven wireframe using the existing master pipeline. Do not introduce a new source format.

### 3. Overstone acquisition repair + post-fix proof
Separate track. Repair the Overpass 406 only when returning to Overstone, then prove the existing model-generation fix in a populated 18-hole package.

### 4. F/M/B validation
Analyse all 18 Overstone greens and identify the common historical construction rule before testing Poult Wood F/M/B derivation.

### 5. Registration / refinement
Later: establish measured OSM-to-raster control points and registration metrics while retaining OSM geometry and provenance.

### 6. Player-facing GPS course selection
Later: nearest-course selection from the UiDo Course Registry. Do not mix this into the current acquisition fix.

## EXACT NEXT STEP

**Inspect the Northampton acquisition result and determine why the physical OSM query/boundary produced refs 1–3 and 5–18 but not hole 4. Repair only that acquisition/identity path, without inventing or replacing source geometry. Then rerun the existing Northampton one-ping pipeline and prove Course Packet → packet QA → wireframe.**

## DO NOT REBUILD

1. Do not ask for or recreate the authoritative Overstone OSM capture.
2. Do not recreate the complete Overstone normalised source; it is present and authoritative.
3. Do not recreate or promote Library v0.4 without locating and comparing the actual artifact.
4. Do not rebuild the entire Overstone pipeline because of the historical Overpass 406; repair only its acquisition step.
5. Do not replace EA aerial/LiDAR acquisition with manual portal steps.
6. Do not invent an OSM-to-raster transform or reuse an unmeasured one.
7. Do not use validation GPS as candidate-generation geometry.
8. Do not generate PNGs merely to demonstrate progress.
9. Do not treat screenshots/diagnostics as source of truth when underlying data exists.
10. Do not silently overwrite verified/source geometry with derived geometry.
11. Do not treat the old successful Overstone package as proof that the newer model-generation fix is incorporated.
12. Do not promote F/M/B to a universal rule before all-18 validation.
13. Do not treat OpenYardage as UiDo source geometry; it is a sense check only.
14. Do not treat Poult Wood wireframe QA as replacement source geometry.
15. Do not treat stale catalogue metadata as evidence of a published second course.
16. Do not declare an artifact missing until GitHub history, workflow artifacts and the UiDo Library have been checked.
17. Do not ask the user to repeat information already recorded here or in the source manifests/locks/course model/Library.
18. Do not rerun Northampton blindly: the current failure is specifically **missing OSM hole 4**, not a generic endpoint failure.
19. Do not relax the 18-hole identity check just to make the pipeline pass.

## CHANGE DISCIPLINE

Whenever meaningful UiDo work changes project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite source data.
