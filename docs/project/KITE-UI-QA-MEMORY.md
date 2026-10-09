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

**Not yet answered:** After a player edits a previously saved scorecard and taps Save, should Kite save immediately and then show a brief “Changes Saved” pop-up using the shared component, or show a confirmation before saving?

**Suggested default, awaiting user confirmation:** Save immediately, then show a brief “Changes Saved” pop-up. Editing already requires an explicit Edit Scorecard action, so another pre-save confirmation may add unnecessary friction.

## Working protocol

- Preserve the decisions above; do not ask them again unless new evidence exposes a genuine conflict.
- Continue asking one genuine unresolved question at a time.
- Treat these as product/design decisions, not proof that Figma has already been edited or that implementation exists.
- Before implementation, inspect the existing Figma screens and code and preserve user edits. Record implementation status separately from product decisions.
- Do not manually run or dispatch GitHub Actions unless explicitly requested or genuinely needed.
