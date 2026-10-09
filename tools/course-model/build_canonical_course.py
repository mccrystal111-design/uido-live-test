#!/usr/bin/env python3
"""Build the provider-agnostic UiDo canonical course model.

Physical geometry is course-scoped. Hole records own routing, green F/M/B
anchors and relationships, not cloned copies of physical features. Completeness
is gated on measured registration and verified feature associations.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


BUCKET_TYPES = {
    "tees": "TEE",
    "fairways": "FAIRWAY",
    "rough": "ROUGH",
    "green_source_features": "GREEN",
    "paths": "PATH",
    "context": None,
}
CANONICAL_TYPE_MAP = {
    "WATER": "water",
    "WATER_HAZARD": "water",
    "TEE": "teeing_area",
    "FAIRWAY": "fairway",
    "ROUGH": "rough",
    "GREEN": "green",
    "BUNKER": "bunker",
    "DRIVING_RANGE": "driving_range",
    "PATH": "path",
    "WOOD": "woodland",
    "WOODLAND": "woodland",
    "OOB": "out_of_bounds",
    "STRUCTURE": "structure",
    "TARGET": "target",
    "UNKNOWN": "unknown",
}


def source_available(model: dict, source_id: str) -> bool:
    return any(
        str(source.get("id")) == source_id
        and source.get("status") in {"available", "acquired_for_build", "captured"}
        for source in model.get("sources", [])
    )


def iter_hole_features(hole: dict):
    for bucket, default_type in BUCKET_TYPES.items():
        for feature in hole.get(bucket, []) or []:
            yield feature, default_type

    for feature in hole.get("hazards", []) or []:
        yield feature, str(feature.get("type", "UNKNOWN")).upper()


def registration_is_verified(registration: dict | None) -> bool:
    """Only a measured registration solution can satisfy the publication gate."""
    registration = registration or {}
    return (
        registration.get("status") in {"registered", "verified", "complete"}
        and bool(registration.get("transform"))
        and bool(registration.get("metrics"))
    )


def association_is_verified(feature: dict) -> bool:
    """Distance-based association evidence is not equivalent to verification."""
    association = feature.get("association") or {}
    status = str(association.get("status") or feature.get("association_status") or "").lower()
    return status in {"verified", "confirmed"} or association.get("verified") is True


def associations_are_verified(model: dict) -> bool:
    for hole in model.get("holes", []):
        for feature, _default_type in iter_hole_features(hole):
            if not association_is_verified(feature):
                return False

    for feature in model.get("unassigned_features", []) or []:
        association = feature.get("association") or {}
        method = association.get("method")
        feature_type = str(feature.get("type") or "").upper()
        if method == "non-hole-course-feature" and feature_type in {
            "DRIVING_RANGE", "WOODLAND", "STRUCTURE", "OOB"
        }:
            continue
        if not association_is_verified(feature):
            return False
    return True


def normalize_green(green: dict | None) -> dict | None:
    if not green:
        return None
    result = {}
    provenance = green.get("provenance") or {}
    for position in ("front", "middle", "back"):
        point = green.get(position)
        if not isinstance(point, dict):
            return None
        lon, lat = point.get("lon"), point.get("lat")
        if (
            not isinstance(lon, (int, float))
            or isinstance(lon, bool)
            or not isinstance(lat, (int, float))
            or isinstance(lat, bool)
            or not math.isfinite(lon)
            or not math.isfinite(lat)
            or not -180 <= lon <= 180
            or not -90 <= lat <= 90
        ):
            return None
        result[position] = {"lon": lon, "lat": lat}
    result["provenance"] = {
        position: str(provenance.get(position) or "source:unknown")
        for position in ("front", "middle", "back")
    }
    return result


def green_anchors_are_complete(model: dict) -> bool:
    return all(normalize_green(hole.get("green")) is not None for hole in model.get("holes", []))


def normalize_feature(feature: dict, default_type: str | None, associations: list[dict]) -> dict | None:
    geometry = feature.get("geometry")
    if not geometry:
        return None

    feature_id = feature.get("id")
    if feature_id is None:
        feature_id = feature.get("source_id")
    if feature_id is None:
        return None
    feature_id = str(feature_id)

    raw_type = str(feature.get("type") or default_type or "UNKNOWN").upper()
    canonical_type = CANONICAL_TYPE_MAP.get(raw_type, raw_type.lower())
    raw_provenance = feature.get("provenance")
    source_refs = feature.get("source_refs") or []
    if isinstance(raw_provenance, dict):
        provenance = dict(raw_provenance)
        provenance.setdefault("source_feature_id", str(source_refs[0] if source_refs else feature_id))
    elif isinstance(raw_provenance, str) and raw_provenance.startswith("source:"):
        provenance = {
            "source_id": raw_provenance.split(":", 1)[1],
            "source_feature_id": str(source_refs[0] if source_refs else feature_id),
        }
    else:
        provenance = {
            "source_id": str(feature.get("source_id") or "unknown"),
            "source_feature_id": str(source_refs[0] if source_refs else feature_id),
        }

    raw_status = str(feature.get("verification_status") or feature.get("status") or "source").lower()
    if raw_status in {"verified", "confirmed"}:
        verification_status = "verified"
    elif raw_status == "conflict":
        verification_status = "conflict"
    elif raw_status in {"unknown", "unresolved"}:
        verification_status = raw_status
    else:
        verification_status = "supported"

    raw_quality = feature.get("quality_status")
    if raw_quality:
        quality_status = str(raw_quality)
    elif str(feature.get("confidence") or "source").lower() in {"source", "source_only"}:
        quality_status = "source_only"
    else:
        quality_status = "unknown"

    result = {
        "id": feature_id,
        "type": canonical_type,
        "geometry": geometry,
        "provenance": provenance,
        "verification_status": verification_status,
        "quality_status": quality_status,
    }
    if associations:
        result["association_evidence"] = associations
    return result


def build_route(hole: dict) -> dict | None:
    routing = hole.get("routing")
    if not routing:
        return None
    # Accept either a direct GeoJSON geometry or an upstream feature wrapper,
    # but always emit the canonical direct-geometry form.
    if isinstance(routing, dict) and routing.get("type") in {
        "Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"
    } and "coordinates" in routing:
        return routing
    geometry = routing.get("geometry") if isinstance(routing, dict) else None
    return geometry if isinstance(geometry, dict) else None


def route_provenance(hole: dict) -> dict | None:
    explicit = hole.get("routing_provenance")
    if isinstance(explicit, dict) and explicit.get("source_id") and explicit.get("source_feature_id"):
        return explicit
    routing = hole.get("routing")
    if not isinstance(routing, dict):
        return None
    raw_provenance = routing.get("provenance")
    source_refs = routing.get("source_refs") or []
    if isinstance(raw_provenance, dict):
        source_id = raw_provenance.get("source_id") or "unknown"
        source_feature_id = raw_provenance.get("source_feature_id") or (source_refs[0] if source_refs else routing.get("id"))
    elif isinstance(raw_provenance, str) and raw_provenance.startswith("source:"):
        source_id = raw_provenance.split(":", 1)[1]
        source_feature_id = source_refs[0] if source_refs else routing.get("id")
    else:
        source_id = str(routing.get("source_id") or "unknown")
        source_feature_id = source_refs[0] if source_refs else routing.get("id")
    if source_feature_id is None:
        source_feature_id = f"hole:{int(hole['hole_number'])}:routing"
    return {"source_id": str(source_id), "source_feature_id": str(source_feature_id)}


def build_canonical(model: dict) -> dict:
    osm_available = source_available(model, "osm")

    holes = []
    physical = {}
    unresolved = []
    conflicts = []

    for raw_hole in sorted(model.get("holes", []), key=lambda h: int(h["hole_number"])):
        number = int(raw_hole["hole_number"])
        route = build_route(raw_hole)
        truth = "CONFIRMED"

        if route is None:
            truth = "INCOMPLETE"
            unresolved.append({"hole": number, "feature": "routing"})

        green = normalize_green(raw_hole.get("green"))
        if green is None:
            unresolved.append({"hole": number, "feature": "green_anchors"})

        for feature, default_type in iter_hole_features(raw_hole):
            normalized = normalize_feature(
                feature,
                default_type,
                [{
                    "hole": number,
                    "method": (feature.get("association") or {}).get("method", "upstream_association"),
                    "evidence": feature.get("association"),
                }],
            )
            if normalized is None:
                unresolved.append({"hole": number, "feature": "geometry_without_identity"})
                truth = "INCOMPLETE"
                continue

            feature_id = normalized["id"]
            if feature_id in physical:
                prior = physical[feature_id]
                prior.setdefault("association_evidence", []).extend(
                    normalized.get("association_evidence", [])
                )
            else:
                physical[feature_id] = normalized

        if raw_hole.get("conflicts"):
            truth = "CONFLICT"
            conflicts.extend(
                {"hole": number, "conflict": item} for item in raw_hole["conflicts"]
            )

        hole_record = {
            "hole_number": number,
            "par": raw_hole.get("par"),
            "routing": route,
            "routing_provenance": route_provenance(raw_hole),
            "truth": truth,
        }
        if green is not None:
            hole_record["green"] = green
        holes.append(hole_record)

    # Preserve source geometry that has not been associated to a hole.
    for feature in model.get("unassigned_features", []) or []:
        normalized = normalize_feature(
            feature,
            None,
            [{
                "method": "unassigned_course_geometry",
                "evidence": feature.get("association"),
            }],
        )
        if normalized is not None:
            physical.setdefault(normalized["id"], normalized)

    features = sorted(physical.values(), key=lambda feature: feature["id"])

    # Route presence does not prove physical-feature association or registration.
    if not registration_is_verified(model.get("registration")):
        unresolved.append("satellite_registration")
    if not associations_are_verified(model):
        unresolved.append("hole_feature_association")
    if not green_anchors_are_complete(model):
        unresolved.append("green_anchors")

    complete = (
        len(holes) == 18
        and not unresolved
        and not conflicts
        and bool(features)
        and osm_available
    )

    return {
        "schema": "uido.course.canonical.v2",
        "course": model.get("course", {}),
        "provenance": {
            "stage": "enriched_candidate",
            "policy": (
                "Physical geometry is course-scoped and source-preserved. Holes "
                "contain routing, green F/M/B anchors and relationships only. "
                "Shared physical features retain one stable identity and may be "
                "referenced by multiple holes."
            ),
            "sources": model.get("sources", []),
            "upstream_model_schema": model.get("schema_version"),
        },
        "geometry": {
            "scope": "course",
            "features": features,
        },
        "holes": holes,
        "validation": {
            "course_complete": complete,
            "holes_complete": sum(1 for hole in holes if hole["truth"] == "CONFIRMED"),
            "physical_geometry_count": len(features),
            "unique_physical_ids": len({feature["id"] for feature in features}),
            "unresolved_features": unresolved,
            "conflicts": conflicts,
            "status": "complete" if complete else "draft_source_import",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    model = json.loads(Path(args.model).read_text(encoding="utf-8"))
    canonical = build_canonical(model)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(canonical, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(canonical["validation"], indent=2))


if __name__ == "__main__":
    main()
