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


---

## Consolidated Kite Adult V1 UI Audit — 12 October 2026

### Purpose
Identify genuine missing adult V1 UI by comparing the current Figma page/frame inventory and Developer Notes against the agreed golfer journey. This is an audit of what is represented in the design, not a request to redesign existing screens. No Figma or app implementation changes were made.

### Existing design coverage confirmed
- **Home:** `93:2`
- **Start Round:** `124:25` — course dropdown, player/guest add, Stroke Play/Stableford, tee choice, Start Round.
- **Yardage / Tee Shot:** `190:136` — yardage, bunker information, fairway hit/left miss/right miss control, selected club and carry/total display.
- **Approach states:** `219:2`, `229:143`, `255:267` — approach/score-entry/finish-hole states.
- **Scorecard:** `261:30` — 18-hole scoring, score edit affordance and round statistics.
- **Round Complete:** `261:125` — round summary, View/Edit Scorecard, End Round, Discard Round.
- **Player Profile:** `295:5` — handicap, home course & tees, playing preferences, clubs & carry distances.
- **Stats:** `302:5`; **Scores:** `302:121`.
- **Developer Notes / Q&A Handoff:** `302:162`, including the Player Profile inline-edit interaction rule.

### Prioritised gap register

**Priority 1 — Login / Sign-up flow (confirmed missing from the reviewed page inventory).**
The Home screen assumes an existing player/profile, but no login or registration screen is present in the reviewed Kite page inventory. Agreed direction: simple Google, Apple or email sign-up/sign-in. This is the first gap to design.

**Priority 2 — First-run onboarding / profile setup states (required by agreed journey; not represented as a dedicated flow in the reviewed inventory).**
Agreed journey is sign-up/sign-in → optional Player Profile setup → Home. Profile setup can be skipped, with a clear indication that some functionality may be limited when relevant details are absent. Design the first-run states and skip path without duplicating the existing Player Profile overview.

**Priority 3 — Player Profile expanded edit states (interaction pattern specified; detailed form content not yet evidenced in the reviewed frames).**
Developer Notes specify that each section expands in place and Save/Cancel remain within that section. The current visible frames show the collapsed summary states only. The detailed expanded fields/layouts still need to be located elsewhere in Figma or designed if they do not exist. This applies to all four sections: Handicap; Home course & tees; Playing preferences; Clubs & carry distances. Do not create four separate edit pages by default.

**Priority 4 — Club-bag setup/edit details (specific states required by agreed product decisions; detailed UI not yet evidenced in the reviewed frames).**
The existing profile has a Clubs & carry distances summary and “Manage bag” entry point. Required behaviour to support: full bag setup; optional shortcut entering Driver and 7-iron carry to estimate other clubs; estimates editable later; ability to skip all bag setup; no nagging/repeated prompts. The club-bag expanded editor/setup states need to be checked against this requirement. Treat this as a detailed part of Priority 3, not a separate duplicate profile page.

### Not gaps based on current evidence
- Course selection / Start Round setup: already exists.
- Scorecard and round-completion screens: already exist.
- Stats and Scores pages: already exist.
- Player Profile overview: already exists.
- Junior/family UI: explicitly future scope, not adult V1.
- GPS/live-yardage functionality: out of scope for this UI gap audit.

### Round-flow decisions to preserve
- Pressing fairway hit / left miss / right miss records the result, currently selected club and GPS location where available.
- After a shot is recorded, advance directly to the next shot's yardage screen.
- The chequered flag is specifically for finishing the 18th hole; it opens Round Complete.
- End Round is the final confirmation to retain/finish the round; Discard Round is separate.

### Audit status / next action
The first consolidated audit is complete based on the reviewed frame inventory and Q&A handoff. The first confirmed missing page is Login/Sign-up. Priorities 2–4 are required flow/detail states not evidenced in the reviewed page frames; before creating anything, check whether any expanded/setup states are already represented elsewhere in the Figma file. Do not keep repeating screen summaries; use this register as the current working list and amend it only when new evidence or a user decision changes the status.

## Authentication and first-run decisions — 13 October 2026

