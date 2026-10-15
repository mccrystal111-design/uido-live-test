# Kite Screen Inventory & Gap Check

**Reviewed:** 15 October 2026  
**Figma file:** UiDo — Brand & Product Design System  
**Figma file key:** 6peEDBx1XNqpZ3UAeUlHyI  
**Product page:** 02 — Product UI (page 6:2)  
**Scope:** Inventory of current top-level screen/state frames and a gap check against the confirmed family/player-management decisions. Read-only Figma inspection; no designs or workflows were changed.

## Summary

The existing file contains a substantial adult Kite V1 product flow: entry/authentication, first-run profile and bag setup, start round, yardage, scorecard, end round, scores/stats, and adult player-profile editing states.

The new joint scorecard frame is present and lays out four players across 18 holes, with round totals and round statistics. This closes an important **four-player scorecard display** gap.

The family/player feature set and prior decisions remain part of the first Kite V1 release, documented in the family/player Q&A. The user has deferred rebuilding family/junior screens for the current build slice. The adult multi-player round flow remains required: an Add Player popup (Player Name, Handicap, Tee) supporting up to four players, a populated four-player Start Round state, and a four-player Round Complete card with joint-scorecard access. The current End Round screen is still a single-player summary. The confirmed update is one similar group state card with result summaries for up to four players and a way to open the joint scorecard.

## Screens and states already in Figma

Node IDs link to the corresponding Figma frame.

### Core Kite and golf-round screens

| Screen/state | Figma frame |
|---|---|
| Front Screen — Navy White — Construction V1 | [93:2](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=93-2) |
| Start Round — Navy White — V1 | [124:25](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=124-25) |
| Yardage — Tee Shot | [190:136](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=190-136) |
| Yardage — Par 3 Approach (three variants) | [219:2](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=219-2), [229:143](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=229-143), [255:267](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=255-267) |
| Single-player 18-hole scorecard — V1 | [261:30](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=261-30) |
| Joint four-player scorecard — V1 | [438:148](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=438-148) |
| End Round — V1 | [261:125](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=261-125) |
| Scores — V1 | [302:121](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=302-121) |
| Stats — V1 | [302:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=302-5) |

The joint scorecard frame shows four player names/handicaps, four score columns, front and back nines, round totals, round statistics, and an End Round action. The confirmed round cap is four total players, including the signed-in golfer; family players and saved guests count toward that cap.

### Player profile and bag states

| Screen/state | Figma frame |
|---|---|
| Player Profile overview, including Switch Player control | [295:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=295-5) |
| Handicap edit | [408:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=408-5) |
| Home course and tees edit | [409:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=409-5) |
| Playing preferences edit | [409:41](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=409-41) |
| Manage Bag edit/list | [410:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=410-5) |
| Inactive clubs section, 12/13 clubs plus putter | [411:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=411-5) |
| Remove club confirmation | [411:249](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=411-249) |
| Edit club abbreviation popup | [420:142](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=420-142) |
| Make club inactive confirmation | [429:15](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=429-15) |
| Add club popup | [429:146](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=429-146) |

The developer notes say profile sections expand in place, with Save and Cancel kept inside the edited section. The current profile overview shows a player-switch affordance but no switcher or family roster state.

The bag design already shows the 13-club count plus separate putter, carry/total columns, a separate putter row, add-club, abbreviation editing, inactive/reactivate handling, and removal confirmation. The add-club state starts carry blank and offers an estimated total with manual total entry.

### Welcome, authentication, account creation, and first-run setup

| Screen/state | Figma frame |
|---|---|
| Welcome / Entry — V1 | [353:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=353-5) |
| Authentication — V1 | [354:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=354-5) |
| Create Account — V1 | [357:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=357-5) |
| Password Reset — Email Form | [357:44](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=357-44) |
| Password Reset — Neutral Confirmation | [357:68](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=357-68) |
| Email Verification Reminder | [357:88](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=357-88) |
| Authentication — Provider Failure | [357:111](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=357-111) |
| Log in — Incorrect Credentials | [358:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=358-5) |
| Create Account — Existing Email | [358:42](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=358-42) |
| Create Account — Invalid Email | [358:82](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=358-82) |
| Create Account — Password Mismatch | [358:121](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=358-121) |
| First-run Profile — Personal Details | [359:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=359-5) |
| First-run Bag Setup — Choose Route | [359:34](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=359-34) |
| Bag Setup — Quick Setup | [359:62](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=359-62) |
| Bag Setup — Full Entry | [359:93](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=359-93) |
| Guest-to-Account — Transfer Consent | [359:156](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=359-156) |
| Guest-to-Account — Keep Local Rounds | [359:180](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=359-180) |
| Guest-to-Account — Transfer Complete | [359:200](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=359-200) |

