# UiDo — Project Source of Truth

**Last updated:** 2026-09-20  
**Repository:** `mccrystal111-design/uido-live-test`  
**Canonical project:** UiDo golf decision engine / virtual caddie / SmartShot intelligence.

## Purpose

This document is the starting point for any new UiDo chat or development session. It records what exists, what is authoritative, what has already been done, what remains, and what must **not** be rebuilt.

A fresh session should read this document before asking the user for data or proposing to repeat earlier work.

## Core pipeline

`source capture -> deterministic normalisation -> provider-neutral course model -> measured OSM/satellite registration -> satellite feature refinement -> LiDAR enrichment -> verification/fusion -> phone/watch/renderers`

The guiding data policy is:

**source preserved -> derived explicit -> verified -> never silently replaced**

OSM provides the structural skeleton. Satellite imagery refines visible geometry. LiDAR provides terrain/height/vegetation structure. Verification is kept separate from candidate generation.

## Authoritative Overstone source data

### Recovered OSM capture — authoritative raw source

The original Overstone OSM GeoJSON has been recovered and persisted. **Do not ask the user to re-upload it.**

- Original uploaded filename: `export (1).geojson`
- Canonical recovered filename: `overstone-park-osm-capture-v0.2.geojson`
- UiDo Library: `/UiDo/Overstone/source/overstone-park-osm-capture-v0.2.geojson`
- Source identity lock: `course-models/OVERSTONE_OSM_SOURCE_LOCK.json`
- Source manifest: `course-models/OVERSTONE_SOURCE_MANIFEST.json`

The recovered capture contains the documented Overstone source counts:
- 18 holes
- 18 pins
- 20 greens
- 30 tee polygons
- 17 fairway polygons
- 31 bunkers
- 23 rough polygons
- 17 cart paths
- 2 water hazards
- 1 driving range

Preserve these source features. Do not invent an 18th fairway or collapse multiple tee polygons merely to force symmetry.

### Existing course model

- `course-models/overstone-park-v0.1.json`
- Schema: `uido.course.v0.1`
- Contains all 18 green F/M/B anchors.
- Current extraction status is green-anchor/source-feature stage; refined tee/fairway/hazard geometry is not yet complete.
- Registration transform and metrics must remain null until a measured OSM-to-satellite solution exists.

### Existing extraction and registration tooling

- `tools/course-model/build_overstone_model.py` — deterministic source normalisation.
- `tools/course-model/register_affine.py` — measured affine registration from real control points; reports residuals/RMS/max error.
- `docs/UI_DO_COURSE_MODEL_V0.1.md` — provenance and model rules.
- `docs/UI_DO_COURSE_EXTRACTION_ALGORITHM.md`
- `docs/UI_DO_COURSE_PIXEL_MODEL.md`
- `docs/UI_DO_PIXEL_TAGGER_SPEC.md`
- `docs/UI_DO_WHOLE_COURSE_TEE_EXTRACTION_ALGORITHM.md`

## Public imagery and LiDAR source strategy

The pipeline is now being shifted away from user-supplied screenshots as the primary imagery source.

The preferred public source is the **Environment Agency / Defra Vertical Aerial Photography** dataset. It provides orthorectified RGB/NIR aerial imagery at roughly 10–50 cm resolution, in ECW tiles on British National Grid, under the Open Government Licence. The Defra catalogue provides tile/date/resolution metadata and an area-of-interest download workflow. citeturn2view0

Overstone is approximately **52.27789, -0.81722**, around OSGB36 easting 480793 / northing 265074 (SP8065 area). The public-source execution plan is recorded in `course-models/OVERSTONE_PUBLIC_SOURCE_PLAN.json`.

For independent contextual validation, the Natural England/Sport England Sport Facilities dataset contains golf-course site points under OGL, while OS Open Greenspace is available as current open vector data. These are validation/context layers, not replacements for the detailed course model. citeturn3view0turn3search1

For terrain and vegetation, the Environment Agency National LiDAR Programme provides 1 m data products including point cloud, DSM, DTM, First Return DSM and intensity; the catalogue identifies the survey/tile/date. The EA also provides composite DTM/DSM products covering England. citeturn2view1turn2view2

The intended source hierarchy is now:

`EA aerial imagery -> OSM structural geometry -> pixel refinement -> EA LiDAR vegetation/terrain -> verification/fusion`

The objective is to work from the underlying geospatial sources, not screenshots, and use screenshots only as optional visual diagnostics.

## Satellite state

The working visual strategy and live test viewer exist, including an Esri World Imagery whole-course viewer:

- `uido-whole-course-satellite-test.html`

The historical controlled Hole 2 acquisition/analysis workflow is documented in:

- `tools/earth-studio/README.md`
- `tools/earth-studio/hole2-kml.kml`
- `uido-hole2-satellite-analysis.html`

A local Hole 2 satellite asset is referenced by the analysis page but is not currently present in the repository. It is no longer the preferred primary imagery source: first identify and acquire the fixed public EA aerial tile(s) for Overstone. Treat the old asset as historical/prototype material, not as a reason to fall back to screenshots.

## Registration state

Measured OSM-to-satellite registration is a distinct pipeline stage.

