# UiDo — New Chat Starter

Use this file as the orientation point for new UiDo chats. Prefer the repository source of truth over conversational memory.

## Product brand — 2026-10-06

**Kite is now the single base product brand.** The previous separate Kite/Hawk brand concept is superseded.

Kite is one golf app for adult and junior players, with multiple player profiles within the same family/account. A parent should be able to switch between players and track a child's shots/rounds easily; the child can also use the same app independently.

Kite is deliberately not golf-specific or explicitly child-branded. The brand can support a wider visual/product language around:
- aerial perspective / looking down from a kite, naturally connecting to GPS and course mapping;
- movement and direction;
- play, freedom and curiosity;
- the kite's tether as a metaphor for parent/child connection and shared activity.

**Product principle:** do not create a separate "kids mode" as a separate product identity. Players are first-class objects and the UI adapts to the active player.

Conceptual product relationship:
**Family/account -> Players -> Rounds -> Shots**

The canonical course database remains independent of the brand/UI and is consumed by Kite. Course data, player identity, round/session data and presentation remain separate building blocks.

Do not reintroduce Hawk as a separate customer-facing brand unless a later decision explicitly reverses DEC-014 in the Decision Log.

## UiDo Core User Database — current baseline

UiDo Core is the complete customer/data model. Kite is the current customer-facing product brand. The legacy `hawk.html` file is a prototype harness for Core persistence work, not a separate customer-facing brand.

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
- One permanent UiDo identity follows the customer across Kite experiences and future product surfaces.
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
- docs/project/KITE-UI-QA-MEMORY.md — cumulative Kite UI Q&A decisions (Stats, saved rounds, end-of-round flow).
- database/schema/uido-core-user-data-v1.sql

Do not re-ask settled Core decisions. If a database question depends on an existing UiDo product/UI/statistics decision, retrieve the project source of truth first.

## Caddie recommendation loop — 2026-10-10

**Decision: DEC-017 — recommendation → commitment → pre-round handshake → on-course execution → measured result → improved recommendation.**

UiDo should turn relevant performance patterns into actionable experiments, not just display statistics. A player can accept and lock a recommendation for their next round. At the pre-round handshake, briefly ask when they last played and whether they have practised since, then remind them of the active experiment. Avoid repeating known, current answers; let the golfer skip or change the experiment. During play, the caddie reminds them when a relevant situation occurs and explains the reason (for example, testing one club more at suitable approach distances when short misses are frequent). Capture the shot context and outcome, then compare comparable shots after the round to decide whether to retain, revise or discard the experiment.

Guardrails:
- Make metric scope, club/distance sample and sample size clear.
- Do not infer that a club change is warranted from an overall miss percentage alone.
- Compare like-for-like conditions where possible; account for lie, distance, wind/elevation and other material context.
- Treat a small sample as provisional, not proof.
- The player owns the experiment; prompts should be relevant and unobtrusive.


## Club distance stats and shot variants — DEC-018 (2026-10-10)

For every club in the player's bag, the later club-stats view should show:
- **Shortest recorded distance**
- **Longest recorded distance**
- **Average recorded distance**

These values must be editable by the player, including later corrections or manual entry. Keep edits auditable/separate from the raw shot history; do not silently rewrite recorded shots when a reference value is edited. Make clear whether values represent observed shot data or player-edited club reference values.

Shot capture must also support **partial/controlled wedge shots** and **punch shots** as identifiable shot types or variants. They should be filterable/analysable separately from full-swing shots so they do not distort a club's normal-distance picture. Preserve relevant context when available and allow later correction of recorded stats; unknown values remain blank rather than being represented as zero or a dash.

## Q&A Discovery Mode

When Kieron explicitly starts a Q&A:
- Ask exactly one genuine unresolved question at a time.
- Do not re-ask settled decisions.
- For voice, keep questions concise.
- Record confirmed decisions in the appropriate Q&A source-of-truth file.
- When the Q&A is complete, persist the final decisions to the project docs.

## Mandatory visual QA rule

**Every visual change must be pixel checked in the actual system where it will be used before it is presented as approved.**

