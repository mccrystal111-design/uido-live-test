#!/usr/bin/env python3
"""Register one GolfCourseAPI course in the UiDo registry."""
from __future__ import annotations
import argparse, hashlib, json, os, re, urllib.error, urllib.request, uuid
from pathlib import Path
from typing import Any
BASE_URL="https://api.golfcourseapi.com"; REGISTRY=Path("course-models/COURSE_REGISTRY.json")
PROVIDER_DIR=Path("course-models/provider-data/golfcourseapi")
UIDO_NAMESPACE=uuid.UUID("7b5f9c2d-8b3d-4e68-9a0f-0c8c1f7b6a21")

def api_json(path: str) -> dict[str, Any]:
    key=os.environ.get("GOLFCOURSEAPI_API_KEY")
    if not key: raise SystemExit("GOLFCOURSEAPI_API_KEY is not set")
    req=urllib.request.Request(f"{BASE_URL}{path}",headers={"Authorization":f"Key {key}","Accept":"application/json","User-Agent":"UiDo-course-registration/1.1"})
    try:
        with urllib.request.urlopen(req,timeout=30) as response: payload=json.load(response)
    except urllib.error.HTTPError as exc: raise SystemExit(f"GolfCourseAPI returned HTTP {exc.code}: {exc.read().decode('utf-8',errors='replace')}") from exc
    except urllib.error.URLError as exc: raise SystemExit(f"GolfCourseAPI request failed: {exc}") from exc
    if not isinstance(payload,dict): raise SystemExit("GolfCourseAPI returned an unexpected response")
    return payload

def slugify(value:str)->str:
    value=re.sub(r"[^a-z0-9]+","-",value.lower()).strip("-")
    if not value: raise SystemExit("Course name cannot produce a valid UiDo course id")
    return value

def stable_uido_id(provider_id:str)->str:
    return f"uido-course-{uuid.uuid5(UIDO_NAMESPACE,f'golfcourseapi:{provider_id}')}"

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("provider_id",help="GolfCourseAPI course id")
    parser.add_argument("--expected-country",help="Refuse registration if the detailed record is not in this country.")
    args=parser.parse_args()
    detail=api_json(f"/v1/courses/{args.provider_id}")
    provider_record=detail.get("course") if isinstance(detail.get("course"),dict) else detail
    location=provider_record.get("location") or {}
    name=provider_record.get("course_name") or provider_record.get("name") or provider_record.get("club_name")
    if not name: raise SystemExit("GolfCourseAPI course detail contains no course name")
    actual_country=str(location.get("country") or detail.get("country") or location.get("country_code") or detail.get("country_code") or "").strip()
    if args.expected_country:
        aliases = {
            "united kingdom": {"united kingdom", "uk", "great britain", "gb", "gbr", "england", "scotland", "wales", "northern ireland"},
            "usa": {"usa", "us", "united states", "united states of america"},
        }
        expected = args.expected_country.strip().casefold()
        accepted = aliases.get(expected, {expected})
        if actual_country.casefold() not in accepted:
        raise SystemExit(f"Course {args.provider_id} is in {actual_country or 'an unknown country'}, not the expected country {args.expected_country}")
    provider_id=str(provider_record.get("id",args.provider_id))
    course_id=slugify(name)
    registry=json.loads(REGISTRY.read_text()); courses=registry.setdefault("courses",{})
    for existing_id,existing in courses.items():
        if str(existing.get("identity",{}).get("provider_id",""))==provider_id:
            print(json.dumps({"status":"already-registered","course_id":existing_id},indent=2)); return 0
    if course_id in courses: course_id=f"{course_id}-{hashlib.sha1(provider_id.encode()).hexdigest()[:8]}"
    record={"identity":{"uido_id":stable_uido_id(provider_id),"provider":"golfcourseapi","provider_id":provider_id},
            "name":name,"club_name":provider_record.get("club_name"),"holes":provider_record.get("holes"),"par":provider_record.get("par"),
            "location":{k:location.get(k) for k in ("latitude","longitude","city","state","country")},
            "lifecycle":{"status":"registered"}}
    courses[course_id]=record
    registry["schema_version"]="uido.course-registry.v0.2"
    PROVIDER_DIR.mkdir(parents=True, exist_ok=True)
    provider_path=PROVIDER_DIR / f"{provider_id}.json"
    provider_path.write_text(json.dumps({
        "provider": "golfcourseapi",
        "provider_id": provider_id,
        "endpoint": f"/v1/courses/{provider_id}",
        "captured_course": provider_record,
    }, indent=2) + "\n")
    REGISTRY.write_text(json.dumps(registry,indent=2)+"\n")
    print(json.dumps({"status":"registered","course_id":course_id,"provider_snapshot":str(provider_path),"record":record},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