Do **not**:
- invent a transform;
- use validation GPS as a shortcut for candidate registration;
- reconstruct a transform from screenshots;
- silently apply an old/unmeasured transform.

The next registration step is to obtain/locate real measured control points against the fixed satellite raster, then run `register_affine.py` and record residuals and registration version in the course model. A machine-readable control-point template now exists at `course-models/OVERSTONE_REGISTRATION_CONTROL_POINTS.json`.

## Feature refinement

The established approach is two-pass:

1. Whole-course positive maintained-surface discovery.
2. Hole-specific refinement constrained by the OSM/source ROIs.

Established visual methods include feature-specific local signatures rather than one universal threshold. Green detection has used a local CIE Lab signature and spatial coherence; tee detection similarly uses local turf signatures and spatial opening. Bunkers, fairway/rough boundaries, trees and other features require their own evidence.

Do not turn visual experiments into authoritative course geometry without provenance and validation.

## LiDAR

LiDAR has not yet been ingested into the Overstone model.

Planned role:
- terrain/elevation
- tree/vegetation structure
- height/visibility context
- refinement of geometry where RGB imagery alone is ambiguous

## Existing useful project history

The repository already contains substantial prior UiDo work including:
- Overstone green geometry and F/M/B anchors.
- Overstone provider-neutral course model.
- deterministic model builder.
- measured registration tool.
- Hole 1/Hole 2 satellite analysis prototypes.
- whole-course satellite and tee-extraction experiments.
- Earth Studio acquisition instructions and KML.

Do not recreate these merely because a new chat cannot see an old conversation.

## DO NOT REBUILD

1. **Do not ask for `export (1).geojson` again.** It is recovered and persisted in the UiDo Library.
2. Do not recreate the Overstone OSM capture from screenshots or memory.
3. Do not invent missing course geometry to make counts look tidy.
4. Do not replace source geometry with derived geometry.
5. Do not overwrite verified/source features silently.
6. Do not generate PNGs simply to demonstrate progress.
7. Do not treat a screenshot/diagnostic as the source of truth when the underlying data exists.
8. Do not invent or reuse an unmeasured OSM-to-satellite transform.
9. Do not use verified GPS as candidate-generation geometry.
10. Do not ask the user to repeat information already recorded in this document, the source manifest, source lock, course model or Library.
11. If an artifact appears missing from GitHub, check the UiDo Library/conversation sources before declaring it lost.

## Current execution finding

The recovered Overstone OSM capture has been inspected directly. The 177-feature source contains the expected feature counts, but the feature polygons themselves do **not** carry hole numbers. Only the 18 `golf=hole` features have `ref=1..18`; tees, greens, fairways, rough, bunkers, paths and water are unassigned at source level. Therefore the normalisation stage must preserve all source geometry as unassigned source features first. Hole association should be performed spatially after registration, using the hole/green anchors and course geometry, rather than guessed from feature order.

This is an important source-schema fact and should not be lost or rediscovered in a future chat.

## Exact next step

**Source normalisation is now complete.** The exact 177-feature Overstone capture has been normalised without changing its geometry or inventing hole assignments. The normalized artifact is persisted in UiDo Library at `/UiDo/Overstone/source/overstone-source-normalized-v0.1.json` (schema `uido.course.source-normalized.v0.1`).

1. Recover or acquire the fixed satellite raster.
2. Establish real OSM-to-satellite control points.
3. Run the measured affine registration tool and record residuals.
4. Spatially associate the 141 currently unassigned non-hole/pin source features to holes using the registered geometry and existing hole/green anchors.
5. Refine feature geometry using OSM ROIs + satellite evidence.
6. Add LiDAR enrichment.
7. Validate and fuse into the UiDo course model.
8. Only then drive downstream renderers/UI from the model.


The immediate priority is the **public-source data/model pipeline**, not another visual prototype.

## Change discipline

Whenever meaningful UiDo work changes the project state, update this document so that it remains usable as a fresh-chat handover.

If there is a conflict between this document and actual authoritative source data, inspect the authoritative source, resolve the discrepancy explicitly, and update this document. Never silently guess.


## Public-source catalogue resolution — 2026-09-20

The Environment Agency catalogue services have now been confirmed directly. The Vertical Aerial Photography index is an EPSG:27700 polygon layer with fields for filename, survey id, OS 1k/5k references, flown dates, survey year, resolution, imagery type and band count. The National LIDAR Programme index is also EPSG:27700 and exposes tile name, survey id, flown dates, season, resolution and the DSM/DTM/FZ DSM/intensity/point-cloud filenames.

The public dataset records also expose direct download-distribution identifiers for the catalogue packages. A deterministic resolver has been added at tools/course-model/resolve_overstone_public_sources.py; it queries the EA ArcGIS catalogues at the Overstone EPSG:27700 coordinate and falls back to the EA survey-index WFS. It is deliberately metadata-only: no imagery or LiDAR is silently downloaded or transformed.

Current exact-source status: **the EA catalogue services are verified, but the exact Overstone aerial survey/date/resolution and LiDAR survey/date are still pending a live catalogue query.** The next data step is therefore source resolution, not pixel extraction. Once resolved, the raster's own EPSG:27700 georeferencing will be the primary coordinate-to-pixel mapping; any OSM-to-imagery residual will be measured separately rather than used to invent a raster transform.
