#!/usr/bin/env python3
"""Build the provider-agnostic UiDo Canonical Course Source of Truth.

The canonical course owns physical geometry once at course scope. Holes own
routing only: tee/start, direction of travel, destination/green and scorecard
metadata. Any source association retained on a physical feature is evidence,
not ownership.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

FEATURE_TYPES = {
    "tees": "TEE",
    "fairways": "FAIRWAY",
    "rough": "ROUGH",
    "green_source_features": "GREEN",
    "hazards": None,
    "paths": "PATH",
    "context": None,
}

def source_ids_for(item: dict) -> list[str]:
    refs = item.get("source_refs") or []
    return [str(x) for x in refs if x is not None]

def feature_type(item: dict, bucket: str) -> str:
    if bucket == "hazards":
        return str(item.get("type", "UNKNOWN")).upper()
    if bucket == "context":
        return str(item.get("type", "CONTEXT")).upper()
    return FEATURE_TYPES[bucket]

def canonical_feature(item: dict, bucket: str) -> dict:
    out = dict(item)
    out["type"] = feature_type(item, bucket)
    # Association is useful provenance/debug evidence but is explicitly not an
    # ownership relation in the canonical course model.
    if "association" in out:
        out["association_evidence"] = out.pop("association")
    out["source_ids"] = source_ids_for(item)
    return out

def collect_physical_geometry(model: dict) -> list[dict]:
    by_id: dict[str, dict] = {}
    for hole in model.get("holes", []):
        for bucket in FEATURE_TYPES:
            for item in hole.get(bucket, []) or []:
                feature = canonical_feature(item, bucket)
                fid = str(feature.get("id") or feature.get("@id") or "")
                if not fid:
                    continue
                existing = by_id.get(fid)
                if existing is None:
                    by_id[fid] = feature
                else:
                    # Merge provenance without cloning the physical geometry.
                    for key in ("source_ids",):
                        merged = list(dict.fromkeys(
                            (existing.get(key) or []) + (feature.get(key) or [])
                        ))
                        existing[key] = merged
                    if feature.get("association_evidence") and not existing.get("association_evidence"):
                        existing["association_evidence"] = feature["association_evidence"]
    # Preserve unassigned source geometry too. It is physical course evidence,
    # not discarded merely because it could not be assigned to a hole.
    for item in model.get("unassigned_features", []) or []:
        feature = dict(item)
        feature["source_ids"] = source_ids_for(item)
        fid = str(feature.get("id") or feature.get("@id") or "")
        if fid and fid not in by_id:
            by_id[fid] = feature
    return sorted(by_id.values(), key=lambda x: str(x.get("id", "")))

def canonical_hole(model_hole: dict) -> dict:
    routing = model_hole.get("routing") or {}
    route = {
        "id": routing.get("id"),
        "geometry": routing.get("geometry"),
        "provenance": routing.get("provenance"),
        "confidence": routing.get("confidence"),
        "source_refs": routing.get("source_refs", []),
        "status": routing.get("status"),
    }
    return {
        "hole_number": int(model_hole["hole_number"]),
        "par": model_hole.get("par"),
        "routing": route,
        "truth": "CONFIRMED" if route.get("geometry") else "INCOMPLETE",
        "conflicts": model_hole.get("conflicts", []),
    }

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="Provider-neutral UiDo course model JSON")
    ap.add_argument("--out", required=True, help="Canonical course JSON")
    args = ap.parse_args()

    model = json.loads(Path(args.model).read_text())
    holes = sorted(
        (canonical_hole(h) for h in model.get("holes", [])),
        key=lambda h: h["hole_number"],
    )
    geometry = collect_physical_geometry(model)

    unresolved = [
        {"hole": h["hole_number"], "issue": "missing_routing_geometry"}
        for h in holes if h["truth"] != "CONFIRMED"
    ]
    conflicts = [
        {"hole": h["hole_number"], "conflict": c}
        for h in holes for c in h.get("conflicts", [])
    ]

    canonical = {
        "schema": "uido.course.canonical.v2",
        "course": model.get("course", {}),
        "provenance": {
            "policy": (
                "Physical geometry is canonical at course scope and retains one stable "
                "feature identity. Hole routing is the only hole-specific geometric "
                "relationship. Source associations are evidence, never ownership."
            ),
            "sources": model.get("sources", []),
            "upstream_model_schema": model.get("schema_version"),
        },
        "geometry": {
            "scope": "course",
            "features": geometry,
        },
        "holes": holes,
        "validation": {
            "course_complete": len(holes) == 18 and not unresolved and not conflicts,
            "holes_complete": sum(h["truth"] == "CONFIRMED" for h in holes),
            "physical_geometry_count": len(geometry),
            "unique_physical_geometry_ids": len({str(x.get("id")) for x in geometry}),
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
