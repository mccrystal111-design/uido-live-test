# UiDo Current State

## Project
UiDo — golf live-test decision/data-capture prototype.

## Canonical design specification
The authoritative screen and behaviour specification is:
`/UiDo/UiDo_Live_Test_Agreed_Round_Flow.docx`

Use that document as the design source of truth. Do not reconstruct the flow from memory.

## Canonical live-test flow
FRONT → NEW ROUND → COURSE → TEE → START ROUND → HOLE VIEW → CHECK WIND → WIND → LIE → START LINE → SHAPE → STRIKE → SHOT RECORDED → SAVE & CONTINUE → WIND.

Alternative:
SHOT RECORDED → FINISH HOLE → SCORE → SAVE & CONTINUE → NEXT HOLE.

Round end:
SCORE → SAVE & FINISH ROUND → FINAL SCORECARD / REVIEW.

## Screen rules
- Front: UiDo identity / PLAY SMARTER; “Better decisions. Lower scores.”; New Round; Past Rounds / Courses / Settings.
- New Round: small course-selection screen; Overstone Park.
- Tee: select tee for the round; no rating/slope; tee persists.
- Hole View: satellite image background, live GPS, GPS accuracy/status, hole/par, Front/Middle/Back yardages, heading/compass, hole recognition, small manual hole selector. UiDo prepares the next hole in the background and activates it when GPS confidence is sufficient. No strategy.
- Check Wind: deliberate capture event at the ball; capture current position/context and move immediately to Wind.
- Wind: 8 directional sectors + Calm; Into/Helping/Left/Right language; arrows toward centre; Calm/½ club/1 club/2 clubs; no compass labels; Confirm wind; wind persists until changed.
- Lie: Fairway/Tee, Semi rough, Deep rough, Bunker, Bare/Other, Obstructed. UiDo predicts lie from GPS/course geometry; highlight prediction in UiDo yellow when confident; player can accept/override. Store predicted and confirmed lie separately. Tee prediction only inside mapped tee area.
- Start Line: “What direction did the ball start on?” Outcome, not intent. No aim suggestion. No yellow box/border. Tap direction immediately advances to Shot Shape; no Confirm button.
- Shot Shape: Hook, Draw, Straight, Fade, Slice only. No Slight Draw/Slight Fade. Tap immediately advances to Shot Strike.
- Shot Strike: existing club/strike graphic as main interaction. Separate Heavy button underneath, subtly distinct with grassy green rather than UiDo yellow. Tap strike choice immediately advances to Shot Recorded.
- Shot Recorded: simple confirmation only. Save & Continue or Finish Hole. Save & Continue saves shot, resets shot inputs, returns immediately to Wind. Next-shot defaults: Lie Fairway, Start Line Centre, Shape Straight, Strike Center. Wind persists until changed.
- Score: starts at hole par; quick selector 1–10; >10 correctable later. Golf score symbols: double bogey double square, bogey square, par plain number + Par, E, birdie circle, eagle double circle, albatross triple circle. Save & Continue prepares next hole; Save & Finish Round goes to final scorecard/review.
- Final scorecard: near-full-screen hole-by-hole score, par, +/- score, golf symbols, front-nine subtotal, back-nine subtotal, total; scores/holes editable before finalising. Detailed shot review belongs here rather than live round.

## Proven satellite / yardage baseline
Historical proven implementation:
- Commit `325b7d0a178ee0678365b4e7947d8a37ad4e0af3` — “Add clean UiDo GPS satellite trial flow”.
- Proven Android loading commit `18c646eb3d6f86fb40f24be5f81defb8bc072a33` — “Load clean GPS satellite prototype in APK”.
- Restored GPS baseline commit `d9fdbfdf79fec8a20c035d51e4aab8f7923bc7e4`.

The proven Hole View uses Leaflet + ArcGIS World Imagery satellite tiles, Overstone Park coordinates, live GPS/watchPosition/native GPS, Haversine yardage, and Front/Middle/Back green positions. Preserve these mechanics rather than replacing them with a new map concept.

Known Overstone constants from the proven prototype:
- Course centre: `52.27789, -0.81722`
- Green front: `52.2776675, -0.8151979`
- Green middle: `52.2777593548, -0.8150508742`
- Green back: `52.2778714, -0.8149234`
- Pin: `52.27775, -0.81499`
- Satellite: ArcGIS World Imagery via `server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`

## Android/build architecture
- Current authoritative Android tree: `android/app/...`
- Root `app/src/main/...` is an older duplicate and is not the current workflow target.
- Current build workflow: `.github/workflows/build-uido-apk.yml`.

## Build verification
The workflow must verify the exact source commit and distinctive agreed-UI fingerprints before and after the Android build, and include the source commit in the APK.

Build #43 / commit `9a67fbf631b08eced7330b630edd25fa10948cf5` technically verified the then-current source, but that source was **not compliant with the agreed round-flow document** and must not be treated as the design baseline.

## Current work
Replace the current `index.html` with the faithful agreed round flow while retaining the proven satellite/live-yardage Hole View mechanics.

## Do not regress
- Do not invent or add screens not in the agreed flow.
- Do not add a separate Pin/Target screen.
- Do not put Actual Club / Shot Distance into the live flow unless a later explicit spec supersedes this document.
- Do not put strategy, club recommendation, target recommendation, aim recommendation, risk overlay, or strategy advice into the live test.
- Do not replace the proven satellite + live yardage Hole View with a different map implementation.
- Do not move scoring into Shot Recorded.
- Do not change the Start Line / Shape / Strike order.
- Do not use the old v0.9 UI as the baseline.

## Continuity rule
Before making code changes in a new chat, read this file and the canonical agreed-flow document, then inspect the current GitHub source. Continue from that state; do not rebuild the product from remembered context.
