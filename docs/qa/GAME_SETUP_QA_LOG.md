# Game Setup Q&A Log

Started: 2026-11-16  
Purpose: Capture agreed rules and open questions for the game setup dialogs. Add to this log as the Q&A continues; distinguish confirmed decisions from suggestions.

## Fly a Kite

### Confirmed

- Fly a Kite replaces String Ball.
- It uses normal golf scoring. Each player still plays off their course handicap.
- A player's handicap number is also their total step allowance for the whole round.
- One step is one move on the course.
- Players may use steps after the tee shot, whenever they choose, but not while on a tee box.
- A player may move to any course position, including water; players may choose to avoid water.
- Repositioning does not add strokes.
- Steps are a movement resource only and do not affect the final result.
- The winner in Individual mode is the player with the lowest net score.
- Available formats:
  - **Individual:** normal net scoring.
  - **VS Battle:** matchplay.
  - **Teams VS Battle:** team matchplay using betterball scoring.
- Team sizes may be uneven, such as two children versus one parent.

### To decide

- How players are assigned to teams in the setup dialog.
- How to handle tied holes or a tied match.

## Treasure Hunt

### Confirmed

- It is an individual-only game.
- There is no golf score; the aim is to explore and dig around the course.
- Players dig after every shot, at the spot where the ball lands.
- Every dig uncovers an item; no dig is empty.
- Each item has its own point value, in addition to the terrain reward and any eligible distance bonus.
- The landing surface determines its item pool. Previously selected examples: occasional lower-value snake in rough, crab in sand/bunker and acorn in trees.
- Item value order: treasure/relics and the long-drive idol highest; gems next; coins below gems; critters and woodland finds lowest.
- Each find earns points, and collected points are totalled at the end.
- The Figma scorecard/end screens show Points as the result, with Total Yards and Total Steps as supporting stats.
- Ground value order is **green > fairway > rough > sand > trees**.
- The largest point-value gap should be between green/fairway and the lower-value areas. Differences among rough, sand and trees should be smaller.
- There is a straight-line distance bonus between consecutive dig spots, but it applies only when the new dig spot is on the fairway or green.

### To decide

- The fairway/green distance bonus grows steadily with straight-line distance, measured in yards (not in tiers). The rate is 1 bonus point per 10 yards of straight-line distance between consecutive dig spots. Bonus applies only when the new dig spot is fairway or green.
- Exact point values for each terrain and item; the reward hierarchy is confirmed.
- Whether water has its own item pool/reward.

## Bingo, Bango, Bongo

### Confirmed

- Individual-only; no team or VS Battle setup.
- Each hole can award one point for each:
  - **Bingo:** first player to reach the green.
  - **Bango:** closest to the hole after everyone has reached the green.
  - **Bongo:** first player to hole out.
- Each award is worth one point. Player totals are shown for the front nine, back nine and overall.

## Dialog design notes

- The Add Player dialog was used as a size and shape placeholder for the Fly a Kite game setup dialog.
- Final setup dialog copy and controls should follow the confirmed rules above; do not treat placeholder fields as game requirements.
- String Ball is out of scope; Fly a Kite replaces it.
