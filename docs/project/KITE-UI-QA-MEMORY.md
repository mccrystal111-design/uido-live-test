# Kite UI Q&A Memory — Stats, Round History & End-of-Round

**Updated:** 2026-10-09  
**Status:** In progress — confirmed decisions recorded; Q&A continues.  
**Purpose:** Durable, cumulative record of Kite UI decisions from the Stats and saved-round Q&A. Use this before continuing the design conversation or implementation.

## Product and architecture principles

- **Kite is the customer-facing product; shared golf/data/statistics capability should remain product-agnostic.** Build the shared engine and data model once; Kite and UiDo decide which capabilities to expose and how to present them.
- **No WHS/GHIN integration is required for Kite.** Kite must not imply a player-entered handicap has been verified or is an official WHS/GHIN Handicap Index.
- Keep player-entered handicap distinct from any calculated practice handicap. Do not silently overwrite the player's entered value with a calculation.
- Build the shared engine's practice-handicap calculation capability so it can be used by UiDo and potentially exposed as a paid Kite feature. Subscription/entitlement decisions belong in the product layer, not inside the calculation engine.
- Retain round/scorecard data in the shared data layer. Subscription tiers should control access to advanced features, not remove access to a player's basic saved scorecards/history.

## Stats screen

### Layout and navigation
- Use **one vertically scrollable Stats page**.
- Provide **sticky tabs at the top** for quick navigation to sections on the same page:
  1. Overview
  2. Scoring
  3. Performance
- Tapping a tab jumps to its section; normal scrolling remains available and the active tab should follow the visible section.
- Do not introduce separate pages or unnecessary back-navigation for these sections.

### Handicap interaction
- Display the player's entered handicap prominently on Stats.
- Make the handicap **tappable to edit in place**; do not force navigation to Player Profile for a quick adjustment.
- Player Profile remains the main place to manage player details. Both screens must update the same underlying player record.
- Clearly distinguish player-entered handicap from a calculated practice handicap and from a verified official handicap (which Kite does not integrate with).

### Free and potential paid features
**Kite Free includes:**
- Player-entered handicap.
- Standard statistics.
- Retained scorecards and round history.
- Basic scoring trends and progress over time.

**Potential Kite paid features include:**
- Calculated practice handicap.
- Advanced statistics and deeper performance analysis.

The shared engine should support calculation independently of whether Kite exposes it in the free or paid tier. Entitlements are not to be hard-coded into the engine.

### Standard Stats baseline
- Score per round and score relative to par.
- Average score.
- Best round and most recent rounds.
- Scoring by hole and by par.
- Scoring trend over time.
- Fairways hit, greens in regulation and putting statistics where the player has recorded the required data.

## Saved round history and scorecard reuse

- Selecting a retained round from Stats or Scores opens the **existing Kite scorecard page**, populated with that specific round's stored data. Reuse the existing design/template rather than creating a separate scorecard UI.
- Each round must be stored as its own persistent record, including its hole-by-hole scores and relevant course/player/round context. Keep a permanent round identifier associated with the opened scorecard so edits cannot affect another round.
- A saved round opens in **Review mode** by default.
- Place **“Edit Scorecard” in the top-right corner**.
- Editing is explicit; the player can review a saved round without accidentally changing it.
- After a saved round is edited and saved, update that specific round and recalculate the affected statistics. Other rounds remain unchanged.

## End Round and completion flow

- The **End Round screen itself is the confirmation/review step**. Do not add a second confirmation before finishing normally.
- End Round lets the player review the scorecard/final result and:
  - return to the scorecard to correct it if it looks wrong;
  - discard the round if it should not be retained; or
  - finish and save the round.
- **Discard Round** invokes a confirmation pop-up (“Are you sure?”). The player can keep the round and return to review, or explicitly confirm discard. Only confirmed discard deletes the round; communicate that it cannot be recovered if that is the actual deletion behaviour.
- Normal Finish does not require an extra confirmation. Save the round, then show a brief **Round Saved** pop-up with links/actions for **Home**, **Scores** and **Stats**. No separate final-results screen is required.
- The same shared pop-up component should support success, destructive confirmation and informational messages.
- Pop-ups use a faded/dimmed background overlay and reuse existing Kite icon assets and the established Kite styling. Do not invent replacement icons if appropriate assets already exist.
- The Round Saved pop-up appears only after saving has actually succeeded. Similarly, a discard success/result must only be shown after the discard operation has completed.
- Tapping Home, Scores or Stats dismisses the Round Saved pop-up and opens the selected destination.

## Saved-scorecard edit confirmation

- After a player edits a saved scorecard and taps Save, save immediately, then show a brief “Changes Saved” pop-up using the shared component.
- The pop-up auto-dismisses after around 1.5–2 seconds and has no dismissal button.
- Show success only after the save succeeds. If saving fails, show a clear error and retry path.

## Working protocol

- Preserve the decisions above; do not ask them again unless new evidence exposes a genuine conflict.
- Continue asking one genuine unresolved question at a time.
- Treat these as product/design decisions, not proof that Figma has already been edited or that implementation exists.
- Before implementation, inspect the existing Figma screens and code and preserve user edits. Record implementation status separately from product decisions.
- Do not manually run or dispatch GitHub Actions unless explicitly requested or genuinely needed.


## Figma baseline inspected — 2026-10-09

Reviewed the current rendered frames on Figma page **02 — Product UI**. Preserve existing work and reconcile agreed behaviours against these screens before adding new UI.

- **Home — `93:2`, “Kite — Front Screen — Navy White — Construction V1”**: already has Start Round, Scores and Stats actions, plus the player/handicap display and profile icon. Do not ask whether Scores and Stats should be added to Home; they already exist.
- **Start Round — `124:25`**: existing course, player selection/add-player, Stroke Play/Stableford and tee-selection layout. Earlier decision remains: Add Player offers a saved player or a round-only guest; a guest must not silently become a permanent profile.
- **Scorecard — `261:30`**: existing long scorecard with player/score summary, front/back hole tables, totals and round statistics. Reuse this as the scorecard template for live rounds and stored rounds; do not create a duplicate saved-round scorecard design.
- **End Round — `261:125`**: current frame is headed “Round complete”, includes View/Edit Scorecard, End Round and Discard Round, and has footer copy saying “Your round is saved to your player profile.” This needs reconciliation with the agreed flow: the End Round screen is the review/confirmation step; normal Finish saves only after the player chooses to finish; Discard requires the shared “Are you sure?” pop-up; successful finish shows the transient Round Saved pop-up with Home, Scores and Stats. Do not assume the current footer or button labels already implement the agreed behaviour.
- **Player Profile — `295:5`**: current profile frame shows player name/switcher, handicap summary, Home course & tees, Playing preferences, and Clubs & carry distances. Preserve user-added changes and existing Google icon assets. Two developer guidance text layers are still inside the phone frame in the current render; they should ultimately live outside the player-facing frame in developer notes, but do not remove or move user content without reconciling with the canvas.
- **Stats page**: no separate top-level Kite Stats screen was identified on the inspected Product UI page. The scorecard contains a Round Statistics section, but that is not the agreed player Stats screen. A dedicated Stats frame will need to be designed later using the confirmed one-page scroll layout and sticky Overview / Scoring / Performance tabs.

This was a baseline review, not a design edit. No Figma layers were changed and no GitHub Actions were run.


## Scores screen — confirmed direction (2026-10-09)

- Create a dedicated **Scores** screen; no existing top-level Scores frame was found in the inspected Product UI page.
- Keep it deliberately simple: a vertically scrollable list of saved-round cards, with each card showing **date played, total/gross score, net score, and course name**.
- Tapping a card opens the existing Scorecard screen in Review mode, populated with that specific saved round. Do not design a second scorecard.
- Avoid graphs, extra performance metrics, filters, and dashboard decoration on Scores; those belong on Stats or can be considered later only if a real need emerges.
- Use the existing Kite navy-and-white styling and established typography/icon assets.
- Any example rounds in the design must be marked as illustrative data, not real saved-round records.
- Each card must be bound to its own persistent round ID in implementation so the correct round opens.
- Design attempt on 2026-10-09 did not complete successfully; no new Scores frame was verified as created. Do not assume the screen exists in Figma yet.


### Scores card typography clarification — 2026-10-09

- **Total/gross score:** large and prominent, matching the large total-score treatment already used on the existing Kite Scorecard screen.
- **Net score:** smaller than the total score and displayed in a neutral colour. Do not use the yellow accent to highlight net score.
- Keep date and course name secondary to the total score.


### Scores list ordering — 2026-10-09

- Show saved rounds in **reverse chronological order**, with the most recently played round first.


### Scores inclusion rule — 2026-10-09

- Scores lists only rounds that have been **ended and retained**.
- Discarded rounds are excluded.
- A round that is still in progress or was abandoned without being ended is not shown in Scores.


### Same-day rounds — 2026-10-09

- Multiple rounds played at the same course on the same date appear as **separate cards**.
- Store a date-and-time timestamp for each round and use it to distinguish rounds and support newest-first ordering. Show the time on the card when needed to disambiguate same-day rounds.


### Scores list limit and archive — 2026-10-09

- The Scores screen displays only the **20 most recent ended and retained rounds**, ordered newest first.
- Older rounds remain stored/archived; they are not deleted when they fall outside the visible top 20.
- Keep the visible Scores screen simple; do not add month/year grouping or infinite scrolling as part of this requirement.
- Whether users need a separate archive/history access point is not yet specified.


### Archived rounds access — 2026-10-09