The following answers are agreed and should be treated as settled; do not ask them again:
- **Authentication methods:** offer Google/Gmail, Apple, and email for both new sign-up and returning-user sign-in.
- **First-run journey:** sign-up/sign-in → optional Player Profile setup → Home.
- **Profile setup:** skippable. Explain a limitation only at the point it matters; do not block entry to Home.
- **Bag setup:** offer full bag entry, or a simplified option entering Driver carry and 7-iron carry to estimate the remaining clubs. Estimated values must be editable later.
- **Skip behaviour:** the golfer may skip all bag setup. Do not nag or repeatedly prompt them; they choose when to update their profile.
- **Reuse existing profile:** use the existing Player Profile overview (295:5); do not create a duplicate overview screen.
- **Scope guardrails:** adult Kite V1 only; junior/family UI is future scope. No Figma edits, app/code changes, or GitHub Actions as part of this curation pass.

### Current next step — Priority 1: authentication details
The Developer Notes / Q&A Handoff (302:162) has been checked. It contains design-system, Stats/Scores, data-safety, QA and Player Profile implementation guidance, but no authentication-specific decisions. The next task is to define only the remaining auth details and then map the minimal Login/Sign-up states:
1. Google/Apple provider hand-off and return/error states.
2. Email sign-up/sign-in and forgotten-password recovery.
3. Whether first-run profile setup asks only for the minimum useful fields initially, with the rest left editable in Player Profile.

Do not ask again about the providers, skippable profile setup, Driver + 7-iron shortcut, editable estimates, or no-nagging rule. Check existing Figma coverage before proposing new screens, and ask one focused question at a time only where a product decision is genuinely missing.

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


### First-run setup layout — decision 13 October 2026
- **Decision:** present optional Player Profile setup as a short **step-by-step flow**, not one long setup screen.
- Provide a clear skip option so the golfer can skip an individual step where appropriate and/or leave the whole setup using **Skip for now**. Skipping leads to Home; do not nag or repeatedly prompt them later.
- Preserve earlier decisions: ask for player name and handicap, but handicap is optional; include home course/tees and bag setup in the short flow as appropriate; bag setup can be full entry or Driver + 7-iron carry to estimate the remaining clubs, with estimates editable later. The golfer can skip all bag setup.
- This is a documented product decision only. No Figma edits, app/code changes, or GitHub Actions.


### First-run setup scope correction — 13 October 2026
- **Decision:** do not ask for home course or preferred tees during first-run onboarding. The user considers these unnecessary in the initial setup.
- Keep onboarding short and step-by-step, with the current focus on player name, optional handicap, and optional club-bag setup. The golfer can skip the whole flow or skip optional steps; skipping leads to Home without nagging.
- This decision applies to first-run onboarding only; the existing Home course & tees section remains part of the Player Profile unless separately changed.


### Club-bag step sequencing — decision 13 October 2026
- **Decision:** show the club-bag setup automatically as the second step after personal details; do not make the golfer opt into opening it.
- The bag step must be clearly optional, with an obvious **Skip** action. The overall setup can still be exited with **Skip for now**; either route leads to Home without nagging or repeated prompts.
- Preserve the agreed choices on the bag step: full bag entry or Driver + 7-iron carry to estimate the rest; estimated distances remain editable later; the golfer may skip the entire bag setup.


### Google / Apple authentication outcomes — decision 13 October 2026
- **Success:** continue into Kite; if this is a new account, offer the agreed optional step-by-step Player Profile setup.
- **Cancelled:** return to the same Log in / Create account screen without displaying an error.
- **Failed:** show a concise, clear error with an option to retry or choose another sign-in method.
- **Existing account detected during sign-up:** guide the golfer to log in rather than create a duplicate account.
- Keep these as states of the single authentication screen where practical; do not add unnecessary screens. Documentation only; no Figma or app changes made.


### Email authentication validation — decision 13 October 2026
- **Decision:** require a valid email address and password for email-based authentication.
- During account creation, ask the golfer to enter the password twice to catch typing mistakes.
- Show clear, concise inline feedback for invalid details, incorrect credentials, or an account that already exists; guide the golfer to the appropriate next action.
- Keep feedback within the single Log in / Create account screen wherever practical, avoiding unnecessary extra screens. Forgot password recovery remains available from Log in.
- Documentation only; no Figma or app changes made.


### Forgot-password recovery flow — decision 13 October 2026
- **Decision:** from Log in, **Forgot password?** opens a simple email-entry form.
- Kite sends a password-reset email and confirms that the request was received. Use a neutral confirmation message that does not reveal whether the email address has an account.
- The golfer follows the link in the email to reset their password, then returns to Log in.
- Keep this focused; no unnecessary extra screens. Documentation only; no Figma or app changes made.