### Supporting/design-reference frames (not product flow screens)

- Developer Notes — Q&A Handoff: [302:162](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=302-162)
- UI Style Menu — V1: [334:5](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=334-5)
- Kite navigation icon study: [98:19](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=98-19)
- UiDo Yardage source recreation and Hawk Home first draft are legacy/reference work, not current Kite product screens: [8:24](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=8-24), [21:2](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo?node-id=21-2)

## Gap check against confirmed family/player requirements

### Family/player screens missing from Figma (V1 scope; current build deferred)

1. **Family player roster/management screen.** There is no screen listing the family’s adult and junior profiles, guest names, or management actions. Keep the current profile overview; add the roster and selection state rather than duplicating profile pages.
2. **Switch-player state.** Player Profile has a Switch Player control, but no player picker, selected-player state, or path back to the profile.
3. **Add/select player flow.** Start Round has an Add / Select Player control, but no picker for saved family profiles or saved guests, no add-existing-Kite-account-to-family-profile state, and no reusable guest name/handicap create/edit state.
4. **Create junior while setting up a round.** No inline junior profile form exists. The junior profile must remain saved if round setup is cancelled.
5. **Junior sign-in and account setup.** Existing auth is email/account oriented. Missing junior-specific parent-created username, parent-set password, junior-chosen four-animal PIN setup, and parent-managed password/PIN reset states.
6. **Junior laptop dashboard.** A frame exists at `445:25`, but the user reports removing the family/junior screen set; this is the lone family/junior frame still on the page and its retention needs confirmation. If retained, it must show the agreed dashboard content and use the locked Kite logo and palette. Junior can see all participants’ scores but cannot edit saved scorecards.
7. **Junior profile management states.** The adult profile edit sections provide a useful base, but there are no family-selected junior profile states showing parent full access, junior edit permissions, and the different handicap permissions.
8. **Removal/deactivation of a junior profile.** No family-player removal confirmation offers the confirmed choices: remove sign-in and retain history, or delete the profile and history.

### Adult V1 screens and interaction gaps (current Figma review: 15 October 2026)

1. **App Settings hub.** No Settings screen is present. The content and popup behavior are now defined in the App Settings Q&A section below.
2. **Add Player and group setup.** Add Player popup is absent; build fields for Player Name, Handicap, and Tee, capped at four total players, plus a populated four-player Start Round state showing each tee and the shared scoring format.
3. **Group Round Complete.** End Round is still a single-player summary. Build a similar group result card for up to four players with access to the joint scorecard.
4. **Club editing.** Add the club categories in Add Club and bag setup popups (keep the main bag list ungrouped); add detailed carry/total editing for existing clubs and a confirmation when changing carry updates total.

Already present in Figma: the joint four-player scorecard `438:148`, club-limit reminder `445:22`, and round-save-failure popup `445:23`. The save-failure behavior still needs to preserve round data on-device and support retry; this is implementation work in addition to the existing popup.

### Player Profile / bag states to finish

- **Club categories should be offered in setup popups, not used to group the main list.** Keep the Manage Bag list ungrouped; provide Woods, Hybrids, Irons, and Wedges as options within Add Club and bag setup popups.
- **Existing club carry/total editor state is not shown.** The add-club popup supports blank carry, estimated total, and manual total; a detailed edit state is still needed for existing club rows.
- **Carry-change confirmation is not shown.** Add the confirmed prompt/state for updating the total after carry changes.
- **Club-limit warning popup is not shown.** The agreed bag count is 13 non-putter clubs plus a separate putter. When exceeding the competition limit, show a non-blocking reminder that the Rules of Golf allow 14 clubs total including the putter; adding the club is not prevented.

### Unresolved or exploratory family-player decisions

- Adult conversion flow: parent starts and completes the transfer when ready; preserve round history; create a separate adult account managed by its owner. The parent’s access after separation is still unanswered.
- Future “fun” scoring formats and rules remain undecided.
- Full co-parent/account-link management is in the confirmed V1 family scope and can be kept as a small extension to the family roster: an adult with an existing Kite account can be added to a family profile; a no-account adult is a guest. Avoid creating an unlinked guardian-management subsystem.

## Adult V1 build list — family/junior screens deferred

