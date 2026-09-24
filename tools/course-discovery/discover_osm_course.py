#!/usr/bin/env python3
"""Discover a golf course from OpenStreetMap when the primary provider has no match."""
from __future__ import annotations
import argparse, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

OVERPASS_ENDPOINTS = [
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

def get_json(url: str, *, params=None, data=None, headers=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url, data=data, headers=headers or {"Accept": "application/json",
        "User-Agent": "UiDo-course-discovery/1.0 (+https://github.com/mccrystal111-design/uido-live-test)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)

def tokens(v: str) -> set[str]:
    return set(re.sub(r"[^a-z0-9]+", " ", v.casefold()).split())

def score(wanted: set[str], text: str) -> float:
    got = tokens(text)
    return len(wanted & got) / max(1, len(wanted | got))

def overpass(query: str):
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            req = urllib.request.Request(
                endpoint, data=urllib.parse.urlencode({"data": query}).encode(),
                headers={"Accept":"application/json","Content-Type":"application/x-www-form-urlencoded",
                         "User-Agent":"UiDo-course-discovery/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r), endpoint
        except Exception:
            continue
    raise SystemExit("All Overpass endpoints failed.")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--country", default="United Kingdom")
    p.add_argument("--output", default="osm-discovery.json")
    args = p.parse_args()

    wanted = tokens(args.query)
    params = {"format":"jsonv2","limit":10,"q":f"{args.query}, {args.country}"}
    places = get_json("https://nominatim.openstreetmap.org/search", params=params,
                      headers={"Accept":"application/json","User-Agent":"UiDo-course-discovery/1.0"})
    ranked = []
    for x in places if isinstance(places, list) else []:
        text = " ".join(str(x.get(k) or "") for k in ("name","display_name","type","class"))
        s = score(wanted, text)
        if x.get("lat") and x.get("lon"):
            ranked.append((s, x))
    if not ranked:
        raise SystemExit("OSM/Nominatim returned no usable course candidates.")
    ranked.sort(key=lambda z: z[0], reverse=True)
    _, place = ranked[0]
    lat, lon = float(place["lat"]), float(place["lon"])

    escaped = re.escape(args.query.replace("'", ""))[:80]
    q = f"""[out:json][timeout:180];
(
  nwr["golf"="hole"]["golf:course:name"~"{escaped}",i](around:5000,{lat},{lon});
  nwr["golf"="course"]["name"~"{escaped}",i](around:5000,{lat},{lon});
);
out center tags geom;"""
    payload, endpoint = overpass(q)
    elements = payload.get("elements", [])
    wanted_holes = []
    course_elements = []
    for e in elements:
        tags = e.get("tags") or {}
        if tags.get("golf") == "hole":
            ref = str(tags.get("ref") or "").strip()
            course_name = str(tags.get("golf:course:name") or "")
            if ref.isdigit() and 1 <= int(ref) <= 18:
                wanted_holes.append(e)
        if tags.get("golf") == "course":
            course_elements.append(e)

    if len(wanted_holes) != 18:
        # Some OSM mappings put the course name on the course feature rather than
        # every hole. In that case accept exactly 18 numbered holes only when the
        # selected course feature itself is a strong name match.
        strong_course = [e for e in course_elements
                         if score(wanted, str((e.get("tags") or {}).get("name") or "")) >= 0.5]
        if not strong_course:
            raise SystemExit(f"OSM fallback found {len(wanted_holes)} numbered holes; cannot identify an 18-hole course confidently.")

    points = []
    pars = []
    for e in wanted_holes:
        tags = e.get("tags") or {}
        if tags.get("par") is not None:
            try: pars.append(int(str(tags["par"]).split(".")[0]))
            except ValueError: pass
        for pt in e.get("geometry") or []:
            if "lat" in pt and "lon" in pt:
                points.append((float(pt["lat"]), float(pt["lon"])))
        c = e.get("center")
        if c and c.get("lat") is not None:
            points.append((float(c["lat"]), float(c["lon"])))
    if not points:
        for e in course_elements:
            c = e.get("center")
            if c and c.get("lat") is not None:
                points.append((float(c["lat"]), float(c["lon"])))
    if len(pars) != 18:
        raise SystemExit(f"OSM fallback identified the course but only {len(pars)} hole pars; refusing to invent par.")
    par = sum(pars)
    west, east = min(x[1] for x in points)-0.0005, max(x[1] for x in points)+0.0005
    south, north = min(x[0] for x in points)-0.0005, max(x[0] for x in points)+0.0005

    course_name = args.query.strip()
    for e in course_elements:
        name = str((e.get("tags") or {}).get("name") or "")
        if score(wanted, name) >= 0.5:
            course_name = name
            break
    source_id = f"osm-{place.get('osm_type','unknown')}-{place.get('osm_id','unknown')}"
    course_id = re.sub(r"[^a-z0-9]+","-",course_name.casefold()).strip("-")
    root = Path("course-models")
    root.mkdir(exist_ok=True)
    manifest_path = root / f"{course_id.upper().replace('-','_')}_SOURCE_MANIFEST.json"
    manifest = {
        "schema": "uido.course.source-manifest.v0.2",
        "source": "osm",
        "target_course": {
            "course_id": course_id, "name": course_name, "holes": 18, "par": par,
            "boundary": {"west": west, "south": south, "east": east, "north": north, "crs":"EPSG:4326"},
            "location": {"latitude": lat, "longitude": lon, "country": args.country},
        },
        "provenance": {"discovery_source":"nominatim", "geometry_source":"overpass",
                       "overpass_endpoint":endpoint, "primary_provider":"golfcourseapi",
                       "primary_provider_status":"no_match"},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    result = {
        "source":"osm", "provider_id":source_id, "course_id":course_id,
        "name":course_name, "club_name": place.get("display_name"),
        "holes":18, "par":par, "location":{"latitude":lat,"longitude":lon},
        "source_manifest":str(manifest_path)
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
