# UiDo — Project Source of Truth

**Last updated:** 2026-09-23  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

This is the first file a fresh UiDo session should read. It records authoritative data, completed work, current blockers, exact next step, and what must not be rebuilt.

## Current state

**Course acquisition → packet pipeline: VALIDATED. Wireframe stage: IMPLEMENTED, NOT YET PROVEN IN THE MASTER RUN.**

Master workflow run `35849229103` successfully completed **Stage 1 acquisition** and **Stage 2 packet QA** for Poult Wood. Its artifacts `uido-course-acquisition-poult-wood` and `uido-course-packet-poult-wood` are present and unexpired. The run's actual job list contains only acquisition and packet-QA jobs; there is **no Stage 3 wireframe job in that run**. Do not describe that run as proof of packet-driven wireframe output.

Current repository head is `9734dc0e1011d1c35b716208a66a9f82ba870d10` (`Harden wireframe fairway source handling`). That commit hardens the downstream renderer so focused fairway queries treat relations as authoritative features and member ways only as reconstruction inputs, preventing duplicate rendering/counting. It also fails closed if the packet does not contain all 18 target hole routes.

The repository is using a modular course pipeline:
- `.github/workflows/build-course-ea.yml` — reusable/manual acquisition.
- `.github/workflows/build-course.yml` — master orchestration.
- `course-models/COURSE_PIPELINE.md` — architecture contract.
- `PROJECT_STATUS.md` — human handover/source of truth.

**Current active job: run the current master pipeline for Poult Wood and prove Stage 3 wireframe consumes the canonical Course Packet.**

Acquisition and downstream processing remain separate. Once acquired and QA'd, the Course Packet is the persisted hand-off/memory layer. Downstream stages must not silently re-query or recapture OSM/EA data. The architecture contract explicitly requires downstream stages to consume the packet rather than recapturing source data. fileciteturn3file0

## Recent course-model findings

### F/M/B derivation — corrected and still under investigation

`course-models/FMB_DERIVATION.md` is corrected to the proper historical association: the recovered historical F/M/B test belongs to **Overstone hole 2**, not hole 1. The OSM green/route relationship and Front/Back source vertices are proven, but the exact historical point-selection algorithm is **not** proven.

Required validation: analyse all 18 Overstone greens to identify the common F/B/M construction rule before testing Poult Wood. Do not promote a universal F/M/B derivation yet.

### Hole orientation / OpenYardage sense check

`course-models/HOLE_ORIENTATION_SENSE_CHECK.md` defines the intended local frame: Y = forward along play, X = left/right, while preserving underlying geospatial geometry. OpenYardage is an independent golf-useful sense check only; discrepancies become QA warnings, not automatic geometry edits.

### Poult Wood — source identity confirmed; QA work active

`course-models/POULT_WOOD_SOURCE_MANIFEST.json` records the 18-hole Poult Wood target and retains the raw OSM source without invented geometry.

The existing Poult Wood fairway association logic is important and must be preserved when the wireframe workflow is refactored. It reconstructs OSM fairway multipolygon relations from their members and associates them to the target 18 holes without inventing, smoothing or moving geometry.

## Authoritative Overstone source

### Raw OSM — authoritative

Do not ask the user to re-upload the OSM capture.

- Library: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
- Library file id: `file_00000000e32481f4a00f707344416e79`
- SHA-256: `e1eebf606f5e2767cfdf2af3951f7e2f50660b5b6b75ff2567af5c755a01b16e`
- GitHub identity lock: `course-models/OVERSTONE_OSM_SOURCE_LOCK.json`
- GitHub manifest: `course-models/OVERSTONE_SOURCE_MANIFEST.json`

### Normalised source — authoritative derived artifact

- Library: `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json`
- Library file id: `file_0000000052948210969af327286d4488`
- Schema: `uido.course.source-normalized.v0.1`
- SHA-256: `876eb808a978f577057747f71cca759d4032ed5cc776c3bf036eb126ce6b28e9`
- Status: **complete**; source geometry unchanged.

Library retrieval reconfirms both authoritative Overstone files are present. fileciteturn7file0 fileciteturn7file1

### Library v0.4 discrepancy

A previously recorded `/UiDo/UiDo_Overstone_Course_Model_v0.4.json` is still not surfaced by the current Library search. Treat v0.4 as **unlocated/not verified**, not deleted. Do not recreate it or silently promote it over the GitHub v0.1 model.

