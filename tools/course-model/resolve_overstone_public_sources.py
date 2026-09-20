#!/usr/bin/env python3
"""Resolve Environment Agency public imagery/LiDAR records covering Overstone.

This resolves catalogue metadata only. It does not download imagery or LAZ.
"""
from __future__ import annotations
import argparse, json, xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
import requests

EA="https://environment.data.gov.uk"
ARCGIS=EA+"/KB6uNVj5ZcJr7jUP/ArcGIS/rest/services"
VAP=ARCGIS+"/Vertical_Aerial_Photography_Catalogues/FeatureServer/0"
LIDAR=ARCGIS+"/National_LIDAR_Programme_Catalogues/FeatureServer/0"
WFS=EA+"/spatialdata/survey-index-files/wfs"
E,N=480792.63,265074.40
GRID="SP8065"

def arcgis_point(layer:str)->list[dict[str,Any]]:
    p={"where":"1=1","geometry":f"{E},{N}","geometryType":"esriGeometryPoint",
       "inSR":"27700","spatialRel":"esriSpatialRelIntersects","outFields":"*",
       "returnGeometry":"false","f":"json"}
    r=requests.get(layer+"/query",params=p,timeout=60); r.raise_for_status()
    j=r.json()
    if "error" in j: raise RuntimeError(j["error"])
    return [f["attributes"] for f in j.get("features",[])]

def wfs_types()->list[str]:
    p={"service":"WFS","version":"2.0.0","request":"GetCapabilities"}
    r=requests.get(WFS,params=p,timeout=60); r.raise_for_status()
    root=ET.fromstring(r.text); out=[]
    for ft in root.iter():
        if ft.tag.endswith("FeatureType"):
            for c in ft:
                if c.tag.endswith("Name") and c.text: out.append(c.text.strip())
    return out

def wfs_bbox(name:str)->list[dict[str,Any]]:
    p={"service":"WFS","version":"2.0.0","request":"GetFeature","typeNames":name,
       "bbox":"480000,265000,485000,270000,EPSG:27700",
       "outputFormat":"application/json","srsName":"EPSG:27700","count":"200"}
    r=requests.get(WFS,params=p,timeout=120); r.raise_for_status()
    return [f.get("properties",{}) for f in r.json().get("features",[])]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="overstone-public-source-resolution.json")
    a=ap.parse_args()
    out={"schema_version":"uido.course.public-source-resolution.v0.1",
         "course":"overstone-park","site":{"easting":E,"northing":N,"epsg":27700,"national_grid_5km":GRID},
         "vap":{"method":"arcgis_point","records":[]},"lidar":{"method":"arcgis_point","records":[]},
         "errors":[]}
    for k,url in (("vap",VAP),("lidar",LIDAR)):
        try: out[k]["records"]=arcgis_point(url)
        except Exception as e: out["errors"].append(f"{k} ArcGIS: {e}")
    if not out["vap"]["records"] or not out["lidar"]["records"]:
        try:
            names=wfs_types(); out["wfs_feature_types"]=names
            for name in names:
                low=name.lower()
                if "vertical" in low and not out["vap"]["records"]:
                    try:
                        out["vap"]["records"]=wfs_bbox(name); out["vap"]["method"]="wfs_sp8065_bbox"
                    except Exception as e: out["errors"].append(f"vap WFS {name}: {e}")
                if "lidar" in low and "national" in low and not out["lidar"]["records"]:
                    try:
                        out["lidar"]["records"]=wfs_bbox(name); out["lidar"]["method"]="wfs_sp8065_bbox"
                    except Exception as e: out["errors"].append(f"lidar WFS {name}: {e}")
        except Exception as e: out["errors"].append(f"WFS discovery: {e}")
    out["status"]={"vap_resolved":bool(out["vap"]["records"]),"lidar_resolved":bool(out["lidar"]["records"])}
    Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__": main()
