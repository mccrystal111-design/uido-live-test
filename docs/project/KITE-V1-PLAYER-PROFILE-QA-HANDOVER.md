# Kite V1 Player Profile Editing Q&A — Handover

**Updated:** 13 October 2026  
**Purpose:** Continue the focused Q&A defining the editing states for the existing Kite adult V1 Player Profile. This is design curation and decision logging, not implementation.

## Current task
We are defining what happens when each editable section on the existing Player Profile expands. Ask one genuine, focused question at a time. Check the current Figma and the decision log before asking anything; never ask the user to repeat settled decisions. After each answer, update the GitHub decision log and QA memory, then verify each write by fetching the file again.

## Relevant links
- **Figma file:** https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo-%25E2%2582%25AC-Brand---Product-Design-System?node-id=6-2&p=f&t=3oIfwrUpM1RdoZkX-0
- **Product UI page:** node `6:2`
- **Player Profile overview:** frame `295:5`
- **Developer Notes / Q&A Handoff:** frame `302:162` (profile implementation notes include inline expansion with Save/Cancel)
- **Decision log:** https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/KITE-V1-UI-CONVERSATION-DECISION-LOG.md
- **QA memory:** https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/KITE-UI-QA-MEMORY.md
- **New Chat Starter:** https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/NEW-CHAT-STARTER.md

## Settled decisions in this Q&A

### 1. Handicap
- Inline expanded editor.
- Simple manual entry: golfer changes the handicap number and chooses Save or Cancel.
- Do not add source-selection controls for calculated practice handicap or official verification in this V1 editor.
- Detailed accepted numeric range/validation is not yet defined.

### 2. Home course & tees
- Edit both the home course and preferred tees for that course.
- These are profile defaults; Start Round still allows a different course/tee per round.
- Changing course refreshes available tee options. Do not retain a tee unavailable at the new course.

### 3. Playing preferences
- Allow changing units: yards/metres.
- Include relevant app display preferences supported by Kite V1 only; do not invent unsupported gameplay settings.
- Use inline Save/Cancel.

### 4. Clubs & carry distances / Manage bag
- Use a compact editable list for quick changes, with each club row opening more detailed controls when needed.
- Show carry and total distances clearly.
- Carry is the primary value. Total is estimated unless manually overridden; identify estimated values.
- Keep inline Save/Cancel; routine distance edits should not require a separate page per club.

## Existing product rules to preserve
- Existing profile overview is frame `295:5`; do not create a duplicate overview.
- Existing Developer Notes specify inline section expansion with Save/Cancel.
- Personal club carry/total distances are editable. Total distance is estimated from carry using the agreed club-category multipliers unless manually overridden.
- Tee changes affect course/playing yardages only; do not overwrite personal club distances or regenerate an existing saved bag.
- Missing statistics/data must not be misrepresented as zero. Keep player-entered handicap distinct from any future calculated practice handicap in product logic, even though the V1 editor here is simple manual entry.
- Adult Kite V1 only; junior/family UI is future scope.

## Current status
- The decisions above are documented in the Decision Log.
- The bag-editor layout decision is also recorded in QA Memory.
- The expanded editor states still need to be represented/verified in Figma and QA'd when built. No Figma edits or app/code implementation have been made in this Q&A.
- No GitHub Actions have been run.

## Recommended next question
Continue the **Manage bag** editor details. A useful next decision is what detailed controls open when a club row is tapped: club name/type, carry distance, total distance, whether total is estimated or manually overridden, and add/remove club actions. Keep it to one question, offering a concise recommended option.

## Working rules for the next chat
1. Read the latest Decision Log and QA Memory before proceeding; this handover is an index, not a substitute for the latest source of truth.
2. Check relevant Figma frames/nodes before claiming something is missing.
3. Ask one question at a time and accept a direct natural-language answer.
4. After every answer, update the Decision Log and QA Memory sequentially using fresh file SHA values, then re-fetch to verify.
5. If a GitHub write fails, state that honestly and do not claim it was saved. Use the available GitHub connector directly; do not hand off to Work mode.
6. Do not edit Figma, implement app code, or run GitHub Actions unless explicitly authorised.
7. Avoid repeated summaries and speculative questions; preserve decisions faithfully.
