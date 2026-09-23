#!/usr/bin/env python3
"""Validate the UiDo course registry without external services."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REGISTRY = Path("course-models/COURSE_REGISTRY.json")
COURSE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_STATUSES = {
    "discovered", "registered", "acquisition-ready", "acquired",
    "packet-validated", "wireframe-ready", "uido-ready",
}


def main() -> int:
    data = json.loads(REGISTRY.read_text())
    if data.get("schema_version") not in {"uido.course-registry.v0.1", "uido.course-registry.v0.2"}:
        raise SystemExit("Unsupported registry schema_version")
    courses = data.get("courses")
    if not isinstance(courses, dict) or not courses:
        raise SystemExit("Registry must contain at least one course")

    seen_uido_ids = set()
    seen_provider_ids = set()

    for course_id, course in courses.items():
        if not COURSE_ID_RE.fullmatch(course_id):
            raise SystemExit(f"Invalid course id: {course_id}")
        if not course.get("name"):
            raise SystemExit(f"{course_id}: missing name")

        identity = course.get("identity", {})
        uido_id = identity.get("uido_id")
        if uido_id:
            if uido_id in seen_uido_ids:
                raise SystemExit(f"Duplicate UiDo id: {uido_id}")
            seen_uido_ids.add(uido_id)

        if identity.get("provider") == "golfcourseapi" and identity.get("provider_id") is not None:
            provider_id = str(identity["provider_id"])
            if provider_id in seen_provider_ids:
                raise SystemExit(f"Duplicate GolfCourseAPI id: {provider_id}")
            seen_provider_ids.add(provider_id)

        status = course.get("lifecycle", {}).get("status")
        if status and status not in VALID_STATUSES:
            raise SystemExit(f"{course_id}: invalid lifecycle status {status}")

        if "boundary" in course:
            boundary = course["boundary"]
            for key in ("west", "south", "east", "north"):
                if not isinstance(boundary.get(key), (int, float)):
                    raise SystemExit(f"{course_id}: invalid boundary.{key}")

    print(f"Registry valid: {len(courses)} courses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
