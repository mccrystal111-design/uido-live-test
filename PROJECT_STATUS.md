# UiDo — Project Source of Truth

**Last updated:** 2026-09-21  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, completed work, current blockers, exact next step, and what must not be rebuilt.

## Current state

**Course data foundation: READY.** Overstone's authoritative OSM capture is recovered and identity-locked; deterministic normalisation and the provider-neutral course model exist. Public EA source resolution is complete. **EA aerial acquisition is proven. The combined builder has now also successfully acquired LiDAR and rendered the compact aerial overview in-run; the run failed only at terrain-layer assembly, so no final course-package/review artifact was produced.**

The terrain failure is fixed in the current workflow commit `161f7206a7c088174bc64c1a1dd62d875705145d` (`Fix LiDAR terrain file discovery`). The workflow is configured to run on changes to itself as well as manual dispatch. The next run must prove terrain assembly and then the downstream package/review artifacts.

**Do not start another visual prototype.** The immediate priority is the public-source data/model pipeline and course-package build.

## Authoritative Overstone source

### Raw OSM — authoritative

Do not ask the user to re-upload the OSM capture.

- Library: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
- Library file id: `file_00000000e32481f4a00f707344416e79`
- SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- GitHub identity lock: `course-models/OVERSTONE_OSM_SOURCE_LOCK.json`
- GitHub manifest: `course-models/OVERSTONE_SOURCE_MANIFEST.json`

Source counts: 18 holes, 18 pins, 20 greens, 30 tees, 17 fairways, 31 bunkers, 23 rough, 17 paths, 2 water hazards, 1 driving range; 177 features total. Only `golf=hole` features carry explicit `ref=1..18`; other feature classes must be associated spatially/derived, never by feature order.

### Normalised source — authoritative derived artifact

- Library: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
- Library file id: `file_0000000052948210969af327286d4488`
- Schema: `uido.course.source-normalized.v0.1`
- SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
- Status: **complete**; source geometry unchanged; no invented hole assignments. Library report confirms 177 features and 141 non-explicit-hole features.

## Course model state

### GitHub canonical model

- `course-models/overstone-park-v0.1.json`
- Schema: `uido.course.v0.1`
- Contains all 18 green F/M/B anchors.
- Registration transform/metrics remain null until measured control points are used.

### Library discrepancy — preserve, do not overwrite

The previous status recorded a newer Library `/UiDo/UiDo_Overstone_Course_Model_v0.4.json`. A current Library search and the `/UiDo/Overstone` folder listing do **not** surface that file; the folder currently exposes the authoritative raw OSM, normalised source and its report only. Treat v0.4 as **unlocated/not verified in the current Library index**, not deleted or missing by assumption. Do not promote, recreate or overwrite v0.1 until the v0.4 artifact is actually located and compared.

## EA public-source state

### Catalogue resolution — COMPLETE

Exact Overstone EA coverage is resolved in EPSG:27700.

**Aerial:** 2013, 0.25 m, product `vertical_aerial_photography_tiles_night_time`. Required source ECWs are:
- SP8064 — `P00055683`
- SP8065 — `P00055670`
- SP8164 — `P00055697`
- SP8165 — `P00055618`

**LiDAR:** 1 m survey `P_10738`, flown 2020-01-29 and 2020-03-06; required tiles SP8060 and SP8065, with DSM, DTM, FZ DSM, intensity, LAZ and VOM records already resolved in the repository manifests.

Course footprint: EPSG:27700 E 480137.49–481451.93 / N 264803.28–266016.15.

### Automated aerial acquisition — PROVEN

`.github/workflows/build-overstone-ea.yml` is the active Overstone acquisition/build runner. It discovers the EA product/tiles from the fixed Overstone footprint, downloads the EA survey ZIPs, validates ZIP/raster contents, retries failures, records URLs/byte counts/SHA-256 and uploads artifacts.

**Successful aerial proof:** workflow run `35545736650` / commit `75d4c9d9ee5e74de395483c2e1b4c3d6a291b5b2`. Both download steps succeeded and the artifact `overstone-ea-aerial-capture` was created. Artifact id `10616132263`, size 24,883,030 bytes, SHA-256 `90efebca7e9a2980256a1c95389052978e137d01da7b544ec7cd4fe53be22208`, expiry 2026-10-04.

The artifact contains the two required download blocks SP8060/SP8065 and all four required Overstone ECWs (`P00055683`, `P00055670`, `P00055697`, `P00055618`). **Do not call aerial acquisition unproven.**

### Combined LiDAR acquisition — PROVEN IN-RUN; ARTIFACT NOT PRESERVED

Workflow run `35595037521` / commit `228cc4ae449ed56d8da430b5123eb7e80bc64d29` successfully completed **Discover and download EA National LiDAR terrain** before the later terrain-step failure. This proves the corrected EA catalogue discovery plus DTM/DSM acquisition/extraction path reached completion for the Overstone run.

However, the job failed during terrain assembly, so the `overstone-ea-lidar-capture` upload step was skipped. Therefore **do not claim a reusable LiDAR artifact is persisted**; the acquisition path is proven, but a successful end-to-end run is still required to preserve the capture artifact.

### Compact aerial post-render — PROVEN IN-RUN; ARTIFACT NOT PRESERVED

The same run `35595037521` successfully completed the ECW/GDAL render stage. It built the course VRT and produced:
- `overstone-overview.webp` (~21 KB)
- `overstone-overview.jpg` (~58 KB)
- `overstone.vrt` (~11 KB)
- `render.json`

