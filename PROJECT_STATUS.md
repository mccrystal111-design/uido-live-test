# UiDo — Project Source of Truth

**Last updated:** 2026-09-21  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, completed work, current blockers, exact next step, and what must not be rebuilt.

## Current state

**Overstone data foundation: READY.** The authoritative OSM capture and deterministic normalised source remain locked and unchanged. The provider-neutral v0.1 course model remains the GitHub canonical model. EA aerial acquisition is proven. A later successful combined build also completed EA LiDAR acquisition, terrain assembly, compact aerial rendering, the UiDo offline course package and the human-review bundle.

The successful end-to-end proof is workflow run `35608919741` on commit `2c4697c77fbceeec2d8789245570668f1a513f7e`. Its four unexpired artifacts are recorded below. These are real GitHub Actions artifacts, not screenshots or inferred outputs.

The **current repository head** is commit `b71a974c771852be7a3382bfd6a368672f353379` (`Add Lo Flag Icon asset`). This latest asset commit does not change the Overstone builder status. The latest verified Overstone run remains `35627704315` on commit `9ca6c0974a3928eba3d9b7aadf4d97254ef673ea`; it reaches EA aerial acquisition, LiDAR acquisition, compact aerial rendering and terrain assembly successfully, but currently fails at **Acquire Overstone OSM golf source** because the Overpass request returns HTTP `406`. This is a current workflow/integration blocker, not a failure of the EA data path or terrain path.

**Recent UI asset work:** `assets/Lo_Flag_Icon.svg` is now committed at `b71a974c771852be7a3382bfd6a368672f353379`. This is a completed asset addition only; it does not supersede any existing UI source-of-truth blueprint or alter the course-data pipeline.

**Do not start another visual prototype.** The next product-engineering slice is now the hand-off from the successful Overstone course package into the UiDo course loader, as defined by GitHub Issue #2.

## Authoritative Overstone source

### Raw OSM — authoritative

Do not ask the user to re-upload the OSM capture.

- Library: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
- Library file id: `file_00000000e32481f4a00f707344416e79`
- SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- GitHub identity lock: `course-models/OVERSTONE_OSM_SOURCE_LOCK.json`
- GitHub manifest: `course-models/OVERSTONE_SOURCE_MANIFEST.json`

Library search reconfirms this file is present and indexed. Source counts: 18 holes, 18 pins, 20 greens, 30 tees, 17 fairways, 31 bunkers, 23 rough, 17 paths, 2 water hazards, 1 driving range; 177 features total. Only `golf=hole` features carry explicit `ref=1..18`; other feature classes must be associated spatially/derived, never by feature order.

### Normalised source — authoritative derived artifact

- Library: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
- Library file id: `file_0000000052948210969af327286d4488`
- Schema: `uido.course.source-normalized.v0.1`
- SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
- Status: **complete**; source geometry unchanged; no invented hole assignments.

Library search reconfirms this file is present and indexed.

## Course model state

### GitHub canonical model

- `course-models/overstone-park-v0.1.json`
- Schema: `uido.course.v0.1`
- Contains all 18 green F/M/B anchors.
- Registration transform/metrics remain null until measured control points are used.

### Library discrepancy — preserve, do not overwrite

A previously recorded Library `/UiDo/UiDo_Overstone_Course_Model_v0.4.json` is still not surfaced by current Library search/folder indexing. Treat v0.4 as **unlocated/not verified**, not deleted. Do not recreate it, promote it, or overwrite v0.1 until the actual artifact is located and compared.

## EA public-source state

### Catalogue resolution — COMPLETE

Exact Overstone EA coverage is resolved in EPSG:27700.

- Aerial: 2013, 0.25 m, product `vertical_aerial_photography_tiles_night_time`; required ECWs are P00055683, P00055670, P00055697 and P00055618.
- LiDAR: 1 m survey `P_10738`, flown 2020-01-29 and 2020-03-06; required tiles SP8060/SP8065 with DTM/DSM and related records resolved in repository manifests.
- Course footprint: E 480137.49–481451.93 / N 264803.28–266016.15, EPSG:27700.

### Successful combined build — PROVEN

Workflow run `35608919741` / commit `2c4697c77fbceeec2d8789245570668f1a513f7e` completed every build step successfully, including:

1. EA aerial acquisition;
2. EA LiDAR acquisition;
3. compact aerial render;
4. compact terrain layer;
5. UiDo offline course package;
6. Overstone human-review bundle;
7. artifact uploads.

Unexpired artifacts as of 2026-09-21:

- `overstone-uido-course-package` — artifact `10643427997`, 14,378,531 bytes, digest `sha256:f5d9bbc1e8974c83edb0f3ca335606c477101451b477baf7ea4e1a74dba3b147`, expires 2026-10-05.
- `overstone-course-review` — artifact `10644240369`, 691,380 bytes, digest `sha256:9116bb8a8e477660c38c6b849a58b9c4b387ddacd3822928bdba576c3c53e950`, expires 2026-10-05.
- `overstone-ea-lidar-capture` — artifact `10644520389`, 565,217,647 bytes, digest `sha256:9cbd7c44e5a86b4aa8ad4de5ab081103621218f72102ee6d457662147466433f`, expires 2026-10-05.
- `overstone-ea-aerial-capture` — artifact `10643772746`, 24,929,315 bytes, digest `sha256:cf67ac99802888ecab5a9ee9825893e3d074ec832a7c1617cdb4598502f5ed2c`, expires 2026-10-05.

**Important:** the existence and successful creation of these artifacts is verified. The final package/review contents still need deliberate inspection before calling the package contract verified/publishable.