- The mobile Kite Scores screen stays limited to the 20 most recent ended and retained rounds.
- Older rounds remain stored and could potentially be accessed through a Kite website rather than adding archive controls to the mobile screen.
- Website-based archive access is an idea to explore, not a confirmed website scope or implementation decision. Keep older round data retained and associated with the player's account/profile so a future web experience can retrieve it.


### Saved scorecard review behaviour — 2026-10-09

- Tapping a saved round opens its scorecard in **Review mode**, showing the recorded hole-by-hole scores and relevant statistics for that specific round.
- The saved data is not editable by default. Changes are possible only after the player explicitly selects **Edit Scorecard**.
- Preserve the round's own persistent ID so review or edits always target the correct round.


### Saved round timestamp after editing — 2026-10-09

- Editing a saved round preserves its original date and time.
- Update only that round's score data and recalculate the affected statistics; do not change the round timestamp as a side effect of editing.


### Saved round course/player association — 2026-10-09

- Editing a saved scorecard is for correcting that round's score data, not changing who played or which course the round was played at.
- Keep the original player and course association fixed during scorecard editing. If either was recorded incorrectly, treat that as a separate correction workflow rather than a normal scorecard edit; the details of that workflow are not yet specified.


### Saved scorecard editable data — 2026-10-09

- In Edit Scorecard mode, all recorded round stats should be editable, not just hole-by-hole gross scores. This includes putts and other statistics captured for the round.
- Keep the original player and course association fixed, and preserve the original round date/time. Saving updates that round's entered data and recalculates affected statistics; other rounds remain unchanged.


### Adding previously unrecorded stats — 2026-10-09

- When editing a saved scorecard, the player may enter round statistics that were not recorded at the time, such as fairways hit or greens in regulation.
- Treat these as optional data: do not assume an unentered statistic was zero or infer a value. Recalculate the relevant statistics once the player enters or changes the data.


### Display of unentered statistics — 2026-10-09

- If a round statistic has not been entered, leave its display field blank rather than showing a dash or treating it as zero.
- Preserve the distinction between missing data and an actual recorded zero in storage and calculations.


### Stats refresh after saved-round edits — 2026-10-09

- The user has no strong preference about whether the Stats page refreshes immediately after a saved round is edited or on next opening.
- Implementation default: update/recalculate the underlying stats as soon as the saved edit succeeds, so any subsequent view of Stats reflects the latest data. No extra screen or confirmation is needed for the recalculation.


### Leaving saved-scorecard edit mode with unsaved changes — 2026-10-09

- If a player attempts to leave Edit Scorecard mode with unsaved changes, show a confirmation pop-up with three actions: **Save Changes**, **Discard Changes**, and **Continue Editing**.
- Save Changes persists the edits and only reports success after saving succeeds.
- Discard Changes abandons the unsaved edits and preserves the previously saved round.
- Continue Editing closes the pop-up and returns to the edit state without losing the player's current changes.


### Save failure during saved-scorecard editing — 2026-10-09

- If saving fails because of a connection or technical error, keep the player's current edits on screen and allow them to retry.
- Do not show a success confirmation or discard the edits unless the save has actually succeeded. Show a clear error/retry path.


### Successful saved-scorecard edit feedback — 2026-10-09

- After a saved scorecard edit saves successfully, show a brief **“Changes Saved”** pop-down/toast for **1 second**, then dismiss it automatically.
- Return to Review mode after the successful save; the toast is brief feedback, not a separate confirmation step. Never show it before the save succeeds.


### Review mode metadata — 2026-10-09

- Keep the saved scorecard Review mode clean. Show the original round date and relevant playing details; do not add a “last edited” timestamp to the player-facing screen.


### Undo after discarding unsaved scorecard edits — 2026-10-09

- Prefer a brief **Undo** opportunity for **3 seconds** after the player chooses Discard Changes in the unsaved-changes pop-up, rather than adding a second confirmation step.
- The discard action must remain reversible during that window: Undo restores the unsaved edits and returns the player to editing. After the 3-second window expires, abandon the edits and return to Review mode. The previously saved round is never altered by discarding unsaved edits.


## Stats screen Q&A — continued 2026-10-09

### Overview section content

- Immediately beneath the prominent, editable handicap, show a compact summary of **average score, best round and most recent round**.
- Follow this summary with the player's scoring trend.
- Keep the opening view informative but uncluttered; detailed breakdowns belong in the Scoring and Performance sections.


### Stats scoring trend chart — 2026-10-09

- In the Stats Overview section, use a line graph showing the score for each round and the average score over time.
- Mark the player's lowest round score with a star beside that data point.
- Keep the chart easy to read on mobile and avoid unnecessary decoration. The round-by-round detail remains available on Scores.


### Stats chart round-count options — 2026-10-09

- Provide chart range options for the **last 5, 10 or 20 rounds**.
- This is a simple presentation/data-selection control: use the chosen count to select the most recent rounds for the chart and update the plotted round-score and average-over-time series. It should not require a separate statistics engine or a new screen.


### Stats chart average line — 2026-10-09

- Use a **rolling average** for the average-score line rather than one flat average across the selected rounds, because it better communicates form over time.
- The chart range selector remains 5 / 10 / 20 rounds, with 10 as the default. Define and label the rolling-average calculation clearly during implementation so the line is understandable and consistent across selected ranges.


### Rolling-average window — 2026-10-09

- Calculate the rolling average using the **last 3 rounds at each point** in the Stats chart, making it responsive to recent form.
- For the first one or two points where fewer than three rounds are available, use the available rounds rather than inventing data; keep missing data distinct from zero.


### Lowest-round star criterion — 2026-10-09

- The star on the Stats trend chart marks the round with the **best score relative to par**, not simply the fewest gross strokes. Use the round's score-to-par result so performances across different course pars are compared meaningfully.


### Stats chart score measure — 2026-10-09

- Plot each round's result **relative to par** (for example, +4 or −2), not gross strokes.
- Calculate and display the 3-round rolling average using the same relative-to-par measure so the plotted series and trend line are directly comparable across courses.
- The star marks the best round relative to par.


### Stats chart round-length filter — 2026-10-09

- Provide a filter for **9 holes / 18 holes / Both** on the Stats scoring-trend chart.
- When Both is selected, plot each round's score relative to par so 9-hole and 18-hole results can be compared on the same measure; do not convert a 9-hole score into a projected 18-hole gross score.
- The 5 / 10 / 20 selector controls the number of most recent rounds in the selected round-length set. The chart continues to show round score relative to par, a 3-round rolling average on that same measure, and a star for the best relative-to-par round.


### Stats chart round-length filter preference — 2026-10-09

- Remember the player's last selected round-length filter (9 holes / 18 holes / Both) where persistence is available, rather than resetting to a fixed default each time.
- If no saved preference exists yet, choose a sensible initial default; this preference must not affect stored round data or the calculation rules.


### Scoring breakdown by hole par — 2026-10-09

- In the Stats Scoring section, show the **average gross score** separately for par 3s, par 4s and par 5s.
- Do not use average score relative to par for this particular breakdown; the user wants average gross strokes for each hole-par category.


### Putting statistics in Stats — 2026-10-09

- Include average putts per hole and average putts per round in the Scoring section when putting data is available, consistent with familiar golf-statistics conventions.
- Treat putting counts as context, not a standalone verdict on putting performance. Low putt totals can result from missed greens and good chipping/up-and-down play; interpret putting alongside other recorded context such as greens in regulation and scoring rather than implying fewer putts always means better putting.
- If the required data is not recorded, leave the statistic blank rather than displaying zero or a dash.


### Fairways and greens statistics — 2026-10-09

- Include **fairways hit percentage** and **greens in regulation (GIR) percentage** in the Stats Scoring section when the player has recorded the required data.
- Keep these statistics optional; if data is missing, leave the display blank and do not interpret missing data as zero.


### Scoring outcome distribution — 2026-10-09

- Include a familiar golf scoring breakdown in Stats Performance: birdies, pars, bogeys, and double bogeys or worse, shown as the percentage of holes in each category.
- This is a conventional, easy-to-understand scoring summary. Calculate from recorded hole scores relative to each hole's par; do not treat missing hole scores as a scoring category.


### Course-specific stats scope — 2026-10-09

- Do not include average score by hole number (holes 1–18) in the general Stats Performance section. It is too dependent on the particular course.
- Avoid splitting general player stats into separate course-specific views for now. Keep Stats focused on the player's overall game across rounds and courses.


### Handicap trend in Stats — 2026-10-09

- Do not add a handicap-over-time graph to the general Stats Performance section at this stage. Handicap can move sharply after a cluster of good rounds and then remain unchanged through many mediocre rounds, depending on the handicap system's calculation and how often the player plays; a simple trend could be misleading or duplicate the prominent current handicap in Overview.
- Keep the current handicap prominent in Overview. Any future handicap history view should explain the system and its update behaviour rather than presenting the line as a simple measure of current form.


### Recent-form summary — 2026-10-09

- Do not add a separate recent-form count/summary of birdies, pars and bogeys over the last 5 or 10 rounds. The scoring trend chart is sufficient and avoids duplicating information in Performance.


### Front-nine / back-nine scoring breakdown — 2026-10-09

- Include scoring averages split by **Front 9 / Back 9 / Both** across rounds, without creating separate course-specific stats views.
- Provide a filter with **Front 9**, **Back 9** and **Both** options so players can compare starts, finishes or the full round.
- Apply the selected split consistently to the displayed scoring average and use only the holes/rounds available for that selection; do not treat missing scores as zero.


### Nine-hole rounds in front/back averages — 2026-10-09

- A 9-hole round contributes only to the front-nine or back-nine average corresponding to the nine actually played. Never count one 9-hole round as both sides or infer data for the unplayed nine.


### Front/back-nine average measure — 2026-10-09

