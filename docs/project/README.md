# UiDo Project Control Pack

This directory is the durable project-management source of truth. Chat history is supporting context, not the project database.

## Start every session here
1. Read CURRENT-STATE.md.
2. Check ACTION-REGISTER.md for the next unblocked task.
3. Check DEPENDENCIES.md before choosing work.
4. Read DECISION-LOG.md before revisiting established choices.
5. At session end, update CHANGELOG.md and SESSION-HANDOVER.md plus current state and action status.

## Dashboard
Use GitHub Projects first, linked to repository Issues and PRs. Create saved views: Today / Next; Status Board; Roadmap; Blocked; Awaiting Kieron / QA.

Suggested fields: Status, Priority, Workstream, Owner, Blocked by, Start date, Target date, Milestone, Acceptance criteria, Evidence/PR. Dates remain estimates until agreed.

Status vocabulary: Backlog, Ready, In progress, Blocked, Awaiting Kieron, In QA, Done, Parked, Needs verification.

## Operating constraints
- Do not automatically run or rerun GitHub Actions. Kieron starts runs manually; then inspect results and update records.
- A green workflow proves only that workflow/run passed, not that the whole product is correct.
- Product triggers map to real golfer actions, relevant real-world events/conditions, or justified support processes.
- Keep development, deployment and QA triggers isolated from live-user side effects.
- No task is Done without acceptance criteria and evidence.
