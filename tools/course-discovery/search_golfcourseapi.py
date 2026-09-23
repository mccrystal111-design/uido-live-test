#!/usr/bin/env python3
"""Search GolfCourseAPI, hydrate candidates, and apply optional country filtering."""
from __future__ import annotations
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
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
    return normalise(detail)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--country", help="Exact country filter applied to detailed course records.")
    args = parser.parse_args()
    response = request_json("/v1/search", {"search_query": args.query})
    courses = response.get("courses", []) if isinstance(response, dict) else []
    hydrated, detail_errors = [], []
    for course in courses[:max(0, args.limit)]:
        if course.get("id") is None: continue
        try: hydrated.append(hydrate(str(course["id"])))
        except SystemExit as exc: detail_errors.append({"provider_id": str(course["id"]), "error": str(exc)})
    if args.country:
        aliases = {
            "united kingdom": {"united kingdom", "uk", "great britain", "gb", "gbr", "england", "scotland", "wales", "northern ireland"},
            "usa": {"usa", "us", "united states", "united states of america"},
        }
        expected = args.country.strip().casefold()
        accepted = aliases.get(expected, {expected})
        hydrated = [
            c for c in hydrated
            if str(c.get("location_country") or "").strip().casefold() in accepted
        ]
    print(json.dumps({"query": args.query, "country_filter": args.country, "count": len(hydrated), "courses": hydrated, "detail_errors": detail_errors}, indent=2))
    return 0
if __name__ == "__main__": sys.exit(main())
