# UiDo Course Packet Specification — Draft v0.1

Status: **Draft for implementation review — not an approved geometry contract**  
Last updated: 2026-10-09  
Scope: the versioned, provider-neutral course data package consumed by the UiDo renderer/course loader, with a delivery boundary that can support offline play. This is not a Supabase schema decision and does not define player, round, or shot data.

## 1. Purpose and boundary

A course packet is a self-contained, immutable, versioned snapshot of the course data required to identify and render one or more holes without requiring the acquisition pipeline or network at render time.

The intended path is:

`source providers → acquisition/registration/refinement → canonical course model → validated course packet → local cache/offline package → course loader → renderer`

The renderer consumes canonical geometry and metadata, not provider-specific source records. Preserve source geometry and provenance alongside refined/canonical geometry; never silently replace source evidence.

Keep these concerns separate:

- **Course packet:** stable course identity, hole geometry/features, course metadata, provenance references, validation results and asset references.
- **Round/session packet:** selected tee/pin, player position, conditions, shots, decisions and score. It may reference a course packet by ID and revision but must not mutate it.
- **Presentation assets:** optional renderer assets/textures. Geometry must remain usable if an optional texture is absent; a missing required geometry record must fail validation.

## 2. Draft design principles

1. **Provider-neutral:** no consumer should need to know whether geometry came from OSM, survey imagery, LiDAR or another source.
2. **Immutable revisions:** corrections create a new packet revision; never mutate a packet already referenced by a recorded round.
3. **Offline-first:** all required geometry and metadata needed for the selected course/holes are included in or deterministically resolvable from the downloaded package.
4. **Explicit coordinate and unit rules:** no implicit axis swaps, hidden scale factors or per-file assumptions.
5. **Traceable geometry:** every canonical feature can be traced to source(s), transformation/refinement process and validation status.
6. **Fail visibly:** malformed or incompatible data must produce a specific validation error, not a blank canvas or plausible-looking wrong hole.
7. **No live-golfer side effects:** packet building, validation, publishing and QA must not create live rounds, alter player state or send golfer-facing notifications.
8. **Keep course data separate from identity:** course packages contain no personal player data, authentication secrets or service-role credentials.

## 3. Package layout (logical contract)

The physical archive format is intentionally not fixed in v0.1. A directory, ZIP or object-store bundle may implement the same logical structure.

```text
course-packet/
  manifest.json                 # required: identity, versions, files, checksums
  course.json                   # required: course-level metadata
  holes/
    01.geojson                  # required for each included hole
    02.geojson
    ...
  provenance/
    sources.json                # required: source references and processing history
  validation/
    report.json                 # required: schema + geometry validation summary
  assets/
    ...                         # optional, content-addressed renderer assets
```

A partial/offline subset must declare its coverage explicitly. Do not label a packet as a complete 18-hole course unless all expected holes and required features pass validation.

## 4. Manifest contract

`manifest.json` is the entry point and must contain:

| Field | Requirement | Meaning |
|---|---|---|
| `packet_format` | required string | Contract version, initially `uido.course-packet/0.1` |
| `course_id` | required stable string | UiDo canonical course identifier; never derive identity from display name alone |
| `course_revision` | required string | Immutable revision identifier for this course snapshot |
| `created_at` | required ISO-8601 UTC timestamp | Build time, not a golfer event |
| `producer` | required object | Builder name and version/commit where available |
| `coverage` | required object | Included hole IDs and whether coverage is complete or partial |
| `coordinate_reference` | required object | CRS identifier and axis order used by geometry files |
| `units` | required object | Canonical linear and elevation units |
| `files` | required array | Relative path, media type, byte size and SHA-256 for each packaged file except the manifest itself |
| `minimum_loader_version` | required string | Earliest loader version that can consume this packet |
| `extensions` | optional object | Namespaced, explicitly versioned extension fields |

Manifest paths must be relative, normalized and remain inside the package root. Reject absolute paths, traversal segments (`..`), duplicate paths and undeclared files where strict mode is enabled. The manifest cannot self-hash; a transport/index record may hash the final archive separately.