- Use **average score relative to par** for the Front 9 / Back 9 / Both breakdown, consistent with the 18-hole scoring averages and the main scoring-trend chart. Do not switch to gross strokes for the nine-hole comparison.


### Reuse front/back-nine filter in scoring breakdowns — 2026-10-09

- Reuse the **Front 9 / Back 9 / Both** filter for the birdie/par/bogey scoring-outcome breakdown, provided it can be shared without unnecessary implementation complexity.
- Prefer one consistent filter state across related Performance scoring components rather than separate controls that can disagree. If the UI/implementation requires independent filters, keep the behaviour clear and simple.


### Grouped scoring outcome categories — 2026-10-09

- Keep the Performance scoring-outcome categories grouped for a clean mobile display: **birdie or better**, **par**, **bogey**, and **double bogey or worse**. Do not split eagles or triple bogeys into separate categories at this stage.


### Fairways and GIR use the nine filter — 2026-10-09

- Fairways-hit percentage and greens-in-regulation (GIR) percentage should follow the shared **Front 9 / Back 9 / Both** filter, consistent with the other Performance breakdowns.
- Calculate each percentage from the eligible holes for the selected nine(s) where the relevant data is recorded; do not count missing data as misses or zeros.


### Putting stats use the nine filter — 2026-10-09

- Average putts per hole and average putts per round should follow the shared **Front 9 / Back 9 / Both** filter. When Front 9 or Back 9 is selected, calculate the putting figures from the relevant played holes/round segments only.
- Keep putting statistics contextual rather than treating low putt counts alone as proof of good putting. Missing putting data remains missing and is not treated as zero.


### Sticky Performance filter header — 2026-10-09

- Place the shared **Front 9 / Back 9 / Both** selector once at the top of the Stats Performance section.
- Keep the selector/header row sticky while the player scrolls through Performance so it remains visible and continues to control all relevant statistics below it.
- Ensure the sticky row does not obscure content and behaves sensibly on a mobile viewport.


### Sticky Stats navigation and Performance filter — 2026-10-09

- Keep the main **Overview / Scoring / Performance** tabs sticky at the top of the Stats page during scrolling.
- Keep the **Front 9 / Back 9 / Both** filter row sticky beneath the main tabs while the player is in the Performance section.
- Both rows remain visible together when relevant, with careful mobile spacing so neither overlaps nor obscures page content. The filter controls the relevant Performance statistics below it.


### Overview summary and round-length filter — 2026-10-09

- Where practical, let the Overview summary metrics (average score, best round and most recent round) respect the same **9 holes / 18 holes / Both** filter used by the scoring-trend chart.
- This is a preference for consistent filtering, not a reason to complicate the layout. Ensure the summary compares like with like and does not combine 9-hole and 18-hole gross totals as if they were equivalent.


### Remember Stats chart round-count preference — 2026-10-09

- Remember the player's last selected **5 / 10 / 20 rounds** chart range where preference persistence is available, just as with the 9 holes / 18 holes / Both filter.
- If no saved range exists, default to **10 rounds**. This preference changes only the displayed range, not stored round data.


### Stats Overview summary-card layout — 2026-10-09

- Preferred initial design direction: compact cards for **average score**, **best round** and **most recent round**.
- This is provisional until the user sees an example. Present a rendered visual example for review before treating the layout as approved; do not make Figma changes during Q&A.


### Stats Overview chart placement — 2026-10-09

- Provisional layout: place the scoring-trend chart immediately beneath the three compact summary cards, with the 5 / 10 / 20 round-count and 9 holes / 18 holes / Both filters directly above the graph.
- This layout is not yet approved. The user wants to see an example and try it in Figma later before confirming the arrangement. Do not change Figma during Q&A.


### Stats Scoring layout — 2026-10-09

- Preferred provisional layout: use three compact cards for average gross score on **par 3s**, **par 4s** and **par 5s**, mirroring the three-card pattern proposed for Overview.
- Confirm the visual treatment when the user can try the rendered Stats page in Figma; do not make Figma changes during Q&A.


### Putting figures in Stats — 2026-10-09

- Show both **average putts per hole** and **average putts per round** in the Stats Scoring section.
- Both figures follow the shared **Front 9 / Back 9 / Both** filter where relevant. If putting data is missing, leave the figure blank rather than treating it as zero.


### Stats Performance scoring outcome visualisation — 2026-10-09

- Use a **horizontal bar chart** for the percentages of holes scored as birdie or better, par, bogey, and double bogey or worse.
- Reuse the familiar visual language already used for Round Statistics on the existing Scorecard where practical, so the Stats page feels consistent with the rest of Kite.
- This confirms the chart type; review the final sizing and visual treatment in the Figma example before treating those details as final. Do not make Figma changes during Q&A.


### Stats Performance numerical layout — 2026-10-09

- Preferred provisional direction: use cards for **fairways hit %** and **greens in regulation (GIR) %**, followed by the putting figures and horizontal scoring-outcome bar chart.
- The user needs to see the rendered layout before approving the cards. Avoid making them so small that labels or values feel cramped; adjust sizing and grouping during the Figma review. Do not change Figma during Q&A.


### Stats Scoring card consistency — 2026-10-09

- Use **three cards in a single row** for the average gross scores on par 3s, par 4s and par 5s, following the same three-card pattern used elsewhere in Stats for visual consistency.
- Treat the single-row layout as the preferred direction, then validate readability and spacing in the Figma example; do not change Figma during Q&A.


### Stats Performance section order — 2026-10-09

- Preferred order: (1) fairways hit % and GIR % cards, (2) putting figures, and (3) the horizontal scoring-outcome bar chart.
- This order is agreed as the content sequence; sizing and final spacing remain subject to visual review in Figma.


### Stats additional short-game and penalty statistics — 2026-10-09

- Include **penalties per round**, **up-and-down percentage**, and **sand-save percentage** in Stats Performance, provided the required data has been recorded.
- Up-and-down percentage is successful up-and-downs divided by eligible attempts: the player misses the green and holes out in two strokes or fewer.
- Sand-save percentage is successful sand saves divided by eligible greenside-bunker attempts, where the player gets the ball into the hole in two strokes or fewer.
- Penalties per round is calculated only from rounds with recorded penalty data. Missing attempts or penalty data must not be treated as zero; leave the statistic blank when there is insufficient recorded data.
- These are additional statistics beyond the initial fairways/GIR cards, putting figures and scoring-outcome bar chart. Keep the layout provisional until reviewed in Figma; do not make Figma changes during Q&A.


### Stats Short Game & Penalties subsection — 2026-10-09

- Group **penalties per round**, **up-and-down percentage**, and **sand-save percentage** in a separate **Short Game & Penalties** subsection beneath the main Performance statistics, rather than adding more cards to the primary layout.
- Keep the exact presentation provisional until the Stats page is reviewed in Figma; do not make Figma changes during Q&A.


### Derive short-game statistics from captured round data — 2026-10-09

- Do not add a separate manual entry step for up-and-downs or sand saves if they can be calculated reliably from the existing hole-by-hole data.
- The current scorecard/live-round capture includes sand-shot information and GIR, alongside hole scores and putting data. Use these recorded inputs to derive sand-save and up-and-down attempts/conversions where the data supports an unambiguous calculation.
- Avoid guessing when the available data is insufficient to determine an attempt or outcome; preserve missing/unknown data rather than fabricating a result. Revisit any genuinely missing capture fields only if the calculation cannot be made from the existing record.


### Putts as an input to short-game derivation — 2026-10-09

- The user confirms putts are also captured. Consider **sand-shot/greenside-bunker information, GIR, putts and hole score** together when deriving sand-save and up-and-down attempts and conversions.
- These may be sufficient for many cases, so do not introduce extra manual inputs by default. Before implementation, validate the exact existing shot/lie data and calculation rules; only mark cases unknown where the captured data cannot distinguish an attempt or outcome reliably.


### User-defined up-and-down and sand-save rules — 2026-10-09

- **Up-and-down:** classify a hole as an up-and-down when the player missed the green and then took **one putt** to finish the hole.
- **Sand save:** classify a hole as a sand save when the player missed the green into a bunker, played a recorded sand shot, and then took **one putt** to finish the hole.
- Use the existing missed-green/GIR, sand-shot and putt records to derive these outcomes rather than adding separate manual entry by default.
- Validate how bunker location and the number/order of shots are represented in the current data model before implementation. Do not count ambiguous cases as successes or failures; keep insufficient data unknown.


### Up-and-down and sand-save par requirement — 2026-10-09

- Refine both success rules to require the hole to be completed in **par** as well as the relevant recovery pattern:
  - **Up-and-down:** missed the green, took one putt, and finished the hole in par.
  - **Sand save:** missed the green into a greenside bunker, played a recorded sand shot, took one putt, and finished the hole in par.
- Use these as the user's requested success definitions for Kite. Keep attempt denominators based on eligible recorded opportunities, and do not classify incomplete/ambiguous data as a miss or a success.


### Final terminology for recovery statistics — 2026-10-09

- Use the labels **Scrambling %** and **Sand Saves %** in Stats Performance.
- **Scrambling success:** missed the green in regulation and finished the hole in par or better.
- **Sand-save success:** played from a greenside bunker and finished the hole in par or better.
- Derive these from recorded GIR, shot/lie and hole-score data where possible. Count only eligible, known attempts in the denominator; do not treat missing or ambiguous data as a failure or success.


### Best Round card details — 2026-10-09

- In the Stats Overview **Best Round** card, make score relative to par the primary, prominent figure.
- Beneath it, show the best gross score and the course par for that round in smaller text (for example, **Best score +2** with **Best gross 75 / Par 72** underneath).
- Preserve the round/course context so the par displayed is the par that applied to that recorded round, not an assumed standard par. Keep the exact visual hierarchy provisional until reviewed in Figma; do not make Figma changes during Q&A.


