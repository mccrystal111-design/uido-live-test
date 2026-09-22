# UiDo F/M/B Green Coordinate Derivation

## Status

**Validated on Overstone hole 1.**

The investigation recovered the original UiDo Overstone Front/Middle/Back GPS values from the historical live-test HTML and compared them with the recovered Overstone OSM source.

## Proven derivation

The historical Overstone hole 1 values were:

- Front: `52.2762446, -0.8166103`
- Middle: `52.2761187565, -0.8166885565`
- Back: `52.2759866, -0.8167443`

The recovered OSM source contains:

- `way/798091452` tagged `golf=green`
- `way/798140682` tagged `golf=hole`, `ref=1`

The green polygon contains the historical Front and Back coordinates as boundary vertices. Its centroid is:

- latitude: `52.27611875652174`
- longitude: `-0.8166885565217391`

which matches the historical Middle coordinate to floating-point precision.

The hole routing runs from the south-western end of the hole towards the north-eastern end, establishing the playing direction needed to distinguish Front from Back.

## UiDo derivation model

For a hole with valid OSM routing and green geometry:

1. Obtain the hole routing geometry.
2. Determine the direction of play from the hole routing.
3. Associate the relevant `golf=green` geometry.
4. Determine the green boundary endpoints in the playing direction.
5. Derive Front from the boundary at the playing-front end.
6. Derive Back from the opposite boundary.
7. Derive Middle from the green polygon centroid.
8. Store the resulting F/M/B coordinates as **derived course-model data**.
9. Preserve the original OSM geometry and provenance; never overwrite the source geometry.

## Important qualification

The Overstone hole 1 comparison proves that this derivation reproduces the original historical coordinates for that hole.

It does **not** yet prove that the exact same boundary-selection rule reproduces historical F/M/B values for every Overstone hole, nor that it is optimal for every course.

## Next validation

1. Run the deterministic derivation across all 18 Overstone holes.
2. Compare against any recovered historical UiDo F/M/B coordinates.
3. Run the same method against Poult Wood.
4. Record exceptions where OSM green geometry is incomplete, ambiguous or unsuitable.
5. Only then promote the method to the standard course-acquisition pipeline.

## Architecture decision

UiDo should treat F/M/B as a **derived property of the provider-neutral course model**, with OSM green geometry and hole routing retained as the source evidence.

A separate F/M/B GPS provider is therefore **not required for the proven Overstone case**. External providers can remain optional validation/fallback sources if later testing demonstrates a need for them.