For deterministic builds, sort file entries by normalized path, serialize JSON consistently (UTF-8, stable key ordering, no insignificant whitespace where feasible), and compute checksums over the exact stored bytes. Reproducible archive byte-for-byte identity is a later optimization, not a v0.1 acceptance requirement.

## 5. Course and hole model

### Course metadata

`course.json` should carry stable `course_id`, human-readable name, known aliases, locality/country when known, expected hole count, par/yardage metadata when verified, source links/identifiers, and the canonical revision. Unverified values must be marked as such rather than guessed.

### Hole geometry

Each hole file is GeoJSON using WGS 84 longitude/latitude coordinates (RFC 7946 order: longitude, latitude) unless a later, explicit format version approves a different encoding. Elevation may be carried as a third coordinate only when its datum and unit are known; otherwise store elevation separately with its reference/datum.

Each hole record must have a stable `hole_id`, display hole number, par where verified, geometry version, and typed features. Required feature classes for the AGNOSTIC45 base are:

- tee areas
- fairway
- rough / playable-area boundaries where available
- green
- bunkers
- water
- paths where present

A feature needs a stable ID, a controlled feature type, valid geometry, provenance references and a quality/status value. Geometry type must be constrained by feature type in the canonical schema (for example, an area feature must not silently accept a Point). The exact allowed geometry cardinality and multipart rules must be agreed in the canonical geometry contract before being enforced in production.

Direction of play is hole-specific and must be explicit. Do not infer direction solely from feature ordering or share it across holes. Shared course features may be referenced by ID only if the packet also guarantees they resolve offline.

### Coordinate handling

- GeoJSON geographic geometry uses longitude then latitude, not latitude then longitude.
- Rendering transforms geographic coordinates into a local metric coordinate system through one documented, tested transform.
- The transform must preserve orientation and scale and expose enough metadata to reproduce it.
- Never mix degrees and metres in the same coordinate array.
- A packet may include precomputed local coordinates as an optimization only if the CRS/transform definition is recorded and geographic source coordinates/provenance remain available.
- Distance and elevation values use metres internally. Convert yards/feet at UI or import/export boundaries, with unit labels explicit.

## 6. Provenance and refinement

`provenance/sources.json` records, per source:

- source ID, provider/type, source identifier/URL where lawful, retrieval timestamp and source revision/date if available;
- source geometry/file checksum and licensing/usage note when known;
- transformation/refinement steps, software version/commit, parameters and output references;
- registration transform and error metrics where imagery registration was performed;
- feature-level links from canonical geometry to source feature(s);
- quality flags, unresolved conflicts and manual corrections.

Do not store credentials, access tokens or private URLs containing secrets. Retain original source geometry as a separate artifact or durable reference; a canonical refined boundary is not a substitute for source evidence.

## 7. Validation gates

A packet is publishable only when these gates pass or an explicitly allowed warning is recorded:

1. **Package integrity:** manifest parses; every declared file exists; sizes and SHA-256 checksums match; no unsafe paths.
2. **Schema compatibility:** packet format, required fields and feature types are supported by the declared loader version.
3. **Geometry validity:** coordinates are finite and in range; rings are closed where required; geometry is non-empty and structurally valid; no accidental lat/lon inversion detected by plausibility checks.
4. **Course coverage:** hole IDs/numbers are unique; declared complete coverage matches expected hole count; every required feature class has either geometry or an explicit missing/unknown status.
5. **Spatial consistency:** hole features lie within plausible course bounds; direction of play is present; transform is stable and not mirrored/scaled incorrectly.
6. **Provenance:** canonical features link to sources or are explicitly marked as manually authored with author/time/change reason.
7. **Renderer smoke test:** loader can load the packet offline and render selected holes with expected SVG/geometry roots and positive dimensions, without uncaught errors.
8. **Diagnostics:** report machine-readable errors/warnings with file, feature/hole ID and actionable reason.

