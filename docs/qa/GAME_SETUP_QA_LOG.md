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
- Players choose their own team sides in Teams VS Battle.

### To decide

- How players are assigned to teams in the setup dialog.
- Tied matchplay holes are halved, as in normal matchplay.
- If a match is tied after 9 or 18 holes, it remains a tie.

## Treasure Hunt

### Confirmed

- It is a cooperative, just-for-fun hunt; there are no individual scores or competitive rankings.
- Treasure Hunt can be played individually or with a group of up to four players (**1–4 players**), selected in the shared player setup before choosing a game.
- All players contribute to one shared points total; there are no per-player totals.
- There is no golf score; the aim is to explore and dig around the course.
- Players dig after every shot, at the spot where the ball lands.
- Every dig uncovers an item; no dig is empty.
- Each item has its own point value, in addition to the terrain reward and any eligible distance bonus.
- The landing surface determines its item pool. Examples include an occasional lower-value snake in rough, crab in sand/bunker, and acorn in trees.
- Item value order: treasure/relics and the long-drive idol highest; gems next; coins below gems; critters and woodland finds lowest.
- Each find earns points, and collected points are totalled at the end.
- Players can choose a 9-hole or 18-hole hunt, and can end early to go to the end-of-round screen with their current totals.
- The Figma scorecard/end screens show Points as the result, with Total Yards and Total Steps as supporting stats. Example totals on the screens (such as 140 points in play and 1,251 at the end) are placeholders, not a target scoring scale.
- Ground value order is **green > fairway > rough > sand > trees**.
- Terrain bonuses are added to each item's points: **green +5, fairway +4, rough +2, sand +1, trees +0, water +0**.
- The largest point-value gap should be between green/fairway and the lower-value areas. Differences among rough, sand and trees should be smaller.
- The distance bonus is a straight-line distance between consecutive dig spots, measured in yards. It grows steadily rather than using tiers, at **1 bonus point per 10 yards**.
- The distance bonus applies only when the new dig spot is on the fairway or green.
- Each collectible is worth more than 20 and less than 90 points, before terrain and eligible distance bonuses: old boot 21; critters and woodland finds 25; copper coin 32; silver coin 38; common gem 48; treasure chest 65; relics 78; long-drive idol 85.
- Gem variants are valued by rarity, with rarer gemstones worth more. The colour variants use real gemstone names: turquoise, citrine (yellow), amethyst (purple), pink sapphire, and black opal. Their game point ladder is inspired by rarity, not a literal real-world price scale.
- Water is a valid landing area and always yields an item; an old boot is the water-pool example and is a low-value find.
- The old boot is the lowest-value collectible.

## Bingo, Bango, Bongo

### Confirmed

- Individual-only; no team or VS Battle setup.
- Each hole can award one point for each:
  - **Bingo:** first player to reach the green.
  - **Bango:** closest to the hole after everyone has reached the green.
  - **Bongo:** first player to hole out.
- Each award is worth one point. Player totals are shown for the front nine, back nine and overall.

## Dialog design notes

- Players are selected before choosing a game; game-specific setup dialogs should not ask to add players again.
- The Add Player dialog was used as a size and shape placeholder for the Fly a Kite game setup dialog.
- Final setup dialog copy and controls should follow the confirmed rules above; do not treat placeholder fields as game requirements.
- String Ball is out of scope; Fly a Kite replaces it.
