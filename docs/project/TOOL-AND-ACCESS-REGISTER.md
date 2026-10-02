# UiDo Tool & Access Register

**Last checked:** 2026-10-02  
**Purpose:** One durable record of the tools, access routes, verified capabilities, limitations and setup gaps used to build and operate UiDo. This register is an operational map, not a store for credentials.

## Rules for every session

1. Start at [the project control pack](README.md) and read the Project Brief, Current State, Action Register, Dependencies, Decision Log, and this register.
2. Verify access and current state in the actual tool before relying on a note here. A connected integration does not guarantee access to every project or operation.
3. Distinguish **verified in this session**, **available but not verified for this task**, and **not exposed in this session**.
4. Record changes to tools, access routes, permissions, and working procedures here when they are discovered. Add a checked date and evidence, not assumptions.
5. Never put passwords, access tokens, private keys, recovery codes, or other secrets in this document. Store secrets only in the appropriate secret manager/settings.
6. Do not ask Kieron to repeat details already recorded and still verified. Ask only when an owner-only permission or product decision is genuinely required.
7. Do not claim browser QA, tests, deployment, or access verification unless the relevant result was observed.

## Tool register

| Tool / service | UiDo purpose | Access route | Status at last check | Notes / limits |
|---|---|---|---|---|
| GitHub repository | Source code, project records, issues, PRs, commits | [mccrystal111-design/uido-live-test](https://github.com/mccrystal111-design/uido-live-test); connected GitHub tools in this ChatGPT environment | **Verified in session** — repository files read and commits made through the connector | Prefer the connector for repository-native work. Check the current branch/default branch and file SHA before editing. Do not infer that a commit's workflows passed without checking runs/statuses. |
| GitHub Actions | Build, course acquisition, QA and deployment workflows | Repository `Actions` tab; connected GitHub tools for runs, jobs, steps, logs and artifacts | **Available; per-run verification required** | Let configured triggers run normally. Use manual dispatch/reruns only when there is a clear reason. Avoid duplicate runs. Record workflow name, run URL/ID, triggering commit, status and relevant log evidence. A green run proves only that run passed. |
| GitHub Pages | Publish dashboard and static UiDo pages | [Live project dashboard](https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html); source workflow [deploy-pages.yml](../../.github/workflows/deploy-pages.yml) | **Verified** — deployment run #36982434145 succeeded and Playwright run #36982461137 verified the published dashboard at mobile and desktop sizes | Dashboard is read-only and queries public GitHub issues, open PRs and recent workflow runs. Its source must be copied into the Pages output by the deploy workflow. Playwright verified the deployed URL at mobile and desktop widths; see run #36982461137. |
| Figma | Design source, UI references, editable frames and visual review | [UiDo Figma file](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI); connected Figma tools | **Connector verified in session** — identity/workspace query succeeded; design tools are exposed | The file and its editable Dashboard page are known project assets. Check file/node permissions for each edit/export. The connector identity response is not proof that every operation is permitted. Figma design is not a live GitHub data connection. |
| Supabase | Potential data storage, database, storage, edge functions and backend services | Connected Supabase tools; project URL/ID must be discovered from the authenticated project list before acting | **Connector responds; no projects were returned on 2026-10-02** | Do not assume a UiDo project exists or create one automatically. Verify account/org and project visibility with Kieron if a project is expected. Decide schema, access control, retention, offline and sync requirements before choosing what belongs in Supabase. Never log keys or credentials. |
| Playwright + Chromium | Repeatable browser QA: page rendering, console/network errors, responsive screenshots and SVG diagnostics | GitHub Actions workflows [visual-qa-agnostic45.yml](../../.github/workflows/visual-qa-agnostic45.yml) for AG45 and [project-dashboard-browser-qa.yml](../../.github/workflows/project-dashboard-browser-qa.yml) for the published dashboard, using the official Playwright Python container and Chromium; job artifacts are linked from each run. | **Verified via GitHub Actions** — AGNOSTIC45 Visual QA run [#36925474787](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36925474787) completed successfully on source commit `fc51a6d624bf00e2c290bce7cc40f004e2d76bd6`. A dashboard-specific live-page QA workflow was added in commit `9bc63015d319a79b0dc7f946137081d54cde5415`; its first run [#36982461137](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137) passed on 2026-10-02. It verified HTTP 200, title/heading, live counts, no refresh failure, no console/page errors, no failed HTTP responses and no horizontal overflow at 390×844 and 1440×900. Artifact: [screenshots/report](https://github.com/mccrystal111-design/uido-live-test/actions/runs/36982461137/artifacts/11216560509). | This is a repository-hosted Playwright route, not a direct browser-control tool in the current ChatGPT session. The AG45 harness tests AG45-specific selectors/geometry; the dashboard has its own browser workflow. The dashboard run uploaded screenshots and a report in artifact `project-dashboard-browser-qa`, expiring 2026-10-23. |
| ChatGPT connected tools | Orchestrate GitHub, Figma and Supabase operations from a session | Tools listed in the active session's available integrations | **Verified for GitHub, Figma and Supabase at the level stated above** | Tool availability can differ between sessions and modes. At session start, inspect available tools rather than assuming every prior integration is still present. |
| Web search | Public documentation, external references and fresh public information | ChatGPT web search | **Available in this session** | Useful for public docs and external facts; not a replacement for GitHub connector access to repository-native operations. Cite sources for claims that depend on web research. |
| Files / project library | Search and read prior project documents or uploaded references | ChatGPT Files tools via the active session | **Tool family exposed; task-specific availability must be checked** | Search the Library when the user refers to an earlier file not attached in the current chat. A file card/title does not prove a local path. Never invent download paths. |
| Course-data sources | Course discovery, course geometry, registration/refinement and provenance | Source-specific code/configuration and workflows in the repository; inspect current implementation before use | **Source-specific verification required** | Historical sources include OSM/Overpass, Nominatim and GolfCourseAPI. Do not assume availability, terms, quotas or current behaviour. Record the exact source, request/result and geometry provenance for each acquisition task. |
| GitHub Projects | Native project board and saved views | Repository/owner's GitHub Projects UI or an integration explicitly supporting project creation/configuration | **Not configured as of 2026-10-02** | OPS-003 tracks this. Existing dashboard and Figma dashboard are not a substitute for a native GitHub Project. |

## Standard procedures

### Repository changes
1. Read the relevant source and project record from the current default branch.
2. Confirm the intended file, current blob SHA, and acceptance criteria.
3. Make a focused change with an informative commit message.
4. Inspect the resulting commit and the workflows triggered by it.
5. Read relevant run/job/log/artifact evidence. Do not treat commit creation as test success.
6. Update Current State, Action Register, Changelog and Session Handover when the change affects project status or next actions.

### GitHub Actions
1. Find the workflow that actually owns the task; inspect its triggers and dependencies.
2. Prefer the normal configured trigger when it is appropriate.
3. Use manual dispatch or rerun only when needed to validate a specific commit, recover a failure, or perform an explicitly requested operation.
4. Record the run URL/ID, commit SHA, trigger, conclusion and any material errors.
5. Keep development, deployment and QA effects isolated from live golfer-facing side effects.

### Browser QA with Playwright/Chromium
1. Confirm Playwright package/runtime and compatible Chromium binary are installed or connect to a verified Playwright browser service.
2. Navigate to the exact deployed URL; wait for page readiness.
3. Capture page title, final URL, key visible content and screenshot.
4. Collect page errors, console errors and failed network requests.
5. Test the key interactions and relevant viewport sizes.
6. Save a concise evidence report and link any artifacts. If no Playwright runtime is available, report the limitation and use a clearly labelled alternative; do not call it Playwright testing. The repository-hosted dashboard workflow checks the deployed page at mobile and desktop widths, live GitHub data loading, console/page errors and horizontal overflow.

### Figma
1. Open the canonical UiDo file and locate the relevant page/node.
2. Inspect design context/screenshot before editing.
3. Preserve approved product/brand constraints and clearly separate proposed work from approved design.
4. After an edit, inspect the resulting frame/node and report what was actually verified.

### Supabase
1. List accessible organisations/projects and confirm the intended project ID and URL.
2. Review current schema, migrations, access policies and relevant functions before modifying anything.
3. Define data classification, user access, retention, backup, offline/sync and migration needs.
4. Make the smallest justified change; verify with schema/query/advisor evidence as appropriate.
5. Never place service-role keys or other secrets in code, issues, commits or this register.

## Session verification log

| Date | Check | Result |
|---|---|---|
| 2026-10-02 | GitHub repository access | Project control files fetched and repository documentation commits made through connected GitHub tools. |
| 2026-10-02 | Figma connector | Identity/workspace query succeeded; project Figma URL is recorded above. Per-operation edit access still requires checking. |
| 2026-10-02 | Supabase connector | Project-list call returned an empty project list. No UiDo Supabase project was verified as accessible. |
| 2026-10-02 | Playwright/Chromium | AG45 QA #36925474787 passed. Dashboard QA #36982461137 passed at 390×844 and 1440×900; live data loaded with no browser errors, failed responses or horizontal overflow. Artifacts linked above. |
| 2026-10-02 | GitHub Pages dashboard | Deployment #36982434145 succeeded; Playwright QA #36982461137 confirmed HTTP 200, expected page content, live data and no browser errors or horizontal overflow. |

## Maintenance

Update this register when a tool is added/removed, an access route changes, a permission issue is resolved, or a procedure changes. Keep Current State focused on the current project baseline and use this file for reusable operational knowledge.
