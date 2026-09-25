# UiDo — Project Source of Truth

**Last updated:** 2026-09-25  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, verified work, current blockers, exact next step, and what must not be rebuilt.

## CURRENT STATE

**Overstone playground navigation:** Hole 1 detail has camera zoom (buttons/wheel), pan, and a minimap that can be toggled. When the minimap is off, the minimap and its viewfinder/window are hard-hidden to reclaim screen space. The Overstone playground now uses a correctly sized device-pixel canvas backing store; the previous CSS-only canvas sizing was stretching the 300×150 default canvas across the phone viewport. The minimap/viewfinder has been removed. Hole 1 remains on the metric, direction-aligned camera with 0.35–8× zoom. GPS mode now requests a fresh high-accuracy position, follows it with watchPosition, recenters the camera on the player, and updates live green F/M/B plus bunker front/back yardages. Panning and pinch zoom use the same camera model, and the minimap viewfinder follows the rotated viewport.


**Overstone course-view playground: full-course context + Hole 1 detail implemented.** The playground now loads an 18-hole course context from the authoritative Overstone OSM hole routes and keeps the existing Hole 1 detailed measurement layer as the active drill-down. The renderer can toggle between full-course overview and Hole 1 detail without changing source geometry.

**Poult Wood course acquisition → Course Packet → packet-driven wireframe: VALIDATED.**  
**GolfCourseAPI discovery/registration: IMPLEMENTED; Northampton registry metadata is complete.**  
**Northampton physical acquisition: BLOCKED earlier than OSM hole validation by OSM course-identity resolution.**

Current `main` head: `cc7336344825d46bc056043984c9871b69a8f69b` (`Restore source polygon edges for hole wireframes`). The previous status file was stale at `27e0df2…`; this reconciliation corrects that discrepancy.

The latest master physical-acquisition run is `35994500134` (2026-09-24). It is a **Northampton** test and failed in `prepare_physical_acquisition.py` before OSM capture. The log records:

- registered target: `Northampton Golf Club`
- best returned OSM named candidate: `Northamptonshire County Golf Course`
- calculated name similarity: `0.00`
- first Overpass endpoint then timed out
- no physical OSM artifact was produced and downstream acquisition was skipped

Therefore the previous status statement that the current run had already reached an OSM result missing hole 4 is now historical, not the current failure mode. The new workflow change intended to preserve OSM evidence gaps has **not yet been proven**, because identity preparation fails before that stage.

## VERIFIED RECENT WORK

- `54a88e608…` changed the physical acquisition workflow so incomplete OSM hole coverage is recorded as an evidence gap rather than immediately aborting the entire acquisition chain. It also hardens artifact paths for default/manual course execution. This change is not yet validated end-to-end because the latest run stopped during identity preparation.
- `ed0dc127…` added resilient Overpass endpoint fallback.
- `60836d469…` relaxed packet QA so a course may use standalone fairway ways when no fairway relations exist; fairway source data is still required.
- Poult Wood master run `35851974870` remains the verified end-to-end reference: Stage 1 acquisition, Stage 2 packet QA, Stage 3 packet-driven wireframe and Stage 4 summary all succeeded.
- The renderer treats fairway relations as authoritative features and member ways as reconstruction inputs only, preventing duplicate rendering/counting and failing closed if all 18 target hole routes are not present.
- GolfCourseAPI discovery/import and registry workflows are implemented. Northampton is registered with provider `golfcourseapi`, provider id `51sjdksg`, 18 holes and par 72.

## NORTHAMPTON — ACTIVE NEW-COURSE TEST

Registry record: `name = Northampton`, `club_name = Northampton Golf Club`, provider id `51sjdksg`, coordinates `52.2736073,-0.9750302`, 18 holes, par 72. The registry itself is present and valid.

The current blocker is **OSM identity matching**, not yet hole completeness. `prepare_physical_acquisition.py` queries named `leisure=golf_course` candidates within 5 km and compares cleaned name tokens. For the latest run it received a best candidate named **Northamptonshire County Golf Course** with similarity `0.00`, so the fail-closed threshold stopped acquisition. The endpoint timeout is secondary; the run did receive enough data to identify the candidate before failing the identity gate.

Do not assume either the provider identity or OSM candidate is wrong. Inspect the returned OSM candidate set and registry/provider naming first. Only after identity is correctly resolved should the physical OSM hole coverage be re-evaluated. The earlier observed missing-hole-4 result (refs 1–3 and 5–18) remains a historical diagnostic from the prior acquisition path and must not be treated as the current run's output.

## COURSE PIPELINE CONTRACT

The architecture is modular:

- `.github/workflows/build-course-ea.yml` — reusable/manual physical acquisition.
- `.github/workflows/build-course.yml` — master orchestration.
- `course-models/COURSE_PIPELINE.md` — Course Packet hand-off contract.
- `PROJECT_STATUS.md` — source of truth.