### Current builder regression

Run `35627704315` on commit `9ca6c0974a3928eba3d9b7aadf4d97254ef673ea` completed the following successfully before failing:

- EA aerial discovery/download;
- EA LiDAR discovery/download/extraction;
- ECW/GDAL compact aerial render;
- DTM/DSM terrain VRT + COG + previews.

It failed at **Acquire Overstone OSM golf source** with `curl: (22) The requested URL returned error: 406` from `https://overpass-api.de/api/interpreter`. Therefore the EA acquisition/terrain path is not the blocker. The existing authoritative OSM source must not be recreated just to work around this regression.

The previous terrain `find` syntax failure is **not** a current blocker; the current run proves the terrain fix works.

## Issue #2 build contract

GitHub Issue #2 is the active build sequence: **vertical slices**, each with data → UI → decision/state and a test harness before integration.

Sequence: Overstone course loader → player position → shot situation model → SmartPoint → SmartShot → Caddie → shot lifecycle → playable hole → 18-hole round → live course testing.

Engineering rules: deterministic fixtures before live sensors; test each component before integration; do not change two layers simultaneously while debugging; keep Parking Lot features out of this phase.

## Registration / refinement state

Measured OSM-to-raster registration is still a separate stage. `course-models/OVERSTONE_REGISTRATION_CONTROL_POINTS.json` is the control-point template. Do not invent/reuse a transform or use validation GPS as candidate-generation geometry. After the package/loader contract is verified, obtain real measured control points, run `register_affine.py`, and record residuals/RMS/max error.

Established refinement remains two-pass: whole-course maintained-surface discovery, then hole-specific refinement constrained by source ROIs. Preserve feature provenance/confidence. LiDAR is intended for terrain/elevation, vegetation/tree structure, height/visibility context and ambiguous geometry refinement.

## UI / product state

The Library remains the source of truth for the current UI: premium golf instrument aesthetic, light/dark system, persistent navigation icon language and the GPS/Yardage/Wind/Lie/Start Line/Shape/Strike live shot flow. Strategy stays out of the live flow until SmartShot is ready.

The current Library also contains approved UI source-of-truth blueprints for the premium aesthetic, live round flow, Shape tile and Putts/Score tile. The newly committed `assets/Lo_Flag_Icon.svg` is an asset addition, not a replacement for those blueprints.

## Beta environment discrepancy

Current `beta/catalog.json` still says the second course is generic `Second course` with no package URL, while a later commit is explicitly titled `Use Poult Wood as second beta course`. Treat the catalog as **stale beta metadata**, not as proof that a second course package exists. This is separate from the Overstone package work.

## Outstanding work

1. **Inspect the successful `overstone-uido-course-package` and `overstone-course-review` artifacts from run `35608919741` and define/verify the loader contract.**
2. Build the Overstone course-loader vertical slice and prove one real hole renders from the successful package.
3. Resolve the current Overpass HTTP 406 regression in the builder without replacing or recreating the authoritative OSM source.
4. Verify player-position/distance fixtures against the real course package.
5. Establish measured OSM-to-raster control points and registration metrics.
6. Locate and deliberately reconcile Library v0.4 before promoting a new course-model version.
7. Keep beta metadata/package links aligned once an approved package is published.

## EXACT NEXT STEP

**Use the successful artifact `overstone-uido-course-package` from run `35608919741` as the input to Issue #2 Step 1. Inspect its manifest/schema/file structure, define the exact package → UiDo course-loader contract, then build a deterministic test harness that selects one real Overstone hole and renders its real geometry.**

Do **not** rebuild the course data. Do **not** wait for a new EA acquisition run before starting the loader contract: the successful package already exists and is unexpired.

Separately, fix the current builder's Overpass 406 only as a contained acquisition-step repair. Do not touch the authoritative source files or alter the successful EA/LiDAR processing path while doing so.

## DO NOT REBUILD

1. **Do not ask for `export (1).geojson` again.** The authoritative OSM capture is recovered and persisted.
2. Do not recreate the normalised source; it is complete and persisted.
3. Do not recreate the course model from screenshots, memory or a fresh OSM scrape.
4. Do not replace source geometry with derived geometry or silently overwrite verified/source features.
5. Do not invent an OSM-to-raster transform or reuse an unmeasured one.
6. Do not use validation GPS as candidate-generation geometry.
7. Do not generate PNGs merely to demonstrate progress.
8. Do not treat screenshots/diagnostics as the source of truth when underlying data exists.
9. Do not ask the user to repeat information already recorded here, in source manifests/locks, the course model or the Library.
10. If a GitHub artifact appears missing, check its artifact history and Library/conversation sources before declaring it lost.
11. Do not silently promote Library v0.4 over GitHub v0.1; the current Library index does not surface v0.4, so locate it before any promotion decision.
12. Do not treat EA catalogue connectivity as equivalent to acquisition; both aerial and LiDAR acquisition are now proven.
13. Do not treat the old pre-fix terrain failure as a current blocker; the successful run proves terrain assembly works.
14. Do not replace the working EA aerial/LiDAR runner with manual portal steps.
15. Do not declare the provider-neutral package/loader contract verified until the actual successful package and review artifacts have been inspected.
16. Do not treat the stale beta catalog as evidence that a second course package exists.
17. Do not rebuild the entire Overstone pipeline because of the current Overpass 406; repair only the failing OSM acquisition step.
18. Do not treat the `Lo_Flag_Icon.svg` asset commit as evidence that the Overstone/course-loader state has changed.

## Change discipline

Whenever meaningful UiDo work changes project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite source data.
