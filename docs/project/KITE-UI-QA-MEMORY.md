

### Profile Q&A — Putter has no distance fields (confirmed 14 October 2026)
- The separate putter row does not show carry or total distance fields.
- The carry/total editor controls apply to the other club types.
- Detailed Figma state still requires build and visual QA; no Figma/app changes or GitHub Actions.


### Profile Q&A — Club-limit warning popup (confirmed 14 October 2026)
- Keep Kite’s normal allowance at 13 non-putter clubs plus the separately listed putter.
- If the player attempts to exceed the competition allowance, show a warning popup. It is a reminder, not a hard block; adding a club is not prevented.
- Use the shared R&A/USGA Rules of Golf, Rule 4.1b: no more than 14 clubs total, including the putter. Kite’s separate-putter bag model represents this as up to 13 other clubs plus one putter. [R&A Rule 4](https://www.randa.org/en/rog/the-rules-of-golf/rule-4) · [USGA Rule 4 FAQ](https://www.usga.org/RulesFAQ/rules_answer.asp?FAQidx=246&Rule=0&Topic=9).


### Round setup Q&A — Four-player maximum (confirmed 14 October 2026)
- Start Round allows up to four total players, including the signed-in golfer; saved family players and guests count toward the same cap.
- This matches the existing joint scorecard design.


### End Round Q&A — Group result card (confirmed 14 October 2026)
- End Round should show one state card for the group with a result summary for each participant, up to four players.
- Reuse the existing one-player End Round card as the visual pattern and include access to the full joint scorecard.


### Round recovery Q&A — Save failure retry (confirmed 14 October 2026)
- When a round save fails, retain the round and all entered scores on the device and allow the golfer to retry saving later.


### Round recovery Q&A — Resume after app/phone interruption (confirmed 14 October 2026)
- An in-progress round should always remain resumable. If Kite closes or the phone restarts, retain the current round and let the golfer resume when reopening the app.
- If saving also fails, keep the round and entered scores on-device and allow a retry.


### Profile Q&A — Club categories in popups (confirmed 14 October 2026)
- Keep the main Manage Bag club list ungrouped.
- Offer club categories within Add Club and bag setup popups to make navigation easier. This supersedes the earlier grouped-list proposal.


### Start Round Q&A — Two multi-player states (confirmed 14 October 2026)
- Create an Add Player popup with Player Name, Handicap, and Tee.
- Create a separate Start Round state showing all four players together, including their selected tees, to demonstrate the completed group layout.


### Round recovery Q&A — Immediate resume on app open (confirmed 14 October 2026)
- If an unfinished round exists when Kite opens, return the golfer straight to that round.
- Avoid a recurring “Resume round?” prompt; the golfer can choose to close or leave the round from the round flow.


### Family/junior V1 scope clarification (confirmed 14 October 2026)
- Treat all previously confirmed answers in `KITE-FAMILY-PLAYER-MANAGEMENT-QA.md` as requirements for the first Kite V1 release, unless explicitly marked exploratory or unresolved.
- Do not re-ask already confirmed family/junior decisions as phase-scope questions.


### Product UI review — family screen cleanup and adult popup states (checked 14 October 2026)
- The user reports deleting the family/junior screens to avoid confusing scope, retaining adult screen states and requesting applicable states be presented as popups.
- Current Product UI metadata shows adult popup states `445:22` Club Limit Reminder, `445:23` Round Save Failure, and `445:24` Resume Interrupted Round. Screenshots confirm the first two are overlays on existing adult screens.
- `445:24` currently presents a recurring “Resume Your Round?” prompt. This conflicts with the confirmed behavior: reopen directly into an unfinished round without a recurring prompt. Treat `445:24` as needing revision/removal.
- One family/junior screen, `445:25` Junior Laptop Dashboard, remains on the Product UI page. Confirm whether this is intentionally retained; other family/junior flow frames are no longer present.
- The remaining dashboard uses a plain yellow “KITE” text header and does not match the existing logo lockup; align it with the locked Kite brand if it remains in scope. Read-only review; no Figma edits made.


### Adult multi-player flow remains in scope after family-screen cleanup (confirmed 14 October 2026)
- Keep the Start Round **Add Player popup** in the adult V1 build. Include Player Name, Handicap, and Tee; allow additions up to four total players.
- Keep a populated **four-player Start Round state** showing the group and each player's tee.
- Keep a **four-player Round Complete / End Round state** with results for each player and access to the joint scorecard, modeled on the existing single-player completion card.
- These adult round screens are separate from family roster and junior-management screens, which are being reworked through the family/junior Q&A.


### App Settings Q&A — Measurement preference access (confirmed 15 October 2026)
- Follow the reference pattern of a simple Settings hub: grouped rows show current values and open lightweight selection or information popups as appropriate.
- Make the yards/metres preference available in both App Settings and Player Profile Playing Preferences.
- Include a Celsius/Fahrenheit selector in App Settings for temperature or weather displays.
- Do not include a left/right-handed preference in V1 App Settings.
- Do not include notification controls in V1 App Settings.
- V1 is English-only; omit a language selector from App Settings.
- Include controls in V1 App Settings to view or change the account sign-in email and password.