- **Figma:** render the changed frame/component at the intended viewport/scale and inspect the actual rendered pixels, not just the layer tree, coordinates or properties.
- **Browser HTML:** render the actual page in the target browser/viewport and inspect the screenshot/pixels.
- If a visual change exists in both Figma and HTML, **both must be checked**.
- A structural check, green automation run, successful build, or matching coordinates is **not** visual approval.
- Do not say a change is “pixel checked”, “visually checked”, “QA green” or equivalent unless the rendered result has actually been inspected.
- If the rendered result is wrong, correct it and render/check again before presenting it.
- Treat this as a mandatory gate for every visual change, including small icons, colours, spacing, z-order/layering, typography, overlays and controls.
- Preserve the approved Figma source of truth; do not use an HTML screenshot as a substitute for the Figma design check.

## Visual QA shorthand

**QA: Figma + browser pixel-check.**

Use this as the standing shorthand for the mandatory visual QA rule: render and inspect the actual pixels in Figma, and in the browser/HTML system when one exists. Never claim a visual check without actually inspecting the rendered result.

## Visual-development rule

For visually precise UI work:

Figma/design source -> implementation -> actual rendered page -> screenshot at target viewport -> inspect screenshot -> correct -> render again -> inspect again -> only then present the live link.

Do not claim visual QA is green without inspecting actual rendered pixels. Preserve approved Figma decisions and do not invent requirements from experimental playgrounds.

## Product-to-APK development path - 2026-10-06

The intended long-term product is an Android APK. The agreed development path is to **design in Figma first, build/test the UI in HTML, then package the same application into Android when ready**, rather than building a throwaway website and rebuilding the product natively.

This is an additive architecture decision:
- Figma is the visual source of truth.
- HTML is the initial development/testing/rendering layer.
- The application/data/decision logic should be structured so it can be reused when packaged for Android.
- Separate HTML screens/pages are preferred for patch safety and version control, with shared application logic/styles where appropriate rather than duplicated standalone applications.
- The existing approved Yardage page remains a protected/proven starting point; do not rebuild it merely to establish the architecture.
- Future Android-specific capabilities (for example deeper sensors, background GPS, Bluetooth/ANT+, Garmin/launch-monitor integrations, native permissions or lifecycle behavior) may require an Android bridge/plugin layer. Do not assume every browser capability will transfer unchanged.
- Candidate Android packaging approach is a web-to-Android bridge such as Capacitor; this is an implementation direction, not a final locked technology decision.
- The intended workflow is: **Figma -> approved visual -> HTML implementation -> rendered screenshot/pixel check -> refine -> approved screen -> Android packaging/integration**.
- Do not build the front page directly in HTML before its Figma design has been agreed.
- Do not delete, replace or reinterpret the approved Yardage work in order to follow this architecture.

The goal is to avoid a rebuild while still allowing fast visual iteration and real-device testing before APK packaging.

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

## Kite front screen — 2026-10-06

The Kite front/home screen is now moving from the orange concept into the approved **navy + white** brand colourway.

### Brand treatment
- Primary identity: deep navy background with white logo/icon treatment.
- Approved logo direction: the thin white hex golf icon based on the exact Google strategy SVG path, paired with the Sora ExtraLight lowercase `kite` wordmark with the i-dot removed.
- The hex icon sits immediately to the left of `kite`, with its visible height matched to the lowercase `k`.
- Orange remains a possible secondary/accent colour; it is not the default front-screen background.

### Front-screen content
Remove the temporary positioning tags/descriptors from the orange concept:
- `GOLF GPS`
- `PLAY WITH CLARITY`
- `EST. 2026`

These are deliberately omitted so the brand does not become dated or unnecessarily restrictive.

The front-screen actions are exactly:
- **Start Round** — primary action
- **Scores** — scoring/history
- **Stats** — player performance

### Golf-course graphic
The orange concept's golf-course image is visual reference only. Rebuild the front screen in Figma as editable layers rather than placing the supplied screenshot as a flattened UI. Explore a striking **navy/white golf-course treatment**; the course graphic is a major visual element of the screen and should be treated as designed artwork, not just a recoloured photograph.

Do not begin HTML implementation of the front page until the Figma design is agreed.