Once acquired and QA'd, the **Course Packet is the persisted hand-off layer**. Downstream stages must consume the packet and must not silently re-query or recapture OSM/EA data.

Poult Wood run `35851974870` is the proof that this packet-driven wireframe path works. The Library wireframe artifact is QA output, not source geometry.

## AUTHORITATIVE OVERSTONE SOURCE

Raw OSM and normalised source remain authoritative and present in the UiDo Library; they must not be recreated or replaced.

- Raw OSM: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
  - Library file id: `file_00000000e32481f4a00f707344416e79`
  - SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- Normalised: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
  - Library file id: `file_0000000052948210969af327286d4488`
  - SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
  - Schema: `uido.course.source-normalized.v0.1`

Library retrieval confirms the normalised source contains **18 HOLE features**, preserves source geometry exactly, and explicitly contains Overstone hole 4 (`way/798140685`).

### Library v0.4 discrepancy

Previously recorded `/UiDo/UiDo_Overstone_Course_Model_v0.4.json` remains **unlocated/not verified**. Do not recreate it or assume deletion. Do not promote it over the verified GitHub model without locating and comparing the actual artifact.

## OVERSTONE BUILDER STATUS

The earlier Overstone acquisition regression remains a separate, contained issue: run `35627704315` failed at Overpass HTTP 406 after EA aerial, LiDAR, compact aerial and terrain completed. The successful combined run `35608919741` remains the known-good fixture for those acquisition/downstream stages.

The newer model-generation fix is still not proven in a successful post-fix Overstone package build. Repair the acquisition issue only when returning to that track.

## COURSE-MODEL FINDINGS

- **F/M/B:** `course-models/FMB_DERIVATION.md` is correctly associated with historical Overstone hole 2. The exact universal point-selection algorithm is not proven; analyse all 18 Overstone greens before promotion.
- **Hole orientation:** `course-models/HOLE_ORIENTATION_SENSE_CHECK.md`: Y = direction of play, X = left/right. OpenYardage is an independent sense check only.
- **Poult Wood:** `course-models/POULT_WOOD_SOURCE_MANIFEST.json` remains the source identity record. Preserve existing fairway multipolygon reconstruction and hole association logic. Do not invent, smooth, move or replace source geometry.

## JOBS TO DO — FRESH-CHAT HANDOVER

### 1. Northampton identity repair
**STATUS: BLOCKED AT OSM COURSE-IDENTITY RESOLUTION**

Inspect the actual OSM candidate response for Northampton and determine why the registered `Northampton Golf Club` target produces `Northamptonshire County Golf Course` as the best named candidate with similarity `0.00`. Determine whether the issue is provider naming, OSM naming, candidate filtering, or course-location selection. Repair only the identity-selection path; do not weaken the fail-closed gate merely to continue.

### 2. Northampton physical acquisition proof
After identity resolution succeeds, rerun the existing one-ping path and record the actual OSM hole refs returned. If hole 4 is still absent, diagnose the physical query/boundary/identity selection specifically at that point. Then prove Course Packet → packet QA → packet-driven wireframe.

### 3. Overstone acquisition repair + post-fix proof
Separate track. Repair the Overpass 406 only when returning to Overstone, then prove the existing model-generation fix in a populated 18-hole package.

### 4. F/M/B validation
Analyse all 18 Overstone greens and identify the common historical construction rule before testing Poult Wood F/M/B derivation.

### 5. Registration / refinement
Later: establish measured OSM-to-raster control points and registration metrics while retaining OSM geometry and provenance.

### 6. Player-facing GPS course selection
Later: nearest-course selection from the UiDo Course Registry. Do not mix this into the current acquisition fix.

## EXACT NEXT STEP

**Inspect the OSM candidate set returned during Northampton physical-source preparation and resolve the identity mismatch (`Northampton Golf Club` → `Northamptonshire County Golf Course`, similarity `0.00`). Repair only the identity-selection path, rerun the existing Northampton acquisition, then evaluate the actual OSM hole refs before making any hole-coverage change.**

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
18. Do not rerun Northampton blindly: the **current** failure is identity resolution before OSM capture; the older missing-hole-4 result is historical until reproduced.
19. Do not relax the identity threshold or 18-hole identity check merely to make the pipeline pass.
20. Do not invent or copy Northampton hole 4 geometry from another course.

## CHANGE DISCIPLINE

Whenever meaningful UiDo work changes project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite source data.

### 2026-09-25 — Overstone playground live GPS / information rail
- Overstone Hole 1 playground now has a dedicated right-hand information rail so the hole canvas gets a cleaner, larger working area.
- Moved course/status, live green + bunker yardages, and hole information into stacked right-side boxes.
- Removed the on-map bunker L/R markers and the legend; bunker yardage labels remain as front/back distances only.
- Added a Hide info / Show info control so the information rail can be collapsed and the hole view can expand to the full screen.
- The existing **Use GPS** control is the live-location handover: it requests the device location, switches off the fixed test player, centres the camera on the live position, and then watches for position updates. Browser/device permission is required.
- Code commit: `d654bd4afa72ac0b76e729adb837f4a09d6c259d`.

