#!/usr/bin/env python3
"""Build provider-neutral UiDo course geometry from OSM golf features."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
MAP={"bunker":"BUNKER","tee":"TEE","rough":"ROUGH","green":"GREEN","fairway":"FAIRWAY","water_hazard":"WATER","cartpath":"PATH","path":"PATH","wood":"WOODLAND","woodland":"WOODLAND","oob":"OOB"}
def props(f):
 p=f.get("properties") or {}; t=p.get("tags") or {}; return {**p,**t} if isinstance(t,dict) else p
def feats(d):
 if "features" in d:return d["features"]
 out=[]
 for e in d.get("elements",[]):
  p={"@id":f"{e.get('type','element')}/{e.get('id')}"};p.update(e.get("tags") or {});g=e.get("geometry")
  if isinstance(g,dict): geom=g
  elif isinstance(g,list): geom={"type":"LineString","coordinates":[[x["lon"],x["lat"]] for x in g]}
  else: continue
  out.append({"type":"Feature","properties":p,"geometry":geom})
 return out
def cent(g):
 if g["type"]=="Point":return g["coordinates"]
 pts=g["coordinates"][0] if g["type"]=="Polygon" else g["coordinates"]
 return [sum(x for x,y in pts)/len(pts),sum(y for x,y in pts)/len(pts)]
def dist(a,b):
 return math.hypot((a[0]-b[0])*math.cos(math.radians((a[1]+b[1])/2)),a[1]-b[1])*111000
def sd(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];q=dx*dx+dy*dy;t=((p[0]-a[0])*dx+(p[1]-a[1])*dy)/q if q else 0;t=max(0,min(1,t));return dist(p,[a[0]+t*dx,a[1]+t*dy])
def pts(g):
 if g["type"]=="Point":return [g["coordinates"]]
 if g["type"]=="LineString":return g["coordinates"]
 if g["type"]=="Polygon":return [p for r in g["coordinates"] for p in r]
 return [p for poly in g["coordinates"] for r in poly for p in r]
def ld(g,line):return min(sd(p,line[i],line[i+1]) for p in pts(g) for i in range(len(line)-1))
def obj(f,t,assoc):
 p=props(f);fid=str(p.get("@id") or f.get("id") or "unknown")
 return {"id":fid,"type":t,"geometry":f["geometry"],"provenance":"source:osm","confidence":"source","evidence":{"source_tags":p},"source_refs":[fid],"status":"source","association":assoc}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--osm",required=True);ap.add_argument("--greens",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
 fs=feats(json.loads(Path(a.osm).read_text()));gd=json.loads(Path(a.greens).read_text())["greenPoints"];holesrc={}
 for f in fs:
  p=props(f)
  if p.get("golf")=="hole" and str(p.get("ref","")).isdigit():holesrc[int(p["ref"])]=f
 holes={}
 for n in range(1,19):
  g=gd[str(n)];hf=holesrc[n];p=props(hf);fid=str(p.get("@id"));par=int(p["par"]) if str(p.get("par","")).isdigit() else None
  holes[n]={"hole_number":n,"par":par,"green":{"front":{"lon":g["front"][0],"lat":g["front"][1]},"middle":{"lon":g["middle"][0],"lat":g["middle"][1]},"back":{"lon":g["back"][0],"lat":g["back"][1]},"provenance":{"front":"source:greens","middle":"source:greens","back":"source:greens"}},"green_source_features":[],"tees":[],"fairways":[],"rough":[],"hazards":[],"paths":[],"context":[],"routing":{"id":fid,"type":"HOLE","geometry":hf["geometry"],"par":par,"provenance":"source:osm","confidence":"source","source_refs":[fid],"status":"source"},"conflicts":[],"extraction_status":"source_geometry_populated"}
 buckets={"tee":"tees","fairway":"fairways","rough":"rough","bunker":"hazards","water_hazard":"hazards","cartpath":"paths","path":"paths","wood":"context","woodland":"context"};un=[]
 for f in fs:
  p=props(f);g=str(p.get("golf","")).lower()
  if g in ("","hole","pin"):continue
  if g=="driving_range":un.append(obj(f,"DRIVING_RANGE",{"method":"non-hole-course-feature"}));continue
  if g=="green":
   c=cent(f["geometry"]);z,n=min((dist(c,[holes[i]["green"]["middle"]["lon"],holes[i]["green"]["middle"]["lat"]]),i) for i in range(1,19))
   (holes[n]["green_source_features"] if z<=30 else un).append(obj(f,"GREEN",{"method":"nearest_green_anchor","distance_m":round(z,2)}));continue
  b=buckets.get(g)
  if not b:continue
  best=(1e99,None)
  for n in range(1,19):
   line=holesrc[n]["geometry"]["coordinates"];z=dist(cent(f["geometry"]),line[0]) if g=="tee" else ld(f["geometry"],line)
   if z<best[0]:best=(z,n)
  if best[1]:holes[best[1]][b].append(obj(f,MAP.get(g,g.upper()),{"method":"nearest_hole_path","distance_m":round(best[0],2),"reference":"hole_start" if g=="tee" else "hole_line"}))
  else:un.append(obj(f,MAP.get(g,g.upper()),{"method":"no_hole_path"}))
 model={"schema_version":"uido.course.v0.2","course":{"id":"overstone-park","name":"Overstone Park","location":{"country":"GB"}},"provenance_policy":"source_preserved_derived_explicit_verified_never_silent_replace","sources":[{"id":"greens","kind":"source","provider":"UiDo green F/M/B dataset","status":"available"},{"id":"osm","kind":"source","provider":"OpenStreetMap","status":"acquired_for_build"},{"id":"ea-aerial","kind":"source","provider":"Environment Agency","status":"imagery"},{"id":"ea-lidar","kind":"source","provider":"Environment Agency","status":"terrain"}],"registration":{"status":"pending_measured_solution","transform":None,"metrics":None},"holes":[holes[i] for i in range(1,19)],"unassigned_features":un,"feature_vocabulary":["GREEN","TEE","FAIRWAY","ROUGH","BUNKER","WATER","WOODLAND","PATH","STRUCTURE","OOB","UNKNOWN"],"confidence_states":["source","derived","verified","conflict","unknown"],"notes":["OSM geometry is source data and is never overwritten by imagery or LiDAR.","Hole association is deterministic and retains association evidence.","Unassigned features remain visible and are never invented.","Registration remains separate and is not fabricated."]}
 Path(a.out).write_text(json.dumps(model,indent=2)+"\n");assert all(h["routing"] and h["tees"] and h["fairways"] for h in model["holes"]);print("PASS: 18 holes have routing, tee and fairway geometry")
if __name__=="__main__":main()
