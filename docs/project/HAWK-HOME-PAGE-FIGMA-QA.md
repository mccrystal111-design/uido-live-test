# Hawk Home Page — Figma Q&A Log

**Date:** 2026-10-06  
**Purpose:** Durable record of the voice Q&A used to define the Hawk Home Page Figma briefing.  
**Status:** Q&A complete; ready for Figma briefing/design.

## Product direction

### Q1 — Primary purpose
**Decision:** Hawk Home should get the golfer into a round as quickly as possible.

Hawk is a simpler golf product than full UiDo, while remaining closely related and sharing the same Core foundation.

### Q2 — Home page contents
**Decision:** The Hawk Home page should contain:
- Start Round
- Scores
- Stats
- A dedicated advert space

The screen should remain simple. Advert integration must be considered as part of the visual design so it feels intentional rather than intrusive.

### Q3 — Scores
**Decision:** Scores opens the customer's logged scorecard history.

This should include all relevant logged rounds/sessions, including WHS, GHIN, UiDo and practice activity where available. The scorecard experience should remain close to the established normal UiDo scorecard experience rather than being reinvented for Hawk.

### Q4 — Stats
**Decision:** Hawk Stats should be deliberately simpler than UiDo Insights.

Hawk should show familiar standard golf statistics such as:
- Fairways hit
- Greens in regulation
- Putts
- Scoring
- Other normal golf-app statistics

Advanced UiDo decision/insight functionality remains a UiDo differentiator and should not clutter Hawk Stats.

### Q5 — Customer identity on Home
**Decision:** Keep the personal information minimal.

If the golfer is logged in, their name may appear in the top-right area. Their handicap may also appear there when available. This is supporting information, not the main focus of the Home page.

### Q6 — Start Round course selection
**Decision:** Start Round should use GPS to identify the nearest course.

The course-selection step should show:
- Nearest course
- A small distance indicator
- A dropdown/selector allowing the golfer to choose another course

Default distance presentation should be yards and miles. Metric/metres can be supported for appropriate regions later.

### Q7 — Round setup flow
**Decision:** After course selection, the golfer selects:
1. Tee
2. Scoring method
3. Begin Round

After Begin Round, Hawk should move directly to the first hole.

If the golfer is starting somewhere other than Hole 1, there should be a way to jump to the appropriate hole.

### Q8 — Scoring methods
**Decision:** Keep scoring methods simple:
- Stroke Play
- Stableford

Do not introduce additional scoring modes at this stage.

### Q9 — Tee selection
**Decision:** Do not force a default tee.

A preferred/default tee may exist in player preferences, but the actual tee must be explicitly selected for the round and recorded as historical round context.

### Q10 — Home page scope
**Decision:** No additional Home-page functions are required at this stage beyond Start Round, Scores, Stats, customer identity/handicap where available, and advert space.

## Figma design constraints

- Figma is the visual source of truth.
- The approved Yardage page is a protected/proven reference and must not be deleted, replaced or reinterpreted to build Home.
- Design the Home page in Figma before coding HTML.
- Keep the Home page simple and golf-first.
- Advert placement must be visually intentional and must not overwhelm Start Round.
- Hawk should feel related to UiDo without exposing advanced UiDo Insights functionality.
- The eventual workflow remains: Figma -> approved visual -> HTML -> rendered screenshot/pixel check -> refine -> Android packaging.