### 2026-09-25 — Overstone GPS camera follow
- Live GPS mode now follows the player as the GPS position changes instead of leaving the camera behind.
- Camera follow places the player toward the lower-middle of the view and clamps camera movement against the Hole 1 extents so the hole does not simply disappear off-screen as the player moves.
- Test mode remains manually movable and unchanged.
- Code commit: `89daa3af2671e53c721d72e7ca7e240493177a65`.

### 2026-09-25 — Overstone fixed viewfinder / free-roam framing
- When information is visible, Hole 1 now uses a fixed left-side viewfinder width while the right-side boxes float over the live map.
- Initial/Fit framing calculates zoom from the available viewfinder dimensions so the hole is fitted to the phone view rather than using the full-screen width.
- Added a **Fit** control to snap back to that framing.
- Hiding info removes the viewfinder constraint: the map returns to full-screen and normal pan/zoom is free.
- GPS updates no longer recenter the fixed viewfinder; the player moves within the fixed hole view.
- Code commits: `b7c7fdddd6c6fadd926be178c68e1fb64cdbc53b`, `f63bb01061b88ce37bdc8d1e3ae498d56fd02e45`.


### 2026-09-25 — Overstone Holes 2–18 wireframes
- Added compact source-derived wireframe data for Holes 2–18 from the authoritative Overstone OSM capture.
- Hole selection now renders fairway, green, tee and bunker geometry for the selected hole while preserving the working F/M/B and live bunker yardage calculations.
- Hole 1 remains on its separately verified detailed source layer.
- The compact renderer uses a 0.5 m quantised local coordinate representation for the playground wireframe; the authoritative OSM source is unchanged.
- Added `overstone/hole-wireframes.js` and wired it into `overstone/index.html`.
- Commits: `ddce5bc498c3afd33368a0fa6a4c80aa2292c2b9`, `d0e539c42ed99cc19a2f87a82ef6ff64f270043c`.
- No GitHub Action was automatically rerun; manual Pages/playground testing is the next validation step.


### 2026-09-25 — Hole selector and wireframe presentation refinement
- Replaced the cramped native Hole dropdown with a visible UiDo hole picker that opens an 18-hole grid and clearly shows the active hole.
- Smoothed the canvas rendering of source-derived polygon wireframes using quadratic curve interpolation at render time; source data itself is unchanged.
- F/M/B, live GPS and yardage logic are unchanged.
- Commit: `6fb567d795d0ddd6c1814696e49d66c1dc4d44ae`.


### 2026-09-25 — Hole 3 bunker geometry and picker width
- Widened the mobile info rail so the Hole picker has more breathing room.
- Replaced the three Hole 3 bunker render polygons with geometry transformed directly from the authoritative Overstone OSM bunker polygons `way/798091424`, `way/798091425`, and `way/798091426`.
- The bunker yardage endpoints and live F/M/B logic remain unchanged.
- Commits: `8e8ec298be7ab2ddc6ba59262238ed8eca1e2421`, `7530ddc6237a5f9e93b50880c536517a3c05fd45`.


### 2026-09-25 — Restore source polygon rendering
- Reverted the quadratic smoothing pass for Holes 2–18 polygons. The renderer now follows the stored source polygon vertices directly, matching the proven Hole 1 rendering approach rather than bending the source geometry at render time.
- Mobile hole picker width remains at 168px.
- Commit: `cc7336344825d46bc056043984c9871b69a8f69b`.


### 2026-09-25 — Overstone playground clean course-model rebuild
- Replaced the patched/compact hole-wireframe runtime path with overstone/course-source-model.js generated from the authoritative recovered Overstone OSM capture.
- All 18 holes now use the same source-derived model shape: hole route, exact OSM feature geometry, green F/M/B anchors, and bunker live-yardage metadata.
- Feature-to-hole association is resolved once against the nearest authoritative hole route with conservative feature-type distance gates; the recovered source contains 31 bunkers and the rebuilt model assigns all 31 exactly once.
- Hole 1 bunker front/back/anchor metadata remains the previously verified Hole 1 reference values; its geometry is sourced from the same OSM model as the other holes.
- The renderer now handles Polygon and LineString source features directly, including fairway, rough, green, bunker, tee, water and cartpath, with no geometry smoothing or compact coordinate reconstruction.
- The proven camera/projection, GPS, F/M/B yardage, live bunker yardage, hole picker and full-course context were retained.
- overstone/hole-wireframes.js is no longer loaded and is removed from the runtime tree. hole1-layer.js remains as a historical/reference fixture but is no longer used by the playground runtime.
- No GitHub Actions run was triggered.
- Code commit: c9b396ccc451a61a987c1526809ffa3ad5b8f7bc.
