#!/usr/bin/env python3
"""Build the Overstone canonical v2 draft deterministically from the pinned normalized fixture.

This adapter intentionally preserves the current committed canonical artifact's shape.
It does not infer hole-feature associations, perform satellite registration, or publish.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

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
CANONICAL_REVISION = "v1-osm-source"
PROVENANCE_POLICY = "source_preserved_derived_explicit_verified_never_silent_replace"


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build(source: dict, registry: dict) -> dict:
    if source.get("schema") != "uido.course.source-normalized.v0.1":
        raise ValueError(f"Unsupported source schema: {source.get('schema')!r}")
    if source.get("course_id") != "overstone-park":
        raise ValueError("This adapter is scoped to the pinned Overstone source fixture")

    registry_course = registry.get("courses", {}).get("overstone-park", {})
    if not registry_course.get("name"):
        raise ValueError("Overstone course name is missing from COURSE_REGISTRY.json")

    source_features = source.get("features", [])
    route_features = [f for f in source_features if f.get("canonical_type") == "HOLE"]
    physical_source = [f for f in source_features if f.get("canonical_type") != "HOLE"]

    routes = {}
    for feature in route_features:
        raw_number = feature.get("hole_ref")
        if not str(raw_number or "").isdigit():
            raise ValueError(f"Source hole feature has no numeric hole_ref: {feature.get('source_id')}")
        number = int(raw_number)
        if number in routes:
            raise ValueError(f"Duplicate source route for hole {number}")
        if not feature.get("geometry"):
            raise ValueError(f"Source route for hole {number} has no geometry")
        routes[number] = feature

    if set(routes) != set(range(1, 19)):
        raise ValueError("Source fixture must provide exactly one route for holes 1–18")

    physical = {}
    for feature in physical_source:
        feature_id = str(feature.get("source_id") or "")
        source_type = feature.get("canonical_type")
        if not feature_id:
            raise ValueError("Physical source feature is missing source_id")
        if feature_id in physical:
            raise ValueError(f"Duplicate physical source ID: {feature_id}")
        if source_type not in TYPE_MAP:
            raise ValueError(f"No canonical type mapping for {source_type!r} ({feature_id})")
        geometry = feature.get("geometry")
        if not geometry:
            raise ValueError(f"Physical source feature has no geometry: {feature_id}")
        physical[feature_id] = {
            "id": feature_id,
            "type": TYPE_MAP[source_type],
            "geometry": geometry,
            "provenance": {
                "source_id": "osm",
                "source_feature_id": feature_id,
            },
            "verification_status": "supported",
            "quality_status": "source_only",
        }

    holes = []
    for number in range(1, 19):
        feature = routes[number]
        properties = feature.get("properties") or {}
        raw_par = properties.get("par")
        par = int(raw_par) if str(raw_par or "").isdigit() else None
        holes.append({
            "hole_number": number,
            "par": par,
            "routing": feature["geometry"],
            "truth": "CONFIRMED",
        })

    unresolved = ["satellite_registration", "hole_feature_association"]
    canonical = {
        "schema": "uido.course.canonical.v2",
        "course": {
            "id": "overstone-park",
            "name": registry_course["name"],
            "country_code": "GB",
            "timezone": "Europe/London",
            "current_revision": CANONICAL_REVISION,
        },
        "provenance": {
            "policy": PROVENANCE_POLICY,
            "upstream_model_schema": source["schema"],
            "sources": [
                {
                    "id": "osm",
                    "provider": "OpenStreetMap",
                    "source_sha256": source["source"]["sha256"],
                },
                {
                    "id": "greens",
                    "provider": "UiDo existing green F/M/B dataset",
                    "source": "course_green_data.json",
                },
            ],
        },
        "geometry": {
            "scope": "course",
            "features": list(physical.values()),
        },
        "holes": holes,
        "validation": {
            "course_complete": False,
            "holes_complete": len(holes),
            "physical_geometry_count": len(physical),
            "unique_physical_ids": len(physical),
            "unresolved_features": unresolved,
            "conflicts": [],
            "status": "draft_source_import",
        },
    }
    return canonical


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Pinned source-normalized JSON fixture")
    parser.add_argument("--registry", required=True, help="UiDo course registry JSON")
    parser.add_argument("--out", required=True, help="Output canonical v2 JSON path")
    args = parser.parse_args()

    canonical = build(load(args.source), load(args.registry))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(canonical, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(canonical["validation"], indent=2))


if __name__ == "__main__":
    main()
