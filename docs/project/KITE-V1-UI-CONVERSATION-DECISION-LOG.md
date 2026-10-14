

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
