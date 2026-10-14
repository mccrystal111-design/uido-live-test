

### Player Profile editing Q&A — Putter has no distance fields, confirmed 14 October 2026
- The separate putter row does not show carry or total distance fields.
- The carry/total editor controls apply to the other club types.
- Documentation only; no Figma edits, app/code changes, or GitHub Actions.


### Player Profile Q&A — Club-limit warning popup (confirmed 14 October 2026)
- Keep Kite’s normal allowance at 13 non-putter clubs plus the separately listed putter.
- If a player attempts to exceed the competition allowance, show a warning popup. This is a reminder, not a hard block; do not prevent adding the club.
- Use the shared R&A/USGA Rules of Golf, Rule 4.1b: no more than 14 clubs total, including the putter. Kite’s separate-putter bag model represents this as up to 13 other clubs plus one putter. [R&A Rule 4](https://www.randa.org/en/rog/the-rules-of-golf/rule-4) · [USGA Rule 4 FAQ](https://www.usga.org/RulesFAQ/rules_answer.asp?FAQidx=246&Rule=0&Topic=9).


### Start Round Q&A — Maximum four players (confirmed 14 October 2026)
- Limit a round to four total players, counting the signed-in golfer and any selected family players or saved guests.
- Match the Start Round participant cap to the existing joint scorecard for up to four players.


### End Round Q&A — Up to four player result card (confirmed 14 October 2026)
- For a group round, show one End Round state card with a result summary for each player, supporting up to four players.
- Base the layout on the existing single-player End Round card and provide a way to open the full joint scorecard.


### Round recovery Q&A — Keep round when save fails (confirmed 14 October 2026)
- If saving a round fails, keep the round and entered scores on the device so the golfer can retry saving later without losing their work.


### Round recovery Q&A — In-progress round always resumable (confirmed 14 October 2026)
- Keep an in-progress round in a resumable state throughout play. If Kite closes or the phone restarts, retain the round so the golfer can resume when they reopen the app.
- This complements the save-failure decision: preserve the round and entered scores locally if saving fails, with a retry path.


### Player Profile Q&A — Club categories belong in setup popups (confirmed 14 October 2026)
- Supersedes the earlier proposal to group the Manage Bag list under Woods, Hybrids, Irons, and Wedges.
- Keep the main bag list ungrouped for easier navigation. Present club categories as options within the Add Club popup and bag setup popups.


### Start Round Q&A — Add Player popup and four-player overview states (confirmed 14 October 2026)
- Build two Start Round design states: (1) the existing round setup with an Add Player popup containing Player Name, Handicap, and Tee; (2) the round setup populated with four players to show the group layout.
- Keep the four-player state within the four-player maximum and show each player's tee. Use one shared scoring format for the round, as already decided.
