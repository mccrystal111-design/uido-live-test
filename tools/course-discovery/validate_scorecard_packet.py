#!/usr/bin/env python3
"""Validate a UiDo canonical tee/scorecard packet."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"Scorecard invalid: {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scorecard_file", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.scorecard_file.read_text())
    if payload.get("schema_version") != "uido.scorecard.v0.1":
        fail("unexpected schema_version")
    if not payload.get("provider") or not payload.get("provider_id"):
        fail("missing provider provenance")
    tee_sets = payload.get("tee_sets")
    if not isinstance(tee_sets, list) or not tee_sets:
        fail("no tee sets")

    seen = set()
    for tee in tee_sets:
        category = tee.get("category")
        name = tee.get("tee_name")
        key = (category, name)
        if key in seen:
            fail(f"duplicate tee set {category}/{name}")
        seen.add(key)

        holes = tee.get("holes")
        if tee.get("number_of_holes") != 18 or not isinstance(holes, list) or len(holes) != 18:
            fail(f"{category}/{name} does not contain exactly 18 holes")

        numbers = [hole.get("hole") for hole in holes]
        if numbers != list(range(1, 19)):
            fail(f"{category}/{name} hole numbering is not 1..18")

        pars = [hole.get("par") for hole in holes]
        yards = [hole.get("yardage") for hole in holes]
        if any(not isinstance(value, (int, float)) for value in pars):
            fail(f"{category}/{name} contains a missing/non-numeric par")
        if any(not isinstance(value, (int, float)) for value in yards):
            fail(f"{category}/{name} contains a missing/non-numeric yardage")

        par_sum = sum(pars)
        yard_sum = sum(yards)
        if tee.get("par_total") != par_sum:
            fail(f"{category}/{name} par_total {tee.get('par_total')} != hole sum {par_sum}")
        if tee.get("total_yards") != yard_sum:
            fail(f"{category}/{name} total_yards {tee.get('total_yards')} != hole sum {yard_sum}")

        for field in ("course_rating", "slope_rating"):
            if not isinstance(tee.get(field), (int, float)):
                fail(f"{category}/{name} missing/non-numeric {field}")

    print(f"Scorecard valid: {len(tee_sets)} tee sets, 18 holes each")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