### Most Recent Round card details — 2026-10-09

- Keep the Stats Overview **Most Recent Round** card consistent with **Best Round**: show score relative to par as the primary, prominent figure.
- Beneath it, show the gross score and the course par for that specific round in smaller text. Use the par recorded for that round/course rather than assuming a standard par.
- Keep the exact visual hierarchy provisional until reviewed in Figma; do not make Figma changes during Q&A.

### Q&A closed — Kite Figma implementation handoff — 2026-10-09

- Q&A is closed. Editable Figma frames created on `02 — Product UI`: `Kite — Stats — V1` (302:5), `Kite — Scores — V1` (302:121), and `Kite — Developer Notes — Q&A Handoff` (302:162). Existing screens were preserved; new screens were placed alongside them.
- Stats visual prototype includes handicap, Overview/Scoring/Performance navigation, Average/Best/Most Recent cards, relative-to-par trend chart, 9/18/Both and 5/10/20 controls, Par 3/4/5 averages, fairways/GIR, putting, grouped outcome bars and Short Game & Penalties.
- Average, Best and Most Recent cards share relative-to-par prominence; average gross and average course par support decimal values. Per-round course par must be used for relative-to-par calculations.
- Scores prototype is a simple newest-first retained-round list, intended to open each existing Scorecard in Review mode. Sample scores/dates are visual placeholders only.
- Developer notes frame contains the Q&A decisions and implementation constraints. Navigation, sticky behaviour, round data, calculations and interactions are not yet wired; End Round save messaging still needs reconciliation.
- No GitHub Actions were run. Screens remain subject to visual QA and iteration.


## Kite Page UI voice Q&A log — 2026-10-10, from approximately 20:46 UK time

**Purpose:** Detailed summary of the voice conversation about the Kite Figma screens. This is a decision log/transcript summary, not a verbatim audio transcript. Decisions below are the latest direction from this session and supersede older provisional visual directions where they conflict. This is documentation only: do not infer that Figma or application code has already been changed.

### 1. Shared page backgrounds and visual consistency

- Use the **exact same cream background colour already used on the existing Scorecard screen** on:
  - Start Round
  - Scorecard
  - Player Profile
  - Stats
  - Scores
- The reason is to make boxes, buttons, selected areas and nested page panels stand out, while keeping the non-on-course experience visually consistent.
- **Do not apply the cream treatment everywhere.** Keep Home/front screen visually distinct as the opening/home experience; keep Yardage clean, bright and uncluttered for use on the course; keep End Round / Round Complete distinct as a finite finish/discard state.
- Treat the existing Scorecard cream as the source of truth; do not approximate the shade or create variants.
- Scores cards should use that same cream treatment and **drop shadows** to give them clearer separation/depth.

### 2. Design-system rules are a high-priority requirement

The user explicitly stressed that newly created pages must be “bang on” against the established UI principles from the start, in Figma and later in code. New screens must not drift in font sizes, colours, spacing or dimensions.

- Create/maintain one authoritative set of UI principles in Figma Developer Notes and the GitHub project documentation.
- Record and reuse the approved typography, colour palette, spacing, component sizes, shadows, selected/active states and interaction conventions.
- Existing approved page headers on Scorecard, End Round and Player Profile use **Sora SemiBold at 25 pt**. Use this as the initial reference standard and verify it against the actual Figma styles before publishing the full specification.
- Stats and Scores were observed to have header sizing inconsistent with those pages (Scores looked like Sora SemiBold 20 pt); align them to the verified standard rather than treating each new page independently.
- Document heading, subheading, body, label and numeric styles, including font family/weight/size/colour; spacing and padding; corner treatment; shadows; and shared components.
- Add a **new-page design checklist**: before a new page is considered complete, compare it with approved screens and tokens, use existing components/styles where possible, and document any intentional exception.
- Do not invent unverified values for every colour/spacing token. Inspect the actual Figma source and record exact values in the implementation phase.
- The user wants the UI principles tightened across both Figma design and eventual HTML/APK implementation. A visual mismatch should be treated as a design-system/QA issue, not accepted as normal drift.

### 3. Stats page — filters and scoring trend

The user has already made some UI adjustments in Figma. Preserve those edits during future implementation.

- The scoring trend round-length filter is **9 holes / 18 holes / Both**.
- The range control is labelled **“rounds”** in lowercase, with the selected count displayed beneath it.
- Available counts are **5, 10 and 20**; they should work as direct, easy-to-tap buttons that immediately change the trend chart.
- The user currently has the chart range set to **5**. For this scoring-trend control, retain **5 as the default** unless later review changes it. This supersedes the older provisional 10-round default recorded earlier for this particular trend UI.
- The current line graph in Figma does not look like a proper line graph to the user. It may be a Figma/rendering issue or something that could also affect the actual HTML/APK implementation.
- Before assuming the graph is acceptable, inspect the Figma result and test the relevant implementation/render in **Chromium**, using the available Stagehand/visual QA workflow and pixel comparison where practical. Confirm that the graph genuinely renders as a clear line graph, with sensible connected data points/lines, rather than merely assuming it will look right in production.
- This is a QA task to investigate; do not claim it has already been tested or fixed.

### 4. Stats page — rethink hierarchy and meaning of tabs

The user considers the current Stats page layout/hierarchy confusing and wants a proper rework rather than cosmetic changes.

- Keep the main sections/tabs: **Overview, Scoring, Performance**, but make the hierarchy clear and meaningful.
- Avoid a page that says “Overview” as the main section and then repeats “Overview” immediately as a subheading. Use the main tab as the section heading and make subheadings describe their actual content.
- Intended mental model:
  - **Overview = what is happening** to the player's game.
  - **Scoring = scoring results and patterns.**
  - **Performance = why those results are happening and what the player can improve.**
- The current placement of the scoring trend makes it unclear whether it belongs to Overview or Scoring. Resolve this deliberately in the redesign and make tab labels, section headings and content hierarchy agree.
- Treat this as a structural rework of the Stats page, including section hierarchy and content order. Do not merely add more cards to the current layout.

### 5. Stats Performance — progress over time, not percentages in isolation

The existing Fairways Hit % and Greens in Regulation (GIR) % cards do not tell the whole story when shown only as averages.

- Replace the isolated Fairways Hit and GIR percentage cards with **trend visualisations over time** (line graph or a clear bar chart, whichever communicates progression best).
- Let the user select the last **5 / 10 / 20 rounds**, using the same simple direct-button pattern as the scoring trend. The Performance trend should default to **20 rounds**, so the player gets a useful longer-term view, while being able to compare recent 5- or 10-round form.
- The purpose is to show whether recent performance is better or worse than the longer-run average; e.g. an overall 64% fairway figure can conceal much better recent form.
- Calculate from eligible recorded data only. Missing fairway/GIR data must not be treated as a miss or zero. Make the chart's range and metric clear.
- Decide during the redesign whether line or bar charts communicate progression most clearly, and keep the chart styling aligned with the shared design system.

### 6. Stats Performance — prioritise Short Game & Penalties over putting

The user considers short-game recovery and penalty avoidance more directly actionable for improving scores than average putts alone, particularly for mid- and high-handicap golfers.

- Bring **Scrambling %**, **Sand Saves %**, and **Penalties per round** higher in the Performance section, above putting statistics.
- Treat **Short Game & Penalties as part of Performance**, not as a separate peer section outside Performance.
- Keep putting statistics available, but give them lower visual priority than the three short-game/penalty measures.
- Preserve the existing agreed definitions:
  - Scrambling success: missed the green in regulation and finished the hole in par or better.
  - Sand-save success: played from a greenside bunker and finished the hole in par or better.
  - Penalties per round: use recorded penalty data only.
- Calculate only from eligible, known attempts/rounds. Unknown or ambiguous inputs are not failures or successes. Validate that the stored shot/lie, GIR, putt and hole-score fields support reliable derivation before implementation; do not add unnecessary manual entry by default.
- Intended narrative: Overview tells the golfer what is happening; Scoring shows scoring results; Performance helps explain the causes and opportunities to improve.

### 7. Scoring-outcome visualisation

- The existing Stats scoring-outcome graphic feels loose and less polished than the **Round Statistics** visualisation already used on the Scorecard.
- Reuse that existing Scorecard Round Statistics visual style as the reference: compact/tight layout, bold readable values, consistent colours, clear headers and established fonts.
- Prefer reuse of the existing component or its visual rules where practical rather than creating a separate, inconsistent chart style.
- Preserve the agreed grouped outcome categories: birdie or better, par, bogey, double bogey or worse. Keep the chart compact and legible on mobile.

### 8. Scores screen — card treatment and diagnostic insight

The user is happy with the general direction and had no further broad Scores-page changes beyond the details below.

**Card appearance**
- Apply the exact Scorecard cream background and a drop shadow to every tappable round card.
- Keep the cards clear and readable, with enough visual life and useful context without clutter.

**Score area and navigation**
- Each card has two distinct tap targets/behaviours:
  1. Tapping the main score area opens that specific round's **Scorecard in Review mode**.
  2. Tapping the key-stat badge/box opens the player's **Stats page**, supporting reflection and improvement rather than simply revisiting the scorecard.
- Make the different tap areas visually obvious and ensure the stat badge does not accidentally trigger the scorecard action.

**Gross and net score hierarchy**
- Make the gross score and score relative to par the prominent score area; for example, **77 / +5** as the main gross-score result, with the **net score 73** shown smaller and directly beneath/adjacent according to the card layout.
- Do not use a separate full line saying “Net 73” if a clear smaller net number can do the job. Ensure the net number is still unambiguously identified as net score through a clear, consistent presentation.
- Keep course name and date as supporting details; time may be shown where useful.

