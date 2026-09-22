# UiDo F/M/B Green Coordinate Derivation

## Status

**Validated against the recovered Overstone historical test on the correct hole: hole 2.**

The historical live-test HTML contained:
- Front: `52.2762446, -0.8166103`
- Middle: `52.2761187565, -0.8166885565`
- Back: `52.2759866, -0.8167443`

The associated OSM green is `way/798091452`. Spatial comparison shows this green belongs to the terminal end of OSM hole route `way/798140683`, whose `ref` is **2**.

### Proven source relationship

The recovered OSM source contains:
- `way/798091452` tagged `golf=green`
- `way/798140683` tagged `golf=hole`, `ref=2`

The green polygon centroid is:
- longitude: `-0.8166742136119863`
- latitude: `52.276126311402734`

The historical Middle coordinate is extremely close to this centroid. The earlier exact-centroid statement was based on an incorrect hole/green association and has been corrected here.

The historical Front and Back coordinates are both vertices of the same OSM green polygon:
- Front: `[-0.8166103, 52.2762446]`
- Back: `[-0.8167443, 52.2759866]`

The hole-2 terminal route direction also orders those vertices correctly: Front is on the playing-front side and Back on the far side.

## What the evidence now tells us

We can now reproduce the **ordering** of F/M/B from OSM hole routing + green geometry.

For the recovered historical test:
- projecting green boundary vertices onto the final hole-route direction places the historical Front near the front extreme;
- the historical Back is near the back extreme;
- the historical coordinates are actual source vertices, not fabricated points.

However, the historical Middle is **not exactly the mathematical polygon centroid of this green**. Therefore the previous assumption that the old UiDo M point was simply the centroid must be discarded.

## Current derivation hypothesis

The evidence supports a deterministic geometric method based on:
1. hole routing establishes playing direction;
2. associated green polygon supplies the source boundary;
3. Front/Back are selected from the green boundary in that direction;
4. Middle is a point derived from the green geometry along the playing axis.

The exact historical point-selection rule is still under investigation. In particular, we need to determine why the historical F/B vertices are selected rather than the absolute projection extrema, and how the historical M point was generated.

## Architecture decision

F/M/B remains a **derived property of the provider-neutral course model**, with OSM green geometry and hole routing retained as source evidence.

A separate F/M/B GPS provider is therefore not required for the current proven source relationship, but the exact universal derivation rule must be validated before it is promoted to production.

## Next validation

1. Analyse all 18 Overstone greens against their hole-route directions.
2. Identify the geometric rule that selects F/B source vertices.
3. Determine the historical M rule.
4. Run the resulting candidate algorithm against Poult Wood.
5. Record exceptions and only then promote the rule to standard acquisition.
