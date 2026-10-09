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
