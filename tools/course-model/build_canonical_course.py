#!/usr/bin/env python3
"""Build the provider-agnostic UiDo Canonical Course Source of Truth.

Input is the existing provider-neutral course model. The canonical layer is
deliberately renderer-independent: it records what is known about every hole
and every feature class, including explicit NONE and UNKNOWN states.

No geometry is changed, invented, smoothed, or re-associated here.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

FEATURES = {
    "tee": ("tees", "TEE"),
    "fairway": ("fairways", "FAIRWAY"),
    "rough": ("rough", "ROUGH"),
    "green": ("green_source_features", "GREEN"),
    "bunkers": ("hazards", "BUNKER"),
    "water": ("hazards", "WATER"),
    "paths": ("paths", "PATH"),
    "context": ("context", None),
}


def source_available(model: dict, source_id: str) -> bool:
    return any(
        str(s.get("id")) == source_id and s.get("status") in {"available", "acquired_for_build", "captured"}
        for s in model.get("sources", [])
    )


def source_ids_for(items: list[dict]) -> list[str]:
    ids = []
    for item in items:
        for ref in item.get("source_refs", []):
            if ref not in ids:
                ids.append(ref)
    return ids


def split_hazards(items: list[dict], wanted_type: str) -> list[dict]:
    return [x for x in items if str(x.get("type", "")).upper() == wanted_type]


def feature_set(
    items: list[dict],
    *,
    scope: str,
    notes: list[str] | None = None,
    explicit_none: bool = False,
) -> dict:
    items = items or []
    if items:
        return {
            "status": "CONFIRMED",
            "scope": scope,
            "features": items,
            "source_ids": source_ids_for(items),
            "notes": notes or [],
        }
    # Empty association is not proof that the real course has no such feature.
    # CONFIRMED_NONE is reserved for an upstream packet that explicitly records
    # absence; otherwise canonical truth remains UNKNOWN.
    return {
        "status": "CONFIRMED_NONE" if explicit_none else "UNKNOWN",
        "scope": scope,
        "features": [],
        "source_ids": [],
        "notes": notes or [],
    }


def canonical_hole(model_hole: dict, osm_available: bool) -> dict:
    hazards = model_hole.get("hazards", [])
    source_scope = "source:osm-capture" if osm_available else "unknown:source-unavailable"

    bunker_items = split_hazards(hazards, "BUNKER")
    water_items = split_hazards(hazards, "WATER")

    green_items = model_hole.get("green_source_features", [])
    # The F/M/B coordinates are retained as source data from the green dataset;
    # they are not converted into a renderer-specific representation.
    if green_items:
        green_notes = []
    elif model_hole.get("green"):
        green_notes = ["F/M/B coordinates are available; source polygon association is not represented in this model."]
    else:
        green_notes = ["No green geometry or green coordinate source was available."]

    features = {
        "tee": feature_set(model_hole.get("tees"), scope=source_scope),
        "fairway": feature_set(model_hole.get("fairways"), scope=source_scope),
        "rough": feature_set(model_hole.get("rough"), scope=source_scope),
        "green": feature_set(green_items, scope=source_scope, notes=green_notes),
        "bunkers": feature_set(bunker_items, scope=source_scope),
        "water": feature_set(water_items, scope=source_scope),
        "paths": feature_set(model_hole.get("paths"), scope=source_scope),
        "context": feature_set(model_hole.get("context"), scope=source_scope),
    }

    unresolved = [
        name for name, value in features.items()
        if value["status"] == "UNKNOWN"
    ]
    truth = "INCOMPLETE" if unresolved else "CONFIRMED"

    return {
        "hole_number": int(model_hole["hole_number"]),
        "par": model_hole.get("par"),
        "routing": model_hole.get("routing"),
        "truth": truth,
        "features": features,
        "unresolved_features": unresolved,
        "conflicts": model_hole.get("conflicts", []),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="Provider-neutral UiDo course model JSON")
    ap.add_argument("--out", required=True, help="Canonical course JSON")
    args = ap.parse_args()

    model = json.loads(Path(args.model).read_text())
    holes = [canonical_hole(h, source_available(model, "osm")) for h in model.get("holes", [])]
    holes.sort(key=lambda h: h["hole_number"])

    unresolved = []
    conflicts = []
    for hole in holes:
        for feature in hole["unresolved_features"]:
            unresolved.append({"hole": hole["hole_number"], "feature": feature})
        for conflict in hole["conflicts"]:
            conflicts.append({"hole": hole["hole_number"], "conflict": conflict})

    complete = (
        len(holes) == 18
        and not unresolved
        and not conflicts
        and all(h["truth"] == "CONFIRMED" for h in holes)
    )

    canonical = {
        "schema": "uido.course.canonical.v1",
        "course": model.get("course", {}),
        "provenance": {
            "policy": (
                "Canonical geometry is source-preserved. The canonical layer records "
                "truth state and provenance; it never mutates geometry or silently "
                "promotes inference to source truth."
            ),
            "sources": model.get("sources", []),
            "upstream_model_schema": model.get("schema_version"),
        },
        "holes": holes,
        "validation": {
            "course_complete": complete,
            "holes_complete": sum(1 for h in holes if h["truth"] == "CONFIRMED"),
            "unresolved_features": unresolved,
            "conflicts": conflicts,
        },
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(canonical, indent=2) + "\n")
    print(json.dumps(canonical["validation"], indent=2))


if __name__ == "__main__":
    main()
