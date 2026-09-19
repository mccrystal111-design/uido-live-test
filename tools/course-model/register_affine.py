#!/usr/bin/env python3
import argparse,json,math
from pathlib import Path

def solve3(A,b):
    A=[row[:] + [bb] for row,bb in zip(A,b)]
    for i in range(3):
        p=max(range(i,3),key=lambda r:abs(A[r][i])); A[i],A[p]=A[p],A[i]
        q=A[i][i]
        if abs(q)<1e-12: raise ValueError("Control points are degenerate")
        A[i]=[v/q for v in A[i]]
        for r in range(3):
            if r==i: continue
            q=A[r][i]; A[r]=[A[r][c]-q*A[i][c] for c in range(4)]
    return [A[i][3] for i in range(3)]

def fit(points,target):
    N=[[p["source"][0],p["source"][1],1.0] for p in points]
    NtN=[[sum(r[i]*r[j] for r in N) for j in range(3)] for i in range(3)]
    Ntb=[sum(N[k][i]*points[k]["target"][target] for k in range(len(points))) for i in range(3)]
    return solve3(NtN,Ntb)

ap=argparse.ArgumentParser(); ap.add_argument("--control",required=True); ap.add_argument("--pixel-m",type=float); ap.add_argument("--out",required=True); a=ap.parse_args()
pts=json.loads(Path(a.control).read_text())
if len(pts)<3: raise SystemExit("Need at least 3 control points")
ax=fit(pts,0); ay=fit(pts,1); rows=[]
for p in pts:
    lon,lat=p["source"]; x,y=p["target"]
    px=ax[0]*lon+ax[1]*lat+ax[2]; py=ay[0]*lon+ay[1]*lat+ay[2]
    dx,dy=px-x,py-y; rp=math.hypot(dx,dy)
    rows.append({"id":p.get("id"),"residual_px":[dx,dy],"residual_px_magnitude":rp,"residual_m":rp*a.pixel_m if a.pixel_m else None})
rms=math.sqrt(sum(r["residual_px_magnitude"]**2 for r in rows)/len(rows))
result={"schema_version":"uido.registration.v0.1","transform":{"type":"affine","x":ax,"y":ay,"source_crs":"EPSG:4326","target":"satellite_pixel"},"metrics":{"control_points":len(pts),"rms_px":rms,"rms_m":rms*a.pixel_m if a.pixel_m else None,"max_px":max(r["residual_px_magnitude"] for r in rows),"max_m":max(r["residual_px_magnitude"] for r in rows)*a.pixel_m if a.pixel_m else None},"controls":rows}
Path(a.out).write_text(json.dumps(result,indent=2)); print(json.dumps(result["metrics"],indent=2))