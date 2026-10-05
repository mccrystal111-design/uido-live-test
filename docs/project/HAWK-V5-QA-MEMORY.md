# UiDo — Hawk / V5 Q&A Memory

Updated: 2026-10-05

## Cumulative Q&A memory

```
V5 MEMORY: Hawk start → Start Round / Scores / Stats → equal-sized controls, Start Round distinguished by colour → setup Course + Tees + scoring format → GPS starts at app load → course selection uses UiDo's future canonical course database and shows nearby courses ordered by distance, closest first → tee selection is data-driven from canonical course data (Red/Yellow/White/Blue etc. as available) → scoring formats are Stroke Play and Stableford, with possible team elements but V5 remains primarily an individual product with no live leaderboard → Start Round opens directly on Hole 1 using the established V4 yardage page → current hole stays active → Score + Putts advances to next hole → tap hole header (e.g. HOLE 1 · PAR 4 (net score)) to Jump to Hole → 6×3 hole selector with buttons 1–18 only → select hole closes popup and opens selected hole → GPS continuously updates in background → when player has stopped and GPS accuracy is better than 4m, hold that position → when movement resumes, live yardage updates resume → bottom three dots represent functional bunker-page pagination → swipe horizontally between bunker pages to see additional fairway/greenside bunker sets → main F/M/B yardages remain fixed while bunker information changes so the golfer can compare carry/runout mentally → bunker presentation remains unchanged from V4 → dots are functional pagination, not decoration → no additional scoring setup options beyond Stroke Play and Stableford.
```

## Agreed V5 build order

1. Finish the V5 yardage-page functionality first.
2. Use the established V4 yardage page as the visual/interaction baseline rather than redesigning it.
3. Implement functional bunker-page swiping/pagination while keeping the main yardage numbers fixed.
4. Once the V5 yardage page is solid, move on to the Wind page using the established UiDo wind-tile rules.

## Status

Q&A discovery is **substantially captured but remains open for any further V5 questions**. This is the current accumulated memory; no Hawk/V5 implementation should begin until the Q&A is finished and the final memory is agreed.

## Discovery protocol

- One question at a time.
- No build/edit/code during discovery unless explicitly requested.
- After every answer, update the single cumulative MEMORY line.
- MEMORY is the complete accumulated decision set, not only the latest answer.
- Keep MEMORY concise and copyable.
- Persist the final agreed memory into project source-of-truth before implementation.
