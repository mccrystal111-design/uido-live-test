#!/usr/bin/env python3
"""Prepare physical acquisition metadata for a registered UiDo course.

Existing authoritative source manifests/boundaries are preserved. For a newly
registered course, discover the OSM golf-course footprint around the provider
coordinate and write an ephemeral source manifest for the acquisition packet.
GolfCourseAPI is never queried here.
"""
from __future__ import annotations
import argparse, json, math, re, urllib.parse, urllib.request
from pathlib import Path

REGISTRY = Path("course-models/COURSE_REGISTRY.json")
# Prefer the current UK-capable Private.coffee instance. Keep global
# fallbacks because public Overpass capacity can be transiently unavailable.
ENDPOINTS = [
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

def clean(value: str) -> str:
    parts = re.sub(r"[^a-z0-9]+", " ", value.casefold()).split()
    stop_words = {"golf", "course", "club"}
    return " ".join(part for part in parts if part not in stop_words)

def similarity(target: str, candidate: str) -> float:
    a, b = set(clean(target).split()), set(clean(candidate).split())
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def geometry_points(element: dict) -> list[tuple[float, float]]:
    points = []
    for p in element.get("geometry", []) or []:
        if "lat" in p and "lon" in p:
            points.append((float(p["lat"]), float(p["lon"])))
    center = element.get("center")
    if not points and isinstance(center, dict) and "lat" in center and "lon" in center:
        points.append((float(center["lat"]), float(center["lon"])))
    return points

def distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
    y = math.radians(lat2 - lat1)
    return 6371000 * math.sqrt(x*x + y*y)

def geocode_venue(course: dict, selection: str = "") -> tuple[float, float, dict]:
    """Resolve a venue anchor when provider course GPS is absent."""
    club_name = str(course.get("club_name") or "").strip()
    location = course.get("location") or {}
    city = str(location.get("city") or "").strip()
    country = str(location.get("country") or "").strip()
    if not club_name:
        raise SystemExit("Cannot geocode venue anchor: registered course has no club_name")

    # Try the venue identity first, then progressively broader geographic
    # anchors. A geocoder can legitimately return a neighbouring golf club for
    # an ambiguous venue name; in that case a locality anchor is safer because
    # the subsequent OSM step resolves the actual course identity.
    cleaned_venue = clean(club_name)
    queries = [
        ", ".join(p for p in [club_name, city, country] if p),
        ", ".join(p for p in [club_name, country] if p),
        ", ".join(p for p in [cleaned_venue, city, country] if p),
        ", ".join(p for p in [cleaned_venue, city] if p),
        ", ".join(p for p in [city, country] if p),
        club_name,
    ]
    all_candidates = []
    seen = set()
    for query_text in queries:
        params = urllib.parse.urlencode({
            "q": query_text, "format": "jsonv2", "limit": 5, "addressdetails": 1
        })
        req = urllib.request.Request(
            "https://nominatim.openstreetmap.org/search?" + params,
            headers={
                "Accept": "application/json",
                "User-Agent": "UiDo-course-builder/1.0 (+https://github.com/mccrystal111-design/uido-live-test)",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                results = json.load(response)
        except Exception as exc:
            print(f"Venue geocoding query failed: {query_text!r}: {exc}")
            continue

        ranked = []
        for result in results if isinstance(results, list) else []:
            if not result.get("lat") or not result.get("lon"):
                continue
            display = str(result.get("display_name") or "").casefold()
            name = str(result.get("name") or display)
            score = similarity(club_name, name)
            if "golf" in display and "club" in display:
                score += 0.15
            ranked.append((score, result))

        ranked.sort(key=lambda item: item[0], reverse=True)
        for score, result in ranked:
            key = (str(result.get("osm_type") or ""), str(result.get("osm_id") or ""))
            if key not in seen:
                seen.add(key)
                all_candidates.append((score, query_text, result))

    if not all_candidates:
        raise SystemExit(
            f"No geocoded venue anchor found for {club_name!r}; "
            "searched venue and locality candidates"
        )

    all_candidates.sort(key=lambda item: item[0], reverse=True)

    if selection:
        wanted = clean(selection)
        matches = [
            item for item in all_candidates
            if clean(str(item[2].get("name") or item[2].get("display_name") or "")) == wanted
        ]
        if not matches:
            options = "\n".join(
                f"  - {item[2].get('name') or item[2].get('display_name')}"
                for item in all_candidates[:10]
            )
            raise SystemExit(
                f"Venue selection {selection!r} was not found. Candidates were:\n{options}"
            )
        chosen = matches[0]
    else:
        chosen = all_candidates[0]
        plausible = [
            item for item in all_candidates
            if item[0] >= max(0.35, chosen[0] - 0.20)
        ]
        if chosen[0] < 0.75 or len(plausible) > 1:
            options = "\n".join(
                f"  - {item[2].get('name') or item[2].get('display_name')} "
                f"[score {item[0]:.2f}]"
                for item in all_candidates[:10]
            )
            raise SystemExit(
                f"IDENTITY_CONFIRMATION_REQUIRED for {club_name!r}. "
                f"Choose one of these venue candidates and rerun with --venue-selection:\n{options}"
            )

    best_score, query_text, best = chosen
    try:
        lat, lon = float(best["lat"]), float(best["lon"])
    except (TypeError, ValueError):
        raise SystemExit("Selected venue candidate has no usable coordinates")
    return lat, lon, {
        "provider": "nominatim",
        "query": query_text,
        "display_name": best.get("display_name"),
        "osm_type": best.get("osm_type"),
        "osm_id": best.get("osm_id"),
        "latitude": lat,
        "longitude": lon,
        "address": best.get("address") or {},
        "selection_score": best_score,
    }

def query_overpass(lat: float, lon: float) -> dict:
    query = (
        '[out:json][timeout:120];'
        f'nwr["leisure"="golf_course"](around:5000,{lat},{lon});'
        'out center geom;'
    )
    body = urllib.parse.urlencode({"data": query}).encode()
    for endpoint in ENDPOINTS:
        last_error = None
        for attempt in range(1, 4):
            try:
                req = urllib.request.Request(
                    endpoint,
                    data=body,
                    headers={
                        "Accept": "application/json",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": "UiDo-course-builder/1.0 (+https://github.com/mccrystal111-design/uido-live-test)",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=180) as response:
                    payload = json.load(response)
                if isinstance(payload, dict):
                    return payload
                raise RuntimeError("Overpass returned a non-object response")
            except Exception as exc:
                last_error = exc
                print(f"OSM discovery endpoint failed: {endpoint} (attempt {attempt}/3): {exc}")
        print(f"Moving to next Overpass endpoint after retries: {endpoint}: {last_error}")
    raise SystemExit("Unable to discover an OSM golf-course footprint from the available Overpass endpoints.")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("course_id")\n    parser.add_argument("--venue-selection", default="", help="Exact venue name selected during UiDo identity resolution.")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text())
    course = registry.get("courses", {}).get(args.course_id)
    if not isinstance(course, dict):
        raise SystemExit(f"Unknown course id: {args.course_id}")

    # A verified boundary is sufficient physical authority for acquisition.
    # If a source manifest is already persisted, preserve it unchanged. Otherwise
    # materialise an ephemeral acquisition manifest from the registry boundary
    # without making another identity-discovery Overpass call.
    if course.get("boundary"):
        boundary = course["boundary"]
        source_manifest = course.get("source_manifest")
        if source_manifest:
            print(json.dumps({
                "status": "existing",
                "course_id": args.course_id,
                "boundary": boundary,
                "source_manifest": source_manifest,
            }, indent=2))
            return 0

        holes = course.get("holes")
        par = course.get("par")
        if holes != 18 or par is None:
            raise SystemExit(
                f"{args.course_id}: physical acquisition requires 18 holes and a known par; "
                f"got holes={holes}, par={par}"
            )
        manifest = {
            "schema_version": "uido.course-source-manifest.v0.2",
            "course": args.course_id,
            "target_course": {
                "name": course.get("club_name") or course.get("name") or args.course_id,
                "holes": int(holes),
                "par": int(par),
                "boundary": boundary,
            },
            "identity_validation": {
                "provider": course.get("identity", {}).get("provider"),
                "provider_id": course.get("identity", {}).get("provider_id"),
                "provider_coordinates": {
                    "latitude": (course.get("location") or {}).get("latitude"),
                    "longitude": (course.get("location") or {}).get("longitude"),
                },
                "identity_result": "PASS",
                "basis": "registry_physical_authority",
            },
            "osm_capture": {
                "status": "to_be_acquired",
                "authority": "OpenStreetMap",
                "geometry_policy": "raw source retained; no geometry invented",
            },
        }
        output = args.output or Path("build") / args.course_id / "physical-source-manifest.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(manifest, indent=2) + "\n")
        print(json.dumps({
            "status": "registry_boundary",
            "course_id": args.course_id,
            "manifest": str(output),
            "boundary": boundary,
        }, indent=2))
        return 0

    location = course.get("location") or {}
    coordinate_source = "provider_course"
    venue_anchor = None
    try:
        lat, lon = float(location["latitude"]), float(location["longitude"])
    except (KeyError, TypeError, ValueError):
        lat, lon, venue_anchor = geocode_venue(course, args.venue_selection)
        coordinate_source = "venue_geocode"

    target_names = [
        str(course.get("club_name") or ""),
        " ".join(
            part for part in [
                str(course.get("club_name") or ""),
                str(course.get("name") or ""),
            ] if part
        ),
        str(course.get("name") or ""),
        args.course_id,
    ]
    target_names = [name for name in target_names if name.strip()]
    identity_label = next((name for name in target_names if name.strip()), args.course_id)

    payload = query_overpass(lat, lon)
    candidates = []
    for element in payload.get("elements", []) or []:
        tags = element.get("tags") or {}
        name = str(tags.get("name") or "").strip()
        # Unnamed leisure=golf_course geometry is not sufficient evidence for
        # course identity. Keep the matcher fail-closed rather than allowing an
        # unnamed polygon to outrank a named course.
        if not name:
            continue
        points = geometry_points(element)
        if not points:
            continue
        center_lat = sum(p[0] for p in points) / len(points)
        center_lon = sum(p[1] for p in points) / len(points)
        dist = distance_m(lat, lon, center_lat, center_lon)
        score = max(similarity(target, name) for target in target_names)
        if any(clean(target) == clean(name) for target in target_names):
            score = 1.0
        candidates.append({
            "element": element,
            "name": name,
            "similarity": score,
            "distance_m": dist,
            "points": points,
        })

    if not candidates:
        raise SystemExit(f"No OSM leisure=golf_course footprint found near {identity_label}")

    candidates.sort(key=lambda x: (-x["similarity"], x["distance_m"]))
    best = candidates[0]
    if best["similarity"] < 0.34:
        raise SystemExit(
            f"OSM course identity is ambiguous for {identity_label}; best candidate "
            f"{best['name']!r} has similarity {best['similarity']:.2f}"
        )
    if len(candidates) > 1 and best["similarity"] == candidates[1]["similarity"] and abs(best["distance_m"] - candidates[1]["distance_m"]) < 100:
        raise SystemExit(f"OSM course identity is ambiguous for {identity_label}")

    points = best["points"]
    west = min(p[1] for p in points)
    east = max(p[1] for p in points)
    south = min(p[0] for p in points)
    north = max(p[0] for p in points)

    holes = course.get("holes")
    par = course.get("par")
    if holes != 18 or par is None:
        raise SystemExit(f"{args.course_id}: physical acquisition requires 18 holes and a known par; got holes={holes}, par={par}")

    manifest = {
        "schema_version": "uido.course-source-manifest.v0.2",
        "course": args.course_id,
        "target_course": {
            "name": course["name"],
            "holes": int(holes),
            "par": int(par),
            "boundary": {"west": west, "south": south, "east": east, "north": north, "crs": "EPSG:4326"},
        },
        "identity_validation": {
            "provider": course.get("identity", {}).get("provider"),
            "provider_id": course.get("identity", {}).get("provider_id"),
            "provider_coordinates": {
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
            },
            "search_anchor": {
                "type": coordinate_source,
                "latitude": lat,
                "longitude": lon,
                "source": venue_anchor or {"provider": "golfcourseapi"},
            },
            "osm_element": {
                "type": best["element"].get("type"),
                "id": best["element"].get("id"),
                "name": best["name"],
                "similarity": best["similarity"],
                "distance_m": best["distance_m"],
            },
            "identity_result": "PASS",
        },
        "osm_capture": {
            "status": "to_be_acquired",
            "authority": "OpenStreetMap",
            "geometry_policy": "raw source retained; no geometry invented",
        },
    }
    output = args.output or Path("build") / args.course_id / "physical-source-manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": "generated", "manifest": str(output), "candidate": {
        "name": best["name"], "type": best["element"].get("type"), "id": best["element"].get("id"),
        "similarity": best["similarity"], "distance_m": best["distance_m"],
        "boundary": manifest["target_course"]["boundary"],
    }}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
