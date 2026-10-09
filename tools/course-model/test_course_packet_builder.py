#!/usr/bin/env python3
"""Tests for draft packet structure, manifest hashes and the no-publish gate."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_course_packet import build_packet, collect_input_artifacts  # noqa: E402
from jsonschema import Draft202012Validator, FormatChecker  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_PATH = ROOT / "course-models/canonical/overstone-park-v1.json"
REGISTRY_PATH = ROOT / "course-models/COURSE_REGISTRY.json"
MANIFEST_SCHEMA_PATH = ROOT / "course-packages/schema/uido-course-packet-manifest-v0.1.schema.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class CoursePacketBuilderTests(unittest.TestCase):
    def setUp(self):
        self.canonical = load(CANONICAL_PATH)
        self.registry = load(REGISTRY_PATH)
        self.producer_commit = "0" * 40
        self.created_at = "2026-10-09T00:00:00Z"
        self.input_artifacts = collect_input_artifacts(
            CANONICAL_PATH, REGISTRY_PATH, self.canonical["provenance"]["stage"]
        )

    def test_incomplete_canonical_requires_explicit_draft_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "packet"
            with self.assertRaisesRegex(ValueError, "pass --draft"):
                build_packet(
                    self.canonical, self.registry, output, self.producer_commit,
                    "0.1.0", self.created_at, False, self.input_artifacts,
                )
            self.assertFalse(output.exists())

    def test_draft_packet_manifest_files_and_checksums_are_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "packet"
            manifest = build_packet(
                self.canonical, self.registry, output, self.producer_commit,
                "0.1.0", self.created_at, True, self.input_artifacts,
            )

            schema = load(MANIFEST_SCHEMA_PATH)
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema, format_checker=FormatChecker()).validate(manifest)

            self.assertEqual(manifest["course_id"], "overstone-park")
            self.assertEqual(manifest["course_revision"], "v1-osm-source")
            self.assertEqual(manifest["extensions"]["canonical_stage"], "source_only_draft")
            self.assertFalse(manifest["extensions"]["publishable"])
            self.assertFalse(manifest["coverage"]["complete"])
            self.assertEqual(manifest["coverage"]["status"], "draft")
            self.assertEqual(manifest["coverage"]["included_hole_numbers"], list(range(1, 19)))

            entries = manifest["files"]
            paths = [entry["path"] for entry in entries]
            self.assertEqual(paths, sorted(paths))
            self.assertEqual(len(paths), len(set(paths)))
            self.assertNotIn("manifest.json", paths)

            actual_paths = sorted(
                path.relative_to(output).as_posix()
                for path in output.rglob("*")
                if path.is_file() and path.name != "manifest.json"
            )
            self.assertEqual(paths, actual_paths)

            for entry in entries:
                self.assertFalse(entry["path"].startswith("/"))
                self.assertNotIn("..", Path(entry["path"]).parts)
                data = (output / entry["path"]).read_bytes()
                self.assertEqual(entry["byte_size"], len(data))
                self.assertEqual(entry["sha256"], hashlib.sha256(data).hexdigest())

            features = load(output / "features.geojson")
            self.assertEqual(features["type"], "FeatureCollection")
            self.assertEqual(len(features["features"]), 159)

            for number in range(1, 19):
                hole = load(output / f"holes/{number:02d}.geojson")
                self.assertEqual(hole["type"], "FeatureCollection")
                self.assertEqual(hole["properties"]["hole_number"], number)
                self.assertEqual(len(hole["features"]), 4)
                self.assertEqual(
                    {feature["properties"].get("position") for feature in hole["features"] if feature["properties"]["feature_type"] == "green_anchor"},
                    {"front", "middle", "back"},
                )
                self.assertTrue(hole["properties"]["routing_provenance"]["source_feature_id"])

            report = load(output / "validation/report.json")
            self.assertFalse(report["packet_validation"]["publishable"])
            self.assertIn("satellite_registration", report["packet_validation"]["blocking_gates"])
            self.assertIn("hole_feature_association", report["packet_validation"]["blocking_gates"])
            self.assertTrue((output / "provenance/sources.json").is_file())
            provenance = load(output / "provenance/sources.json")
            input_paths = [item["path"] for item in provenance["input_artifacts"]]
            self.assertEqual(input_paths, sorted(input_paths))
            self.assertIn("course-models/source-normalized/overstone-source-normalized-v0.1.json", input_paths)
            self.assertIn("course_green_data.json", input_paths)
            green_source = next(source for source in provenance["sources"] if source["id"] == "greens")
            self.assertRegex(green_source["source_sha256"], r"^[a-f0-9]{64}$")
            for item in provenance["input_artifacts"]:
                self.assertRegex(item["sha256"], r"^[a-f0-9]{64}$")


if __name__ == "__main__":
    unittest.main(verbosity=2)
