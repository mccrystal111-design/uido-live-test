#!/usr/bin/env python3
"""Browser contract test for Kite round/shot writes using a mocked Supabase client.

No real credentials, network API calls or database writes are used.
"""
from __future__ import annotations

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
USER_ID = "00000000-0000-4000-8000-000000000004"
COURSE_ID = "00000000-0000-4000-8000-000000000001"
VERSION_ID = "00000000-0000-4000-8000-000000000002"
TEE_ID = "00000000-0000-4000-8000-000000000003"
ROUND_ID = "00000000-0000-4000-8000-000000000005"
HOLE_ROW_ID = "00000000-0000-4000-8000-000000000006"

MOCK_SUPABASE = r"""
(() => {
  const state = window.__coreMock = {
    user: { id: "00000000-0000-4000-8000-000000000004", email: "qa@example.test" },
    calls: [],
    versionAvailable: true,
    courseAvailable: true,
    teeSetAvailable: true
  };
  const COURSE_ID = "00000000-0000-4000-8000-000000000001";
  const VERSION_ID = "00000000-0000-4000-8000-000000000002";
  const TEE_ID = "00000000-0000-4000-8000-000000000003";

  function query(table) {
    let operation = "select";
    let payload = null;
    const filters = [];
    const q = {
      select() { return q; },
      eq(column, value) { filters.push({ column, value }); return q; },
      maybeSingle() {
        state.calls.push({ table, operation, filters: [...filters] });
        if (table === "uido_profiles") {
          return Promise.resolve({ data: { id: state.user.id, display_name: "QA Player" }, error: null });
        }
        if (table === "course_versions") {
          return Promise.resolve({
            data: state.versionAvailable ? { id: VERSION_ID, course_id: COURSE_ID, status: "published" } : null,
            error: null
          });
        }
        if (table === "courses") {
          return Promise.resolve({
            data: state.courseAvailable ? { id: COURSE_ID, status: "active" } : null,
            error: null
          });
        }
        if (table === "tee_sets") {
          return Promise.resolve({
            data: state.teeSetAvailable ? { id: TEE_ID, course_version_id: VERSION_ID } : null,
            error: null
          });
        }
        return Promise.resolve({ data: null, error: null });
      },
      insert(value) {
        operation = "insert";
        payload = value;
        state.calls.push({ table, operation, payload: value });
        return q;
      },
      update(value) {
        operation = "update";
        payload = value;
        state.calls.push({ table, operation, payload: value });
        return q;
      },
      single() {
        const id = table === "uido_rounds" ? "00000000-0000-4000-8000-000000000005"
          : table === "uido_round_holes" ? "00000000-0000-4000-8000-000000000006"
          : "00000000-0000-4000-8000-000000000007";
        return Promise.resolve({ data: { id, ...(payload || {}) }, error: null });
      },
      then(resolve, reject) {
        return Promise.resolve({ data: null, error: null }).then(resolve, reject);
      }
    };
    return q;
  }

  const auth = {
    onAuthStateChange() { return { data: { subscription: { unsubscribe() {} } } }; },
    async getSession() { return { data: { session: { user: state.user } }, error: null }; },
    async signOut() { return { error: null }; },
    async signUp() { return { data: { user: state.user, session: null }, error: null }; },
    async signInWithPassword() { return { data: { user: state.user, session: { user: state.user } }, error: null }; }
  };
  window.supabase = { createClient() { return { auth, from: query }; } };
})();
"""


