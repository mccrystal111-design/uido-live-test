#!/usr/bin/env python3
"""Build UiDo's canonical tee/scorecard packet from a captured provider record."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("provider_file", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.provider_file.read_text())
    course = payload.get("captured_course") or {}
    tees = course.get("tees") or {}
    canonical = {
        "schema_version": "uido.scorecard.v0.1",
        "provider": payload.get("provider"),
        "provider_id": payload.get("provider_id"),
        "course_name": course.get("course_name"),
        "club_name": course.get("club_name"),
        "tee_sets": [],
    }
    for category in ("male", "female"):
        for tee in tees.get(category, []) or []:
            # GolfCourseAPI can return 9-hole composite/loop tee records alongside
            # the 18-hole course tees. UiDo's canonical course packet is explicitly
            # an 18-hole scorecard, so retain only complete 18-hole tee sets.
            if tee.get("number_of_holes") != 18:
                continue
            holes = []
            for number, hole in enumerate(tee.get("holes", []) or [], 1):
                holes.append({
                    "hole": number,
                    "par": hole.get("par"),
                    "yardage": hole.get("yardage"),
                    "handicap": hole.get("handicap"),
                })
            canonical["tee_sets"].append({
                "category": category,
                "tee_name": tee.get("tee_name"),
                "course_rating": tee.get("course_rating"),
                "slope_rating": tee.get("slope_rating"),
                "total_yards": tee.get("total_yards"),
                "total_meters": tee.get("total_meters"),
                "number_of_holes": tee.get("number_of_holes"),
                "par_total": tee.get("par_total"),
                "holes": holes,
            })
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(canonical, indent=2) + "\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
