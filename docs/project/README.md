# UiDo Project Control Pack

This directory is the durable project-management source of truth. Chat history is supporting context, not the project database.

## Start every session here
0. Read [PROJECT-BRIEF.md](PROJECT-BRIEF.md) for the stable product and working principles; use [NEW-CHAT-STARTER.md](NEW-CHAT-STARTER.md) to onboard a new conversation.
1. Read [TOOL-AND-ACCESS-REGISTER.md](TOOL-AND-ACCESS-REGISTER.md) and verify the tools needed for the current task. Do not assume access from an old session.
2. Open the [live project dashboard](../../project-dashboard.html).
3. Read CURRENT-STATE.md and SESSION-HANDOVER.md.
4. Check ACTION-REGISTER.md for the next unblocked task.
5. Check DEPENDENCIES.md before choosing work.
6. Read DECISION-LOG.md before revisiting established choices.
7. Inspect actual source, commit and workflow evidence before treating any status as verified.
8. At session end, update CHANGELOG.md and SESSION-HANDOVER.md plus current state and action status. Update the tool register when an access route or process changes.

## Dashboard
- [Live dashboard source](../../project-dashboard.html) — reads public GitHub issues, open PRs and recent workflow runs, with manual and five-minute refresh.
- [Intended GitHub Pages URL](https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html) — the workflow copies the file into the published site; verify the rendered page after deployment changes.
- [Figma dashboard design](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI) — editable visual design; it is not itself a live GitHub data connection.
- GitHub's native Projects board and saved views are not yet configured. OPS-003 tracks the remaining work.

When available, create saved views: Today / Next; Status Board; Roadmap; Blocked; Awaiting Kieron / QA.

Suggested fields: Status, Priority, Workstream, Owner, Blocked by, Start date, Target date, Milestone, Acceptance criteria, Evidence/PR. Dates remain estimates until agreed.

Status vocabulary: Backlog, Ready, In progress, Blocked, Awaiting Kieron, In QA, Done, Parked, Needs verification.

## Operating constraints
- Let configured GitHub Actions triggers run normally for code changes, tests and deployments. Use manual dispatch/reruns when they serve a clear purpose; do not duplicate an automatic run unnecessarily.
- A green workflow proves only that workflow/run passed, not that the whole product is correct.
- Product triggers map to real golfer actions, relevant real-world events/conditions, or justified support processes.
- Keep development, deployment and QA triggers isolated from live-user side effects.
- No task is Done without acceptance criteria and evidence.