### Email verification and guest play — decision 13 October 2026
- **Email verification:** email/password accounts should be asked to verify their email, but verification must **never block the golfer from playing golf**. Allow access while unverified and show a clear, non-blocking reminder with an option to resend the verification email.
- Google and Apple sign-in do not need this additional email-verification step in the Kite flow.
- **Guest play:** the user raised that Kite should offer an option to play without signing in. Record this as a product direction to include a **Play without signing in** / guest path, with its precise capabilities and data persistence to be clarified before implementation. Do not force account creation before a golfer can start playing.
- This revises the earlier working assumption that account creation is required before using Kite. Account creation/sign-in remains available for golfers who want a profile and account-linked features.
- Documentation only; no Figma or app changes made.


### Welcome screen and saving rounds — decisions 13 October 2026
- **Entry point:** add a Welcome / Entry screen before the existing Home screen. Keep the current Home screen; this is a new entry screen, not a replacement.
- Offer two clear paths: **Play without signing in** and **Sign in or create an account**. Account sign-in offers Google, Apple, or email/password as already agreed.
- **Guest play:** golfers can access core play without registration. Guest rounds should be retained locally on the device so a golfer can finish and review a round without an account.
- **Account-linked saving:** signing in/creating an account is the path to saving rounds to the golfer's account and, when supported, accessing history across devices. Do not imply cross-device sync exists until implemented.
- Do not risk losing a round or block play because the golfer has not registered. Email verification remains non-blocking.
- Add Welcome / Entry screen to the missing-page register ahead of authentication. This is a product decision/documentation update only; no Figma or app changes made, and no GitHub Actions run.


### Guest-round import after account creation — decision 13 October 2026
- **Decision:** when a guest golfer later signs in or creates an account, Kite should offer to transfer/import their locally saved guest rounds into that account.
- Make this an explicit, consent-based choice; do not silently merge or upload guest round history.
- If they decline, preserve the local guest rounds and let them continue playing. Explain clearly if any local-only data will not be available on other devices.
- This is a required product behaviour to account for in the guest-to-account flow; implementation details and conflict handling can be specified later. No Figma or app changes made.


### Welcome screen primary action — decision 13 October 2026
- **Decision:** make **Play without signing in** the prominent yellow primary button on the Welcome / Entry screen.
- Keep **Sign in or create an account** as the secondary action. This supports Kite's promise of quick, low-friction access to golf while keeping account-based saving available.
- Preserve the existing Home screen; Welcome / Entry is a new pre-home screen. No Figma or app changes made.


### Prefilled starter bag distances — user-provided baseline, 13 October 2026
The user supplied the following **men's everyday amateur / approximately 15-handicap** distances as the candidate default starter bag. Treat these as estimated starting values, not measured or universally representative distances. Show carry and total separately, and allow the golfer to edit them.

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
| Pitching Wedge (PW) | 105 | 121 |
| Gap Wedge (GW) | 95 | 104 |
| Sand Wedge (SW) | 83 | 84 |
| Lob Wedge (LW) | 72 | 75 |

**Driver carry default:** the user gave a 215–225 yd range; 220 yd is the midpoint for a single editable prefill value. Preserve the original range in this note. Starter bag should be a fast option in onboarding; retain the alternative Driver + 7-iron personalisation route and the clear skip option. No Figma or app changes made.


### Women's amateur starter-bag distance baseline — user-provided, 13 October 2026
The user supplied this women's amateur distance range as a separate candidate baseline for Kite's prefilled starter bag. **Ignore the LPGA pro columns** for this product decision. Values are approximate ranges, not universal or measured distances. For a single prefill value, use the midpoint of each range, rounded to the nearest yard; preserve the original ranges in this log. Keep carry and total separate, and make every value editable.

| Club | Amateur carry range (yd) | Amateur total range (yd) | Suggested prefill carry midpoint (yd) | Suggested prefill total midpoint (yd) |
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
| Pitching Wedge | 58–68 | 68–78 | 63 | 73 |
| Gap Wedge | 50–60 | 58–66 | 55 | 62 |
| Sand Wedge | 42–50 | 46–54 | 46 | 50 |
| Lob Wedge | 35–42 | 38–44 | 39 | 41 |

This should be offered as a distinct women's amateur starter profile, alongside the previously recorded men's everyday-amateur starter bag. Do not assume sex determines actual distance or prevent the golfer choosing/editing any bag. No Figma or app changes made.


