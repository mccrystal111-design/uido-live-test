#!/usr/bin/env python3
"""Search GolfCourseAPI, hydrate candidates, and apply optional country filtering."""
from __future__ import annotations
import argparse, json, os, re, sys, urllib.error, urllib.parse, urllib.request
from typing import Any
BASE_URL = "https://api.golfcourseapi.com"

def request_json(path: str, params: dict[str, Any] | None = None) -> Any:
    key = os.environ.get("GOLFCOURSEAPI_API_KEY")
    if not key: raise SystemExit("GOLFCOURSEAPI_API_KEY is not set")
    url = f"{BASE_URL}{path}" + (("?" + urllib.parse.urlencode(params)) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Key {key}", "Accept": "application/json", "User-Agent": "UiDo-course-discovery/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response: return json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"GolfCourseAPI returned HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except urllib.error.URLError as exc: raise SystemExit(f"GolfCourseAPI request failed: {exc}") from exc

def clean_query(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    stop_words = {"golf", "course", "club"}
    return " ".join(part for part in value.split() if part not in stop_words)

def normalise(course: dict[str, Any]) -> dict[str, Any]:
    location = course.get("location") or {}
    # GolfCourseAPI has used both nested and top-level location fields across
    # responses. Keep the provider adapter tolerant, while preserving one
    # canonical UiDo shape downstream.
    def loc_value(key: str):
        return location.get(key) if location.get(key) is not None else course.get(key)

    country = loc_value("country")
    if country is None:
        country = location.get("country_code") or course.get("country_code")
    return {"provider_id": str(course.get("id")) if course.get("id") is not None else None,
            "name": course.get("course_name") or course.get("name") or course.get("club_name"),
            "club_name": course.get("club_name"),
            "location": {k: loc_value(k) for k in ("latitude","longitude","city","state")},
            "location_country": country,
            "holes": course.get("holes"), "par": course.get("par"),
            "_diagnostics": {
                "top_level_keys": sorted(course.keys()),
                "location_keys": sorted(location.keys()),
                "location_country_raw": location.get("country"),
                "top_level_country_raw": course.get("country"),
                "location_country_code_raw": location.get("country_code"),
                "top_level_country_code_raw": course.get("country_code"),
            }}

def hydrate(provider_id: str) -> dict[str, Any]:
    detail = request_json(f"/v1/courses/{urllib.parse.quote(provider_id, safe='')}")
    if not isinstance(detail, dict): raise SystemExit(f"GolfCourseAPI returned unexpected detail for {provider_id}")
    # GolfCourseAPI wraps the detailed record in {"course": ...}.
    # Accept the wrapper explicitly and fail closed if the payload is malformed.
    record = detail.get("course") if isinstance(detail.get("course"), dict) else detail
    if not isinstance(record, dict): raise SystemExit(f"GolfCourseAPI returned malformed detail for {provider_id}")
    if record.get("id") is None:
        record = dict(record)
        record["id"] = provider_id
    return normalise(record)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--country", help="Country filter applied to search results.")
    args = parser.parse_args()
    query = clean_query(args.query)
    if not query:
        raise SystemExit("Course search query is empty after normalization.")
    response = request_json("/v1/search", {"search_query": query})
    courses = response.get("courses", []) if isinstance(response, dict) else []
    normalized = [normalise(course) for course in courses[:max(0, args.limit)] if isinstance(course, dict) and course.get("id") is not None]
    candidates = normalized
    if args.country:
        aliases = {"united kingdom": {"united kingdom", "uk", "great britain", "gb", "gbr", "england", "scotland", "wales", "northern ireland"}, "usa": {"usa", "us", "united states", "united states of america"}}
        expected = args.country.strip().casefold()
        accepted = aliases.get(expected, {expected})
        candidates = [c for c in normalized if str(c.get("location_country") or "").strip().casefold() in accepted]
    print(json.dumps({"query": args.query, "normalized_query": query, "country_filter": args.country, "count": len(candidates), "courses": candidates, "detail_lookup": "deferred_until_registration"}, indent=2))
    return 0

if __name__ == "__main__": sys.exit(main())
