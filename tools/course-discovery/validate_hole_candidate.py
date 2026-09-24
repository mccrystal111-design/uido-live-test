#!/usr/bin/env python3
"""Build provider-neutral geometric evidence for unreferenced OSM golf-hole candidates."""
import json, math, os, sys
from pathlib import Path

try:
    import numpy as np
    import rasterio
    from rasterio.warp import transform
except ImportError as exc:
    raise SystemExit(f"Missing validation dependency: {exc}")

COURSE = os.environ["COURSE_ID"]
ROOT = Path("build") / COURSE
OSM_ROOT = ROOT / "osm"

def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 6371008.8 * 2 * math.asin(math.sqrt(h))

def bearing(a, b):
    la1, la2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1]-a[1])
    x = math.sin(dl) * math.cos(la2)
    y = math.cos(la1)*math.sin(la2) - math.sin(la1)*math.cos(la2)*math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360

def geometry(e):
    return [(float(p["lat"]), float(p["lon"])) for p in e.get("geometry", []) if "lat" in p and "lon" in p]

def centre(g):
    return (sum(p[0] for p in g)/len(g), sum(p[1] for p in g)/len(g))

def path_length(g):
    return sum(hav(g[i], g[i+1]) for i in range(len(g)-1))

def endpoint_context(candidate_geom, neighbour):
    ng = geometry(neighbour)
    if not ng:
        return None
    c0, c1 = candidate_geom[0], candidate_geom[-1]
    n0, n1 = ng[0], ng[-1]
    pairs = [
        ("candidate_start_to_neighbour_start", hav(c0, n0)),
        ("candidate_start_to_neighbour_end", hav(c0, n1)),
        ("candidate_end_to_neighbour_start", hav(c1, n0)),
        ("candidate_end_to_neighbour_end", hav(c1, n1)),
    ]
    return min(pairs, key=lambda x: x[1])

holes = [e for e in json.loads((OSM_ROOT/"golf.json").read_text()).get("elements", [])
         if (e.get("tags") or {}).get("golf") == "hole"]
numbered = {str((e.get("tags") or {}).get("ref")): e for e in holes
            if str((e.get("tags") or {}).get("ref", "")).isdigit()
            and 1 <= int((e.get("tags") or {}).get("ref")) <= 18}
report = json.loads((OSM_ROOT/"hole-candidates.json").read_text())
unreferenced = report.get("unreferenced_candidates", [])
missing = report.get("summary", {}).get("missing_numbered_refs", [])

if not unreferenced:
    out = {"schema":"uido.course.osm-hole-geometric-validation.v0.2","course_id":COURSE,
           "status":"no_candidates","candidates":[]}
    (OSM_ROOT/"hole-candidate-geometric-validation.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))
    sys.exit(0)

lidar_manifest_path = ROOT/"ea-lidar"/"manifest.json"
lidar_manifest = json.loads(lidar_manifest_path.read_text()) if lidar_manifest_path.exists() else {}
rasters = sorted((ROOT/"ea-lidar"/"sources").rglob("*.tif"))

def lidar_profile(g):
    samples = []
    for tif in rasters:
        with rasterio.open(tif) as ds:
            xs, ys = transform("EPSG:4326", ds.crs, [p[1] for p in g], [p[0] for p in g])
            inside = [(x,y) for x,y in zip(xs,ys)
                       if ds.bounds.left <= x <= ds.bounds.right and ds.bounds.bottom <= y <= ds.bounds.top]
            if not inside:
                continue
            vals = [float(v[0]) for v in ds.sample(inside, indexes=1) if np.isfinite(v[0])]
            if vals:
                samples.extend(vals)
    return samples

results = []
for candidate_summary in unreferenced:
    cid = candidate_summary.get("id")
    candidate = next((e for e in holes if e.get("id") == cid), None)
    if not candidate:
        continue
    g = geometry(candidate)
    if len(g) < 2:
        continue
    c = centre(g)
    entry = {
        "candidate": {
            "type": candidate.get("type"), "id": cid, "tags": candidate.get("tags", {}),
            "centre": {"latitude": c[0], "longitude": c[1]},
            "node_count": len(g), "path_length_m": path_length(g),
            "bearing_deg": bearing(g[0], g[-1])
        },
        "adjacent_holes": {},
        "lidar": {"status": lidar_manifest.get("status"), "year": lidar_manifest.get("year"),
                  "resolution_m": lidar_manifest.get("resolution_m"), "coverage":"not_sampled"},
        "candidate_assignments": []
    }
    for missing_ref in missing:
        n = int(missing_ref)
        neighbours = {}
        if str(n-1) in numbered:
            neighbours["previous"] = endpoint_context(g, numbered[str(n-1)])
        if str(n+1) in numbered:
            neighbours["next"] = endpoint_context(g, numbered[str(n+1)])
        entry["adjacent_holes"][missing_ref] = neighbours
        distances = [x[1] for x in neighbours.values() if x]
        # This is evidence only: endpoint proximity is a routing signal, not identity proof.
        score = None if not distances else 1.0 / (1.0 + (sum(distances)/len(distances))/100.0)
        entry["candidate_assignments"].append({
            "missing_hole_ref": missing_ref,
            "endpoint_proximity_score": round(score, 4) if score is not None else None,
            "basis": "candidate endpoints compared with endpoints of adjacent numbered-hole geometries"
        })
    vals = lidar_profile(g)
    if vals:
        entry["lidar"].update({"coverage":"covered","sample_count":len(vals),
                               "elevation_min_m":min(vals),"elevation_max_m":max(vals),
                               "elevation_range_m":max(vals)-min(vals)})
    results.append(entry)

out = {
    "schema":"uido.course.osm-hole-geometric-validation.v0.2",
    "course_id":COURSE,
    "purpose":"Diagnostic geometric evidence only; no candidate is promoted to canonical geometry.",
    "missing_hole_refs":missing,
    "candidates":results,
    "assessment":{"status":"candidate_evidence","canonical":False,
                  "note":"Endpoint proximity and LiDAR surface variation are evidence signals. Hole identity still requires corroborating independent evidence or sufficient multi-signal confidence."}
}
(OSM_ROOT/"hole-candidate-geometric-validation.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))