**One key-stat callout on every round card**
- Every round card should have a compact **key-stat badge/box** on the right-hand side, using the available card width.
- It should highlight the most informative positive or negative performance factor for that specific round:
  - Good round: surface a meaningful strength to reinforce.
  - Poor round: surface the most relevant weakness or possible reason for the score.
- Examples of the *kind* of insight include fairways hit being lower than usual, GIR being unusually strong/weak, excessive putts, penalties, or recovery performance. These are examples, not a fixed list or hard-coded rule.
- The intent is diagnostic: **the outcome is what happened; the reason is what the golfer may be able to change.** The insight should help a golfer review a round and think about what to repeat or improve next time.
- Use a badge/card treatment that is consistent with the existing Stats visual language, so the stat looks like one of the player's other stats rather than an unrelated decorative label.
- Define the mechanism for selecting the key stat separately during product/data design. It should be based on the round's available data and meaningful comparison/baseline, not arbitrarily label one stat as “best” or “worst”.
- Not every round will have enough data for every candidate stat. Handle missing data honestly and avoid inventing a positive/negative insight when the evidence is insufficient.
- This is a new product behaviour to specify and prototype; it is not yet implemented.

### 9. Weather context for a round — premium feature proposal

The user proposed a weather indicator to give round scores context, especially for recreational golfers without a competition-based handicap process or official handicap index.

- Where data access permits, retrieve weather for the **round's recorded date/time and location/area**, rather than asking the player to enter it manually.
- The user believes the existing Supabase setup may be able to support retrieving weather for a given area and time. This is a technical investigation, **not a verified Supabase capability**; check the appropriate weather source/API and data architecture before promising it.
- Show a subtle weather/context indicator on the Scores card (for example, high wind or rain) when reliable data is available. The intent is to help the golfer understand that conditions may have influenced a score and avoid over-interpreting a difficult round as poor ability.
- Consider using the same conditions as context in future stats/round insights, but do not claim weather-adjusted handicap calculations or a formal Competition Scratch Score (CSS) equivalent unless a defensible calculation and rules are separately specified.
- **Premium/paid feature only.** The user explicitly said sourcing weather information for each round should not be part of the free/ad-supported tier. Do not include it in Kite Free/ad-supported scope.
- Investigate API/data costs, location/time accuracy, storage/caching, availability for past rounds and entitlement enforcement before implementation. Do not call this a confirmed feature until feasibility is established.

### 10. Workflow and immediate next steps

- The voice session was a **Q&A/design review only**. Do not silently start editing Figma while still reviewing.
- Preserve changes the user has already made to the Stats screen.
- Next implementation/QA work, after the user authorises moving from review to build:
  1. Inspect the latest Figma frames and identify the exact Scorecard cream and approved typography/component tokens.
  2. Update the Figma Developer Notes with the authoritative design-system specification and new-page checklist.
  3. Rework Stats section hierarchy and performance visualisations as described above.
  4. Update Scores card styling, gross/net hierarchy, independent tap targets and key-stat callout.
  5. Validate the scoring-trend chart and other visualisations in Chromium with screenshot/pixel QA where practical.
  6. Investigate weather-source feasibility for date/time/location, keeping it outside free/ad-supported scope.
  7. Record implementation status and QA evidence separately from decisions; do not claim any item is implemented until verified.
- Do not run or dispatch GitHub Actions as part of this documentation update.

### 11. Kite UI Style Menu v1 — living reference

**Purpose and authority**
- The curated, current Figma screens remain the visual source of truth. The style menu documents established patterns; it must not force a redesign of already-curated screens.
- Figma visual reference: a separate frame on the `02 — Product UI` page named **Kite — UI Style Menu — V1** (frame ID `334:5`). Existing product screens and Developer Notes were not altered when this frame was created.
- This file remains the written decision record. Update this section as decisions are confirmed during page curation; keep implementation status distinct from proposals.
- Status labels: **Confirmed** = directly verified in current Figma; **Provisional** = useful working default, not locked; **To resolve** = needs review before standardising.

**Confirmed page backgrounds**
- Kite Navy `#0E1C2B`: Home and End Round.
- Kite Ivory `#F4F1E6`: Start Round, Scorecard, Player Profile, Stats and Scores.
- These values were checked against current Figma frame fills on 12 October 2026. Developer Notes uses a separate neutral background and is not included in the app-screen ivory rule.

**Typography — observed roles, not a fully locked type scale**
- Typeface in current screens: Sora.
- Page title: 25 px, SemiBold (observed).
- Section heading: 12–13 px, SemiBold (observed range).
- Supporting text: 10–11 px, Regular (observed range).
- Metric values: 22–29 px, Bold/SemiBold (observed range).
- Hero score: 40–62 px, Bold/SemiBold (observed range).
- Other sizes remain screen-specific until the remaining screens are curated. Do not force all text into these roles prematurely.

**Observed colour candidates**
- Navy `#0E1C2B`; white `#FFFFFF`; slate `#606870`; divider grey `#DCDDDB`; bar-track grey `#E5E7EB`; red `#F71928`; green `#009951`; bunker brown `#AC7F5E`; deep navy `#0E2334`; yellow `#FFCC00`.
- Colour roles are recorded from current screens, but nearby grey/neutral variants still need a usage audit. Do not merge similar tokens until the differences are understood.

**Components and layout**
- Common observed card corner radii include 8, 10 and 12 px.
- Provisional spacing defaults for evaluation only: compact gaps 4–8 px; standard gaps 12–16 px; section separation 20–24 px; divider 1 px.
- Shadow values/presets remain provisional. Preserve existing effects until the current screens have been audited.
- These defaults are not yet formal Figma styles, variables or component rules.

**New-screen curation checklist**
1. Check hierarchy and readability at mobile scale.
2. Reuse established colour and typography roles where appropriate.
3. Check cards, buttons, dividers, spacing and effects against curated screens.
4. Preserve intentional screen-specific differences.
5. Record exceptions and unresolved choices instead of guessing.
6. Do not alter a curated screen merely to make it conform to this draft.
7. Promote a token to confirmed only after checking it against current designs.

**To resolve before token lock**
- Audit remaining screens, including current Scores details.
- Review near-duplicate greys and neutrals and determine whether they are intentional.
- Verify spacing and shadow values against actual current Figma properties.
- After the page curation is sufficiently stable, create reusable named Figma text, colour and effect styles/variables from approved tokens.

**Change log — 12 October 2026**
- Created the separate Figma Style Menu v1 frame (`334:5`) as a living reference. No product-screen designs were changed.
- Verified the listed app-screen background colours against current frame fills.
- No GitHub Actions were run.

### 12. Spacing register — required during screen curation

- **Spacing is not yet fully measured or standardised.** The Style Menu's 4–8 px compact gaps, 12–16 px standard gaps, and 20–24 px section spacing are provisional suggestions, not verified design rules.
- During curation, maintain a measured register for each reviewed screen: screen edge margins; card/tile internal padding; horizontal and vertical gaps between adjacent elements; section-to-section spacing; button/control dimensions and spacing; repeated component dimensions; corner radii; and shadow/effect properties where applicable.
- Capture the actual measured value, screen/frame and element/context, whether the value is repeated, and status (confirmed, provisional, exception/to resolve). Avoid averaging distinct intentional patterns into one token.
- Auto Layout item spacing and padding can be read directly where present. Several screens use manually positioned elements, so their geometry must be measured from node bounds/coordinates; an Auto Layout-only audit is incomplete.
- Do not retrofit layouts just to create consistent numbers. Record existing patterns first, discuss outliers during curation, and only promote recurring approved values to reusable tokens after the audit.
- Change log — 12 October 2026: Figma Style Menu updated to explicitly mark spacing as not yet measured and to require a measured spacing register. No product-screen layouts changed.


---

## Kite adult V1 UI curation — Q&A answers so far (12 October 2026)

This section records the decisions from the ongoing screen-by-screen curation of missing Kite adult V1 UI pages. The detailed working log is `docs/project/KITE-V1-UI-CONVERSATION-DECISION-LOG.md`.

### Scope and review method
- Curate missing **Kite adult V1 UI pages** by reviewing existing Figma screens first.
- Keep UiDo and future Kite Kids/junior UI out of current adult V1 scope.
- Do not re-review GPS/live-yardage functionality; the user already understands that experience.
- Review one screen/flow at a time. Ask only about genuine uncertainties and do not repeat settled questions.
- Do not change Figma or implementation code unless explicitly requested. Do not run GitHub Actions.
- Only add confirmed gaps to the missing-page register after existing screen coverage has been reviewed. Rank genuine gaps by priority.

### Authentication and onboarding
1. **First confirmed missing flow:** Login / Sign-up. Home already has a profile area for a logged-in user, so the missing piece is the entry/authentication flow.
2. **Keep sign-up simple:** Google/Gmail, Apple, or email. Returning users should be able to sign in through the same options.
3. **Working onboarding flow:** Sign up/log in → Player Profile setup (can skip) → Home.
4. **Allow skipping profile setup:** explain that some functionality may be limited if relevant details are missing; do not force every field.
5. **Club-bag setup:** offer full bag setup. If the golfer skips full setup, offer the simpler option of entering driver carry and 7-iron carry, then estimate other club distances from those anchors.
6. **Allow skipping all bag setup:** this must remain a valid choice. Do not nag or repeatedly prompt the golfer to complete/update the bag.
7. **Editable data:** estimated clubs/distances must be editable later. The golfer chooses when to update the bag.
8. **Reuse existing Player Profile frame:** Figma frame `295:5` exists. Do not propose a duplicate profile page. The exact bag-management interactions still need verification before claiming full coverage.

