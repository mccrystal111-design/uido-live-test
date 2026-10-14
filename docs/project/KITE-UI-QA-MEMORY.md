

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
