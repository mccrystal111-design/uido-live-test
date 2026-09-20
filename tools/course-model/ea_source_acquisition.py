#!/usr/bin/env python3
"""UiDo Overstone source acquisition adapter."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
import requests

EA = "https://environment.data.gov.uk"
ARCGIS = EA + "/KB6uNVj5ZcJr7jUP/ArcGIS/rest/services"
VAP = ARCGIS + "/Vertical_Aerial_Photography_Catalogues/FeatureServer/0"
LIDAR = ARCGIS + "/National_LIDAR_Programme_Catalogues/FeatureServer/0"

def query(layer: str, bbox: tuple[float,float,float,float]) -> list[dict[str,Any]]:
    minx,miny,maxx,maxy = bbox
    geometry = json.dumps({"xmin":minx,"ymin":miny,"xmax":maxx,"ymax":maxy,
                           "spatialReference":{"wkid":27700}})
    params = {"where":"1=1","geometry":geometry,
              "geometryType":"esriGeometryEnvelope","inSR":"27700",
              "spatialRel":"esriSpatialRelIntersects","outFields":"*",
              "returnGeometry":"false","f":"json"}
    r = requests.get(layer + "/query", params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "error" in data: raise RuntimeError(data["error"])
    return [f["attributes"] for f in data.get("features",[])]

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--bbox", nargs=4, type=float, required=True)
    ap.add_argument("--out", required=True)
    a=ap.parse_args()
    bbox=tuple(a.bbox)
    result={
      "schema_version":"uido.source-acquisition-resolution.v0.1",
      "crs":"EPSG:27700",
      "bbox":dict(zip(("min_e","min_n","max_e","max_n"),bbox)),
      "providers":{
        "ea_vertical_aerial_photography":{
          "catalogue_url":VAP,"records":query(VAP,bbox),
          "automated_download_status":"unverified"},
        "ea_national_lidar":{
          "catalogue_url":LIDAR,"records":query(LIDAR,bbox),
          "automated_download_status":"unverified"}},
      "policy":"Do not promote an acquisition route to production until a clean non-interactive retrieval test succeeds."
    }
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
