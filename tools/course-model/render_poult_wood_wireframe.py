#!/usr/bin/env python3
"""Render a read-only Poult Wood source wireframe for human QA.

OSM geometry is plotted as acquired. Fairway multipolygon relations are resolved
through their member ways; no geometry is invented, smoothed, or rewritten.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import matplotlib.pyplot as plt

BOUNDARY = (0.2958967, 51.2184284, 0.3095094, 51.2276149)

def pts(e):
    return [(p["lon"], p["lat"]) for p in e.get("geometry", [])]

def centroid(e):
    p = pts(e)
    if not p: return None
    return (sum(x for x,y in p)/len(p), sum(y for x,y in p)/len(p))

def dist2(a,b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def hole_number(e):
    r = str(e.get("tags",{}).get("ref",""))
    return int(r) if r.isdigit() else None

def relation_segments(rel, by_id):
    out = []
    for m in rel.get("members", []):
        if m.get("type") != "way" or m.get("role") not in ("outer",""):
            continue
        w = by_id.get(("way", m.get("ref")))
        if w and pts(w):
            out.append(pts(w))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--all",required=True)
    ap.add_argument("--fairways",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    all_data=json.loads(Path(args.all).read_text())
    fw_data=json.loads(Path(args.fairways).read_text())
    all_e=all_data.get("elements",[])
    fw_e=fw_data.get("elements",[])

    holes={hole_number(e):e for e in all_e
           if e.get("tags",{}).get("golf")=="hole" and 1 <= (hole_number(e) or 0) <= 18}
    greens=[e for e in all_e if e.get("tags",{}).get("golf")=="green"]
    tees=[e for e in all_e if e.get("tags",{}).get("golf")=="tee"]
    bunkers=[e for e in all_e if e.get("tags",{}).get("golf")=="bunker"]
    water=[e for e in all_e if e.get("tags",{}).get("golf")=="water_hazard"]
    fairway_ways=[e for e in fw_e if e.get("type")=="way" and pts(e)]
    fairway_rels=[e for e in fw_e if e.get("type")=="relation"]

    by_id={(e.get("type"),e.get("id")):e for e in all_e}
    # Focused relation query includes member ways; index them here.
    for e in fw_e:
        by_id[(e.get("type"),e.get("id"))]=e

    fairway_sources=[]
    for w in fairway_ways:
        fairway_sources.append({
            "id":f"way/{w['id']}",
            "relation":False,
            "segments":[pts(w)],
            "centroid":centroid(w)
        })
    for r in fairway_rels:
        segs=relation_segments(r, by_id)
        if segs:
            flat=[p for s in segs for p in s]
            c=(sum(x for x,y in flat)/len(flat),sum(y for x,y in flat)/len(flat))
            fairway_sources.append({
                "id":f"relation/{r['id']}",
                "relation":True,
                "segments":segs,
                "centroid":c,
                "roles":[m.get("role") for m in r.get("members",[]) if m.get("type")=="way"]
            })

    # Associate source fairway elements for QA only. The source geometry retains its ID.
    associations=[]
    for f in fairway_sources:
        c=f["centroid"]
        nearest=min(holes, key=lambda n: dist2(c, centroid(holes[n]))) if c else None
        associations.append({"source":f["id"],"nearest_hole":nearest})

    fig, axes=plt.subplots(3,6,figsize=(18,10), constrained_layout=True)
    for n, ax in enumerate(axes.flat, start=1):
        if n>18:
            ax.axis("off"); continue
        h=holes.get(n)
        if not h:
            ax.set_title(f"Hole {n} — missing OSM route")
            ax.axis("off"); continue

        hp=pts(h)
        if hp:
            ax.plot([p[0] for p in hp],[p[1] for p in hp],linewidth=2,label="route")

        hc=centroid(h)
        # Fairways nearest by source centroid; QA display only.
        candidates=[f for f in fairway_sources if f["centroid"] and
                    dist2(f["centroid"],hc) < 0.000015]
        for f in candidates:
            for s in f["segments"]:
                ax.plot([p[0] for p in s],[p[1] for p in s],linewidth=1.4)
        for e, style in [(tees,":"),(bunkers,""),(water,"")]:
            for x in e:
                c=centroid(x)
                if c and dist2(c,hc)<0.000025:
                    p=pts(x)
                    if len(p)>=2:
                        ax.plot([q[0] for q in p],[q[1] for q in p],linewidth=0.8,linestyle=style)
                    elif c:
                        ax.scatter([c[0]],[c[1]],s=8)

        # Plot all nearby greens.
        for g in greens:
            c=centroid(g)
            if c and dist2(c,hc)<0.00002:
                p=pts(g)
                if len(p)>=2:
                    ax.plot([q[0] for q in p],[q[1] for q in p],linewidth=1.2)

        ax.set_title(f"Hole {n}")
        ax.set_aspect("equal", adjustable="box")
        ax.tick_params(labelsize=6)

    fig.suptitle("UiDo — Poult Wood 18-hole source wireframe QA\nOSM geometry only • fairway relations resolved from source members • no invented geometry")
    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(out,dpi=180)
    plt.close(fig)

    report={
        "schema":"uido.poult-wood.wireframe-qa.v0.1",
        "target_holes":18,
        "osm_holes_found":len(holes),
        "greens":len(greens),
        "tees":len(tees),
        "bunkers":len(bunkers),
        "water":len(water),
        "fairway_source_elements":len(fairway_sources),
        "fairway_ways":len(fairway_ways),
        "fairway_relations":len(fairway_rels),
        "fairway_associations":associations,
        "geometry_policy":"source geometry plotted without mutation; nearest-hole association is QA metadata only"
    }
    (out.parent/"wireframe-report.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