### Starter bag selection — use selected tee, 13 October 2026
- **Decision:** choose the prefilled starter-bag distance profile based on the golfer's selected tee, rather than asking them to choose a men's/women's or longer/shorter profile.
- Reuse the tee selection already present in Start Round; avoid asking the golfer the same thing again during onboarding. The starter bag is a convenient initial estimate, and every club distance remains editable.
- **Open implementation detail:** confirm the mapping between tee choices and the available starter distance profiles when the existing tee-selection behaviour and course context are reviewed. Do not assume tee colour universally implies a particular gender or exact ability/distance.
- Keep the Driver + 7-iron personalisation route and the option to skip bag setup. No Figma or app changes made.


### Automatic starter-bag creation — decision 13 October 2026
- **Decision:** create the golfer's starter bag automatically when they start their first round, using the tee selected for that round to choose the default distance profile.
- Do not add a separate mandatory bag-setup step to onboarding. Make the generated bag available to review and edit later in the existing Player Profile.
- Preserve the ability to personalise distances (including Driver + 7-iron), edit all prefilled values, and skip bag setup. Do not imply that estimated distances are measured values.
- The tee-to-distance-profile mapping must be grounded in course/tee context and must not assume tee colour universally indicates gender or ability. No Figma/app changes made.


### Tee changes do not overwrite personal club distances — confirmed 13 October 2026
- Changing the selected tee changes the course/playing yardages, but must **not** overwrite or silently recalculate the golfer's personal club carry/total distances.
- Preserve the golfer's saved, editable club distances when they choose different tees. Starter-bag defaults are only used when creating the initial bag; tee changes later do not reset personal data.
- No Figma/app changes made.

### Club distance editing — estimate total from carry, allow override — confirmed 13 October 2026
- The golfer edits **carry distance** as the primary personal value; Kite estimates the corresponding total distance.
- Allow the golfer to **override total distance manually** when the estimate does not match their real-world experience.
- Keep both values visible where useful, make it clear which total is estimated versus manually overridden, and preserve saved values when tees change.
- No Figma/app changes made.

### Club total-distance roll multipliers — user-provided ranges, 13 October 2026
Use club-category-specific roll multipliers to estimate total distance from carry. The user supplied these candidate ranges:
- **Driver & fairway woods:** 1.08–1.12 (example: 150 yd carry × 1.10 = 165 yd total).
- **Hybrids & long irons (3i–5i):** 1.06–1.08 (example: 110 yd × 1.07 = 118 yd).
- **Mid-irons (6i–8i):** 1.04–1.06 (example: 85 yd × 1.05 = 89 yd).
- **Short irons & wedges (9i–LW):** 1.01–1.03 (example: 60 yd × 1.02 = 61 yd).
- Total remains an estimate derived from carry, and the golfer can manually override it.
- **Still to decide:** which default multiplier to use within each range. Do not silently treat the example multipliers as final defaults until confirmed.
- No Figma/app changes made.

### Default roll multipliers confirmed — 13 October 2026
The user approved the midpoint of each proposed club-category range as Kite's default total-distance estimate:
- **Driver & fairway woods:** carry × **1.10**
- **Hybrids & long irons (3i–5i):** carry × **1.07**
- **Mid-irons (6i–8i):** carry × **1.05**
- **Short irons & wedges (9i–LW):** carry × **1.02**
These are starting estimates. Golfers can manually override total distance; switching tees must not overwrite saved personal club distances. This supersedes the open question about which multiplier to choose. No Figma/app changes made.

### Guest first-round starter bag — confirmed 13 October 2026
- For a golfer's **first round without signing in**, create the starter bag automatically when they start the round, using the selected tee to choose the default distance profile.
- Do not interrupt guest round-start with a separate bag-setup screen. The generated bag is editable later in Player Profile/profile management.
- Apply the previously confirmed club-category roll multipliers for estimated total distances; carry and total remain editable, and tee changes do not overwrite saved distances.
- This answer explicitly confirms the guest first-round path. Whether the same no-interruption behaviour should apply to a signed-in golfer's first round remains open. No Figma/app changes made.

### Starter bag fallback for signed-in first round — confirmed 13 October 2026
- Signed-in golfers have already been offered the opportunity to personalise their bag during optional first-run setup.
- If they skip that option or have no saved bag when they start their first round, Kite automatically creates the starter bag from the selected tee. Do not interrupt round-start with another bag-setup prompt.
- If they already configured/saved a bag, preserve and use their own club data; never replace it with the starter defaults.
- The same fallback principle applies to guest golfers: create the starter bag when they start their first round without signing in, then allow edits later.
- No Figma/app changes made.

