# UiDo — New Chat Starter

Use this file as the orientation point for new UiDo chats. Prefer the repository source of truth over conversational memory.

## UiDo Core User Database — current baseline

UiDo Core is the complete customer/data model. Hawk is a simplified product variant of Core, not a separate customer identity/database.

The live Core customer-data foundation is now in Supabase:

- uido_profiles — permanent Auth-linked customer identity/profile, home course and lifecycle/retention state.
- uido_user_preferences — mutable customer preferences/settings.
- uido_handicap_records — historical handicap records for UiDo Practice Handicap and future WHS/GHIN/other providers.
- uido_equipment — equipment history.
- uido_clubs — club inventory and carry-distance history.
- uido_rounds — permanent Round IDs, course + course-version linkage, tee selection, round/session type, timestamps, start GPS, course-selection method and device context.
- uido_round_holes — hole-by-hole scores/putts.
- uido_shots — available UiDo shot flow: GPS, club, lie, wind, trajectory, shape, outcome, Free Aim/decision data, source data and UiDo interpretation.
- uido_external_records — provider-neutral external records for future Garmin, TrackMan, WHS, GHIN and other integrations, retaining original payloads separately from UiDo interpretation.

Core principles already agreed:
- One permanent UiDo identity follows the customer through Hawk to UiDo.
- Core should capture as much useful player data as reasonably available; products decide what to display.
- Historical data should be retained rather than overwritten when relevant.
- Practice sessions are first-class records and may include partial-hole or repeated-position practice.
- Each round has a permanent Round ID and retains the course version used.
- Tee selection and relevant rating/slope context belong to the round.
- Device context is useful for product improvement and future device integrations.
- Preferences are separate from historical player activity; defaults do not dictate actual round choices.
- Equipment and club/carry history should be retained.
- External source records should preserve source identity and original payload; UiDo interpretation is separate.
- Approximately five-year recoverability after account retirement, followed by anonymization, is the current direction and remains subject to final legal/privacy implementation.
- Entitlement/subscription schema is deferred until the Core model is established.
- Exact Core schema-versioning strategy remains open.

Source-of-truth files:
- docs/project/UIDO-CORE-DATABASE-BASELINE.md
- docs/project/Q&A-UIDO-USER-DATABASE-CORE.md
- database/schema/uido-core-user-data-v1.sql

Do not re-ask settled Core decisions. If a database question depends on an existing UiDo product/UI/statistics decision, retrieve the project source of truth first.

## Q&A Discovery Mode

When Kieron explicitly starts a Q&A:
- Ask exactly one genuine unresolved question at a time.
- Do not re-ask settled decisions.
- For voice, keep questions concise.
- Record confirmed decisions in the appropriate Q&A source-of-truth file.
- When the Q&A is complete, persist the final decisions to the project docs.

## Visual-development rule

For visually precise UI work:

Figma/design source -> implementation -> actual rendered page -> screenshot at target viewport -> inspect screenshot -> correct -> render again -> inspect again -> only then present the live link.

Do not claim visual QA is green without inspecting actual rendered pixels. Preserve approved Figma decisions and do not invent requirements from experimental playgrounds.

## Mandatory first-session checklist

1. Read PROJECT-BRIEF, TOOL-AND-ACCESS-REGISTER, CURRENT-STATE, ACTION-REGISTER, DEPENDENCIES, DECISION-LOG and latest SESSION-HANDOVER.
2. For Core/database work, read the Core database baseline and Q&A log first.
3. Verify actual tool/access availability; docs are not proof of current access.
4. Inspect relevant current code, recent commits, open PRs and workflow runs.
5. State the verified baseline and highest-priority unblocked action.
6. Continue existing implementation; do not rebuild proven work without evidence.
7. Do not manually rerun/dispatch GitHub Actions unless needed. Normal triggers may run.
8. Do not ask Kieron to repeat information that is documented and still verified.
9. Update relevant project records at meaningful checkpoints.

## Voice handoff — “Crack on”

When Kieron says “crack on”, that is the explicit handoff from conversation to execution.

- Stop conversationally responding and begin the agreed work.
- Do not ask another question unless genuinely blocked by missing information/access.
- Use available tools and continue until a meaningful checkpoint or genuine blocker.
- If Kieron says “stop”, stop the current line of work immediately.

## Visual error capture

Read docs/project/chat.md before visually precise work. Never mix Figma absolute coordinates with CSS child-relative coordinates. Green automation is not equivalent to visual approval.

Now inspect the current source of truth and continue with the highest-priority unblocked action.