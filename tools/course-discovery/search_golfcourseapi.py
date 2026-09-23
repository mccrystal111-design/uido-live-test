#!/usr/bin/env python3
"""Search GolfCourseAPI and print normalised course candidates."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://api.golfcourseapi.com"


def request_json(path: str, params: dict[str, Any] | None = None) -> Any:
    api_key = os.environ.get("GOLFCOURSEAPI_API_KEY")
    if not api_key:
        raise SystemExit("GOLFCOURSEAPI_API_KEY is not set")
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Key {api_key}",
            "Accept": "application/json",
            "User-Agent": "UiDo-course-discovery/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GolfCourseAPI returned HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"GolfCourseAPI request failed: {exc}") from exc


def normalise(course: dict[str, Any]) -> dict[str, Any]:
    location = course.get("location") or {}
    return {
        "provider_id": course.get("id"),
        "name": course.get("course_name") or course.get("name") or course.get("club_name"),
        "club_name": course.get("club_name"),
        "location": {
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "city": location.get("city"),
            "state": location.get("state"),
            "country": location.get("country"),
        },
        "holes": course.get("holes"),
        "par": course.get("par"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="GolfCourseAPI search query")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    response = request_json("/v1/search", {"search_query": args.query})
    courses = response.get("courses", []) if isinstance(response, dict) else []
    results = [normalise(c) for c in courses[: max(0, args.limit)]]
    print(json.dumps({"query": args.query, "count": len(results), "courses": results}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
