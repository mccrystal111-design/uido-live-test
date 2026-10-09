#!/usr/bin/env python3
"""Unit tests for canonical course completeness gates; no network or database access."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_canonical_course import build_canonical  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


def sample_model(registration=None, association=None, missing_route=None, missing_green=None):
    feature = {
        "id": "way/test-tee",
        "type": "TEE",
        "provenance": "source:osm",
        "source_refs": ["way/test-tee"],
        "confidence": "source",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-0.1, 52.0],
                [-0.0999, 52.0],
                [-0.0999, 52.0001],
                [-0.1, 52.0001],
                [-0.1, 52.0],
            ]],
        },
        "association": association or {"method": "manual", "status": "verified"},
    }
    holes = []
    for number in range(1, 19):
        holes.append({
            "hole_number": number,
            "par": 4,
            "routing": {
                "type": "LineString",
                "coordinates": [[-0.1, 52.0], [-0.099, 52.001]],
            } if number != missing_route else None,
            "routing_provenance": {
                "source_id": "osm", "source_feature_id": f"way/test-route-{number}"
            } if number != missing_route else None,
            "green": None if number == missing_green else {
                "front": {"lon": -0.1001, "lat": 52.0001},
                "middle": {"lon": -0.1000, "lat": 52.0002},
                "back": {"lon": -0.0999, "lat": 52.0003},
                "provenance": {"front": "source:greens", "middle": "source:greens", "back": "source:greens"},
            },
            "tees": [feature] if number == 1 else [],
            "fairways": [],
            "rough": [],
            "green_source_features": [],
            "paths": [],
            "context": [],
            "hazards": [],
            "conflicts": [],
        })
    return {
        "schema_version": "uido.course.v0.2",
        "course": {"id": "test-course", "name": "Test Course"},
        "sources": [{"id": "osm", "status": "available"}],
        "registration": registration or {
            "status": "verified",
            "transform": {"matrix": [[1, 0, 0], [0, 1, 0]]},
            "metrics": {"rmse_m": 0.2},
        },
        "holes": holes,
        "unassigned_features": [],
    }


class CanonicalCompletenessGateTests(unittest.TestCase):
    def test_unmeasured_registration_blocks_completeness(self):
        model = sample_model(
            registration={"status": "pending_measured_solution", "transform": None, "metrics": None}
        )
        result = build_canonical(model)
        self.assertFalse(result["validation"]["course_complete"])
        self.assertIn("satellite_registration", result["validation"]["unresolved_features"])
        self.assertNotIn("hole_feature_association", result["validation"]["unresolved_features"])

    def test_nearest_path_heuristic_does_not_count_as_verified_association(self):
        model = sample_model(association={"method": "nearest_hole_path", "distance_m": 4.2})
        result = build_canonical(model)
        self.assertFalse(result["validation"]["course_complete"])
        self.assertIn("hole_feature_association", result["validation"]["unresolved_features"])
        self.assertNotIn("satellite_registration", result["validation"]["unresolved_features"])

    def test_both_verified_gates_allow_complete_synthetic_fixture(self):
        result = build_canonical(sample_model())
        self.assertTrue(result["validation"]["course_complete"])
        self.assertEqual(result["validation"]["holes_complete"], 18)
        self.assertEqual(result["validation"]["physical_geometry_count"], 1)
        self.assertEqual(result["validation"]["unresolved_features"], [])
        self.assertEqual(result["provenance"]["stage"], "enriched_candidate")
        self.assertEqual(result["geometry"]["features"][0]["type"], "teeing_area")
        self.assertEqual(result["geometry"]["features"][0]["provenance"]["source_id"], "osm")
        self.assertEqual(result["holes"][0]["routing"]["type"], "LineString")
        self.assertIn("front", result["holes"][0]["green"])
        self.assertEqual(result["holes"][0]["routing_provenance"]["source_id"], "osm")

    def test_missing_route_blocks_completeness_even_with_verified_gates(self):
        result = build_canonical(sample_model(missing_route=7))
        self.assertFalse(result["validation"]["course_complete"])
        self.assertIn({"hole": 7, "feature": "routing"}, result["validation"]["unresolved_features"])

    def test_missing_green_anchors_blocks_completeness(self):
        result = build_canonical(sample_model(missing_green=4))
        self.assertFalse(result["validation"]["course_complete"])
        self.assertIn({"hole": 4, "feature": "green_anchors"}, result["validation"]["unresolved_features"])
        self.assertIn("green_anchors", result["validation"]["unresolved_features"])

    def test_output_matches_canonical_json_schema(self):
        root = Path(__file__).resolve().parents[2]
        schema = json.loads((root / "course-models/canonical-course.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(build_canonical(sample_model()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