### Explain automatic starter-bag creation to the golfer — confirmed direction, 13 October 2026
- When the golfer has not personalised a bag, Kite should tell them it is going to build a starter bag for them, rather than creating it without explanation.
- Keep the message brief and reassuring: Kite will use the selected tee to create estimated club distances, and the golfer can edit them later in Player Profile.
- This message explains the automatic first-round fallback; it must not introduce a blocking setup step or delay starting play.
- Exact wording and placement remain open. No Figma/app changes made.

### Account creation: offer own bag, supported by starter set — confirmed 13 October 2026
- When a guest creates an account, offer them the option to build/personalise their own club bag.
- Back the setup with Kite's starter set of estimated club distances so the golfer can begin from sensible defaults rather than entering every club from scratch.
- The golfer can accept the starter bag and edit it, or personalise their own bag; do not force full manual entry.
- Preserve the guest's existing saved rounds and any personal club data where applicable, and require explicit consent before transferring guest rounds to the account as already agreed. The account transition must not silently discard the guest's bag/distance edits.
- No Figma/app changes made.

### Own club-bag setup offers two routes — confirmed 13 October 2026
When the golfer chooses to personalise their bag, offer two clear routes:
1. **Full bag setup:** enter clubs and distances individually.
2. **Quick setup:** enter Driver carry and 7-iron carry; Kite estimates the remaining clubs/distances.
Use the starter set to support estimates and sensible prefilled values. Estimated total distances use the confirmed club-category multipliers and can be manually overridden. Keep the process optional and allow the golfer to return to Player Profile later. No Figma/app changes made.

### Quick Setup saves immediately; edit later — confirmed 13 October 2026
- In Quick Setup, after the golfer enters Driver and 7-iron carry, Kite generates and saves the starter bag immediately.
- Do not add a review/edit step before saving. The golfer can edit individual clubs/distances later in Player Profile.
- Keep estimated values identifiable as estimates; total-distance multipliers and manual total overrides remain as previously agreed. No Figma/app changes made.

### Skipping bag personalisation — automatic starter bag on first round — confirmed 13 October 2026
- If the golfer skips all bag personalisation, Kite still creates a starter bag automatically when they start their first round, using the selected tee to choose the default distance profile.
- Explain briefly that Kite is building a starter bag with estimated club distances; do not block or delay starting the round.
- The golfer can edit the bag and distances later in Player Profile. If they already have a saved/personalised bag, preserve it rather than replacing it with defaults.
- No Figma/app changes made.

### Starter bag is created once only — confirmed 13 October 2026
- Create the automatic starter bag once, when the golfer starts their first round and has no saved/personalised bag.
- Do not rebuild or reset it when the golfer changes tees later. Tee changes affect course yardages only; saved personal club distances remain intact.
- The golfer can edit the starter bag later in Player Profile. No Figma/app changes made.

### Welcome / Entry screen — no tagline — confirmed 13 October 2026
- Do not include a tagline or marketing slogan on the Welcome / Entry screen.
- Keep the entry experience minimal and action-led: Kite branding, prominent yellow **Play without signing in**, and secondary **Sign in or create an account**.
- Do not add a feature tour or lengthy onboarding before the golfer can play. Preserve the existing Home screen; Welcome / Entry sits before it. No Figma/app changes made.

### Guest entry destination — confirmed 13 October 2026
- When the golfer taps **Play without signing in** on Welcome / Entry, take them **straight to Start Round** (Figma frame 124:25), not Home.
- Rationale: the existing Home screen contains Stats and Scores, which are not the immediate destination for a guest who wants to start playing.
- Keep the existing Home screen for its current purpose; this decision changes only the guest entry route.
- This updates the previously recorded general guest path: Welcome → Play without signing in → Start Round. The signed-in/authenticated path remains governed by the existing auth and optional profile-setup decisions.
- Documentation only; no Figma edits, app/code changes, or GitHub Actions.

### Start Round course selector — confirmed 13 October 2026
- The course selector should be populated with **all courses available in Kite's course catalogue**, not only a manually curated shortlist or courses already played.
- Use the golfer's current location to calculate distance to each course and sort the list by proximity, with the **closest course at the top** by default.
- The golfer can still choose a different course from the list.
- This assumes location permission is available; exact fallback behaviour when location is unavailable, and whether the full catalogue is already stored/downloaded versus fetched from a service, remain implementation details to verify rather than assume.
- Documentation only; no Figma edits, app/code changes, or GitHub Actions.