## Overstone model-generation / acquisition issue

The latest known Overstone builder regression remains run `35627704315` on commit `9ca6c0974a3928eba3d9b7aadf4d97254ef673ea`: EA aerial, LiDAR, compact aerial rendering and terrain complete; the run fails only at **Acquire Overstone OSM golf source** with Overpass HTTP 406.

The model-generation fix is present but not proven in a successful post-fix package build because acquisition is blocked before model generation.

Do not replace the authoritative OSM source because of this acquisition regression. Repair only the failing acquisition step, then prove the post-fix model build.

## Successful combined Overstone build

Workflow run `35608919741` / commit `2c4697c77fbceeec2d8789245570668f1a513f7e` completed:
1. EA aerial acquisition;
2. EA LiDAR acquisition;
3. compact aerial render;
4. terrain layer;
5. UiDo offline course package;
6. human-review bundle;
7. artifact uploads.

The existence of the old package does not prove the newer model-generation fix is incorporated.

## Issue #2 / build sequence

GitHub Issue #2 remains the active vertical-slice build contract: Overstone course loader → player position → shot situation model → SmartPoint → SmartShot → Caddie → shot lifecycle → playable hole → 18-hole round → live course testing.

Engineering rules: deterministic fixtures before live sensors; test each component before integration; do not change two layers simultaneously while debugging; keep Parking Lot features out of this phase.

## Registration / refinement

Measured OSM-to-raster registration remains a separate stage. `course-models/OVERSTONE_REGISTRATION_CONTROL_POINTS.json` is the control-point template. Do not invent/reuse a transform or use validation GPS as candidate-generation geometry.

## UI / product state

The Library remains the UI source of truth: premium golf instrument aesthetic, light/dark system, persistent navigation icon language and the GPS/Yardage/Wind/Lie/Start Line/Shape/Strike live shot flow. Strategy remains out of the live flow until SmartShot is ready. The current Library design direction explicitly keeps the live sequence as GPS/Yardage → Wind → Lie → Start Line → Shape → Strike, with a premium golf-instrument aesthetic rather than a generic software dashboard. fileciteturn6file4

## Unified course pipeline

The separate capture pots are now joined through a modular master pipeline.

- `.github/workflows/build-course-ea.yml` is manually runnable and reusable via `workflow_call`.
- `.github/workflows/build-course.yml` is the master orchestration workflow.
- The master calls acquisition, downloads the resulting acquisition artifact, validates the standard packet contract, and republishes the validated packet as `uido-course-packet-<course-id>`.
- `course-models/COURSE_PIPELINE.md` is the architecture contract: the Course Packet is the hand-off between acquisition and every downstream processing stage.
- Downstream processing must not silently recapture OSM/EA data.
- Acquisition and processing can therefore be iterated independently without losing the captured source state.

The master pipeline's Poult Wood run `35849229103` proved the **acquisition → packet QA foundation**, not Stage 3. The current wireframe refactor is present on `main` but requires a fresh master run to prove packet-driven execution.

## JOBS TO DO — fresh-chat handover

**This section is the persistent working queue. A new chat should start here rather than reconstructing the plan from conversation history.**

### 1. NEXT — Validate packet-driven wireframe stage

**Status: IMPLEMENTED — READY TO RUN**

The wireframe workflow and renderer have now been refactored so the downstream stage consumes `uido-course-packet-<course-id>` rather than independently querying Overpass.

Recent hardening on `main`:
- fairway **relations** are treated as the authoritative fairway features;
- member ways are reconstruction inputs only;
- duplicate rendering/counting of relation + member geometry is prevented;
- the stage fails closed if the packet lacks any of the 18 target hole routes.

Requirements:
- Keep the current Poult Wood wireframe/fairway association logic.
- Preserve OSM fairway multipolygon relation reconstruction.
- Do not invent, smooth, move or replace source geometry.
- Do not silently recapture OSM/EA if packet data is available.
- Make the wireframe workflow reusable against any valid Course Packet.
- Have the master pipeline invoke the wireframe stage after packet QA.
- The resulting wireframe should be a downstream processing artifact, not a new source of truth.

### 2. Add GolfCourseAPI discovery/import layer

**Status: PLANNED**

