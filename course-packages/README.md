# UiDo Course Package

The UiDo Course Package is the offline runtime unit downloaded by the phone/watch before a round.

## Architecture

OSM + EA aerial + EA LiDAR + future providers
→ provider adapters
→ normalized source manifest
→ course processing
→ provider-neutral course model
→ compact UiDo Course Package
→ phone/watch

The player never downloads raw EA/OSM/LiDAR data.

## Package principles

- Offline-first: everything required for normal round play is local.
- Provider-neutral: runtime code consumes UiDo data, not EA/OSM-specific formats.
- Versioned: package schema and course revision are explicit.
- Provenance-preserving: source, derived and verified data remain distinguishable.
- Incremental: imagery, terrain and future layers can be independently versioned.
- Reviewable: acquisition success does not automatically publish a course.
- Compact: raw provider files stay in the central ingestion/archive layer.

## Initial package layout

course.json
manifest.json
holes/
  01.json ... 18.json
layers/
  overview.webp
  imagery/
  terrain/
  greens/
review/
  review.json

The exact tile layout is deliberately left open until the Overstone render benchmark is complete.

## Lifecycle

1. DISCOVER — identify course and footprint.
2. ACQUIRE — automatically obtain provider data.
3. PROCESS — crop, transform, derive and validate.
4. REVIEW — surface conflicts/errors for human review.
5. PUBLISH — create an immutable course revision.
6. DOWNLOAD — phone/watch obtains the compact package.
7. PLAY — runtime reads the package offline.

Acquisition is not publication.

## Overstone proof

Overstone Park is the first end-to-end acquisition target. The existing provider-neutral course model remains the source of truth for existing course structure; new EA layers are additive and must not silently replace OSM geometry.

## F/M/B green coordinate derivation

Validated during Overstone investigation: UiDo can derive Front/Middle/Back green GPS coordinates deterministically from OSM course geometry rather than requiring a separate F/M/B GPS provider.

For a hole:
- OSM `golf=hole` routing establishes the direction of play.
- The associated OSM `golf=green` polygon supplies the green geometry.
- Front and Back are derived from the green boundary in the playing direction.
- Middle is derived from the green polygon centroid.
- The resulting coordinates remain explicitly marked as **derived**, with OSM retained as the source geometry.

### Overstone validation

Overstone hole 1 reproduces the historical UiDo live-test coordinates exactly:
- Front: `52.2762446, -0.8166103`
- Middle: `52.2761187565, -0.8166885565`
- Back: `52.2759866, -0.8167443`

The OSM evidence is:
- green: `way/798091452`
- hole routing: `way/798140682`

The Front and Back values correspond to green boundary vertices and the Middle value corresponds to the green polygon centroid.

This is a validated derivation for Overstone hole 1, not yet a claim that the exact same boundary-selection rule has been independently compared against historical F/M/B data for all 18 holes.

The detailed derivation record is in `course-models/FMB_DERIVATION.md`.

**Next validation:** run the derivation across all 18 Overstone holes, then test the same deterministic method against Poult Wood before promoting it to the standard acquisition pipeline.
