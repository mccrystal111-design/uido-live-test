#!/usr/bin/env python3
"""Register one GolfCourseAPI course in the UiDo registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

BASE_URL = "https://api.golfcourseapi.com"
REGISTRY = Path("course-models/COURSE_REGISTRY.json")
UIDO_NAMESPACE = uuid.UUID("7b5f9c2d-8b3d-4e68-9a0f-0c8c1f7b6a21")


def api_json(path: str) -> dict[str, Any]:
    key = os.environ.get("GOLFCOURSEAPI_API_KEY")
    if not key:
        raise SystemExit("GOLFCOURSEAPI_API_KEY is not set")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        headers={
            "Authorization": f"Key {key}",
            "Accept": "application/json",
            "User-Agent": "UiDo-course-registration/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GolfCourseAPI returned HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"GolfCourseAPI request failed: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("GolfCourseAPI returned an unexpected response")
    return payload


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not value:
        raise SystemExit("Course name cannot produce a valid UiDo course id")
    return value


def stable_uido_id(provider_id: str) -> str:
    return f"uido-course-{uuid.uuid5(UIDO_NAMESPACE, f'golfcourseapi:{provider_id}')}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("provider_id", help="GolfCourseAPI numeric course id")
    args = parser.parse_args()

    detail = api_json(f"/v1/courses/{args.provider_id}")
    location = detail.get("location") or {}
    name = detail.get("course_name") or detail.get("name") or detail.get("club_name")
    if not name:
        raise SystemExit("GolfCourseAPI course detail contains no course name")

    provider_id = str(detail.get("id", args.provider_id))
    course_id = slugify(name)
    registry = json.loads(REGISTRY.read_text())
    courses = registry.setdefault("courses", {})

    for existing_id, existing in courses.items():
        identity = existing.get("identity", {})
        if str(identity.get("provider_id", "")) == provider_id:
            print(json.dumps({"status": "already-registered", "course_id": existing_id}, indent=2))
            return 0

    if course_id in courses:
        digest = hashlib.sha1(provider_id.encode()).hexdigest()[:8]
        course_id = f"{course_id}-{digest}"

    record = {
        "identity": {
            "uido_id": stable_uido_id(provider_id),
            "provider": "golfcourseapi",
            "provider_id": provider_id,
        },
        "name": name,
        "club_name": detail.get("club_name"),
        "holes": detail.get("holes"),
        "par": detail.get("par"),
        "location": {
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "city": location.get("city"),
            "state": location.get("state"),
            "country": location.get("country"),
        },
        "lifecycle": {"status": "registered"},
    }

    courses[course_id] = record
    registry["schema_version"] = "uido.course-registry.v0.2"
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")

    print(json.dumps({"status": "registered", "course_id": course_id, "record": record}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
