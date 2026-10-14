# Kite V1 Player Profile Editing Q&A — Handover

**Updated:** 14 October 2026  
**Status:** Focused editing Q&A complete; ready for the Figma page-builder stage. This record summarizes confirmed product decisions and the current Figma comparison. No Figma edits or app/code implementation were made.

## Current task and working rules

Curate the adult Kite V1 editing states for the existing Player Profile. The Q&A decisions are recorded in the Decision Log and QA Memory. Before building, review both records and this Figma comparison. Preserve existing work and use the existing profile overview; do not create duplicate pages by default.

Do not edit Figma or run GitHub Actions unless explicitly requested. Any later visual changes must be pixel checked in Figma before approval. Keep implementation status separate from product decisions.

## Relevant links

- **Figma file:** https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo-%25E2%2582%25AC-Brand---Product-Design-System?node-id=6-2&p=f&t=3oIfwrUpM1RdoZkX-0
- **Product UI node:** `6:2`
- **Player Profile overview:** frame `295:5`
- **Developer Notes / Q&A Handoff:** frame `302:162`; profile notes text node `318:48`
- **Initial full bag setup:** frame `359:93`
- **Decision Log:** https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/KITE-V1-UI-CONVERSATION-DECISION-LOG.md
- **QA Memory:** https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/KITE-UI-QA-MEMORY.md

## Confirmed profile editing decisions

### Handicap
- Expand the existing section in place.
- Manual handicap number entry with **Save** and **Cancel**.
- Do not add source-selection controls for calculated practice or official handicap in this V1 editor.
- Numeric range and validation details remain open only if implementation requires them.

### Home course & tees
- Allow editing both home course and preferred tees.
- These are profile defaults; Start Round remains editable for an individual round.
- Changing course refreshes available tees and must not retain a tee unavailable at the new course.

### Playing preferences
- Allow yards/metres and relevant display preferences supported in Kite V1.
- Do not invent unsupported gameplay settings.
- Use inline **Save** and **Cancel**.

### Clubs & carry distances / Manage bag
- Use a compact editable bag list for quick changes, with each club row opening detailed controls.
- Group the club list under **Woods, Hybrids, Irons, and Wedges**, using Kite's curated club-type list.
- Allow up to **13 non-putter clubs plus a separately listed putter** in the bag. Show the non-putter count, for example **12/13**.
- If the player attempts to exceed the competition limit, show a warning popup that the Rules of Golf allow no more than **14 clubs total, including the putter** (Rule 4.1b). This is a reminder, not a hard block; do not prevent adding the club. [USGA Rules FAQ](https://www.usga.org/RulesFAQ/rules_answer.asp?FAQidx=246&Rule=0&Topic=9).
- Include the putter automatically during initial setup and display it as its own row. Do not show carry or total fields for the putter.
- For other clubs, detailed controls include club type, carry distance, and total distance. Carry is the primary value.
- Estimate total automatically from carry and clearly identify estimated values. Allow manual total entry.
- When carry changes, show a pop-up asking whether to update total. Offer updating to the new estimate or keeping the current total; do not silently replace a manual total.
- A newly added club starts with blank carry and waits for golfer entry. Once carry is entered, show the estimated total; manual entry remains available.
- Removing a club requires a confirmation pop-up. Show the bag count and retain the club/shot history when the club leaves the active bag.
- Keep the existing section-level **Save** and **Cancel** pattern; routine edits do not require a separate page per club.

## Existing product rules to preserve

- Player Profile is frame `295:5`; reuse it rather than creating a duplicate overview.
- Developer Notes specify that profile sections expand in place and contain their own Save/Cancel controls. Profile data shown in the design is illustrative; implementation must connect it to the selected player record.
- Existing Core decisions preserve relevant equipment and club/carry history. A bag/default change must not rewrite historical shots or saved rounds.
- Tee changes affect course/playing yardages only; they must not reset personal club distances or regenerate a saved bag.
- Adult Kite V1 only; junior/family UI is future scope.

## Figma comparison — inspected 14 October 2026

### Existing coverage
- The rendered `295:5` Player Profile shows the existing player summary, handicap card, and collapsed Home course & tees, Playing preferences, and Clubs & carry distances cards. Reuse this overview.
- The `295:5` layer tree contains summary/collapsed sections only; it does not show the agreed expanded editing states.
- The rendered Developer Notes at `302:162` and profile detail node `318:48` confirm inline expansion with Save/Cancel inside the edited section and illustrative profile data.
- The existing Full Bag Setup frame `359:93` has a club selector with carry/total columns and a Save Bag action. This is initial setup, not the post-setup Manage Bag interaction. It does not demonstrate category-grouped editable rows, the separate automatic putter row, bag count, detailed club-row controls, or removal confirmation.
- The current profile summary says “13 clubs · Manage bag”; reconcile this label with the agreed 13-club allowance plus separately counted putter.

### Work still needed in the page builder
Create/represent and visually QA the expanded inline states for:
1. Handicap manual entry with Save/Cancel.
2. Home course and dependent tee selection.
3. Playing preferences for units and supported V1 display settings.
4. Manage Bag with category-grouped rows, 13-club count, putter row, per-club details, estimated/manual total states, carry-change prompt, blank newly added club state, and add/remove confirmation states.

Use the current profile overview and existing design system. Treat Full Bag Setup as reference for initial setup only; do not assume it satisfies post-setup Manage Bag. The states above are not yet evidenced in the inspected rendered frames. No Figma edits or GitHub Actions were performed for this Q&A.

## Next step

When authorized to build, create the missing expanded states within the existing Player Profile interaction pattern, compare them against the agreed decisions and Developer Notes, then render and inspect the actual Figma pixels before presenting them as approved.
