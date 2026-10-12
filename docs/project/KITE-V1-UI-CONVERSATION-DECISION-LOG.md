# Kite V1 UI — Conversation & Decision Log

**Purpose:** Durable record of decisions and answers from the Kite V1 UI page-inventory conversation. This is a conversation-specific log, separate from the broader `KITE-UI-QA-MEMORY.md`.

**Working rule — keep this file current:** After every new user answer or decision in this ongoing conversation, update this file in GitHub before moving to the next question. Record the answer faithfully, distinguish confirmed decisions from open questions, and preserve superseded decisions in the history rather than silently deleting them. Do not claim an update was saved unless the GitHub write succeeds.

## Scope and collaboration rules

- This task is to curate the missing **Kite adult V1 UI pages**, reviewing the existing designs first.
- Do not mix in UiDo product scope or junior/Kite Kids UI at this stage.
- The user already knows the GPS/live-yardage experience; do not review those screens as part of this task.
- Do not jump to proposing missing pages before reviewing the relevant existing screen and understanding its current purpose and interactions.
- Ask about genuine uncertainties in the existing screens; do not ask the user to repeat decisions already made or information visible in the designs.
- Review one screen/flow at a time, collaboratively. Only add genuine gaps to the missing-page list after the existing coverage is understood.
- Number genuine missing pages by priority, beginning at 1. Do not treat tentative suggestions as confirmed gaps.
- Do not edit Figma or implement code unless explicitly asked.
- Do not run GitHub Actions.
- The user strongly dislikes losing answers or having to repeat decisions. This log is the durable source of truth for this conversation.

## Confirmed decisions

### D-01 — Authentication is the first identified missing UI flow
The existing Home screen includes a profile area at the top for a returning, already-logged-in user. After reviewing that context, the user identified Login and Sign-up as the first missing flow.

### D-02 — Keep authentication/sign-up extremely simple
Preferred sign-up options: Google/Gmail login, Apple login, and email. Returning users should be able to sign in using the same providers or email. The goal is low-friction account creation, not a long registration form.

**Important wording:** The user said sign-up should be the approach. The assistant subsequently recorded account creation as required before using Kite; the user did not challenge that in the conversation. Treat required sign-up as the current working decision, but do not re-ask unless a genuine contradiction emerges.

### D-03 — Player Profile setup follows sign-up
The user thinks it is best to complete the Player Profile so Kite's functionality works. Intended onboarding flow:
1. Sign up / log in.
2. Complete or skip Player Profile setup.
3. Enter Home.

Reuse the existing Player Profile design; do not assume a separate new Player Profile page is required.

### D-04 — Allow skipping profile setup
The user explicitly allows golfers to skip profile setup. Full functionality may not work if they skip relevant information. Do not force completion of every profile field.

### D-05 — Club-bag setup choices
Offer a full club-bag setup. If the golfer skips the full bag setup, ask for two anchor distances:
- Driver carry distance.
- 7-iron carry distance.

Use those two distances to estimate the remaining clubs in the bag. These estimates are only a starting point; golfers may get odd club suggestions and should be able to correct them.

### D-06 — Allow skipping the entire bag setup
The golfer may skip the entire bag/profile bag setup if they wish. Accept that choice. Do not pester them, repeatedly prompt them, or keep reminding them to complete the bag. Let them choose when to return and update it.

### D-07 — Bag data must remain editable
Golfers can choose when to update their bag and club distances later. Estimated clubs/distances must be editable. The existing Player Profile is the intended place to access profile and bag management, subject to verification of the actual interactions.

### D-08 — Existing Player Profile screen is present
Figma file: `6peEDBx1XNqpZ3UAeUlHyI`
Existing Player Profile frame: `295:5`
The screen already exists and should be reviewed/reused rather than proposing a duplicate page. Previous conversation context describes it as covering handicap, home course/tees, playing preferences and club-bag summary/manage access. Its complete interaction behaviour has **not** yet been verified in this conversation.

### D-09 — Preserve decisions and update this log after each answer
The user explicitly requested a new GitHub log for this conversation and wants it updated with each answer, because they dislike losing decisions or memory. This file must be updated as the conversation proceeds. Be transparent if a GitHub update fails.

### D-10 — Start Round: adding players
The existing Start Round screen has a Players section with the current player and an Add option. The user clarified that Add is for adding another player to the round by entering a guest's name, or eventually selecting/adding a junior golfer associated with a family account. Junior/family support is future functionality; do not treat it as part of the current adult V1 scope unless the user revises that decision.


### D-11 — Tee Shot screen: fairway result and club/distance control
On the Yardage / Tee Shot screen (`190:136`), the left-side directional controls at the bottom represent the tee-shot result: fairway hit, left miss, or right miss. The golfer selects one at the ball, once. This also creates an opportunity to capture GPS/location for the shot. This is a shot-result selection, not a control for choosing shot shape.

The `Dr` section is the club selection: Driver, with its carry and total yardage shown. Do not interpret these two figures as GPS distances or as the fairway-result control.


### D-12 — Log the selected club with the shot result
When the golfer presses the fairway-result control (fairway hit, left miss or right miss), the app should log the currently selected club alongside that shot event. The golfer should not need to select the club again at the moment of recording; use the active club selection shown on the screen.


