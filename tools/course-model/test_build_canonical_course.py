#!/usr/bin/env python3
"""Unit tests for canonical course completeness gates; no network or database access."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_canonical_course import build_canonical  # noqa: E402


def sample_model(registration=None, association=None, missing_route=None):
    feature = {
        "id": "way/test-tee",
        "type": "TEE",
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
            "green": None,
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
        "course": {"id": "test-course"},
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

    def test_missing_route_blocks_completeness_even_with_verified_gates(self):
        result = build_canonical(sample_model(missing_route=7))
        self.assertFalse(result["validation"]["course_complete"])
        self.assertIn({"hole": 7, "feature": "routing"}, result["validation"]["unresolved_features"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