Warnings must not be silently upgraded to passes. Validation proves structural readiness, not human approval of visual accuracy.

## 8. Versioning and compatibility

- `packet_format` versions the external packet contract independently from application releases and database migrations.
- Patch-level producer fixes that do not change packet meaning need not change the format version.
- Adding optional fields may be backward-compatible only when old readers safely ignore them.
- Renaming/removing required fields, changing coordinate semantics, units, feature-type meaning or geometry constraints requires a breaking format version.
- A loader must reject unsupported major versions and explain why.
- Keep a small set of fixture packets and compatibility tests for every supported format version.
- A packet revision identifies data content; a format version identifies the structure/semantics. They are not interchangeable.

## 9. Delivery, cache and storage boundaries

The consumer must be able to download or receive one package, validate it locally, cache it by `course_id + course_revision + packet_format`, and use it without network access. Updates should be downloaded as new immutable revisions; never partially overwrite the active cached revision. A failed download or checksum must leave the last valid package intact.

This specification does **not** select Supabase, object storage, Git, a NAS or a CDN as the final delivery backend. Choose the storage/delivery topology after measuring packet size, update frequency, access controls, retention, backup, bandwidth, cost and offline requirements. Supabase may index metadata or coordinate authorized access, but it should not be assumed to be the only place every large immutable geometry/asset file lives.

Course packet files are public/course-domain data unless a source licence says otherwise. Apply source-specific licence and attribution requirements. Private player, round and shot records belong in a separate access-controlled data domain.

## 10. Minimum acceptance tests for v0.1

- A known Overstone fixture builds a packet with manifest, course metadata, hole files, provenance and validation report.
- Every packaged file passes checksum/size verification; a deliberately corrupted file is rejected.
- A missing required hole or duplicate hole ID fails complete-coverage validation.
- A known coordinate fixture confirms longitude/latitude order, local orientation, scale and distance calculation.
- Invalid geometry and unsupported packet major version produce explicit errors.
- The same valid packet loads offline and renders holes 1 and 9 in the existing AGNOSTIC45 base without provider-specific code.
- A new packet revision can be installed without corrupting the previously cached revision.
- No test path writes to live golfer sessions, player profiles, scores or notifications.

## 11. Decisions still open

These are intentionally not guessed in v0.1:

1. Canonical feature schema, geometry type/cardinality and multipart rules — align with the hole-by-hole geometry contract and review PR #3 before approval.
2. Stable course/hole/feature ID generation and migration policy.
3. Whether the delivered bundle is ZIP, directory or another transport container.
4. Whether local metric coordinates are generated during acquisition or by the loader.
5. Asset embedding versus content-addressed sidecar assets and maximum package size.
6. Storage/delivery split between Git, object storage, Supabase metadata/indexing and local device cache.
7. Course completeness/quality thresholds and who approves visual accuracy.

## 12. Immediate implementation sequence

1. Review this draft alongside PR #3; do not merge the PR merely because this draft exists.
2. Freeze the canonical geometry/feature contract with one real Overstone hole fixture and explicit direction-of-play semantics.
3. Implement a packet builder around the successful provider-neutral course-builder output.
4. Implement an independent validator and a small fixture suite.
5. Add a loader adapter to the existing AGNOSTIC45 renderer; prove offline rendering before choosing production storage.
6. Decide delivery/storage responsibilities from measured package size and update needs, then map only the required metadata/index to Supabase if appropriate.

This document is a draft implementation contract. It does not approve the current PR #3 schema, certify existing course geometry as accurate, or decide the production storage provider.

## 13. Alignment with the current canonical database proposal (PR #3)

