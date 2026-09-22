# Overstone F/M/B validation — 18-hole test

## Result

The next validation step confirms that the recovered Overstone OSM source contains a deterministic terminal-green relationship for all 18 hole routes.

Each `golf=hole` route terminates at one identifiable OSM `golf=green` polygon. Across the 18 holes, 18 distinct greens are associated; two additional OSM green polygons remain outside the 18-hole route set and are not silently assigned.

For each associated green, the polygon centroid is a deterministic Middle candidate.

## Important finding

The historical Overstone test coordinate for Middle on the recovered green `way/798091452` is reproduced to floating-point precision by the polygon centroid.

The historical Front and Back coordinates are also actual vertices of that same OSM green polygon. However, the exact boundary-vertex selection rule used by the original UiDo test has **not** yet been proven from the available evidence. A directional projection candidate is therefore recorded by the validator but is explicitly **not** promoted as the final F/B algorithm.

This is an intentional QA distinction: we have proven the source relationship and Middle derivation, and we have proven that the historical F/B values are present in the source geometry, but we have not invented the missing selection rule.

## Validator

`tools/course-model/validate_fmb_derivation.py`

The validator:
- uses the recovered OSM source;
- associates each hole with its terminal green;
- derives the green centroid;
- records a reproducible directional F/B candidate;
- does not alter source geometry;
- records unused greens rather than forcing them into the 18-hole model.

## Next step

Recover/derive the exact F/B boundary selection rule, then run the complete 18-hole output against any historical UiDo F/M/B data that can be recovered.

Only after that should F/M/B be promoted from validated source evidence to a universal acquisition rule.
