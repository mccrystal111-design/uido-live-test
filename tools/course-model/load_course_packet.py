#!/usr/bin/env python3
"""Reference offline course-packet loader and integrity validator.

Reads only local files. It performs no network calls, database writes or publish
operations. The returned object is suitable for contract tests and as a reference
for a future browser/native loader.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_SCHEMA = ROOT / "course-packages/schema/uido-course-packet-manifest-v0.1.schema.json"


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid JSON at {path}") from exc


def safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        bool(value)
        and not path.is_absolute()
        and ".." not in path.parts
        and "\\" not in value
        and "\x00" not in value
    )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_coordinates(lon, lat, label: str) -> None:
    if (
        not isinstance(lon, (int, float)) or isinstance(lon, bool)
        or not isinstance(lat, (int, float)) or isinstance(lat, bool)
        or not -180 <= lon <= 180 or not -90 <= lat <= 90
    ):
        raise ValueError(f"Invalid WGS84 coordinates at {label}")


def load_packet(packet_dir: str | Path) -> dict:
    root = Path(packet_dir).resolve()
    if not root.is_dir():
        raise ValueError(f"Packet directory does not exist: {root}")

    manifest = read_json(root / "manifest.json")
    schema = read_json(MANIFEST_SCHEMA)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(manifest)

    entries = manifest["files"]
    declared_paths = [entry["path"] for entry in entries]
    if len(declared_paths) != len(set(declared_paths)):
        raise ValueError("Manifest contains duplicate file paths")

    for entry in entries:
        relative = entry["path"]
        if not safe_relative_path(relative):
            raise ValueError(f"Unsafe path in manifest: {relative}")
        path = (root / relative).resolve()
        if root not in path.parents:
            raise ValueError(f"Manifest path escapes packet directory: {relative}")
        if not path.is_file():
            raise ValueError(f"Manifest file is missing: {relative}")
        data = path.read_bytes()
        if len(data) != entry["byte_size"]:
            raise ValueError(f"Byte-size mismatch for {relative}")
        if sha256(data) != entry["sha256"].lower():
            raise ValueError(f"SHA-256 mismatch for {relative}")

    actual_paths = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).as_posix() != "manifest.json"
    )
    if sorted(declared_paths) != actual_paths:
        raise ValueError("Packet contains unlisted files or manifest entries that do not match files")

    course = read_json(root / "course.json")
    features_doc = read_json(root / "features.geojson")
    sources = read_json(root / "provenance/sources.json")
    report = read_json(root / "validation/report.json")

    if course.get("course_id") != manifest["course_id"]:
        raise ValueError("course.json course_id does not match manifest")
    if course.get("course_revision") != manifest["course_revision"]:
        raise ValueError("course.json revision does not match manifest")
    if sources.get("stage") != manifest["extensions"]["canonical_stage"]:
        raise ValueError("Source provenance stage does not match manifest")
    if report.get("packet_validation", {}).get("publishable") != manifest["extensions"]["publishable"]:
        raise ValueError("Validation report publishable flag does not match manifest")

    if features_doc.get("type") != "FeatureCollection":
        raise ValueError("features.geojson must be a GeoJSON FeatureCollection")
    physical_features = features_doc.get("features")
    if not isinstance(physical_features, list):
        raise ValueError("features.geojson has no feature list")

    physical_by_id = {}
    for feature in physical_features:
        feature_id = str(feature.get("id") or "")
        if not feature_id or feature_id in physical_by_id:
            raise ValueError(f"Missing or duplicate physical feature ID: {feature_id!r}")
        geometry = feature.get("geometry")
        if not isinstance(geometry, dict) or not geometry.get("type") or "coordinates" not in geometry:
            raise ValueError(f"Invalid geometry for physical feature {feature_id}")
        properties = feature.get("properties") or {}
        provenance = properties.get("provenance")
        if not isinstance(provenance, dict) or not provenance.get("source_id") or not provenance.get("source_feature_id"):
            raise ValueError(f"Missing provenance for physical feature {feature_id}")
        physical_by_id[feature_id] = feature

    holes = {}
    expected_numbers = manifest["coverage"]["included_hole_numbers"]
    for number in expected_numbers:
        relative = f"holes/{int(number):02d}.geojson"
        hole_doc = read_json(root / relative)
        props = hole_doc.get("properties") or {}
        if hole_doc.get("type") != "FeatureCollection":
            raise ValueError(f"{relative} must be a GeoJSON FeatureCollection")
        if props.get("hole_number") != number:
            raise ValueError(f"Hole number mismatch in {relative}")
        hole_id = props.get("hole_id")
        if not hole_id or hole_id in {item["properties"]["hole_id"] for item in holes.values()}:
            raise ValueError(f"Missing or duplicate hole_id in {relative}")

        route_features = [
            feature for feature in hole_doc.get("features", [])
            if (feature.get("properties") or {}).get("feature_type") == "hole_route"
        ]
        if len(route_features) != 1:
            raise ValueError(f"{relative} must contain exactly one route feature")
        route = route_features[0]
        route_props = route.get("properties") or {}
        route_provenance = route_props.get("provenance")
        if not isinstance(route_provenance, dict) or not route_provenance.get("source_id") or not route_provenance.get("source_feature_id"):
            raise ValueError(f"Missing route provenance in {relative}")
        route_geometry = route.get("geometry") or {}
        if route_geometry.get("type") not in {"LineString", "MultiLineString"}:
            raise ValueError(f"Invalid route geometry type in {relative}")

        green_features = [
            feature for feature in hole_doc.get("features", [])
            if (feature.get("properties") or {}).get("feature_type") == "green_anchor"
        ]
        positions = [(feature.get("properties") or {}).get("position") for feature in green_features]
        if set(positions) != {"front", "middle", "back"} or len(positions) != 3:
            raise ValueError(f"{relative} must contain exactly front/middle/back green anchors")
        refs = props.get("green_anchor_refs") or {}
        if set(refs) != {"front", "middle", "back"}:
            raise ValueError(f"Missing green anchor references in {relative}")
        for feature in green_features:
            anchor_props = feature.get("properties") or {}
            position = anchor_props.get("position")
            if refs.get(position) != feature.get("id"):
                raise ValueError(f"Green anchor reference mismatch for {position} in {relative}")
            if not anchor_props.get("provenance"):
                raise ValueError(f"Missing green anchor provenance for {position} in {relative}")
            geometry = feature.get("geometry") or {}
            if geometry.get("type") != "Point" or not isinstance(geometry.get("coordinates"), list) or len(geometry["coordinates"]) != 2:
                raise ValueError(f"Invalid green anchor geometry for {position} in {relative}")
            check_coordinates(geometry["coordinates"][0], geometry["coordinates"][1], f"{relative}:{position}")

        feature_refs = props.get("physical_feature_refs") or []
        missing_refs = sorted(set(feature_refs) - set(physical_by_id))
        if missing_refs:
            raise ValueError(f"Unresolved physical feature references in {relative}: {missing_refs}")

        holes[number] = hole_doc

    if manifest["extensions"]["canonical_stage"] == "source_only_draft" and manifest["extensions"]["publishable"]:
        raise ValueError("A source_only_draft packet cannot be publishable")
    if manifest["extensions"]["publishable"] and not manifest["coverage"]["complete"]:
        raise ValueError("Publishable packet must have complete coverage")
    if manifest["coverage"]["complete"] and len(expected_numbers) != manifest["coverage"]["expected_holes"]:
        raise ValueError("Coverage marked complete but expected hole count does not match")

    return {
        "manifest": manifest,
        "course": course,
        "features": physical_by_id,
        "holes": holes,
        "provenance": sources,
        "validation": report,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet_dir")
    args = parser.parse_args()
    packet = load_packet(args.packet_dir)
    print(json.dumps({
        "course_id": packet["manifest"]["course_id"],
        "course_revision": packet["manifest"]["course_revision"],
        "canonical_stage": packet["manifest"]["extensions"]["canonical_stage"],
        "publishable": packet["manifest"]["extensions"]["publishable"],
        "physical_features": len(packet["features"]),
        "holes_loaded": len(packet["holes"]),
        "green_anchors": sum(
            1 for hole in packet["holes"].values()
            for feature in hole["features"]
            if (feature.get("properties") or {}).get("feature_type") == "green_anchor"
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
