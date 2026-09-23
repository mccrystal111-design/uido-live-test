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
    parser.add_argument("course_id")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text())
    course = registry.get("courses", {}).get(args.course_id)
    if not isinstance(course, dict):
        raise SystemExit(f"Unknown course id: {args.course_id}")

    # Preserve already-established physical authority unchanged.
    if course.get("boundary") and course.get("source_manifest"):
        print(json.dumps({
            "status": "existing",
            "course_id": args.course_id,
            "boundary": course["boundary"],
            "source_manifest": course["source_manifest"],
        }, indent=2))
        return 0

    location = course.get("location") or {}
    try:
        lat, lon = float(location["latitude"]), float(location["longitude"])
    except (KeyError, TypeError, ValueError):
        raise SystemExit(f"{args.course_id}: registered course has no usable provider coordinates")

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
            "provider_coordinates": {"latitude": lat, "longitude": lon},
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