Use GolfCourseAPI as the discovery/index front door, not as physical geometry authority.

Build:
- course discovery/import;
- provider-neutral course registry;
- normalised course identity and metadata;
- registry state/lifecycle such as discovered → registered → acquisition-ready → acquired → QA → wireframe/model → UiDo-ready;
- UK/GB import capability without hard-coding UK into the underlying acquisition engine.

### 3. Northampton Golf Club — first genuinely new end-to-end course

**Status: PLANNED AFTER #2**

Use Northampton Golf Club as the first fresh course that has not been manually built into the pipeline.

Run it through:
**GolfCourseAPI discovery → registry → acquisition → Course Packet → packet QA → wireframe → downstream course model/loader.**

This is the key proof that the architecture is genuinely agnostic rather than Poult/Overstone-specific.

### 4. GPS-aware nearest-course selection in the app

**Status: FUTURE TODO**

On app launch:
- request GPS permission;
- obtain a usable location lock;
- use lat/long against the UiDo Course Registry;
- calculate nearest courses;
- show nearby courses sorted by distance in a dropdown/list;
- distinguish registered/acquired courses from **UiDo-ready** courses;
- allow manual search if GPS is unavailable, permission is denied, or no nearby course is found;
- avoid repeatedly requesting GPS once a usable location has been established.

This is a later player-facing feature; do not mix it into the acquisition refactor.

### 5. Overstone acquisition repair + post-fix proof

**Status: PARALLEL / SEPARATE**

Repair only the Overpass HTTP 406 acquisition failure. Then run the existing model-generation fix and prove a populated 18-hole post-fix package.

Do not rebuild the wider pipeline because of this one acquisition failure.

### 6. F/M/B validation

**Status: VALIDATION TASK**

Analyse all 18 Overstone greens to identify the common historical F/M/B construction rule. Only after the rule is proven should Poult Wood be tested.

F/M/B investigation is **not** permission to rewrite source geometry.

### 7. Registration / refinement

**Status: LATER**

Establish measured OSM-to-raster control points and registration metrics. Preserve OSM geometry and provenance while storing refined UiDo geometry separately.

## EXACT NEXT STEP

**Run the current `main` master course pipeline for Poult Wood using the canonical Course Packet flow and verify Stage 3 — wireframe — actually executes from the packet. Confirm the wireframe output and fairway association report match the trusted previous Poult Wood QA behaviour. If green, move to GolfCourseAPI discovery/import.**

If the master run does not invoke Stage 3, treat that as a workflow wiring discrepancy and repair only the orchestration; do not recapture source data.

## DO NOT REBUILD

1. Do not ask for or recreate the authoritative Overstone OSM capture.
2. Do not recreate the complete normalised source; it is present and authoritative.
3. Do not recreate or promote Library v0.4 without locating and comparing the actual artifact.
4. Do not rebuild the entire Overstone pipeline because of Overpass HTTP 406; repair only the failing acquisition step.
5. Do not replace EA aerial/LiDAR acquisition with manual portal steps.
6. Do not invent an OSM-to-raster transform or reuse an unmeasured one.
7. Do not use validation GPS as candidate-generation geometry.
8. Do not generate PNGs merely to demonstrate progress.
9. Do not treat screenshots/diagnostics as source of truth when underlying data exists.
10. Do not silently overwrite verified/source geometry with derived geometry.
11. Do not treat the old successful package as proof that the new model-generation fix is incorporated.
12. Do not promote the F/M/B derivation to a universal rule; the exact point-selection algorithm is still under investigation.
13. Do not treat OpenYardage as UiDo source geometry; it is an independent sense check only.
14. Do not treat Poult Wood wireframe QA as a replacement for the Overstone Stage 1 contract.
15. Do not treat stale beta catalogue metadata as evidence of a published second-course package.
16. If a GitHub artifact appears missing, check artifact history and Library/conversation sources before declaring it missing.
17. Do not ask the user to repeat information already recorded here or in the source manifests/locks/course model/Library.
18. Do not treat run `35849229103` as proof of Stage 3 wireframe; its verified jobs only cover acquisition and packet QA.

## Change discipline

Whenever meaningful UiDo work changes project state, update this document. If GitHub and Library disagree, inspect both authoritative artifacts, record the discrepancy explicitly, and resolve it deliberately. Never guess or silently overwrite source data.
