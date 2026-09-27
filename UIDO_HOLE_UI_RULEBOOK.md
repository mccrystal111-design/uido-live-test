# UiDo — Universal Hole & Shot-View Rulebook

**Status:** Draft v0.1  
**Purpose:** Course-agnostic UI, camera, GPS, annotation and interaction rules for every UiDo golf hole.  
**Reference implementation:** Overstone playground  
**Principle:** Overstone is the validation course, not the specification. Rules in this document must work for any valid UiDo course model.

## 1. Core principle

UiDo separates four things:

1. **Course data** — authoritative geometry and course-model facts.
2. **Player state** — GPS/test position, heading, speed and shot state.
3. **Camera state** — what part of the course is visible and at what scale.
4. **Screen/UI state** — where the player, labels, rail and controls appear on the device.

A change to one layer must not silently alter another.

**Never move course geometry to solve a screen-layout problem.**

## 2. Coordinate-language contract

When discussing UI positioning, all human-facing positioning instructions refer to **screen position**, not camera coordinates.

- X = left → right
- Y = top → bottom
- 0% = screen edge
- 50% = centre
- 100% = opposite edge

Example: **Player X 35%, Y 85%** means the player arrow must visibly render at that screen position. It does not mean moving GPS coordinates, course geometry, or the hole coordinate system.

The renderer is responsible for translating the requested screen position into camera coordinates.

## 3. Safe playing area

The physical screen and usable playing area are different. UI such as the information rail, safe areas and bottom controls occupy screen space.

The camera should therefore target the player within a **UiDo safe playing area**, not blindly against the physical viewport centre.

If the rail changes width, player/camera composition must adapt without changing course geometry.

## 4. Course loading sequence

When a course is loaded:

1. Load course identity and hole count.
2. Load the selected hole model: par, line of play, green F/M/B, source features, bunkers, water, tees, fairway, rough, paths and verified strategic data.
3. Establish the local rendering frame:
   - local X = left/right relative to the hole
   - local Y = direction of play
   - metres-per-pixel
   - hole bounds
4. Establish initial camera:
   - selected hole fully visible where practical
   - hole aligned to direction of play
   - player at tee/test position
   - annotations shown according to zoom rules
   - GPS follow off unless explicitly enabled
5. Establish UI state: hole selector, rail, controls, GPS state, zoom state and shot state.

## 5. Player position

There is one authoritative player position: **GPS/test position**.

The renderer may maintain a smoothed display position, but this is presentation state only.

### GPS ON
- GPS position becomes authoritative.
- Player follows GPS.
- Camera follows player.
- GPS fixes must not move or rotate course geometry.
- Smoothing may interpolate between fixes.
- Prediction may only be short-lived and must never replace GPS.

### GPS OFF
- GPS watch stops.
- GPS follow stops.
- Player returns to the defined test/manual position.
- Manual map tapping may establish player position.

## 6. Player marker

The player marker is a screen-space marker anchored to GPS/test position.

- Marker position comes from the camera transform.
- Marker visual size remains screen-relative.
- Marker orientation follows reliable travel heading.
- If heading is unavailable, course travel direction is the fallback.
- Heading must never rotate the course coordinate frame.

## 7. GPS camera-follow rule

The camera does not chase GPS coordinates directly in screen space.

The sequence is:

**GPS position → player screen position → camera position**

1. GPS gives player position.
2. Transform player into the hole coordinate frame.
3. Determine desired player screen position from the safe-playing-area rule.
4. Solve the camera position backwards.
5. Smoothly approach that camera target.

## 8. GPS movement behaviour

GPS fixes can arrive irregularly.

- Camera must not snap between fixes.
- Displayed player should smoothly approach new fixes.
- Short-term speed/heading prediction may maintain apparent movement.
- Prediction must be capped.
- New GPS fixes always correct prediction.
- GPS loss must not cause indefinite dead reckoning.

Desired behaviour:

**walk → player moves progressively → course slides smoothly → camera catches up gently**

not:

**walk → freeze → GPS fix → jump**

## 9. Hole orientation

The selected hole establishes a stable direction-of-play frame.

- Direction of play is visually up-course.
- Left/right are relative to the hole.
- The course frame remains stable while the player moves.
- GPS movement must not continually recompute the visual orientation.
- Curved hole geometry remains curved; the camera frame remains stable unless a future explicit heading-follow rule is adopted.

## 10. Automatic zoom

Zoom is a camera property, not a course property.

### Base zoom
Derived from hole bounds, viewport and safe playing area.

### GPS approach zoom
When GPS follow is active, zoom may progressively increase as the player approaches the green.

**Distance to green middle → continuous zoom target**

not threshold-based jumps.

The curve must have a start distance, end distance, minimum zoom, maximum zoom and smooth interpolation.

Automatic zoom must have a hard maximum. The green and immediate decision context must remain usable.

### Manual zoom
Manual zoom takes precedence. Automatic zoom must not immediately fight a user zoom action. A defined re-engagement rule may return control to automatic zoom.

## 11. Annotation visibility by zoom

Zoom is also a semantic display state.

### Whole-hole
Show course geometry, player, green location and essential context. Hide excessive yardage/detail.

### Shot view
Show player, green F/M/B and relevant bunker yardages.

### Close approach
Show green and relevant bunker detail, while keeping labels readable and non-overlapping.

## 12. Green F/M/B

- F/M/B coordinates come from the course model.
- Live yardages are calculated from player position.
- Labels must not move the underlying F/M/B coordinates.
- Screen placement may adapt for readability.
- F/M/B appears when zoom provides enough context to be useful.

## 13. Bunker labels

