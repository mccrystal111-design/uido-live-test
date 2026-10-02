# UiDo Project Control Change Log

## 2026-10-02 — Live dashboard foundation
- Added `project-dashboard.html`, a responsive, read-only dashboard that fetches public repository issues, open pull requests and recent workflow runs directly from the GitHub REST API.
- Dashboard refreshes on demand and every five minutes. It does not trigger or rerun workflows.
- Added the dashboard link to the repository README.
- Added an editable **02 — Project Dashboard** page in the existing Figma file, including a composed, editable dashboard frame.
- Created GitHub issues for OPS-002, OPS-003, DES-001 and RND-001.
- Reconciled the action register and handover to point to the live issue records.
- Commits: dashboard `62f1cba683f15895916753d97f76d52d46b72446`; README/docs updates recorded in subsequent commits.
- Not done: dashboard publication/access verification; native GitHub Projects board and saved views; source/commit/workflow reconciliation; original concept PNG placement; latest AGNOSTIC45 workflow verification.

## 2026-10-02 — Initial control pack
- Added repository entry point and project-control links.
- Added current-state snapshot, action register, dependency map, RACI, decision log and session handover.
- Recorded manual GitHub Actions rule and Real-Golfer Trigger Principle.
- Evidence: this commit contains these control documents.
- Not done at that point: repository reconciliation; GitHub Issues/Project views; concept PNG placement in Figma; current AGNOSTIC45 workflow verification.

## 2026-10-02 — Tool register and browser verification
- Added `docs/project/TOOL-AND-ACCESS-REGISTER.md` and made it mandatory in the project control entry point and new-chat starter.
- Recorded actual access routes and limits: GitHub and Figma integrations respond; no Supabase project was visible to the connected project-list call; Playwright/Chromium is available through repository-hosted GitHub Actions rather than a direct browser-control tool in the chat session.
- Added `.github/workflows/project-dashboard-browser-qa.yml` to test the published dashboard using Playwright/Chromium at mobile and desktop sizes, check live GitHub data, capture browser errors and detect horizontal overflow.
- Dashboard QA passed: [run #36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137), artifact [screenshots/report](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137/artifacts/11216560509). Dashboard rendered at 390×844 and 1440×900 with live data, no console/page errors, failed HTTP responses or horizontal overflow.
- Updated dashboard copy to reflect normal configured workflow triggers rather than instructing the user to run Actions manually.
- AGNOSTIC45 QA evidence recorded: [run #36925474787](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36925474787) passed for the phone-bars review candidate, but the standalone base renderer still needs its own QA and the geometry contract remains outstanding.
- Remaining issue: several legacy workflow records fail on push events with zero jobs. Cause not established; no reruns were started. OPS-002 remains open to diagnose these records and finish reconciling recent PRs.


## 2026-10-02 — AGNOSTIC45 standalone base QA
- Added `.github/workflows/agnostic45-base-qa.yml` to run Playwright/Chromium geometry checks on the standalone base when its source or the QA workflow changes.
- [Run #36982883414](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982883414) passed six cases: holes 1 and 9 at 390×844, 768×1024 and 1440×900.
- Checks confirmed HTTP 200, expected hole-specific title, SVG and rendered geometry root, physical feature paths, routing path, positive SVG size, no horizontal overflow, no uncaught page errors, no console errors and no failed HTTP responses.
- [Screenshots and diagnostics artifact](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982883414/artifacts/11216462231). This is automated structural evidence, not human visual approval or approval of the canonical geometry contract.


## 2026-10-02 — OPS-002 zero-job failure investigation checkpoint
- Rechecked workflow jobs for runs [#36982036792](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982036792) and [#36982882178](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982882178); both returned an empty jobs array.
- Confirmed dashboard QA run [#36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137) has a completed successful browser-QA job, and standalone AGNOSTIC45 base QA run [#36982883414](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982883414) has a completed successful Chromium job.
- The connected GitHub tools exposed in this session do not provide workflow-run metadata/listing, and public web opening of the two zero-job run pages was unavailable. Therefore workflow name, event details, conclusion explanation and check-suite annotations could not be inspected. Root cause remains unresolved; no reruns were initiated.
- Next: inspect the two run detail pages in GitHub Actions and record workflow/event/conclusion/check-suite evidence before deciding whether the records need a workflow fix or can be dispositioned as non-job runs.
