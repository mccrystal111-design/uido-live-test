#!/usr/bin/env python3
"""Course-agnostic AGNOSTIC45 browser/SVG inspection. Evidence is not approval."""
from __future__ import annotations
import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
OUT = ROOT / "visual-qa" / "phone-bars"
OUT.mkdir(parents=True, exist_ok=True)
target = os.environ["TARGET_HTML"].strip()
holes = [int(x.strip()) for x in os.environ["HOLES"].split(",") if x.strip()]
viewports = []
for value in os.environ["VIEWPORTS"].split(","):
    value = value.strip()
    if not value:
        continue
    match = re.fullmatch(r"(\d{2,4})x(\d{2,4})", value)
    if not match:
        raise SystemExit(f"Invalid viewport: {value}")
    viewports.append((int(match.group(1)), int(match.group(2))))
requested_change = os.environ.get("REQUESTED_CHANGE", "")
source_sha = os.environ.get("SOURCE_SHA", "local")
run_url = os.environ.get("RUN_URL", "")
base_url = "http://127.0.0.1:8765/" + target.lstrip("/")
records = []
fatal_count = 0

with sync_playwright() as p:
    browser = p.chromium.launch()
    for hole in holes:
        for width, height in viewports:
            case = f"hole-{hole}_{width}x{height}"
            page = browser.new_page(
                viewport={"width": width, "height": height},
                device_scale_factor=1,
                is_mobile=width <= 430,
                has_touch=width <= 430,
            )
            console_events, page_errors, failed_responses = [], [], []
            page.on("console", lambda msg: console_events.append(
                {"type": msg.type, "text": msg.text[:1000]}
            ) if msg.type in ("warning", "error") else None)
            page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            page.on("response", lambda response: failed_responses.append(
                {"status": response.status, "url": response.url}
            ) if response.status >= 400 else None)
            url = base_url + "?" + urlencode({"hole": hole})
            record = {
                "case": case, "url": url,
                "viewport": {"width": width, "height": height}, "hole": hole,
                "requested_change": requested_change, "source_sha": source_sha,
                "run_url": run_url, "checks": {},
                "console_warnings_errors": console_events,
                "page_errors": page_errors, "http_failures": failed_responses,
            }
            try:
                response = page.goto(url, wait_until="networkidle", timeout=45000)
                page.wait_for_timeout(700)
                record["http_status"] = response.status if response else None
                record["page_title"] = page.title()
                record["document"] = page.evaluate("""() => ({
                  readyState: document.readyState,
                  documentWidth: document.documentElement.scrollWidth,
                  documentHeight: document.documentElement.scrollHeight,
                  innerWidth: window.innerWidth, innerHeight: window.innerHeight,
                  bodyWidth: document.body ? document.body.scrollWidth : null,
                  bodyHeight: document.body ? document.body.scrollHeight : null,
                  background: document.body ? getComputedStyle(document.body).backgroundColor : null
                })""")
                record["svg"] = page.evaluate("""() => [...document.querySelectorAll('svg')].map((svg, index) => {
                  const r = svg.getBoundingClientRect();
                  const geometryRoot = svg.querySelector('#renderedGeometry') ||
                    svg.querySelector('[data-geometry-root]') || svg;
                  const shapes = [...geometryRoot.querySelectorAll('path, polygon, polyline, rect, circle, ellipse, line, use')];
                  const counts = {};
                  for (const el of shapes) {
                    const cls = (el.getAttribute('class') || '').trim().replace(/\\s+/g, '.');
                    const key = el.tagName.toLowerCase() + (cls ? '.' + cls : '');
                    counts[key] = (counts[key] || 0) + 1;
                  }
                  return {
                    index, id: svg.id || null, viewBox: svg.getAttribute('viewBox'),
                    preserveAspectRatio: svg.getAttribute('preserveAspectRatio'),
                    rect: {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom},
                    renderedGeometryId: geometryRoot.id || null, shapeCount: shapes.length,
                    shapeCountsByTagAndClass: counts,
                    clipPaths: [...svg.querySelectorAll('clipPath')].map(c => ({
                      id: c.id || null, units: c.getAttribute('clipPathUnits'), childCount: c.children.length
                    })),
                    emptyGeometryRoot: geometryRoot.children.length === 0
                  };
                })""")
                record["layout_elements"] = page.evaluate("""() => {
                  const selectors = ['#stage','#screen','#topBar','#top-bar','#bottomBar','#bottom-bar',
                    '#rightRail','#right-rail','#courseViewport','#course-viewport','.top-bar','.bottom-bar','.right-rail'];
                  const out = {};
                  for (const selector of selectors) {
                    const el = document.querySelector(selector);
                    if (!el) continue;
                    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
                    out[selector] = {rect:{x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom},
                      display:cs.display, position:cs.position, overflow:cs.overflow};
                  }
                  return out;
                }""")
                doc, svgs, checks = record["document"], record["svg"], record["checks"]
                checks["page_http_ok"] = bool(record["http_status"] and 200 <= record["http_status"] < 400)
                checks["no_document_overflow"] = doc["documentWidth"] <= width + 1 and doc["documentHeight"] <= height + 1
                checks["svg_present"] = len(svgs) > 0
                checks["svg_has_positive_render_size"] = any(s["rect"]["width"] > 0 and s["rect"]["height"] > 0 for s in svgs)
                checks["svg_geometry_present"] = any(s["shapeCount"] > 0 for s in svgs)
                checks["no_uncaught_page_errors"] = len(page_errors) == 0
                checks["no_http_failures"] = len(failed_responses) == 0
                roots = [s for s in svgs if s["renderedGeometryId"] == "renderedGeometry"]
                checks["rendered_geometry_root_nonempty"] = (
                    any(not s["emptyGeometryRoot"] for s in roots) if roots else None
                )
                shot = OUT / f"{case}.png"
                page.screenshot(path=str(shot), full_page=True, animations="disabled")
                record["screenshot"] = str(shot.relative_to(ROOT))
            except Exception as exc:
                record["fatal_error"] = repr(exc)
                fatal_count += 1
                try:
                    page.screenshot(path=str(OUT / f"{case}_failure.png"), full_page=True)
                except Exception:
                    pass
            finally:
                page.close()
            records.append(record)
            print(f"[{'ERROR' if record.get('fatal_error') else 'CAPTURED'}] {case}: "
                  f"status={record.get('http_status')} svg={len(record.get('svg', []))} "
                  f"errors={len(record.get('page_errors', []))}")
    browser.close()

