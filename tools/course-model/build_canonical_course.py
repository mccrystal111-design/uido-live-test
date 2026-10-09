#!/usr/bin/env python3
"""Build the provider-agnostic UiDo canonical course model.

Physical geometry is course-scoped. Hole records own routing and relationships,
not cloned copies of physical features. Completeness is gated on measured
registration and verified feature associations, not merely on data presence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


BUCKET_TYPES = {
    "tees": "TEE",
    "fairways": "FAIRWAY",
    "rough": "ROUGH",
    "green_source_features": "GREEN",
    "paths": "PATH",
    "context": None,
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


def normalize_feature(feature: dict, default_type: str | None, associations: list[dict]) -> dict | None:
    geometry = feature.get("geometry")
    if not geometry:
        return None

    feature_id = feature.get("id")
    if feature_id is None:
        feature_id = feature.get("source_id")
    if feature_id is None:
        return None

    result = dict(feature)
    result["id"] = str(feature_id)
    result["type"] = str(feature.get("type") or default_type or "UNKNOWN").upper()
    result["geometry"] = geometry

    result.setdefault("provenance", "source:osm")
    result.setdefault("confidence", "source")
    result.setdefault("status", "source")

    existing = result.get("associations")
    if existing is not None:
        result["association_evidence"] = existing
        result.pop("associations", None)

    result["association_evidence"] = associations
    return result


def build_route(hole: dict) -> dict | None:
    routing = hole.get("routing")
    if not routing:
        return None

    # Routing geometry is hole-specific relationship data, not physical course
    # geometry. Preserve it exactly and make the role explicit.
    route = dict(routing)
    route["role"] = "hole_route"
    route["hole_number"] = int(hole["hole_number"])

    green = hole.get("green")
    if green:
        route["destination"] = green.get("middle")

    return route


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

        holes.append({
            "hole_number": number,
            "par": raw_hole.get("par"),
            "routing": route,
            "truth": truth,
        })

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

    # These gates are deliberately separate from hole-route truth. Having 18
    # routes does not prove that OSM geometry has been registered to imagery or
    # that physical features have been correctly assigned to holes.
    if not registration_is_verified(model.get("registration")):
        unresolved.append("satellite_registration")
    if not associations_are_verified(model):
        unresolved.append("hole_feature_association")

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
            "policy": (
                "Physical geometry is course-scoped and source-preserved. Holes "
                "contain routing and relationships only. Shared physical features "
                "retain one stable identity and may be referenced by multiple holes."
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