The open draft [PR #3](https://github.com/mccrystal111-design/uido-live-test/pull/3) proposes a canonical database model, while this document defines the **delivery packet** consumed by the loader. They are related but should not be the same serialization by accident: the packet builder maps a specific immutable canonical course version into a self-contained renderer-facing package and retains links back to evidence/provenance.

Inspection of PR #3's head branch at `feature/global-course-database-architecture` on 2026-10-02 found:

- `course.schema.json` requires `course_id`, `canonical_name`, `status`, `location` and `current_version`; it has latitude/longitude metadata and rejects undeclared fields.
- `feature.schema.json` lists feature types and confidence/verification fields, but `geometry` is only constrained to be an object with a description. It does not yet validate GeoJSON `type`, coordinate nesting, geometry-to-feature-type compatibility, coordinate reference semantics or cardinality.
- `provenance.schema.json` captures source/snapshot identifiers, timestamps, transformation and notes, but the packet still needs a clear feature-to-provenance linkage and source-file checksum/registration-error representation.
- The PR description explicitly calls for Overstone and Poult Wood fixtures before changing acquisition code. That sequencing is retained here.

These are observed schema gaps, not a rejection of PR #3. Before approval, use real fixtures to decide whether canonical storage keeps normalized feature records with separate provenance links, while packet output groups the required per-hole data and adds a manifest/file integrity layer. Do not duplicate conflicting definitions of course identity, feature enums or geometry semantics across schemas; make one canonical geometry contract and reference it from both database and packet validation.

## 14. Review checklist before implementation

- [ ] Inspect the actual current Overstone and Poult Wood builder outputs and preserve any useful existing fields.
- [ ] Build at least one real-hole fixture without discarding source geometry or provenance.
- [ ] Agree feature geometry types/cardinality and explicit direction-of-play semantics with the canonical geometry contract.
- [ ] Decide how canonical `course_version_id` maps to packet `course_revision` and how revisions remain immutable.
- [ ] Define a validator report format and decide which conditions are fatal versus warnings.
- [ ] Only after fixture and loader tests pass, decide package archive/container and storage/delivery topology.

## 11. Real Overstone fixture review — 2026-10-09

**Status: fixture inspected; contract and packet are not approved.** This section records observations from the committed files and live Supabase data. It does not certify the geometry as ready for golfers.

### Evidence inspected

- Source-normalized fixture: `course-models/source-normalized/overstone-source-normalized-v0.1.json`
  - 177 source features: 124 Polygon, 35 LineString and 18 Point.
  - Types: 31 BUNKER, 1 DRIVING_RANGE, 17 FAIRWAY, 20 GREEN, 18 HOLE, 18 PIN, 30 TEE, 23 ROUGH, 17 PATH and 2 WATER.
- Committed canonical model: `course-models/canonical/overstone-park-v1.json`
  - 159 course-scoped physical features: 124 Polygon, 17 LineString and 18 Point.
  - The 18 hole routes are stored separately on the hole records; the 18 PIN source features are represented as `target` physical features.
  - All 18 hole records have routing and are marked `CONFIRMED`, while course-level validation correctly remains incomplete with unresolved `satellite_registration` and `hole_feature_association`.
- Live Supabase `uido-production`:
  - Revision `v1-osm-source` remains `draft`.
  - 18 hole rows, 159 feature rows and 159 feature-provenance rows exist for the revision.
  - Public read policies expose course versions, holes, features and tees only when the version is `published`. The draft revision is therefore not a valid public runtime fixture.

### Reproducible draft and canonical contract — 2026-10-09

The pinned source-normalized fixture and committed canonical draft now have a deterministic build path. `tools/course-model/build_overstone_canonical_from_normalized.py` rebuilds the canonical draft from the committed normalized OSM fixture, course registry and `course_green_data.json`. The acceptance workflow validates the output against `canonical-course.schema.json` and compares the rebuilt JSON with the committed artifact.

[Overstone Fixture Acceptance QA run 37913598055](https://github.com/mccrystal111-design/uido-live-test/actions/runs/37913598055) passed:
- 159 stable physical feature IDs, exact source geometry, explicit type mapping and provenance.
- 18 unique hole routes and pars.
- All 54 green front/middle/back anchors match the pinned green source.
- Canonical JSON passes the schema.
- Course completeness remains false while registration and hole-feature association are unresolved.

A separate read-only comparison of the 54 green F/M/B coordinates in `course_green_data.json` with the live Supabase `course_holes` points found no differences greater than 5 cm. No database rows were written.

The generic builder `tools/course-model/build_canonical_course.py` has also been aligned to the same canonical vocabulary and core field structure: lower-case canonical feature types, structured provenance, direct GeoJSON routing, and green F/M/B anchors. It now refuses to mark a course complete unless registration has a measured transform and metrics, feature associations are explicitly verified, green anchors are present, all 18 routes exist, and there are no unresolved conflicts. Six unit tests passed in the same run.

### Two-stage producer contract — explicit, not yet publishable

The two producers now have an explicit `provenance.stage` field required by the canonical schema:

- **`source_only_draft`** is built deterministically from the pinned normalized source fixture. It preserves source IDs/geometry, routes and green F/M/B anchors, while keeping hole-feature association unresolved.
- **`enriched_candidate`** is produced by the live-acquisition/intermediate-model path. It can carry nearest-hole/nearest-green association evidence for review, but that evidence is not verified association. The generic builder now prevents this stage from claiming completeness until registration, associations, routes and green anchors pass.

`.github/workflows/validate-canonical-v2.yml` is explicitly named as a **manual live-acquisition candidate workflow**. It fetches fresh Overpass data to exercise that path; it is not a downstream consumer of the pinned source fixture and must not overwrite the source-only draft. Deterministic acceptance tests use committed fixtures and do not call external providers.

This removes the ambiguity about which stage an artifact belongs to. The remaining work is to define and implement the **promotion contract** from an enriched candidate to an immutable published revision, with a build manifest and package-level QA.

### Contract gaps to resolve before publishing

1. **Authoritative producer:** decide whether the pinned source-normalized adapter is the source-only draft producer and the live-acquisition path a separate candidate stage, or unify them behind one versioned pipeline. Never silently replace the pinned source fixture with a fresh provider response.
2. **Producer manifest:** record source hashes, producer/tool version, producer commit, course revision, schema version and generated asset checksums for each packet.
3. **Geometry validity:** the schema now checks GeoJSON geometry type/coordinates presence, canonical feature types, provenance and green anchor ranges. Still add geometry-type compatibility, polygon ring closure/topology, finite-coordinate checks in the generic builder, and plausible course bounds.
4. **Feature association:** retain nearest-path/nearest-green evidence, but do not treat distance-based heuristics as verified. Course-level completeness must stay false until an explicit verification status exists for required associations.
5. **Satellite registration:** measure and store the transform and error metrics; a source being available is not a registration solution.
6. **Runtime/offline package:** package the 18 routes, 54 F/M/B anchors, physical features, required assets, manifest and hashes; prove that the offline loader preserves these values.
7. **Supabase access:** automate anonymous/authenticated visibility tests against an isolated QA environment. Draft revisions must remain hidden; only published revisions should be visible to runtime clients.

### Acceptance checks — implemented and remaining

**Implemented and green**
- Deterministic build from the pinned source-normalized fixture; exact generated/committed canonical comparison.
- Stable feature IDs, exact geometry, type mapping, provenance links and 18 route/par records.
- All 54 green F/M/B anchors included in the canonical holes and checked against the pinned source.
- Canonical schema validation.
- Publication-gate unit tests: pending registration, heuristic association, missing route and missing green anchors all block completeness; a synthetic fixture with all gates verified can complete.
- Manual read-only comparison of live Supabase F/M/B coordinates against the pinned green source (all within 5 cm).

**Remaining before publishing**
- Unify or explicitly version the pinned adapter and live-acquisition/generic-builder paths.
- Record a reproducible build manifest and asset checksums.
- Strengthen geometry topology and plausible-bounds validation.
- Generate and validate the offline-ready package and verify green anchors survive packaging.
- Automate RLS visibility testing in isolated QA.
- Complete measured satellite registration and explicit physical-feature/hole association.

**Next DATA-001 action:** implement the promotion gate and generated package manifest for the two explicit producer stages, then validate the offline package. Do not publish the live Supabase revision or modify the renderer until registration and association gates pass.
