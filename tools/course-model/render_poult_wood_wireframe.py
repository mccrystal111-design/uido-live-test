#!/usr/bin/env python3
"""Render a Poult Wood source skeleton for human geometry QA.

This pass follows the proven Overstone source-model pattern. OSM remains the
structural source of truth: select the documented target hole routes, associate
source features deterministically to those routes, and preserve the original
geometry. Poult Wood fairways are OSM multipolygon relations, so relation members
are resolved only as a display representation; no geometry is invented, smoothed,
or moved.

Colour is intentionally restrained at this stage; the UiDo presentation palette
is applied only after the source skeleton is visually accepted.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from shapely.geometry import LineString, Polygon
from shapely.ops import linemerge, polygonize, unary_union


EARTH_M_PER_DEG_LAT = 111_320.0


def points(element):
    return [(p["lon"], p["lat"]) for p in element.get("geometry", [])]


def centroid(element):
    p = points(element)
    if not p:
        return None
    return (
        sum(x for x, _ in p) / len(p),
        sum(y for _, y in p) / len(p),
    )


def distance_m(a, b):
    if not a or not b:
        return float("inf")
    mean_lat = math.radians((a[1] + b[1]) * 0.5)
    dx = (a[0] - b[0]) * math.cos(mean_lat) * EARTH_M_PER_DEG_LAT
    dy = (a[1] - b[1]) * EARTH_M_PER_DEG_LAT
    return math.hypot(dx, dy)


def nearest_distance_to_route(point, route):
    if not point or len(route) < 2:
        return float("inf")
    return min(
        distance_m(point, q)
        for q in route
    )


def hole_ref(element):
    ref = str(element.get("tags", {}).get("ref", ""))
    return int(ref) if ref.isdigit() else None


def select_target_holes(elements):
    """Select one route for each documented target ref 1..18.

    Poult Wood's source contains duplicate refs for the additional facility
    course. The target manifest documents refs 1..18; for duplicate refs we
    select the lowest OSM way ID, which is the main-course route in the current
    source capture. The excluded duplicates are retained in the QA report.
    """
    candidates = {}
    excluded = []

    for e in elements:
        if e.get("tags", {}).get("golf") != "hole":
            continue
        ref = hole_ref(e)
        if ref is None or not 1 <= ref <= 18:
            continue
        candidates.setdefault(ref, []).append(e)

    selected = {}
    for ref in range(1, 19):
        options = sorted(candidates.get(ref, []), key=lambda e: int(e["id"]))
        if options:
            selected[ref] = options[0]
            excluded.extend(
                {
                    "ref": ref,
                    "id": e["id"],
                    "reason": "duplicate facility hole route outside target 18-hole route set",
                }
                for e in options[1:]
            )

    return selected, excluded


def build_way_index(elements):
    return {
        (e.get("type"), e.get("id")): e
        for e in elements
        if e.get("type") == "way"
    }


def relation_polygons(relation, way_index):
    """Reconstruct relation polygons from its source member ways.

    Outer and inner members are kept as source geometry. We use Shapely only
    to join member ways and form polygons for display; the coordinates are not
    altered.
    """
    outers = []
    inners = []

    for member in relation.get("members", []):
        if member.get("type") != "way":
            continue
        way = way_index.get(("way", member.get("ref")))
        if not way:
            continue
        p = points(way)
        if len(p) < 2:
            continue
        line = LineString(p)
        if member.get("role") == "inner":
            inners.append(line)
        elif member.get("role") == "outer":
            outers.append(line)

    if not outers:
        return []

    outer_union = unary_union(outers)
    outer_lines = linemerge(outer_union) if outer_union.geom_type != "LineString" else outer_union
    outer_polys = list(polygonize(outer_lines))

    if not outer_polys:
        return []

    if inners:
        inner_union = unary_union(inners)
        inner_lines = linemerge(inner_union) if inner_union.geom_type != "LineString" else inner_union
        inner_polys = list(polygonize(inner_lines))
    else:
        inner_polys = []
    result = []

    for poly in outer_polys:
        carved = poly
        for inner in inner_polys:
            if inner.representative_point().within(poly):
                carved = carved.difference(inner)
        if not carved.is_empty:
            result.append(carved)

    return result


def fairway_sources(all_elements, fairway_elements, target_holes):
    """Return resolved fairway source geometry and target-course associations."""
    all_way_index = build_way_index(all_elements)
    fairway_way_index = build_way_index(fairway_elements)

    # Follow the Overstone rule: the complete OSM capture is authoritative;
    # the focused relation query is only a convenient way to retrieve the
    # relation members needed to reconstruct the source fairway geometry.
    way_index = dict(all_way_index)
    way_index.update(fairway_way_index)

    target_routes = {
        ref: points(h)
        for ref, h in target_holes.items()
        if points(h)
    }

    other_holes = [
        e for e in all_elements
        if e.get("tags", {}).get("golf") == "hole"
        and e not in target_holes.values()
    ]
    other_routes = [points(e) for e in other_holes if points(e)]

    sources = []

    for element in fairway_elements:
        if element.get("type") == "way" and points(element):
            geoms = [LineString(points(element))]
        elif element.get("type") == "relation":
            geoms = relation_polygons(element, way_index)
        else:
            continue

        if not geoms:
            continue

        representative = unary_union(geoms).representative_point()
        rep = (representative.x, representative.y)

        target_distances = {
            ref: nearest_distance_to_route(rep, route)
            for ref, route in target_routes.items()
        }
        other_distance = (
            min(nearest_distance_to_route(rep, route) for route in other_routes)
            if other_routes
            else float("inf")
        )
        nearest_target_ref = min(target_distances, key=target_distances.get)
        nearest_target_distance = target_distances[nearest_target_ref]

        # Keep source fairways belonging to the target 18-hole course. This
        # avoids pulling in the separate 9-hole facility geometry that shares
        # the same acquisition boundary.
        target_associated = nearest_target_distance <= other_distance

        sources.append(
            {
                "id": f"{element.get('type')}/{element.get('id')}",
                "element": element,
                "geometries": geoms,
                "nearest_target_hole": nearest_target_ref,
                "nearest_target_distance_m": round(nearest_target_distance, 2),
                "nearest_other_hole_distance_m": round(other_distance, 2),
                "target_associated": target_associated,
            }
        )

    return sources


def plot_geometry(ax, geom, **kwargs):
    if geom.is_empty:
        return
    if geom.geom_type == "Polygon":
        x, y = geom.exterior.xy
        ax.fill(x, y, **kwargs)
        for ring in geom.interiors:
            rx, ry = ring.xy
            ax.plot(rx, ry, color=kwargs.get("edgecolor", "#555555"), linewidth=0.5)
    elif geom.geom_type in ("LineString", "LinearRing"):
        x, y = geom.xy
        line_kwargs = dict(kwargs)
        line_kwargs.pop("facecolor", None)
        line_kwargs.pop("edgecolor", None)
        if "color" not in line_kwargs:
            line_kwargs["color"] = kwargs.get("edgecolor", "#555555")
        ax.plot(x, y, **line_kwargs)
    elif geom.geom_type in ("MultiPolygon", "MultiLineString", "GeometryCollection"):
        for part in geom.geoms:
            plot_geometry(ax, part, **kwargs)


def draw_scale_bar(ax, boundary, metres=500):
    west, south, east, north = boundary
    lat = (south + north) * 0.5
    deg_lon = metres / (EARTH_M_PER_DEG_LAT * math.cos(math.radians(lat)))
    x0 = west + (east - west) * 0.055
    y0 = south + (north - south) * 0.045
    ax.plot([x0, x0 + deg_lon], [y0, y0], color="#222222", linewidth=2.0, solid_capstyle="butt")
    ax.plot([x0, x0], [y0 - 0.00010, y0 + 0.00010], color="#222222", linewidth=1.0)
    ax.plot([x0 + deg_lon, x0 + deg_lon], [y0 - 0.00010, y0 + 0.00010], color="#222222", linewidth=1.0)
    ax.text(x0 + deg_lon / 2, y0 + 0.00018, f"{metres} m", ha="center", va="bottom", fontsize=8)


def draw_north(ax, boundary):
    west, south, east, north = boundary
    x = east - (east - west) * 0.055
    y = north - (north - south) * 0.09
    ax.annotate(
        "N",
        xy=(x, y + 0.00065),
        xytext=(x, y),
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        arrowprops={"arrowstyle": "-|>", "linewidth": 1.2, "color": "#222222"},
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", required=True)
    ap.add_argument("--fairways", required=True)
    ap.add_argument("--manifest", required=True, help="Canonical course acquisition manifest")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    all_elements = json.loads(Path(args.all).read_text()).get("elements", [])
    fairway_elements = json.loads(Path(args.fairways).read_text()).get("elements", [])
    acquisition = json.loads(Path(args.manifest).read_text())
    course_name = acquisition.get("course", acquisition.get("course_id", "UiDo course"))
    osm_manifest_path = Path(args.all).with_name("manifest.json")
    osm_manifest = json.loads(osm_manifest_path.read_text())
    south, west, north, east = osm_manifest["bbox"]
    boundary = (west, south, east, north)

    target_holes, excluded_holes = select_target_holes(all_elements)

    greens = [e for e in all_elements if e.get("tags", {}).get("golf") == "green"]
    tees = [e for e in all_elements if e.get("tags", {}).get("golf") == "tee"]
    bunkers = [e for e in all_elements if e.get("tags", {}).get("golf") == "bunker"]
    water = [e for e in all_elements if e.get("tags", {}).get("golf") == "water_hazard"]
    pins = [e for e in all_elements if e.get("tags", {}).get("golf") == "pin"]

    fairways = fairway_sources(all_elements, fairway_elements, target_holes)
    target_fairways = [f for f in fairways if f["target_associated"]]

    fig, ax = plt.subplots(figsize=(15, 11))
    ax.set_facecolor("#fbfaf7")

    # Fairway areas: geometry-first neutral fill.
    for source in target_fairways:
        for geom in source["geometries"]:
            plot_geometry(
                ax,
                geom,
                facecolor="#e8e6df",
                edgecolor="#7b7971",
                linewidth=0.65,
                alpha=0.78,
            )

    # Greens.
    for green in greens:
        p = points(green)
        if len(p) >= 3:
            poly = Polygon(p)
            plot_geometry(
                ax,
                poly,
                facecolor="#f5f3ed",
                edgecolor="#444444",
                linewidth=0.85,
                alpha=1.0,
            )

    # Hazards.
    for bunker in bunkers:
        p = points(bunker)
        if len(p) >= 3:
            plot_geometry(
                ax,
                Polygon(p),
                facecolor="#dedbd2",
                edgecolor="#66645f",
                linewidth=0.65,
                alpha=0.9,
            )

    for hazard in water:
        p = points(hazard)
        if len(p) >= 2:
            plot_geometry(
                ax,
                Polygon(p) if len(p) >= 3 else LineString(p),
                facecolor="#d9dce0",
                edgecolor="#4d5258",
                linewidth=0.75,
                alpha=0.9,
            )

    # Tees.
    for tee in tees:
        p = points(tee)
        if len(p) >= 2:
            ax.plot(
                [x for x, _ in p],
                [y for _, y in p],
                color="#555555",
                linewidth=1.1,
            )
        elif p:
            ax.scatter([p[0][0]], [p[0][1]], s=9, color="#555555", zorder=8)

    # Hole routes and numbers. These are the source route geometries, not
    # generated centre-lines.
    for ref, hole in target_holes.items():
        p = points(hole)
        if len(p) >= 2:
            ax.plot(
                [x for x, _ in p],
                [y for _, y in p],
                color="#222222",
                linewidth=1.5,
                zorder=10,
            )
        c = centroid(hole)
        if c:
            ax.text(
                c[0],
                c[1],
                str(ref),
                fontsize=9,
                fontweight="bold",
                color="#222222",
                ha="center",
                va="center",
                bbox={"boxstyle": "circle,pad=0.16", "facecolor": "#fbfaf7", "edgecolor": "none", "alpha": 0.85},
                zorder=20,
            )

    # Pins are genuine OSM source points. They are shown as small neutral
    # targets only; no F/M/B positions are inferred from them.
    for pin in pins:
        if "lat" in pin and "lon" in pin:
            ax.scatter(
                [pin["lon"]],
                [pin["lat"]],
                s=14,
                facecolors="none",
                edgecolors="#333333",
                linewidths=0.8,
                zorder=15,
            )

    # Acquisition boundary, north arrow, grid and scale.
    west, south, east, north = boundary
    ax.plot(
        [west, east, east, west, west],
        [south, south, north, north, south],
        linestyle="--",
        color="#666666",
        linewidth=0.9,
        alpha=0.8,
    )

    ax.set_xlim(west, east)
    ax.set_ylim(south, north)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, color="#d7d5cf", linewidth=0.45, alpha=0.65)
    ax.tick_params(labelsize=7)

    draw_north(ax, boundary)
    draw_scale_bar(ax, boundary)

    legend = [
        Patch(facecolor="#e8e6df", edgecolor="#7b7971", label="OSM fairway source"),
        Patch(facecolor="#f5f3ed", edgecolor="#444444", label="OSM green"),
        Patch(facecolor="#dedbd2", edgecolor="#66645f", label="OSM bunker"),
        Patch(facecolor="#d9dce0", edgecolor="#4d5258", label="OSM water"),
    ]
    ax.legend(handles=legend, loc="lower right", frameon=True, framealpha=0.92, fontsize=8)

    fig.suptitle(
        f"UiDo — {course_name} 18-hole source skeleton QA",
        fontsize=15,
        fontweight="bold",
        y=0.975,
    )
    fig.text(
        0.5,
        0.945,
        "Canonical Course Packet • OSM geometry only • fairway multipolygons resolved from source members • no invented or smoothed geometry",
        ha="center",
        fontsize=9,
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)

    report = {
        "schema": "uido.poult-wood.wireframe-qa.v0.2",
        "target_holes_requested": 18,
        "target_holes_rendered": sorted(target_holes),
        "duplicate_facility_hole_routes_excluded": excluded_holes,
        "greens": len(greens),
        "tees": len(tees),
        "bunkers": len(bunkers),
        "water_hazards": len(water),
        "pins": len(pins),
        "fairway_source_elements": len(fairways),
        "fairway_source_elements_rendered": len(target_fairways),
        "fairway_source_elements_excluded_as_other_facility_course": len(fairways) - len(target_fairways),
        "fairway_associations": [
            {
                "source": f["id"],
                "nearest_target_hole": f["nearest_target_hole"],
                "nearest_target_distance_m": f["nearest_target_distance_m"],
                "nearest_other_hole_distance_m": f["nearest_other_hole_distance_m"],
                "target_associated": f["target_associated"],
            }
            for f in fairways
        ],
        "geometry_policy": "source geometry plotted without mutation; Shapely only joins source relation members for display polygon reconstruction",
        "fmb_policy": "no F/M/B points inferred in this skeleton pass",
    }
    (out.parent / "wireframe-report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
