#!/usr/bin/env python3
"""Probe the EA survey downloader non-interactively and print generated links."""
from __future__ import annotations

import argparse
import json
import os
import time
import zipfile
from pathlib import Path

import shapefile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BBOX = (480137.4894811138, 264803.2820420222, 481451.93252437544, 266016.1542009115)
SURVEY_URL = "https://environment.data.gov.uk/survey"


def make_aoi(out_zip: Path) -> None:
    stem = out_zip.with_suffix("")
    w = shapefile.Writer(str(stem), shapeType=shapefile.POLYGON)
    w.field("id", "N")
    minx, miny, maxx, maxy = BBOX
    w.poly([[(minx,miny),(maxx,miny),(maxx,maxy),(minx,maxy),(minx,miny)]])
    w.record(1)
    w.close()
    stem.with_suffix(".prj").write_text(
        'PROJCS["OSGB 1936 / British National Grid",GEOGCS["OSGB 1936",'
        'DATUM["OSGB_1936",SPHEROID["Airy 1830",6377563.396,299.3249646]],'
        'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],'
        'PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",49],'
        'PARAMETER["central_meridian",-2],PARAMETER["scale_factor",0.9996012717],'
        'PARAMETER["false_easting",400000],PARAMETER["false_northing",-100000],'
        'UNIT["metre",1],AUTHORITY["EPSG","27700"]]',
        encoding="utf-8",
    )
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for p in stem.parent.glob(stem.name + ".*"):
            z.write(p, p.name)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ea-survey-links.json")
    args = ap.parse_args()

    work = Path("ea-survey-aoi")
    work.mkdir(exist_ok=True)
    aoi = work / "overstone-aoi.zip"
    make_aoi(aoi)

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    })
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 180)
    try:
        driver.get(SURVEY_URL)

        # Current EA survey UI: choose "Upload shapefile".
        selects = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "select")
        ))
        upload_select = Select(selects[0])
        labels = [o.text.strip() for o in upload_select.options]
        print("AOI mode options:", labels)
        upload_option = next(o for o in labels if "Upload shapefile" in o)
        upload_select.select_by_visible_text(upload_option)

        file_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        ))
        file_input.send_keys(str(aoi.resolve()))

        available = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.download-button")
        ))
        available.click()

        # The app can re-render while preparing the result list.
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "select")) >= 2)
        selects = d_selects = driver.find_elements(By.CSS_SELECTOR, "select")
        product_select = Select(selects[0])
        products = [
            {"value": o.get_attribute("value"), "text": o.text.strip()}
            for o in product_select.options
        ]
        print("EA products:", json.dumps(products, indent=2))

        vap = [p for p in products if any(
            k in (p["value"] + " " + p["text"]).lower()
            for k in ("aerial", "vertical", "photography", "ortho")
        )]
        if not vap:
            raise RuntimeError("No aerial-photography product exposed by EA survey UI")

        links = []
        for product in vap:
            product_select.select_by_value(product["value"])
            selects = driver.find_elements(By.CSS_SELECTOR, "select")
            if len(selects) < 2:
                continue
            year_select = Select(selects[1])
            years = [o.get_attribute("value") for o in year_select.options]
            for year in years[:3]:
                year_select.select_by_value(year)
                time.sleep(1)
                anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")
                for a in anchors:
                    href = a.get_attribute("href")
                    if href and ("zip" in href.lower() or "download" in href.lower()):
                        links.append({"product": product, "year": year, "href": href})

        result = {"products": products, "aerial_products": vap, "links": links}
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        if not links:
            raise RuntimeError("Aerial product found, but no generated download links captured")
        print("EA survey aerial acquisition probe: PASS")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
