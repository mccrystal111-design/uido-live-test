#!/usr/bin/env python3
"""Export the supplied UK golf-club workbook as a staging JSON seed.

The directory is club-level, not course-level. This exporter intentionally
leaves geometry acquisition and course matching as separate downstream work.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import uuid
from datetime import date, datetime
from pathlib import Path

import pandas as pd


COUNTRY_CODES = {
    "England": ("GB", "ENG"),
    "Scotland": ("GB", "SCT"),
    "Wales": ("GB", "WLS"),
    "Northern Ireland": ("GB", "NIR"),
}


def text(value: object) -> str | None:
    if pd.isna(value):
        return None
    result = str(value).strip()
    return result or None


def json_safe(value: object) -> object:
    if pd.isna(value):
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def export_seed(source: Path, output: Path) -> dict:
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    frame = pd.read_excel(source, sheet_name="Golf clubs", header=4)
    required = {
        "Golf club", "Country", "Postal address", "Phone", "Website",
        "Email", "Contact name", "Contact title", "Directory listing",
        "Page published", "Latitude", "Longitude", "Coordinate status",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Workbook is missing required columns: {missing}")

    records = []
    for row in frame.to_dict(orient="records"):
        listing_url = text(row["Directory listing"])
        if not listing_url:
            raise ValueError("Every club row must retain its source listing URL")
        directory_key = listing_url.rstrip("/").rsplit("/", 1)[-1]
        latitude = json_safe(row["Latitude"])
        longitude = json_safe(row["Longitude"])
        coordinate_status = text(row["Coordinate status"])
        country = text(row["Country"])
        country_code, country_subdivision = COUNTRY_CODES.get(country, ("GB", None))
        records.append({
            "id": str(uuid.uuid5(uuid.NAMESPACE_URL, listing_url.rstrip("/") + "/")),
            "directory_key": f"gbgolf:{directory_key}",
            "club_name": text(row["Golf club"]),
            "country": country,
            "country_code": country_code,
            "country_subdivision": country_subdivision,
            "postal_address": text(row["Postal address"]),
            "phone": text(row["Phone"]),
            "website": text(row["Website"]),
            "email": text(row["Email"]),
            "contact_name": text(row["Contact name"]),
            "contact_title": text(row["Contact title"]),
            "location": None if latitude is None or longitude is None else {
                "type": "Point",
                "coordinates": [float(longitude), float(latitude)],
            },
            "coordinate_status": coordinate_status,
            "coordinate_source": "postcodes.io",
            "source_file_sha256": source_hash,
            "source": {
                "name": "GBGolf.com",
                "listing_url": listing_url,
                "page_published": text(row["Page published"]),
                "coordinate_note": "Postcode centroid; not an exact clubhouse or course pin.",
            },
        })

    keys = [record["directory_key"] for record in records]
    if len(keys) != len(set(keys)):
        raise ValueError("Directory listing URLs did not produce unique keys")

    payload = {
        "schema_version": "uido.uk-club-directory-staging.v1",
        "status": "staging_only_not_loaded",
        "source_file_sha256": source_hash,
        "source_file_name": source.name,
        "record_count": len(records),
        "notes": [
            "Records represent golf clubs, not verified individual courses.",
            "Course matching and course geometry acquisition are separate stages.",
            "Coordinates are postcode centroids where available, not exact pins.",
            "Public directory details are transcribed source data and have not been independently verified.",
        ],
        "clubs": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="Supplied workbook")
    parser.add_argument("--out", type=Path, required=True, help="Staging JSON path")
    parser.add_argument("--copy-csv-out", type=Path, help="Optional one-column CSV for PostgreSQL COPY QA")
    args = parser.parse_args()
    payload = export_seed(args.input, args.out)
    if args.copy_csv_out:
        args.copy_csv_out.parent.mkdir(parents=True, exist_ok=True)
        with args.copy_csv_out.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            for club in payload["clubs"]:
                writer.writerow([json.dumps(club, ensure_ascii=False, separators=(",", ":"))])
    print(json.dumps({"output": str(args.out), "record_count": payload["record_count"], "status": payload["status"]}))


if __name__ == "__main__":
    main()