summary = {
    "schema":"uido.ag45.visual-qa.v1",
    "created_at_utc":datetime.now(timezone.utc).isoformat(),
    "repository":os.environ.get("GITHUB_REPOSITORY",""),
    "source_sha":source_sha, "run_url":run_url, "candidate_html":target,
    "requested_change":requested_change, "holes":holes,
    "viewports":[{"width":w,"height":h} for w,h in viewports],
    "important_note":"Automated browser/SVG checks are evidence, not visual approval. Inspect every screenshot and compare SVG geometry with the requested change.",
    "case_count":len(records), "fatal_case_count":fatal_count, "cases":records,
}
(OUT / "diagnostics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
(OUT / "review-checklist.md").write_text(
    "# Human visual review checklist\n\n"
    f"- Requested change: {requested_change or '(not supplied)'}\n"
    f"- Candidate: {target}\n- Source commit: {source_sha}\n\n"
    "Review every PNG and diagnostics.json. Confirm the requested change is present; the approved camera/projection and course geometry have not shifted unexpectedly; SVG viewBox, clipping, rendered shape counts and bounds make sense; there is no unintended cropping, stretching, overflow, blank render, missing asset, console error or uncaught exception; and phone/desktop layouts remain usable.\n\n"
    "Automated checks are not visual approval. Record PASS / REVIEW / FAIL after comparing evidence with the requested change. This workflow never deploys, promotes, or overwrites the approved base.\n",
    encoding="utf-8",
)
failed = []
for record in records:
    for name, value in record.get("checks", {}).items():
        if value is False:
            failed.append(f"{record['case']}: {name}")
if failed:
    print("Automated checks requiring review/fix:")
    for item in failed:
        print(" - " + item)
    sys.exit(1)
if fatal_count:
    sys.exit(1)
print(f"Evidence captured for {len(records)} case(s) at {OUT}")