def main() -> None:
    errors = []
    dialogs = []
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/hawk.html"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("dialog", lambda dialog: (dialogs.append(dialog.message), dialog.accept()))
            page.route(
                "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2",
                lambda route: route.fulfill(status=200, content_type="application/javascript", body=MOCK_SUPABASE),
            )
            page.goto(url, wait_until="load")
            page.wait_for_function(
                "document.getElementById('hawkApp') && !document.getElementById('hawkApp').hidden"
            )

            # A slug/blank value must fail locally; no round insert may be attempted.
            page.locator("#startRoundButton").click()
            page.locator("#roundCourseId").fill("overstone-park")
            page.locator("#roundVersionId").fill("")
            page.locator("#startRound").click()
            assert dialogs and "valid UUIDs" in dialogs[-1], f"Unexpected invalid-ID feedback: {dialogs}"
            calls = page.evaluate("window.__coreMock.calls")
            assert not any(c["table"] == "uido_rounds" and c["operation"] == "insert" for c in calls), (
                "Invalid course IDs reached the round insert"
            )

            # A well-formed UUID is still rejected if the version is not published.
            page.evaluate("window.__coreMock.versionAvailable = false")
            page.locator("#roundCourseId").fill(COURSE_ID)
            page.locator("#roundVersionId").fill(VERSION_ID)
            page.locator("#startRound").click()
            assert "not published" in dialogs[-1], f"Unexpected unpublished-version feedback: {dialogs[-1]}"
            calls = page.evaluate("window.__coreMock.calls")
            assert not any(c["table"] == "uido_rounds" and c["operation"] == "insert" for c in calls), (
                "Unpublished course version reached the round insert"
            )

            # A tee set from another/unavailable version is rejected.
            page.evaluate("window.__coreMock.versionAvailable = true; window.__coreMock.teeSetAvailable = false")
            page.locator("#roundTeeId").fill(TEE_ID)
            page.locator("#startRound").click()
            assert "does not belong" in dialogs[-1], f"Unexpected tee-set feedback: {dialogs[-1]}"
            calls = page.evaluate("window.__coreMock.calls")
            assert not any(c["table"] == "uido_rounds" and c["operation"] == "insert" for c in calls), (
                "Invalid tee set reached the round insert"
            )

            # Published context inserts a permanent round with non-null course/version IDs.
            page.evaluate("window.__coreMock.teeSetAvailable = true")
            page.locator("#roundTeeId").fill("")
            page.locator("#roundCourseName").fill("QA Course")
            page.locator("#startRound").click()
            page.wait_for_function(
                "window.__coreMock.calls.some(c => c.table === 'uido_rounds' && c.operation === 'insert')"
            )
            round_call = page.evaluate(
                "window.__coreMock.calls.find(c => c.table === 'uido_rounds' && c.operation === 'insert')"
            )
            payload = round_call["payload"]
            assert payload["user_id"] == USER_ID
            assert payload["course_id"] == COURSE_ID
            assert payload["course_version_id"] == VERSION_ID
            assert payload["status"] == "started"
            assert payload["device_context"]["app"] == "kite"
            assert payload["tee_set_id"] is None
            assert page.locator("#roundDialog").evaluate("el => !el.open")

            # Score and shot records must attach to the round/hole and preserve Kite source identity.
            page.locator("#plusStroke").click()
            page.wait_for_function(
                "window.__coreMock.calls.some(c => c.table === 'uido_round_holes' && c.operation === 'insert')"
            )
            page.locator("#recordShot").click()
            page.wait_for_function(
                "window.__coreMock.calls.some(c => c.table === 'uido_shots' && c.operation === 'insert')"
            )
            hole_call = page.evaluate(
                "window.__coreMock.calls.find(c => c.table === 'uido_round_holes' && c.operation === 'insert')"
            )
            shot_call = page.evaluate(
                "window.__coreMock.calls.find(c => c.table === 'uido_shots' && c.operation === 'insert')"
            )
            assert hole_call["payload"]["round_id"] == ROUND_ID
            assert hole_call["payload"]["hole_number"] == 1
            shot = shot_call["payload"]
            assert shot["user_id"] == USER_ID
            assert shot["round_id"] == ROUND_ID
            assert shot["round_hole_id"] == HOLE_ROW_ID
            assert shot["shot_number"] == 1
            assert shot["source_provider"] == "kite"
            assert shot["device_context"]["app"] == "kite"
            assert not errors, f"Browser errors: {errors}"

            print(json.dumps({
                "result": "PASS",
                "scenarios": [
                    "invalid course/version UUID rejected before insert",
                    "unpublished course version rejected before insert",
                    "invalid tee set rejected before insert",
                    "published course context creates round with non-null foreign keys",
                    "score and shot records preserve round/hole ownership and Kite source identity",
                ],
                "mocked_round_insert": payload,
                "mocked_shot_insert": shot,
                "page_errors": errors,
            }, indent=2))
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