Bunker geometry is authoritative.

- Front/back yardages are calculated from current player position.
- Label remains associated with its bunker.
- Placement uses the actual bunker polygon.
- Left/right uses verified bunker semantics, with geometry fallback.
- Complete label should sit outside the bunker where practical.
- Label must not drift toward the green because the player moves.
- Labels should not overlap F/M/B where avoidable.
- If clean display is impossible, relocate/reduce the annotation rather than changing geometry.

## 14. Annotation collision rules

Annotations are presentation objects and must never alter course geometry.

Priority:
1. Player marker
2. Green F/M/B
3. Relevant bunker labels
4. Secondary annotations

Lower-priority annotations move or hide first when collisions occur.

## 15. Information rail

The rail is a UI layer above the course, never a hole boundary.

The course renders underneath it. The safe playing area accounts for the rail so important playing information is not hidden.

Current contents:
- course/hole selector
- par
- green F/M/B
- relevant bunker information
- GPS status

## 16. Bottom controls

- **Course** — full-course navigation
- **−** — zoom out
- **+** — zoom in
- **Fit** — fit selected hole to safe playing area
- **Zoom to Shot** — standard shot-view scale
- **GPS** — enable live GPS
- **GPS On** — GPS active; tapping disables it

Button actions are deterministic and must not silently change another state unless documented.

## 17. Fit

Fit calculates the camera from selected hole bounds, viewport and safe playing area.

Fit must not change source geometry, hole orientation or GPS position.

## 18. Zoom to Shot

Zoom to Shot establishes the standard shot-view scale.

It should:
- centre the current player appropriately
- show useful forward hole context
- preserve stable hole orientation
- respect safe playing area
- avoid placing the player under the rail

## 19. Course view

Course view is navigation, not aiming instruction.

Future rules:
- show the whole course
- show hole positions/routes
- highlight current hole
- allow tapping a hole to enter it
- optionally provide quick navigation to nearby holes

Course view should not inherit shot-view annotation clutter.

## 20. Manual pan

Manual pan temporarily overrides automatic camera positioning.

- Drag changes camera only.
- GPS position does not change.
- Course geometry does not change.
- GPS follow may suspend according to a defined interaction rule.
- A future explicit re-centre/follow action should restore GPS follow.

## 21. Pinch/wheel zoom

Pinch and wheel zoom change camera scale only.

They must not change player position, course geometry, hole orientation or GPS state.

## 22. Free-aim layer

Future free aim is a separate decision layer.

It must not modify course geometry or player GPS.

Potential rules:
- aim point starts at a defined distance along shot direction
- optional constrained aim circle
- player → aim point line
- aim point → green-middle line
- live aim distance
- draggable aim point
- all aim graphics are presentation/decision state

## 23. Course-agnostic requirement

Nothing in this rulebook may depend on Overstone coordinates, hole numbers, bunker IDs, a particular phone or a particular course shape.

Overstone is the reference test case only.

## 24. Source-of-truth hierarchy

When systems disagree:

1. **Authoritative course model**
2. **Live GPS/player state**
3. **Camera transform**
4. **Screen/UI presentation**
5. **Decorative/debug elements**

Never change a higher-level source to compensate for a lower-level presentation problem.

Example: if a bunker label is wrong, change label placement—not bunker geometry.

## 25. Debugging protocol

Describe UI positioning in screen language.

Preferred:
- “Player is too high; move down about 5%.”
- “Green is being hidden behind the rail.”
- “Bunker label is sitting on the green.”

Avoid:
- “Move camera left.”
- “Move the geometry.”
- “Shift the hole.”

The implementation translates the requirement into camera mathematics.

## 26. Acceptance test for every new course

### Load
- [ ] Course loads without changing source geometry
- [ ] Correct hole count
- [ ] Correct selected hole
- [ ] Correct par

### Orientation
- [ ] Direction of play correct
- [ ] Left/right sense correct
- [ ] Hole frame remains stable while GPS moves

### Player
- [ ] Test player at defined position
- [ ] GPS player follows live position
- [ ] Player remains in defined safe screen position
- [ ] Heading behaves correctly

### Camera
- [ ] Fit works
- [ ] Zoom to Shot works
- [ ] Manual zoom works
- [ ] Pinch zoom works
- [ ] Manual pan works
- [ ] GPS follow is smooth

### Annotations
- [ ] F/M/B correct
- [ ] Bunker yardages correct
- [ ] Labels attach to correct geometry
- [ ] Labels do not unnecessarily overlap
- [ ] Annotation visibility changes correctly with zoom

### UI
- [ ] Rail does not clip important course context
- [ ] Bottom controls work
- [ ] GPS toggle works
- [ ] Course navigation works

## 27. Rulebook change policy

When a UI problem is found:

1. Describe observed behaviour.
2. Identify which rule is violated.
3. Change the rule if the behaviour is wrong universally.
4. Change renderer implementation if the rule is correct but implemented incorrectly.
5. Validate against Overstone.
6. Validate against at least one other course before promoting a universal rule.

Do not keep stacking one-off Overstone patches when the underlying rule is unclear.

## 28. Current unresolved design decisions

These need explicit decisions before becoming universal rules:

- Exact safe-playing-area definition around the rail.
- Exact default player screen position.
- Exact automatic zoom curve and maximum.
- When manual pan suspends GPS follow.
- When GPS follow resumes.
- Exact annotation collision algorithm.
- Exact transition between whole-hole, shot and close-approach annotation states.
- Whether camera orientation should ever follow player heading.
- Full-course navigation presentation.
- Free-aim interaction model.

These are **rules to define**, not implementation bugs to patch around.