The render used the fixed Overstone EPSG:27700 footprint and approximately 0.5 m/pixel output. Because the downstream terrain step failed, no final review/package artifact was uploaded. **Do not treat phone-ready rendering/package delivery as complete.**

### Terrain assembly — FIXED, NEXT PROOF TARGET

Run `35595037521` failed at **Build compact terrain layer** with a shell syntax error in the `find` expression, not with a LiDAR/GDAL/data error. The fix is commit `161f7206a7c088174bc64c1a1dd62d875705145d` (`Fix LiDAR terrain file discovery`).

The current workflow now uses a simpler TIFF filter for DTM/DSM discovery. The next run must prove:
1. DTM/DSM VRT creation;
2. COG terrain outputs;
3. terrain previews/manifest;
4. final UiDo package;
5. human review bundle;
6. uploaded LiDAR capture artifact.

### Production architecture

Phone/watch clients should **not** download raw EA/OSM/LiDAR. Central UiDo acquisition/processing should build a compact provider-neutral course package, then the client downloads that package for offline/on-course use.

`course footprint -> provider adapter -> source catalogue -> source download -> raw archive -> processing/render -> UiDo course package -> API/CDN -> phone/watch`

Manual EA portal downloads are development fallback only, not production-approved.

## Registration / refinement state

Measured OSM-to-raster registration is still a separate stage. `course-models/OVERSTONE_REGISTRATION_CONTROL_POINTS.json` is the control-point template. Do not invent/reuse a transform or use validation GPS as candidate-generation geometry. After fixed raster acquisition, obtain real measured control points, run `register_affine.py`, and record residuals/RMS/max error.

Established refinement remains two-pass: whole-course maintained-surface discovery, then hole-specific refinement constrained by source ROIs. Preserve feature provenance/confidence. LiDAR is intended for terrain/elevation, vegetation/tree structure, height/visibility context and ambiguous geometry refinement.

## UI / product state

The Library remains the source of truth for the current UI: premium golf instrument aesthetic, light/dark system, persistent navigation icon language and the GPS/Yardage/Wind/Lie/Start Line/Shape/Strike live shot flow. Strategy stays out of the live flow until SmartShot is ready.

The current UI implementation blueprint locks shared theme tokens, the stroke-based navigation icon contract, tile anatomy, radial navigation and phone/watch continuity before independent tile redesign.

Shape remains a five-choice Hook/Draw/Straight/Fade/Slice roller with the approved interaction blueprint.

## Beta environment discrepancy

A temporary GitHub Pages beta scaffold exists. Current `beta/catalog.json` still says the second course is generic `Second course` and has no package URL, while a later commit is explicitly titled `Use Poult Wood as second beta course`. Treat the catalog as **stale beta metadata**, not as proof that a second course package exists. This is separate from the Overstone course-build blocker.

## Outstanding work

1. **Run/inspect the workflow after commit `161f7206a7c088174bc64c1a1dd62d875705145d`** and prove terrain assembly plus all downstream artifacts.
2. Inspect DTM/DSM outputs and the final package/review bundle; measure size, runtime, visual extent and georeferencing.
3. Preserve the successful LiDAR capture as an uploaded artifact and record its hashes.
4. Build the provider-neutral UiDo course package and review/verification layer to a publishable state.
5. Establish measured OSM-to-raster control points and registration metrics.
6. Locate and deliberately reconcile the previously recorded Library v0.4 course model before promoting a new canonical model version.
7. Keep beta metadata/package links aligned once an approved course package exists.

## EXACT NEXT STEP

**Inspect the workflow run triggered by the current workflow fix commit `161f7206a7c088174bc64c1a1dd62d875705145d`. If no push-triggered run exists, manually run `.github/workflows/build-overstone-ea.yml` using Overstone Park / 2013 / 0.25 m defaults.**

The acquisition and aerial render portions are already proven in-run. The only known failure in the last run was the terrain file-discovery shell syntax, which is now fixed. Do not change the source data or manually download EA files.

If the terrain stage succeeds, inspect the COGs/previews, then the final course package and human review artifacts before moving on to registration/refinement. If it fails, fix only the failing stage and preserve the existing acquired-source logic.

## DO NOT REBUILD

1. **Do not ask for `export (1).geojson` again.** The authoritative OSM capture is recovered and persisted.
2. Do not recreate the normalised source; it is complete and persisted.
3. Do not recreate the course model from screenshots or memory.
4. Do not replace source geometry with derived geometry or silently overwrite verified/source features.
5. Do not invent an OSM-to-raster transform or reuse an unmeasured one.
6. Do not use validation GPS as candidate-generation geometry.
7. Do not generate PNGs merely to demonstrate progress.
8. Do not treat screenshots/diagnostics as the source of truth when underlying data exists.
9. Do not ask the user to repeat information already recorded here, in source manifests/locks, the course model or the Library.
10. If a GitHub artifact appears missing, check its recorded Library/conversation sources and GitHub artifact history before declaring it lost.
11. Do not silently promote Library v0.4 over GitHub v0.1; the current Library index does not surface v0.4, so locate it before any promotion decision.
12. Do not treat EA catalogue connectivity as equivalent to acquisition — aerial acquisition is proven; LiDAR acquisition is proven in-run but its reusable artifact is not yet preserved.
13. Do not treat the pre-fix EA failure as a current blocker.
14. Do not replace the working EA aerial/LiDAR runner with manual portal steps.
15. Do not declare the provider-neutral course package, terrain layer, registration or phone-ready course download complete until actual successful artifacts have been inspected.
16. Do not treat the stale beta catalog as evidence that a second course package exists.

## Change discipline

Whenever meaningful UiDo work changes project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite source data.
