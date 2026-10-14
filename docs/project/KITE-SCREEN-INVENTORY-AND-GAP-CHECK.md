# Kite Screen Inventory & Gap Check

**Reviewed:** 14 October 2026  
**Figma file:** UiDo — Brand & Product Design System  
**Figma file key:** 6peEDBx1XNqpZ3UAeUlHyI  
**Product page:** 02 — Product UI (page 6:2)  
**Scope:** Inventory of current top-level screen/state frames and a gap check against the confirmed family/player-management decisions. Read-only Figma inspection; no designs or workflows were changed.

## Summary

The existing file contains a substantial adult Kite V1 product flow: entry/authentication, first-run profile and bag setup, start round, yardage, scorecard, end round, scores/stats, and adult player-profile editing states.

The new joint scorecard frame is present and lays out four players across 18 holes, with round totals and round statistics. This closes an important **four-player scorecard display** gap.

The family/player flow is still missing its connective screens: family roster, player switching/selection, adding a junior or guest, multi-player setup with a tee for each player, the junior laptop dashboard and junior sign-in states. The current End Round screen is still a single-player summary. The confirmed update is one similar group state card with result summaries for up to four players and a way to open the joint scorecard.

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

### Missing for the first useful family-player design/build

1. **Family player roster/management screen.** There is no screen listing the family’s adult and junior profiles, guest names, or management actions. Keep the current profile overview; add the roster and selection state rather than duplicating profile pages.
2. **Switch-player state.** Player Profile has a Switch Player control, but no player picker, selected-player state, or path back to the profile.
3. **Add/select player flow.** Start Round has an Add / Select Player control, but no picker for saved family profiles or saved guests, no add-existing-Kite-account-to-family-profile state, and no reusable guest name/handicap create/edit state.
4. **Create junior while setting up a round.** No inline junior profile form exists. The junior profile must remain saved if round setup is cancelled.
5. **Junior sign-in and account setup.** Existing auth is email/account oriented. Missing junior-specific parent-created username, parent-set password, junior-chosen four-animal PIN setup, and parent-managed password/PIN reset states.
6. **Junior laptop dashboard.** No desktop/laptop frame exists for the junior’s display name, points, badges, current handicap, past rounds, and scorecards. Junior can see all participants’ scores but cannot edit saved scorecards.
7. **Multi-player Start Round.** Current Start Round shows one current player and one Add / Select Player control. It has one Tee section at round level. The confirmed flow needs up to four players, a tee choice for each player, and one shared scoring format.
8. **Multi-player End Round.** Current End Round is headed “Your Round” and shows one player’s result. It needs a parent-facing saved-round summary for all participants, with access to the joint scorecard and score editing.
9. **Junior profile management states.** The adult profile edit sections provide a useful base, but there are no family-selected junior profile states showing parent full access, junior edit permissions, and the different handicap permissions.
10. **Removal/deactivation of a junior profile.** No family-player removal confirmation offers the confirmed choices: remove sign-in and retain history, or delete the profile and history.

### Player Profile / bag states to finish

- **Club categories should be offered in setup popups, not used to group the main list.** Keep the Manage Bag list ungrouped; provide Woods, Hybrids, Irons, and Wedges as options within Add Club and bag setup popups.
- **Existing club carry/total editor state is not shown.** The add-club popup supports blank carry, estimated total, and manual total; a detailed edit state is still needed for existing club rows.
- **Carry-change confirmation is not shown.** Add the confirmed prompt/state for updating the total after carry changes.
- **Club-limit warning popup is not shown.** The agreed bag count is 13 non-putter clubs plus a separate putter. When exceeding the competition limit, show a non-blocking reminder that the Rules of Golf allow 14 clubs total including the putter; adding the club is not prevented.

### Later, not a blocker for the first family-player screens

- Adult conversion flow: parent starts and completes the transfer when ready; preserve round history; create a separate adult account managed by its owner. The parent’s access after separation is still unanswered.
- Future “fun” scoring formats and rules remain undecided.
- Full co-parent/account-link management can be kept as a small extension to the family roster: an adult with an existing Kite account can be added to a family profile; a no-account adult is a guest. Avoid creating an unlinked guardian-management subsystem.

## Suggested first build slice

1. Add a family roster/player picker reachable from the existing Switch Player and Add / Select Player controls.
2. Design inline Add Junior and Add Guest states, including saved guest name and handicap.
3. Expand Start Round to a maximum of four participants with per-player tee selection and one shared format.
4. Use the existing four-player scorecard frame; update End Round to show all participants and parent edit access.
5. Design the junior sign-in and laptop dashboard states.

This is a structural screen and interaction gap check from Figma frame/layer inspection and the current decision log. It is not a pixel-level visual QA review. No Figma changes or GitHub Actions were run.


### Round recovery — Save failure
- **Save failure/retry state is not shown.** Preserve the round and entered scores on the device after a save failure and provide a clear retry path so the golfer does not lose their work.


### Round recovery — Resume interrupted round
- **Resume state is not shown.** An in-progress round should always remain resumable, including after Kite closes or the phone restarts. Retain current round state and offer resume when the app reopens.
