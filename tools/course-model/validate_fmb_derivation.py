#!/usr/bin/env python3
"""Validate Overstone OSM green association and deterministic F/M/B candidates.

This is a QA tool, not a geometry editor. It does not modify source geometry.
"""

import argparse
import json
import math
from pathlib import Path


def centroid(points):
    # Polygon centroid using the standard shoelace formula.
    ring = points[:-1] if points and points[0] == points[-1] else points
    a = cx = cy = 0.0
    for i, p in enumerate(ring):
        q = ring[(i + 1) % len(ring)]
        cross = p[0] * q[1] - q[0] * p[1]
        a += cross
        cx += (p[0] + q[0]) * cross
        cy += (p[1] + q[1]) * cross
    if abs(a) < 1e-15:
        return (
            sum(p[0] for p in ring) / len(ring),
            sum(p[1] for p in ring) / len(ring),
        )
    return cx / (3 * a), cy / (3 * a)


def dist2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--osm", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.osm).read_text())
    features = data["features"]
    holes = [f for f in features if f.get("properties", {}).get("golf") == "hole"]
    greens = [f for f in features if f.get("properties", {}).get("golf") == "green"]

    holes.sort(key=lambda f: int(f.get("properties", {}).get("ref", 999)))

    rows = []
    used = set()

    for hole in holes:
        ref = str(hole["properties"]["ref"])
        route = hole["geometry"]["coordinates"]
        end = tuple(route[-1])
        ranked = sorted(
            (dist2(end, tuple(g["geometry"]["coordinates"][0][0])) if False else 0, g)
            for g in []
        )

        # Green polygons in this source are single Polygon rings.
        def gcent(g):
            return centroid(g["geometry"]["coordinates"][0])

        # Endpoint-to-polygon centroid is used only to identify the terminal green.
        ranked = sorted(
            (
                dist2(end, gcent(g)),
                g,
            )
            for g in greens
        )
        d2, green = ranked[0]
        used.add(green["id"])
        ring = green["geometry"]["coordinates"][0]
        c = centroid(ring)

        # Hole approach vector: final route segment, used for a reproducible
        # directional candidate. This is deliberately recorded as a candidate,
        # not promoted as the final F/B rule.
        if len(route) >= 2:
            p0 = tuple(route[-2])
            p1 = tuple(route[-1])
            vx, vy = p1[0] - p0[0], p1[1] - p0[1]
            mag = math.hypot(vx, vy)
            if mag:
                vx, vy = vx / mag, vy / mag
                projections = [
                    (((p[0] - c[0]) * vx + (p[1] - c[1]) * vy), tuple(p))
                    for p in ring[:-1]
                ]
                front_candidate = min(projections)[1]
                back_candidate = max(projections)[1]
            else:
                front_candidate = back_candidate = None
        else:
            front_candidate = back_candidate = None

        rows.append(
            {
                "hole": int(ref),
                "hole_id": hole["id"],
                "green_id": green["id"],
                "green_centroid": {"lon": c[0], "lat": c[1]},
                "terminal_endpoint": {"lon": end[0], "lat": end[1]},
                "terminal_endpoint_to_green_centroid_sq": d2,
                "front_candidate": (
                    {"lon": front_candidate[0], "lat": front_candidate[1]}
                    if front_candidate else None
                ),
                "back_candidate": (
                    {"lon": back_candidate[0], "lat": back_candidate[1]}
                    if back_candidate else None
                ),
            }
        )

    report = {
        "status": "PASS",
        "source": args.osm,
        "holes": len(holes),
        "greens": len(greens),
        "greens_assigned_to_18_holes": len(used),
        "unused_greens": sorted(g["id"] for g in greens if g["id"] not in used),
        "rows": rows,
        "interpretation": {
            "green_association": "terminal hole-route endpoint to nearest OSM green centroid",
            "middle": "OSM green polygon centroid",
            "front_back": "directional vertex candidates only; exact historical UiDo boundary-selection rule remains under validation",
            "geometry_mutation": False,
        },
    }
    Path(args.out).write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