### Screens to build
- [ ] **Add Player popup:** Player Name, Handicap, Tee; cap the round at four total players, including the signed-in golfer.
- [ ] **Four-player Start Round state:** show all four players, each player's tee, and the shared round scoring format.
- [ ] **Four-player Round Complete card:** follow the existing single-player result-card pattern, summarize each player's result, and link to the joint scorecard.
- [ ] **App Settings hub:** grouped rows for yards/metres and Celsius/Fahrenheit; account email/password and linked sign-in management; Log Out; Delete Account with confirmation; About rows: Terms of Use — View, Privacy Policy — View, App Version — V1, Software Licences — View; Support items as defined in the App Settings Q&A. Rows open lightweight selection or information popups.
- [ ] **Terms of Use view:** readable destination opened from the Settings row.
- [ ] **Privacy Policy view:** readable destination opened from the Settings row.
- [ ] **Software Licences view:** readable destination opened from the Settings row.
- App Version is displayed inline as “V1”; no separate version screen is needed.

### Player Profile and Bag updates
- [ ] **Club category choices:** offer Woods, Hybrids, Irons, and Wedges within Add Club and bag setup popups. Keep the main Manage Bag list ungrouped.
- [ ] **Edit an existing club:** open detailed carry and total controls from each editable club row. New carry starts blank; estimate total automatically after entry and allow manual total entry. Putter has no carry or total fields.
- [ ] **Carry-change confirmation:** when carry is changed for an existing club, show a prompt to update its total.

### Round behavior to finish
- [ ] **Save-failure recovery:** popup `445:23` exists; retain in-progress round data on-device and allow the player to retry saving later.
- [ ] **Interrupted-round recovery:** restore the unfinished round directly when Kite opens. Do not add a recurring resume-choice popup.

### Already present — retain and reuse
- Four-player joint scorecard: `438:148`.
- Non-blocking club-limit reminder: `445:22`.
- Round-save-failure popup: `445:23`.

Family/junior requirements remain part of V1 and are recorded in `KITE-FAMILY-PLAYER-MANAGEMENT-QA.md`; their screens are deferred. Do not recreate or build those screens until the user asks to resume that work.

This is a structural screen and interaction gap check from Figma frame/layer inspection and the current decision log. It is not a pixel-level visual QA review. No Figma changes or GitHub Actions were run.


### Round recovery — Save failure
- Popup `445:23` is present. Implement the confirmed behavior behind it: retain the round and entered scores on-device after a save failure and allow retry.


### Round recovery — Resume interrupted round
- Keep an in-progress round resumable after Kite closes or the phone restarts. When Kite opens with an unfinished round, take the golfer directly back into it; implement this as round restoration, not a recurring resume prompt.


### Round recovery — Immediate resume behavior
- When Kite opens with an unfinished round, take the golfer straight back into it rather than showing a recurring resume prompt. Let the golfer choose to close or leave it from the round flow; preserve resumability.
- No resume-choice popup is present in the current Product UI structure. Do not add one; the confirmed behavior is to reopen directly into the unfinished round.


### App Settings — V1 Q&A and screen gap (confirmed 15 October 2026)
- No App Settings screen or nested settings state is currently present in Product UI; a dedicated App Settings hub is still missing.
- Keep it lightweight: grouped rows show current values and open small selection or information popups as appropriate.
- General: yards/metres (also available in Player Profile Playing Preferences) and Celsius/Fahrenheit. Do not include handedness, notification controls, or a language selector in V1.
- Account: view/change sign-in email and password; show and manage linked sign-in providers; Log Out at the bottom; Delete Account with a clear confirmation step.
- About: Terms of Use — View; Privacy Policy — View; App Version — V1; Software Licences — View.
- Support: Help/Contact Support and Rate Kite.


### Shared visual requirements for new V1 screens
- Reuse the approved Kite logo lockup and symbol from the Figma brand source; do not recreate or substitute the mark. The lockup is the thin white hex golf symbol beside the lowercase “kite” wordmark in Sora ExtraLight, with the i-dot removed.
- Use Sora typography and match the hierarchy in the existing approved Kite screens and UI Style Menu.
- Use the approved Kite palette: deep navy `#0E1C2B`, warm off-white `#F4F1E6`, and yellow `#FFCC00`; reserve orange for secondary/accent use.
- Match spacing, insets, and alignment to the UI Style Menu and adjacent approved Kite screens. This gap list does not establish a separate numeric spacing scale.
- Apply these standards to the App Settings hub, Add Player popup, populated four-player Start Round state, and four-player Round Complete card.
- Mark a visual state complete only after inspecting the rendered Figma screen at actual size; structural presence alone is not visual approval.
