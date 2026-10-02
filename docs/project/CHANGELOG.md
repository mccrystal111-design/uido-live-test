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