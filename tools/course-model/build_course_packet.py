#!/usr/bin/env python3
"""Build a checksum-manifested UiDo course packet from a canonical course model.

Incomplete models require --draft. This command creates a local QA artefact only;
it never writes to Supabase, publishes a revision or updates the canonical source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_SCHEMA = ROOT / "course-models/canonical-course.schema.json"
MANIFEST_SCHEMA = ROOT / "course-packages/schema/uido-course-packet-manifest-v0.1.schema.json"
REGISTRY_PATH = ROOT / "course-models/COURSE_REGISTRY.json"
MEDIA_TYPES = {
    ".json": "application/json",
    ".geojson": "application/geo+json",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write_json(root: Path, relative_path: str, value: dict) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(stable_bytes(value))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_relative_path(path: str) -> bool:
    pure = PurePosixPath(path)
    return (
        bool(path)
        and not pure.is_absolute()
        and ".." not in pure.parts
        and "\\" not in path
        and "\x00" not in path
    )


def point_feature(feature_id: str, lon: float, lat: float, properties: dict) -> dict:
    return {
        "type": "Feature",
        "id": feature_id,
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": properties,
    }


def route_feature(course_id: str, hole: dict) -> dict:
    number = int(hole["hole_number"])
    provenance = hole.get("routing_provenance")
    return {
        "type": "Feature",
        "id": f"{course_id}:hole:{number:02d}:route",
        "geometry": hole["routing"],
        "properties": {
            "feature_type": "hole_route",
            "hole_id": f"{course_id}:hole:{number:02d}",
            "hole_number": number,
            "truth": hole.get("truth", "UNKNOWN"),
            "provenance": provenance,
        },
    }


def verified_feature_refs(canonical: dict, hole_number: int) -> list[str]:
    refs = []
    for feature in canonical.get("geometry", {}).get("features", []):
        for evidence in feature.get("association_evidence", []) or []:
            evidence_data = evidence.get("evidence") or {}
            evidence_hole = evidence.get("hole", evidence_data.get("hole"))
            status = str(evidence_data.get("status") or evidence_data.get("verification_status") or "").lower()
            verified = status in {"verified", "confirmed"} or evidence_data.get("verified") is True
            if evidence_hole == hole_number and verified:
                refs.append(str(feature["id"]))
                break
    return sorted(set(refs))


def packet_files(canonical: dict, registry: dict) -> dict[str, dict]:
    course = canonical.get("course") or {}
    course_id = str(course["id"])
    revision = str(course.get("current_revision") or course.get("revision") or "")
    if not revision:
        raise ValueError("Canonical course has no immutable revision identifier")

    stage = canonical["provenance"]["stage"]
    validation = canonical.get("validation") or {}
    expected_holes = int(registry.get("courses", {}).get(course_id, {}).get("holes") or 0)
    if expected_holes < 1:
        raise ValueError(f"Registry has no expected hole count for {course_id}")

    hole_records = sorted(canonical.get("holes", []), key=lambda h: int(h["hole_number"]))
    included_numbers = [int(h["hole_number"]) for h in hole_records]
    publishable = (
        stage == "enriched_candidate"
        and validation.get("course_complete") is True
        and not validation.get("unresolved_features")
        and not validation.get("conflicts")
        and len(included_numbers) == expected_holes
        and set(included_numbers) == set(range(1, expected_holes + 1))
        and all(h.get("routing") and h.get("routing_provenance") and h.get("green") for h in hole_records)
    )

    course_json = {
        "course_id": course_id,
        "name": course.get("name"),
        "country_code": course.get("country_code"),
        "timezone": course.get("timezone"),
        "course_revision": revision,
        "expected_holes": expected_holes,
        "course_par": registry.get("courses", {}).get(course_id, {}).get("par"),
        "boundary": registry.get("courses", {}).get(course_id, {}).get("boundary"),
        "canonical_stage": stage,
        "validation_status": validation.get("status", "draft_source_import"),
        "publishable": publishable,
    }

    physical_features = []
    for feature in canonical.get("geometry", {}).get("features", []):
        properties = {
            "feature_type": feature["type"],
            "provenance": feature.get("provenance"),
            "verification_status": feature.get("verification_status", "unknown"),
            "quality_status": feature.get("quality_status", "unknown"),
        }
        if feature.get("association_evidence"):
            properties["association_evidence"] = feature["association_evidence"]
        physical_features.append({
            "type": "Feature",
            "id": str(feature["id"]),
            "geometry": feature["geometry"],
            "properties": properties,
        })
    features_geojson = {
        "type": "FeatureCollection",
        "name": f"{course_id}-physical-features",
        "properties": {
            "course_id": course_id,
            "course_revision": revision,
            "canonical_stage": stage,
            "feature_scope": "course",
        },
        "features": physical_features,
    }

    files = {
        "course.json": course_json,
        "features.geojson": features_geojson,
        "provenance/sources.json": {
            "stage": stage,
            "policy": canonical["provenance"].get("policy"),
            "upstream_model_schema": canonical["provenance"].get("upstream_model_schema"),
            "sources": canonical["provenance"].get("sources", []),
        },
    }

    for hole in hole_records:
        number = int(hole["hole_number"])
        hole_id = f"{course_id}:hole:{number:02d}"
        green = hole.get("green") or {}
        green_features = []
        green_refs = {}
        for position in ("front", "middle", "back"):
            point = green.get(position)
            if not point:
                continue
            anchor_id = f"{hole_id}:green-{position}"
            green_refs[position] = anchor_id
            provenance = (green.get("provenance") or {}).get(position)
            green_features.append(point_feature(
                anchor_id,
                float(point["lon"]),
                float(point["lat"]),
                {
                    "feature_type": "green_anchor",
                    "position": position,
                    "provenance": provenance,
                },
            ))

        features = []
        if hole.get("routing"):
            features.append(route_feature(course_id, hole))
        features.extend(green_features)
        hole_geojson = {
            "type": "FeatureCollection",
            "name": f"{course.get('name') or course_id} — Hole {number}",
            "properties": {
                "hole_id": hole_id,
                "hole_number": number,
                "par": hole.get("par"),
                "geometry_version": canonical.get("schema"),
                "truth": hole.get("truth", "UNKNOWN"),
                "routing_provenance": hole.get("routing_provenance"),
                "green_anchor_refs": green_refs,
                "physical_feature_refs": verified_feature_refs(canonical, number),
            },
            "features": features,
        }
        files[f"holes/{number:02d}.geojson"] = hole_geojson

    blockers = list(validation.get("unresolved_features") or [])
    if stage != "enriched_candidate":
        blockers.append("source_only_draft_not_publishable")
    if len(included_numbers) != expected_holes:
        blockers.append("hole_coverage_incomplete")
    if not all(h.get("green") for h in hole_records):
        blockers.append("green_anchors_incomplete")
    if not all(h.get("routing_provenance") for h in hole_records):
        blockers.append("route_provenance_incomplete")

    files["validation/report.json"] = {
        "canonical_validation": validation,
        "packet_validation": {
            "schema_valid": True,
            "publishable": publishable,
            "canonical_stage": stage,
            "expected_holes": expected_holes,
            "included_hole_numbers": included_numbers,
            "physical_feature_count": len(physical_features),
            "blocking_gates": sorted(set(str(x) for x in blockers)),
        },
    }
    return files


def build_packet(
    canonical: dict,
    registry: dict,
    output: Path,
    producer_commit: str,
    producer_version: str,
    created_at: str,
    allow_draft: bool,
) -> dict:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise RuntimeError("Install jsonschema before building a course packet") from exc

    Draft202012Validator(load(CANONICAL_SCHEMA)).validate(canonical)
    stage = canonical.get("provenance", {}).get("stage")
    if stage not in {"source_only_draft", "enriched_candidate"}:
        raise ValueError(f"Unsupported canonical stage: {stage!r}")

    files = packet_files(canonical, registry)
    validation = canonical.get("validation") or {}
    publishable = (
        stage == "enriched_candidate"
        and validation.get("course_complete") is True
        and not validation.get("unresolved_features")
        and not validation.get("conflicts")
    )
    if not publishable and not allow_draft:
        raise ValueError("Course is not publishable; pass --draft to build a QA-only packet")

    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"Output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    for relative_path, value in sorted(files.items()):
        if not safe_relative_path(relative_path):
            raise ValueError(f"Unsafe generated path: {relative_path}")
        write_json(output, relative_path, value)

    file_entries = []
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        relative = path.relative_to(output).as_posix()
        if not safe_relative_path(relative):
            raise ValueError(f"Unsafe package path: {relative}")
        data = path.read_bytes()
        file_entries.append({
            "path": relative,
            "media_type": MEDIA_TYPES.get(path.suffix, "application/octet-stream"),
            "byte_size": len(data),
            "sha256": sha256(data),
        })

    expected_holes = int(registry.get("courses", {}).get(canonical["course"]["id"], {}).get("holes") or 0)
    included_numbers = sorted(int(h["hole_number"]) for h in canonical.get("holes", []))
    coverage_complete = (
        publishable
        and len(included_numbers) == expected_holes
        and included_numbers == list(range(1, expected_holes + 1))
    )
    created_at = created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    manifest = {
        "packet_format": "uido.course-packet/0.1",
        "course_id": canonical["course"]["id"],
        "course_revision": canonical["course"].get("current_revision") or canonical["course"].get("revision"),
        "created_at": created_at,
        "producer": {
            "name": "tools/course-model/build_course_packet.py",
            "version": producer_version,
            "commit": producer_commit,
        },
        "coverage": {
            "expected_holes": expected_holes,
            "included_hole_numbers": included_numbers,
            "complete": coverage_complete,
            "status": "complete" if coverage_complete else ("partial" if len(included_numbers) != expected_holes else "draft"),
        },
        "coordinate_reference": {
            "id": "EPSG:4326",
            "axis_order": ["longitude", "latitude"],
        },
        "units": {"linear": "metre", "elevation": "metre"},
        "files": file_entries,
        "minimum_loader_version": "0.1.0",
        "extensions": {
            "canonical_stage": stage,
            "validation_status": canonical.get("validation", {}).get("status", "draft_source_import"),
            "publishable": publishable,
        },
    }
    manifest_schema = load(MANIFEST_SCHEMA)
    Draft202012Validator.check_schema(manifest_schema)
    Draft202012Validator(manifest_schema, format_checker=FormatChecker()).validate(manifest)
    write_json(output, "manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", default=str(ROOT / "course-models/canonical/overstone-park-v1.json"))
    parser.add_argument("--registry", default=str(REGISTRY_PATH))
    parser.add_argument("--out", required=True)
    parser.add_argument("--producer-commit", default=os.environ.get("GITHUB_SHA", "working-tree"))
    parser.add_argument("--producer-version", default="0.1.0")
    parser.add_argument("--created-at", default="")
    parser.add_argument("--draft", action="store_true", help="Allow QA-only output when publication gates are unresolved")
    args = parser.parse_args()

    manifest = build_packet(
        load(Path(args.canonical)),
        load(Path(args.registry)),
        Path(args.out),
        args.producer_commit,
        args.producer_version,
        args.created_at,
        args.draft,
    )
    print(json.dumps({
        "packet_dir": str(Path(args.out)),
        "course_id": manifest["course_id"],
        "course_revision": manifest["course_revision"],
        "canonical_stage": manifest["extensions"]["canonical_stage"],
        "publishable": manifest["extensions"]["publishable"],
        "file_count": len(manifest["files"]),
        "coverage": manifest["coverage"],
    }, indent=2))


if __name__ == "__main__":
    main()
