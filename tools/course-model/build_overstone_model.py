#!/usr/bin/env python3
"""Build a provider-neutral UiDo course model from an OSM GeoJSON capture."""
from __future__ import annotations
import argparse, json, math
from collections import Counter
from pathlib import Path

FEATURE_MAP = {"bunker":"BUNKER","tee":"TEE","rough":"ROUGH","green":"GREEN","fairway":"FAIRWAY","water_hazard":"WATER","cartpath":"PATH","path":"PATH","wood":"WOODLAND","woodland":"WOODLAND","oob":"OOB"}

def props_of(f):
    p=f.get("properties") or {}
    tags=p.get("tags")
    return {**p, **tags} if isinstance(tags,dict) else p

def feature_type(p):
    golf=str(p.get("golf","")).lower()
    if golf in FEATURE_MAP: return FEATURE_MAP[golf]
    for k,v in p.items():
        if k in FEATURE_MAP and (v in ("yes",True,1,"1") or k in FEATURE_MAP): return FEATURE_MAP[k]
    if str(p.get("leisure","")).lower()=="golf_course": return "COURSE"
    return None

def hole_number(p):
    for key in ("hole","ref","ref:hole","number","hole_number"):
        v=p.get(key)
        if v is not None and str(v).strip().isdigit():
            n=int(str(v).strip())
            if 1 <= n <= 18: return n
    return None

def load_green_points(path):
    d=json.loads(Path(path).read_text())
    return {int(k):v for k,v in d["greenPoints"].items()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--osm",required=True); ap.add_argument("--greens",required=True); ap.add_argument("--out",required=True)
    a=ap.parse_args()
    src=json.loads(Path(a.osm).read_text()); greens=load_green_points(a.greens)
    model={"schema_version":"uido.course.v0.1","course":{"id":"overstone-park","name":"Overstone Park","location":{"country":"GB"}},
      "provenance_policy":"source_preserved_derived_explicit_verified_never_silent_replace",
      "sources":[{"id":"osm","kind":"source","provider":"OpenStreetMap","status":"ingested"},{"id":"greens","kind":"source","provider":"UiDo supplied green F/M/B dataset","status":"ingested"},{"id":"satellite","kind":"source","provider":"Esri World Imagery","status":"pending_refinement"},{"id":"lidar","kind":"source","provider":"UK elevation/vegetation data","status":"pending_refinement"}],
      "registration":{"status":"pending_measured_solution","transform":None,"metrics":None},"feature_counts":{"source_osm":{},"green_anchors":18},"holes":[]}
    for n in range(1,19):
        g=greens.get(n)
        model["holes"].append({"hole_number":n,"green":{"front":g["front"] if g else None,"middle":g["middle"] if g else None,"back":g["back"] if g else None,"provenance":{"front":"source:greens","middle":"source:greens","back":"source:greens"}}, "tees":[],"fairways":[],"rough":[],"hazards":[],"paths":[],"context":[],"routing":None,"conflicts":[],"extraction_status":"green_anchor_only"})
    for i,f in enumerate(src.get("features",[])):
        p=props_of(f); typ=feature_type(p)
        if not typ or typ=="COURSE": continue
        model["feature_counts"]["source_osm"][typ]=model["feature_counts"]["source_osm"].get(typ,0)+1
        h=hole_number(p)
        item={"id":str(p.get("@id") or p.get("id") or f"source-osm-{i+1}"),"type":typ,"geometry":f.get("geometry"),"provenance":"source:osm","confidence":"source","evidence":{"source_tags":p},"source_refs":[str(p.get("@id") or p.get("id") or f"feature:{i+1}")],"status":"source"}
        bucket="tees" if typ=="TEE" else "fairways" if typ=="FAIRWAY" else "rough" if typ=="ROUGH" else "paths" if typ=="PATH" else "hazards" if typ in ("BUNKER","WATER") else "context"
        if h: model["holes"][h-1][bucket].append(item)
        else: model.setdefault("unassigned_features",[]).append(item)
    model["notes"]=["OSM geometry is source data and is never overwritten by satellite refinement.","Verified GPS must not enter candidate generation; it belongs in a separate validation layer.","Registration remains null until a measured OSM-to-imagery solution exists.","Missing OSM features remain missing; the builder does not invent geometry."]
    Path(a.out).write_text(json.dumps(model,indent=2))
    print(json.dumps({"output":a.out,"feature_counts":model["feature_counts"]},indent=2))

if __name__=="__main__": main()