### Existing Start Round screen — reviewed at high level
Figma frame `124:25`, “Kite — Start Round — Navy White — V1”, already includes:
- Course dropdown/card.
- Players section showing the current player and an **Add** control.
- Format choices: Stroke Play and Stableford.
- Tee choices: White, Yellow and Red.
- Start Round button.

**Player Add clarification:** Add lets the golfer enter a guest player's name for the round. Selecting/adding a junior golfer linked to a family account is a possible future feature, not current adult V1 scope. Do not treat junior/family UI as a current gap.

### Current missing-page register
| Priority | Gap | Status |
|---|---|---|
| 1 | Login / Sign-up authentication flow | Confirmed gap; details still to curate |

No other missing pages have been confirmed. Course selection and round setup must not be listed as missing based on current evidence: the Start Round screen already includes the course dropdown, format, tee selection, player section and Start Round action.

### Next review
Continue reviewing the existing screens and their flow before adding more missing pages. Avoid a review of GPS/live-yardage behaviour. Once existing coverage has been reviewed, compile the prioritised list of confirmed gaps.


### Tee Shot screen clarification — 12 October 2026
On Figma frame `190:136`, the bottom-left three-way result control means **fairway hit / left miss / right miss**. The golfer selects the result once at the ball; that selection is also a GPS/location-capture opportunity. It is not a shot-shape selector.

The `Dr` area is club selection (Driver in the shown state), with **carry and total yardage** displayed. Keep this distinct from the fairway-result selection.


**Shot logging clarification — 12 October 2026:** When the golfer presses the fairway-result control (fairway hit / left miss / right miss), log the currently selected club with that shot event. The golfer should not have to select the club again at the moment of recording.


**Next-shot flow decision — 12 October 2026:** After a shot is recorded with the fairway-result control, advance directly to the next shot's yardage screen. The golfer selects the club for that next shot and records its result using the same flow.


**Chequered-flag clarification — 12 October 2026:** The chequered flag is specifically for the 18th hole to finish the round. It is not the control for advancing from an ordinary hole to the next hole.


## Scorecard and End Round screen review — 12 October 2026

### Scorecard — Figma frame `261:30`
- Shows the player, handicap, gross/net score and front/back totals.
- Lists holes 1–18 with par, index, score, fairways hit/miss, GIR and putts.
- Includes total score and round statistics (birdies, pars, bogeys, fairway %, GIR %, bunker %, up-and-down %, putts, putts/hole, penalties and HCP).
- A note says “Tap a score to edit”; the bottom action is “Save Scorecard & Exit”.
- This is existing coverage; do not list scorecard as a missing page based on current evidence.

### End Round — Figma frame `261:125`
- Shows a round-complete summary with score, net score, +/- figures and front/back totals.
- Actions: “View/Edit Scorecard”, “End Round”, and “Discard Round”.
- States that the round is saved to the player's profile.
- This is existing coverage; do not list End Round as a missing page based on current evidence.

### Flow question still to confirm
The 18th-hole chequered flag is the action for finishing the round. The End Round screen appears to be a summary/confirmation step with separate “End Round” and “Discard Round” actions. Confirm whether tapping the chequered flag opens this End Round screen, with “End Round” then finalising the saved round.


**18th-hole completion flow confirmed — 12 October 2026:** Tapping the chequered flag on hole 18 opens the existing Round Complete screen (`261:125`). The golfer can view/edit the scorecard or choose **End Round** as the final confirmation to finish and retain the round. **Discard Round** is a separate option.


## Player Profile screen review — 12 October 2026
Figma frame `295:5` (“Kite — Player Profile — V1”) has been visually reviewed. Existing coverage:
- Selected player name and **Switch player** control.
- Handicap summary card with edit affordance.
- Editable **Home course & tees** section.
- Editable **Playing preferences** section (summary indicates yards and app preferences).
- Editable **Clubs & carry distances** section, showing the number of clubs and a “Manage bag” summary.

This confirms the main Player Profile overview and a bag-management entry point already exist; do not list the Player Profile overview itself as a missing page. The destination/edit forms and the exact club-bag interactions have not yet been visually inspected, so do not claim their details are confirmed.


**Player Profile interaction status:** The overview (`295:5`) shows edit controls for Handicap, Home course & tees, Playing preferences, and Clubs & carry distances. We have not established what happens after tapping any of these controls. All four destinations/interactions remain to be reviewed; do not assume they open separate pages, and do not focus only on the bag flow until the others are checked too.


**Edit destination review — 12 October 2026:** Inspected the Product UI frame inventory for Player Profile edit destinations. The profile overview (`295:5`) is present, but I have not found distinct destination frames for Handicap, Home course & tees, Playing preferences, or Clubs & carry distances in the current review. This does not prove no such frames exist elsewhere in the file. Keep all four interactions marked **unverified** until they can be traced; do not assume inline/modal/separate-screen behaviour.


**Correction — Player Profile edit destinations remain unknown:** We have not established what happens when any of the four edit controls is tapped. The earlier question asking whether separate screens exist was still unanswered; it was incorrect to turn an incomplete Figma search into a claim that destinations were not found. Status for all four controls is **unknown / not yet established**, not confirmed missing.

**Player Profile edit interaction found in Figma — 12 October 2026:** The Developer Notes / Q&A Handoff frame (`302:162`, detail node `318:48`) explicitly states that editing expands each Profile section in place, with **Save / Cancel** controls staying within the edited section. This is the documented interaction pattern; separate edit pages are not the intended default. The prototype's displayed profile details are illustrative and implementation should connect the UI to the selected player record.


---

## Consolidated Kite Adult V1 UI Gap Audit — 12 October 2026

### Existing screens found
Home (`93:2`); Start Round (`124:25`); Yardage/Tee Shot (`190:136`); Approach states (`219:2`, `229:143`, `255:267`); Scorecard (`261:30`); Round Complete (`261:125`); Player Profile (`295:5`); Stats (`302:5`); Scores (`302:121`); Developer Notes/Q&A Handoff (`302:162`).

### Prioritised gaps
1. **Login / Sign-up — confirmed missing from the reviewed page inventory.** Agreed providers: Google, Apple or email; support both sign-up and returning-user sign-in.
2. **First-run onboarding/profile setup — required by the agreed journey, not represented as a dedicated flow in the reviewed inventory.** Flow: sign-up/sign-in → optional profile setup → Home. Allow skipping; explain limitations only where relevant.
3. **Player Profile expanded edit states — detailed fields/layouts not yet evidenced in the reviewed frames.** Developer Notes specify in-place expansion with Save/Cancel inside each section. Applies to Handicap, Home course & tees, Playing preferences, and Clubs & carry distances. Do not create separate edit pages by default.
4. **Club-bag setup/edit states — detailed UI not yet evidenced in the reviewed frames.** Required options: full bag setup; alternatively enter Driver and 7-iron carry and estimate the rest; make estimates editable; allow skipping all setup; do not nag. Treat as detail within profile setup/edit, not a duplicate profile page.

### Existing coverage / out of scope
Course selection and Start Round, Scorecard, Round Complete, Player Profile overview, Stats and Scores already exist. Junior/family UI is future scope, not adult V1. GPS/live-yardage behaviour is out of scope for this audit.

### Round-flow decisions
- Fairway hit / left miss / right miss records result, current club and GPS location where available.
- After a shot, advance directly to the next shot's yardage screen.
- Chequered flag is for hole 18 and opens Round Complete.
- End Round confirms finishing/retaining the round; Discard Round is separate.

This audit is the current working register. Do not repeat individual screen summaries; update the register only when new evidence or a user decision changes it.

## Kite authentication / first-run decisions — 13 October 2026

- Sign-up and returning-user sign-in both offer Google/Gmail, Apple, or email.
- First-run flow: sign-up/sign-in → optional Player Profile setup → Home.
- Profile setup can be skipped; explain a limitation only when relevant, and do not block Home.
- Bag setup offers full entry or a shortcut using Driver carry + 7-iron carry to estimate the rest. Estimates remain editable.
- The golfer may skip all bag setup. No nagging or repeated prompts; they decide when to update.
- Reuse Player Profile overview frame 295:5. Do not duplicate it.
- Adult Kite V1 only; junior/family UI is future scope. No Figma edits, app/code changes, or GitHub Actions during this curation pass.

Developer Notes frame 302:162 was checked on 13 October. It contains general UI, Stats/Scores, data-safety, QA and profile implementation notes, but no authentication-specific guidance.

Next: continue Priority 1 (Login/Sign-up) by settling only the remaining details: provider hand-off/error states, email sign-in/sign-up and forgotten-password recovery, and minimum fields for optional first-run profile setup. Do not re-ask settled decisions above. Check existing Figma coverage first and ask one focused question at a time.
### Authentication decision — email credentials
- **Decision (13 October 2026):** use email + password for email-based sign-up and returning-user sign-in (Option A). Include a **Forgot password?** recovery path.
- Continue to offer Google/Gmail and Apple as alternatives.
- This settles the email authentication method; it does not authorise implementation or Figma edits yet.

### Authentication layout decision — one screen, two modes
- **Decision (13 October 2026):** use one authentication screen with a **Log in / Create account** mode switch, not separate screens.
- Both modes offer Google/Gmail, Apple, and email + password. Log in includes **Forgot password?** recovery; Create account uses the new-account fields.
- Keep the interface concise and consistent with the existing Kite design system. This is a documented decision only; no Figma or app changes have been made.