### D-13 — After recording a shot, advance to the next shot's yardage screen
After the golfer records a shot using the fairway-result control, Kite should move straight to the next shot's yardage screen. The golfer can then select the club for the next shot and record its result in the same way. This keeps the round flow moving shot by shot.


### D-14 — Chequered flag is for finishing the 18th hole / round
On the score-entry state of the Yardage / Approach screen, the chequered-flag control is specifically for the 18th hole to finish the round. It is not the action to advance from an ordinary hole to the next hole. Preserve this distinction in the round flow.


### D-15 — 18th-hole flag opens Round Complete; End Round confirms
When the golfer taps the chequered flag on the 18th hole, open the existing Round Complete / End Round screen (`261:125`). From there, **End Round** is the final confirmation to finish and retain the round. **View/Edit Scorecard** allows review or correction before confirming; **Discard Round** remains a separate destructive option.


### D-16 — Player Profile edit destinations remain unverified
The Player Profile overview (`295:5`) visually shows edit affordances for Handicap, Home course & tees, Playing preferences, and Clubs & carry distances. We have **not** yet established what happens when any of these edit controls is tapped, whether each opens a separate screen, an inline editor, a modal, or another flow. Review and map all four interactions before deciding that any edit screen is missing; do not single out bag management as the only unknown.


### D-17 — Current Figma review: edit destinations not found yet
The Product UI page was inspected for frames associated with the Player Profile edit controls. The Player Profile overview (`295:5`) is present, but the current frame inventory does not reveal distinct destination frames for Handicap, Home course & tees, Playing preferences, or Clubs & carry distances. This is not proof that no destinations exist elsewhere in the file; the four interactions remain unverified and must be traced in the design before we decide which edit screens need creating.

## Existing Kite UI inventory (known from project context)

These are existing screens, not missing-page proposals:
- Home — Figma frame `93:2`
- Start Round — `124:25`
- Yardage / Tee Shot — `190:136`
- Approach variants — `219:2`, `229:143`, `255:267`
- Scorecard — `261:30`
- End Round — `261:125`
- Player Profile — `295:5`
- Stats — `302:5`
- Scores — `302:121`
- Developer Notes — `302:162`
- Style menu — `334:5`

Figma file: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI/UiDo-%25E2%2582%25AC-Brand---Product-Design-System?node-id=6-2&p=f&t=3oIfwrUpM1RdoZkX-0

## Missing-page register

Only add items here after reviewing existing coverage and confirming that a genuine gap exists.

| Priority | Candidate / gap | Status | Notes |
|---|---|---|---|
| 1 | Login / Sign-up authentication flow | Confirmed gap; details to curate | Google, Apple and email; simple onboarding. Decide whether one screen with states or separate screens only after reviewing flow requirements. |

No other missing pages are confirmed yet. Do not promote earlier speculative suggestions (such as course selection, round setup, saved-round review, settings, account management, or subscription) into the register without first reviewing existing screens and asking about actual gaps.

## Open questions / next review

1. Continue reviewing existing screens before suggesting more missing pages.
2. Start Round (`124:25`) reviewed at a high level: course dropdown; Players (current player and Add); Stroke Play / Stableford; tee choices (White, Yellow, Red); Start Round button.
3. Player Add interaction clarified: add a named guest now; a junior family golfer is a future possibility, not current adult V1 scope.
4. Continue to the next existing screen/flow after this Start Round clarification, and ask only about genuine uncertainties.
5. Authentication details still to curate when appropriate: precise provider/email interaction, forgotten-password path, and which profile setup fields are required versus optional. Do not interrupt the current screen-by-screen review by asking all these at once.
6. Verify actual Player Profile interactions before claiming that bag management is fully covered.
7. After the existing screen review is complete, compile a prioritised list of confirmed missing pages.

## Conversation corrections / guardrails

- The assistant initially jumped to course selection without reviewing the existing Home/profile context. User corrected this: review existing screens first and ask questions about those screens.
- The assistant asked whether sign-up was required after the user had already answered. Do not repeat settled questions.
- The assistant claimed to have reviewed Player Profile and described its coverage, but bag-management interactions have not actually been verified. Be honest about what has and has not been inspected.
- The user wants a careful collaborative curation, not unsolicited criticism, implementation work, or a speculative page list.
- Start Round: the Add player control supports a named guest now; a junior family golfer is a future possibility, not current adult V1 scope.


### D-18 — Correction: edit destinations have not been established
The user correctly pointed out that we have not established what happens when any Player Profile edit control is tapped. Earlier, I asked whether the existing Figma design included separate screens, which confirms this was still an open question. Do not state that the destination screens are missing or “not located” as a conclusion based only on an incomplete inventory search. The correct status for all four controls is **unknown / not yet established**. Continue tracing the design carefully, and if that cannot be resolved from Figma, ask the user rather than infer.

### D-19 — Player Profile edit interaction found in Figma developer notes
Located the existing implementation guidance in the Developer Notes / Q&A Handoff frame (`302:162`, detail node `318:48`): **editing expands each Profile section in place, with Save / Cancel controls staying within the edited section.** This is the intended interaction pattern for the profile sections; do not create separate edit pages by default. The notes also say the displayed profile data is illustrative and implementation should connect it to the selected player record.
