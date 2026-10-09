#!/usr/bin/env python3
"""Deterministic acceptance checks for the committed Overstone source/canonical fixtures.

This validates fixture coherence only. It does not claim that the current canonical
builder can reproduce the committed draft, and it does not approve the course for play.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATH = ROOT / "course-models/source-normalized/overstone-source-normalized-v0.1.json"
CANONICAL_PATH = ROOT / "course-models/canonical/overstone-park-v1.json"
LEGACY_MODEL_PATH = ROOT / "course-models/overstone-park-v0.1.json"

TYPE_MAP = {
    "WATER": "water",
    "TEE": "teeing_area",
    "GREEN": "green",
    "BUNKER": "bunker",
    "FAIRWAY": "fairway",
    "DRIVING_RANGE": "driving_range",
    "ROUGH": "rough",
    "PATH": "path",
    "PIN": "target",
}
EXPECTED_GEOMETRY = {
    "water": "Polygon",
    "teeing_area": "Polygon",
    "green": "Polygon",
    "bunker": "Polygon",
    "fairway": "Polygon",
    "driving_range": "Polygon",
    "rough": "Polygon",
    "path": "LineString",
    "target": "Point",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def positions(coordinates):
    if (
        isinstance(coordinates, list)
        and len(coordinates) >= 2
        and isinstance(coordinates[0], (int, float))
        and not isinstance(coordinates[0], bool)
        and isinstance(coordinates[1], (int, float))
        and not isinstance(coordinates[1], bool)
    ):
        yield coordinates[0], coordinates[1]
        return
    if isinstance(coordinates, list):
        for child in coordinates:
            yield from positions(child)


def check_geometry(geometry, label):
    assert isinstance(geometry, dict), f"{label}: geometry is not an object"
    geometry_type = geometry.get("type")
    assert geometry_type in {"Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"}, (
        f"{label}: unsupported GeoJSON geometry type {geometry_type!r}"
    )
    coords = geometry.get("coordinates")
    points = list(positions(coords))
    assert points, f"{label}: geometry has no coordinate positions"
    for lon, lat in points:
        assert math.isfinite(lon) and math.isfinite(lat), f"{label}: non-finite coordinate"
        assert -180 <= lon <= 180, f"{label}: longitude outside WGS84 range: {lon}"
        assert -90 <= lat <= 90, f"{label}: latitude outside WGS84 range: {lat}"
    return geometry_type


def main():
    source = load(SOURCE_PATH)
    canonical = load(CANONICAL_PATH)

    assert source.get("schema") == "uido.course.source-normalized.v0.1"
    assert canonical.get("schema") == "uido.course.canonical.v2"
    assert source.get("course_id") == canonical.get("course", {}).get("id") == "overstone-park"

    source_features = source.get("features", [])
    source_holes = [f for f in source_features if f.get("canonical_type") == "HOLE"]
    source_physical = [f for f in source_features if f.get("canonical_type") != "HOLE"]
    canonical_features = canonical.get("geometry", {}).get("features", [])
    canonical_holes = canonical.get("holes", [])

    assert len(source_features) == 177, f"Expected 177 source-normalized features, got {len(source_features)}"
    assert len(source_holes) == 18, f"Expected 18 source hole routes, got {len(source_holes)}"
    assert len(source_physical) == 159, f"Expected 159 physical features, got {len(source_physical)}"
    assert len(canonical_features) == 159, f"Expected 159 canonical physical features, got {len(canonical_features)}"
    assert len(canonical_holes) == 18, f"Expected 18 canonical hole records, got {len(canonical_holes)}"

    source_by_id = {str(f["source_id"]): f for f in source_physical}
    canonical_by_id = {str(f["id"]): f for f in canonical_features}
    assert len(source_by_id) == len(source_physical), "Source physical feature IDs are not unique"
    assert len(canonical_by_id) == len(canonical_features), "Canonical physical feature IDs are not unique"
    assert set(source_by_id) == set(canonical_by_id), (
        f"Physical feature identity mismatch: missing={sorted(set(source_by_id)-set(canonical_by_id))[:10]}, "
        f"extra={sorted(set(canonical_by_id)-set(source_by_id))[:10]}"
    )

    for feature_id, source_feature in source_by_id.items():
        feature = canonical_by_id[feature_id]
        expected_type = TYPE_MAP.get(source_feature.get("canonical_type"))
        assert expected_type, f"{feature_id}: no canonical type mapping for {source_feature.get('canonical_type')!r}"
        assert feature.get("type") == expected_type, (
            f"{feature_id}: expected type {expected_type!r}, got {feature.get('type')!r}"
        )
        assert feature.get("geometry") == source_feature.get("geometry"), (
            f"{feature_id}: canonical geometry differs from the pinned source geometry"
        )
        geometry_type = check_geometry(feature.get("geometry"), feature_id)
        assert geometry_type == EXPECTED_GEOMETRY[expected_type], (
            f"{feature_id}: {expected_type} must use {EXPECTED_GEOMETRY[expected_type]}, got {geometry_type}"
        )
        provenance = feature.get("provenance") or {}
        assert provenance.get("source_id") == "osm", f"{feature_id}: missing OSM provenance"
        assert provenance.get("source_feature_id") == feature_id, f"{feature_id}: source feature ID mismatch"
        assert feature.get("verification_status"), f"{feature_id}: missing verification status"
        assert feature.get("quality_status"), f"{feature_id}: missing quality status"

    source_holes_by_number = {}
    for feature in source_holes:
        number = int(feature.get("hole_ref"))
        assert number not in source_holes_by_number, f"Duplicate source route for hole {number}"
        source_holes_by_number[number] = feature
    assert set(source_holes_by_number) == set(range(1, 19)), "Source hole refs must cover 1–18 exactly"

    canonical_holes_by_number = {int(h["hole_number"]): h for h in canonical_holes}
    assert len(canonical_holes_by_number) == 18, "Canonical hole numbers are not unique"
    assert set(canonical_holes_by_number) == set(range(1, 19)), "Canonical hole numbers must cover 1–18 exactly"

    for number in range(1, 19):
        source_hole = source_holes_by_number[number]
        hole = canonical_holes_by_number[number]
        assert hole.get("routing") == source_hole.get("geometry"), f"Hole {number}: routing geometry mismatch"
        raw_par = (source_hole.get("properties") or {}).get("par")
        expected_par = int(raw_par) if str(raw_par or "").isdigit() else None
        assert hole.get("par") == expected_par, f"Hole {number}: par mismatch"
        check_geometry(hole.get("routing"), f"hole {number} routing")

    validation = canonical.get("validation") or {}
    assert validation.get("physical_geometry_count") == len(canonical_features)
    assert validation.get("unique_physical_ids") == len(canonical_by_id)
    assert validation.get("course_complete") is False, "Unverified course must not be marked complete"
    unresolved = set(validation.get("unresolved_features") or [])
    assert {"satellite_registration", "hole_feature_association"}.issubset(unresolved), (
        "Draft must retain the unresolved registration and hole-feature association gates"
    )

    # Guard against treating the older green-anchor staging file as a complete
    # geometry-bearing input to the canonical v2 builder.
    legacy = load(LEGACY_MODEL_PATH)
    buckets = ("tees", "fairways", "rough", "green_source_features", "paths", "context", "hazards")
    legacy_geometry_count = sum(
        len(hole.get(bucket, []) or [])
        for hole in legacy.get("holes", [])
        for bucket in buckets
    ) + len(legacy.get("unassigned_features", []) or [])
    if legacy_geometry_count == 0:
        print("NOTE: legacy v0.1 model is green-anchor-only; do not use it as the physical-geometry fixture.")

    print("PASS: pinned Overstone source and committed canonical draft are internally consistent.")
    print("PASS: 159 stable physical feature IDs, exact source geometry, type mapping and provenance links.")
    print("PASS: 18 unique hole routes and pars match the source fixture.")
    print("PASS: registration/association remain unresolved; course completeness remains false.")
    print("NOTE: this is fixture-coherence QA, not canonical-builder reproducibility or course publication approval.")


if __name__ == "__main__":
    main()