### First-run profile prompt decision — 13 October 2026
- **Clarification:** do not omit profile setup entirely. After account creation/sign-in, actively offer the golfer a short Player Profile setup, with a clear **Skip for now** option.
- Keep authentication itself minimal. In the post-auth profile step, start with the minimum useful details (player name and handicap); make setup skippable and allow the golfer to complete/edit the remaining profile and bag details later.
- Skipping must still lead to Home, with no nagging or repeated prompts. Explain a missing detail only when it affects a feature.
- This preserves the agreed journey: sign-up/sign-in → optional profile setup → Home, while ensuring golfers are invited to add useful details rather than never being asked.

### Handicap in first-run setup — decision 13 October 2026
- Ask the golfer for their handicap during optional first-run Player Profile setup.
- Handicap is not compulsory: the golfer can skip that field and/or choose **Skip for now** for the whole setup, then continue to Home.
- Do not block account creation or use of Kite when handicap is unknown. Keep the value editable later in Player Profile; explain limitations only where a missing handicap actually matters.


### First-run setup layout — confirmed 13 October 2026
- Optional Player Profile setup should be a **short step-by-step flow**, rather than a single long screen.
- Keep a clear skip option at the relevant step and **Skip for now** for the overall setup. Skipping goes to Home and must not trigger nagging or repeated prompts.
- Preserve the previously agreed minimum: ask for player name and handicap (handicap optional); include home course/tees and optional bag setup in the steps as appropriate. Bag setup supports full entry or Driver + 7-iron carry estimates, editable later, and may be skipped entirely.
- Status: product decision recorded; no Figma or app changes made.


### First-run setup scope correction — confirmed 13 October 2026
- Do **not** include home course or preferred tees in the first-run onboarding flow; they are not needed at this stage.
- Keep the step-by-step setup focused on player name, optional handicap, and optional club-bag setup. Keep skip options and no repeated prompts.
- This removes those fields from onboarding only; it does not remove Home course & tees from the existing Player Profile.


### Club-bag step sequencing — confirmed 13 October 2026
- Show club-bag setup automatically as step two after personal details.
- Make its optional nature obvious and provide a clear **Skip** control; retain **Skip for now** for leaving onboarding altogether. Both routes continue to Home without repeated prompts.
- Bag options remain full entry or Driver + 7-iron carry to estimate other clubs; estimates can be edited later and the entire step can be skipped.


### Google / Apple authentication outcomes — confirmed 13 October 2026
- Success continues into Kite; new accounts are offered optional step-by-step profile setup.
- Cancellation returns to the same Log in / Create account screen without an error message.
- Failure shows a short, clear message and offers retry or another sign-in method.
- If the account already exists, guide the golfer to log in instead of creating a duplicate.
- Keep the flow within the single auth screen where practical; avoid unnecessary screens. No Figma or app changes made.


### Email authentication validation — confirmed 13 October 2026
- Email sign-up/login requires a valid email address and password.
- Account creation asks for password confirmation (enter the password twice).
- Use concise inline messages for invalid details, incorrect credentials and existing accounts, with a clear next action.
- Keep these states within the single Log in / Create account screen where practical; retain Forgot password recovery. No Figma or app changes made.


### Forgot-password recovery flow — confirmed 13 October 2026
- Forgot password opens a simple form asking for the email address.
- Send a password-reset email and show a neutral confirmation message that does not disclose whether an account exists for that address.
- The golfer follows the email link to reset their password and then returns to Log in. Keep the flow minimal; no Figma or app changes made.


### Email verification and guest play — decision / direction 13 October 2026
- Email/password users should be prompted to verify their email, but this **must not prevent them from playing golf**. Verification is a non-blocking reminder, with a resend option.
- No extra email-verification step is needed for Google or Apple sign-in in the Kite flow.
- Add a **Play without signing in** / guest path as the intended product direction. Do not force account creation before a golfer can start a round. Exact guest capabilities and whether guest data persists across sessions remain to be decided before implementation.
- This supersedes the earlier working assumption that sign-up is required to use Kite. Sign-in/account creation remains available for account-linked features.
- No Figma or app changes made.


### Welcome screen and round saving — confirmed 13 October 2026
- Add a **Welcome / Entry screen before the existing Home screen**; preserve Home as it is.
- Two paths: **Play without signing in** or **Sign in or create an account** (Google, Apple, or email/password).
- Guest golfers can use core play and retain rounds locally on their device, allowing them to finish and review a round without an account.
- Signing in/creating an account is the route to save rounds to the account and eventually access history across devices. Do not promise cross-device access before it is implemented.
- Never block a round or risk losing it because the golfer has not signed in. Email verification must remain non-blocking.
- Prioritise Welcome / Entry screen before the authentication flow in the missing-page register. Documentation only; no Figma/app changes and no Actions run.


### Guest-to-account round transfer — confirmed 13 October 2026
- When a guest later signs in or creates an account, offer to transfer their locally saved guest rounds into the account.
- Require explicit consent; do not upload or merge guest history silently.
- If declined, preserve guest rounds locally and allow continued play. Be clear that local-only rounds may not be available on other devices.
- Treat this as required behaviour for the guest-to-account flow; no Figma/app changes made.


### Welcome screen primary action — confirmed 13 October 2026
- **Play without signing in** is the prominent yellow primary button.
- **Sign in or create an account** is secondary.
- Rationale: quick, low-friction access to golf is Kite's first promise. Welcome / Entry sits before, and does not replace, the existing Home screen. No Figma/app changes made.


### Prefilled starter bag distances — user-provided baseline, 13 October 2026
The user supplied candidate defaults for a men's everyday amateur / approximately 15-handicap starter bag. Treat them as estimates, not measured or universal distances; keep carry and total separate and all values editable.

| Club | Carry (yd) | Total (yd) |
|---|---:|---:|
| Driver | 220 (provided range 215–225) | 236 |
| 3-Wood | 200 | 215 |
| 3-Hybrid | 185 | 197 |
| 4-Iron | 175 | 186 |
| 5-Iron | 160 | 169 |
| 6-Iron | 150 | 162 |
| 7-Iron | 140 | 154 |
| 8-Iron | 130 | 146 |
| 9-Iron | 118 | 136 |
| PW | 105 | 121 |
| GW | 95 | 104 |
| SW | 83 | 84 |
| LW | 72 | 75 |

Use these as candidate prefilled starter values. For Driver, 220 yd is the midpoint of the supplied 215–225 yd carry range. Keep the Driver + 7-iron custom estimate path and a clear skip option. No Figma/app changes made.


### Women's amateur starter-bag distance baseline — user-provided, 13 October 2026
A separate women's amateur candidate starter bag has been supplied. Ignore the LPGA pro columns. Ranges are approximate; the midpoint columns below are suggested single-value prefills (rounded to nearest yard), not claims about an individual golfer. Carry and total remain separate and editable.

| Club | Amateur carry range (yd) | Amateur total range (yd) | Suggested carry prefill (yd) | Suggested total prefill (yd) |
|---|---:|---:|---:|---:|
| Driver | 140–155 | 174–185 | 148 | 180 |
| 3-Wood | 125–135 | 150–165 | 130 | 158 |
| 5-Wood | 115–125 | 135–145 | 120 | 140 |
| 4-Hybrid | 105–115 | 125–135 | 110 | 130 |
| 5-Iron | 95–105 | 110–120 | 100 | 115 |
| 6-Iron | 88–98 | 100–110 | 93 | 105 |
| 7-Iron | 80–90 | 92–102 | 85 | 97 |
| 8-Iron | 72–82 | 84–94 | 77 | 89 |
| 9-Iron | 65–75 | 76–86 | 70 | 81 |
| PW | 58–68 | 68–78 | 63 | 73 |
| GW | 50–60 | 58–66 | 55 | 62 |
| SW | 42–50 | 46–54 | 46 | 50 |
| LW | 35–42 | 38–44 | 39 | 41 |

Offer this as a separate optional women's amateur starter profile alongside the men's everyday-amateur profile. Do not assume sex determines the golfer's distances; let users choose and edit freely. Ignore LPGA pro distances. No Figma/app changes made.


### Starter bag selection — use selected tee, confirmed 13 October 2026
- Choose the default starter-bag distance profile using the golfer's already-selected tee, rather than asking them to choose a men's/women's or longer/shorter profile.
- Reuse the tee selection in Start Round to avoid asking twice. Distances are initial estimates and remain editable.
- The exact mapping from selected tees to starter distance profiles still needs to be grounded in the current tee-selection/course context; do not assume tee colour universally maps to gender or exact ability.
- Keep Driver + 7-iron personalisation and full bag skip options. No Figma/app changes made.


### Automatic starter-bag creation — confirmed 13 October 2026
- Create the starter bag automatically when the golfer starts their first round, using the selected tee to choose the default distance profile.
- Do not require a separate bag-setup step during onboarding. The golfer can review/edit the generated bag later in the existing Player Profile.
- Keep all values editable, retain the Driver + 7-iron personalisation option and the ability to skip bag setup. Label distances as estimates, not measured values.
- Ground the tee-to-profile mapping in course/tee context; do not universally equate tee colour with gender or ability. No Figma/app changes made.


### Tee changes preserve personal club distances — confirmed 13 October 2026
- Changing tees updates course/playing yardages only. It must not overwrite or silently recalculate the golfer's personal club carry/total distances.
- Starter-bag defaults are used for initial creation only; subsequent tee changes preserve the golfer's saved, editable club distances.
- No Figma/app changes made.

### Club distance editing — carry-led total estimate with override — confirmed 13 October 2026
- Carry distance is the primary value the golfer edits; Kite estimates total distance from it.
- Allow manual override of total distance when the estimate is unsuitable. Distinguish estimated total from a golfer-overridden value where shown.
- Changing tees must not overwrite saved club distances. No Figma/app changes made.

### Club total-distance roll multipliers — user-provided ranges, 13 October 2026
Estimate total distance from carry using a multiplier by club category:
- Driver & fairway woods: **1.08–1.12** (example 1.10).
- Hybrids & long irons (3i–5i): **1.06–1.08** (example 1.07).
- Mid-irons (6i–8i): **1.04–1.06** (example 1.05).
- Short irons & wedges (9i–LW): **1.01–1.03** (example 1.02).
Golfer can override estimated total distance. The final default multiplier within each range remains to be confirmed. No Figma/app changes made.

### Default roll multipliers confirmed — 13 October 2026
Approved defaults for estimating total distance from carry:
- Driver & fairway woods: **1.10**
- Hybrids & long irons (3i–5i): **1.07**
- Mid-irons (6i–8i): **1.05**
- Short irons & wedges (9i–LW): **1.02**
These are estimates; golfers may override total distance. Tee changes do not overwrite personal club distances. The default-multiplier decision is settled. No Figma/app changes made.

### Guest first-round starter bag — confirmed 13 October 2026
- On a guest golfer's first round, create the starter bag automatically when they start the round, based on the selected tee; do not interrupt round-start with a bag-setup screen.
- Make the generated bag available to edit later in Player Profile/profile management. Use the confirmed category roll multipliers for estimated totals; preserve saved distances when tees change.
- This decision explicitly covers the first round without signing in. Signed-in first-round behaviour remains to be confirmed. No Figma/app changes made.

### Starter bag fallback — guest and signed-in first rounds, confirmed 13 October 2026
- The golfer has an optional opportunity to personalise their bag during first-run setup (for signed-in users).
- If they skip bag personalisation or no saved bag exists, automatically create a starter bag from the selected tee when they start their first round; do not interrupt round-start with another setup prompt.
- If a golfer already has a saved/personalised bag, preserve it and do not replace it with defaults. Guest golfers get the same automatic starter-bag fallback on their first round.
- Generated values remain editable later in Player Profile/profile management. No Figma/app changes made.

### Explain automatic starter-bag creation — confirmed direction, 13 October 2026
- If the golfer has not personalised a bag, tell them Kite will build a starter bag for them using the selected tee, with estimated club distances that can be edited later in Player Profile.
- Keep this brief and non-blocking; do not add a setup screen that delays the start of play. Exact wording/placement remains open. No Figma/app changes made.

### Account creation: own-bag option backed by starter set — confirmed 13 October 2026
- When a guest creates an account, offer them the option to build/personalise their own bag, supported by Kite's starter set of estimated distances.
- Let them use and edit the starter set or personalise their bag; do not require entering every club manually.
- Preserve existing guest rounds and personal club data where applicable. Guest-round transfer still requires explicit consent; do not silently discard bag/distance edits during account creation. No Figma/app changes made.

### Own club-bag setup offers two routes — confirmed 13 October 2026
When personalising a bag, offer:
1. **Full setup:** enter each club and distance individually.
2. **Quick setup:** enter Driver carry and 7-iron carry; estimate the remaining clubs/distances using the starter set.
Use confirmed category roll multipliers for estimated totals, allow total-distance overrides, and keep the setup optional/editable later in Player Profile. No Figma/app changes made.

### Quick Setup saves immediately; edit later — confirmed 13 October 2026
- After Driver and 7-iron carry are entered, generate and save the estimated bag immediately; no review/edit step before saving.
- Individual clubs/distances can be edited later in Player Profile. Keep estimates identifiable and allow manual total-distance overrides. No Figma/app changes made.

### Skipping bag personalisation — automatic starter bag on first round — confirmed 13 October 2026
- If bag personalisation is skipped entirely, create a starter bag automatically when the golfer starts their first round, based on the selected tee.
- Briefly explain that Kite is building a starter bag with estimated distances, without delaying play. Make the bag editable later in Player Profile and preserve any existing saved/personalised bag. No Figma/app changes made.

### Starter bag creation timing — confirmed 13 October 2026
- Generate default bag values once at the first round if the golfer has no saved bag.
- Later tee selections must not regenerate or reset club distances. Tee changes affect course yardages only.
- The golfer may edit the bag later in Player Profile. No Figma/app changes made.

### Welcome / Entry screen — no tagline — confirmed 13 October 2026
- No tagline or marketing slogan.
- Keep the screen minimal: Kite branding, yellow primary **Play without signing in**, and secondary **Sign in or create an account**.
- No feature tour or lengthy pre-play onboarding; Welcome / Entry comes before and does not replace Home. No Figma/app changes made.

### Welcome guest-route decision — 13 October 2026
- **Play without signing in** routes directly to **Start Round** (Figma frame 124:25), not Home.
- Reason: existing Home contains Stats and Scores; a guest choosing to play should go straight into round setup.
- Welcome remains before the existing Home; this changes only the guest primary-action destination. Signed-in/authenticated routing remains governed by the agreed auth and optional profile setup flow.
- Documentation only. No Figma edits, app/code changes, or GitHub Actions.

### Start Round course selector — proximity ordering (13 October 2026)
- Populate the selector from the full course catalogue available in Kite.
- Calculate distance from the golfer's current location to courses and show the closest course first by default; golfer can select another course.
- Location-unavailable fallback and the catalogue's storage/delivery mechanism remain to be verified; do not assume those implementation details.
- Documentation only; no Figma/app changes and no GitHub Actions.

### Start Round course selector — no-location fallback (13 October 2026)
- When location is available, order the full Kite course catalogue by distance, closest first, while allowing manual course selection.
- If GPS/location is unavailable or permission is denied, show the full catalogue alphabetically and allow manual selection. Starting a round must not depend on location permission.
- Documentation only; no Figma/app changes and no GitHub Actions.

### Start Round — course changes update tee choices (confirmed 13 October 2026)
- Changing the selected course refreshes the tee options to the tees available for that course.
- Choose a sensible default tee for the newly selected course where possible; allow the golfer to manually select another available tee.
- Do not preserve a selected tee if it is not offered at the new course.
- Tee changes affect course/playing yardages only; they must not reset or recalculate saved personal club distances or regenerate an existing bag.
- No Figma/app changes and no GitHub Actions.

### Start Round course selector — search and filtering (confirmed 13 October 2026)
- Provide a search field for the full course catalogue; filter results as the golfer types.
- With an empty search, retain nearest-first ordering when location is available and alphabetical ordering when it is unavailable/denied.
- Keep manual selection. On course change, update the available tees and choose a sensible default where possible; preserve personal club distances when tees change.
- No Figma/app changes and no GitHub Actions.

### Start Round course search — no-results state (confirmed 13 October 2026)
- When a query has no matches, display **“No courses found”** and provide a clear-search option.
- Avoid a blank results area; clearing the query restores the full catalogue in its applicable sort order.
- No Figma/app changes and no GitHub Actions.

### Start Round — persist last course and tee (confirmed 13 October 2026)
- Remember the golfer's last selected course and tee and preselect them for the next round when still valid.
- Keep both selections editable. Never restrict the golfer to the remembered course.
- If the course or tee is unavailable, fall back to the normal catalogue/tee-default behaviour.
- Retain location-based nearest-first sorting, alphabetical fallback when location is unavailable, and live search filtering.
- No Figma/app changes and no GitHub Actions.

### Start Round — GPS readiness and disabled-location state (confirmed direction, 13 October 2026)
- Live GPS yardages are core functionality; do not start a round without the GPS/location capability needed for live yardages.
- If location is disabled, show **“Location disabled”** and an **“Enable in Settings”** action/instruction.
- Distinguish disabled permission/services from an active GPS fix attempt or weak signal, and provide appropriate recovery/retry guidance.
- Whether course/tee setup is available while GPS acquires a fix, before Start Round is enabled, remains open.
- No Figma/app changes and no GitHub Actions.

### Start Round — GPS acquiring state (confirmed 13 October 2026)
- If location is enabled but a usable fix is not ready, show **“Finding GPS…”** and a retry option.
- Keep the golfer on Start Round until GPS is ready; do not start a round before live yardages can work.
- Distinguish this from disabled location, which shows **“Location disabled”** and **“Enable in Settings”** guidance.
- No Figma/app changes and no GitHub Actions.

### In-round GPS loss — keep round usable (confirmed 13 October 2026)
- If GPS drops mid-round, preserve the active round and score-entry controls.
- Show **“GPS signal lost — trying to reconnect”** and attempt recovery.
- Pause live yardage updates until a usable fix returns, then resume.
- Temporary GPS loss must not discard or block the round.
- No Figma/app changes and no GitHub Actions.

### Yardage screen — GPS accuracy warning only when needed (confirmed 13 October 2026)
- Keep the live-yardage UI clean with no always-visible GPS accuracy indicator.
- Display a warning only when GPS accuracy becomes poor enough to affect the reliability of yardages.
- Maintain separate states for location disabled, GPS acquiring, and GPS signal lost.
- No Figma/app changes and no GitHub Actions.



### Player Profile — Handicap editing decision (13 October 2026)
- Handicap editing is simple manual entry in the existing inline-expanded section.
- Allow the golfer to change the handicap number and choose Save or Cancel.
- Do not add source-selection controls for player-entered, calculated practice, or officially verified handicap to this V1 editor.
- This is a documented interaction decision; the expanded editor still needs to be represented/verified in Figma and QA'd when built. No Figma/app changes made.


### Profile Q&A — bag editor layout (13 October 2026)
- Compact editable club list for quick changes; each row opens detailed controls when needed.
- Show carry and total distances; carry is primary, total is estimated unless overridden, and estimates are labelled.
- Use inline Save/Cancel. Detailed Figma state still requires build/QA.
