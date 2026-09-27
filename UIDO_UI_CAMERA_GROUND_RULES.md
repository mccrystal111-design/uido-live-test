# UiDo — UI & Camera Ground Rules

**Status:** Working agreement v0.1  
**Purpose:** Establish the shared language and design rules for UiDo's hole UI, camera, GPS, positioning and annotations before implementation changes are made.  
**Reference course:** Overstone  
**Scope:** Course-agnostic. Overstone is used to test the rules, not to define them.

---

## 1. Visual result is the specification

When a positioning or camera requirement is discussed, the intended **visible screen result** is the primary specification.

We do not assume that a verbal description such as:

- left
- right
- down
- behind
- ahead
- near the bottom
- move the camera

has the same meaning in code as it does visually.

Before implementation, convert the requirement into an explicit screen specification wherever practical.

Example:

```
Player:       X 82%  Y 88%
Green middle: X 54%  Y 18%
```

The implementation may use any camera mathematics required to achieve that result.

**Do not make the user reason in camera coordinates.**

---

## 2. Screen coordinates have one fixed meaning

For UI/storyboard communication:

- **X = left → right**
- **Y = top → bottom**
- **0% = screen edge**
- **50% = screen centre**
- **100% = opposite screen edge**

These coordinates describe the **visible screen**, not course geometry and not camera coordinates.

A statement such as:

> Player X 82%, Y 88%

means the player marker must visibly appear there.

It does not mean moving the GPS position or course geometry.

---

## 3. Storyboards are the bridge between human intent and code

We will use a dedicated storyboard to test whether visual instructions can be translated reliably into code.

The process is:

**User positions objects visually → screenshot + numeric specification → independent renderer recreates them → compare result.**

This gives us a way to test the translation rather than assuming it is correct.

The storyboard selector and renderer are separate tools deliberately.

---

## 4. Do not use fixed screen coordinates for course features

Player/camera composition may have deliberate screen positions.

Course features such as bunkers, trees, water and greens must **not** be defined by fixed screen coordinates.

Their screen positions are consequences of:

1. Course geometry
2. Direction of play
3. Player position
4. Camera position
5. Camera scale
6. Safe UI area

The same rule must work on different holes and different courses.

---

## 5. Course-side and screen-side are different concepts

Every feature may have a **course relationship** and a **screen position**.

They must never be treated as the same thing.

### Course relationship

For example:

```
Bunker:
side = LEFT
```

means the bunker is on the **left side of the hole relative to direction of play**.

It does **not** mean:

> The bunker must appear on the left side of the phone screen.

### Screen position

The renderer calculates:

```
X = screen position
Y = screen position
```

after applying the current camera and hole orientation.

This distinction is mandatory.

---

## 6. Direction of play is the primary hole orientation reference

For UI/storyboard communication we use:

**TEE → GREEN = direction of play**

Left/right feature relationships are relative to that direction.

We do **not** need North as a normal storyboard reference.

Compass heading/North only becomes relevant when explicitly testing GPS heading, navigation or device orientation.

---

## 7. Hole loading starts from anchors, not a predefined zoom

When a hole loads, the fundamental starting references are:

- **Tee anchor**
- **Green middle anchor**

The initial camera is calculated from the relationship between those anchors and the available safe screen area.

The initial zoom is therefore an **output**, not a predefined course value.

Conceptually:

```
Tee + Green Middle + Safe Screen Area
                ↓
        Initial Camera
                ↓
        Initial Zoom
```

The objective is to establish a sensible whole-hole view with appropriate context.

---

## 8. GPS player position is independent from camera position

There is one authoritative player position.

**GPS/test position → camera presentation**

The GPS position must never be altered to make the player look better on screen.

The camera moves to present the player correctly.

Likewise:

- moving the camera must not move the player
- changing zoom must not move the player
- changing UI layout must not move the player
- changing a label must not move course geometry

---

## 9. GPS follow is a presentation rule

When GPS follow is active:

1. GPS provides player position.
2. Player position is transformed into the hole's stable coordinate frame.
3. A desired player screen position is established.
4. The camera is solved to place the player there.
5. The camera moves smoothly toward that target.

The player is therefore **anchored in screen space by the camera**, while remaining geographically anchored by GPS.

---

## 10. Camera movement must be visually continuous

GPS fixes may arrive irregularly.

The desired behaviour is:

**GPS movement → smooth player movement → smooth course movement → camera follows**

Not:

**GPS fix → sudden jump → new camera position**

Short-term prediction/interpolation can be used for presentation, but new GPS fixes remain authoritative.

---

## 11. Automatic zoom is based on the playing situation

Automatic zoom should be derived from the player's relationship to the hole/green rather than arbitrary fixed zoom levels.

The system can progressively change zoom as the player approaches the green.

The transition should be continuous and smooth.

Automatic zoom must have a defined maximum and must preserve useful decision context.

Manual zoom must not immediately fight the user's action.

---

## 12. Zoom levels are also information states

Zoom determines not only scale but how much information should be presented.

### Whole-hole view

Priorities:

- overall hole shape
- player
- green
- essential hazards/context

Avoid unnecessary detailed yardage clutter.

### Shot view

Priorities:

- player
- forward decision context
- green F/M/B
- relevant bunker information

### Close approach

Priorities:

- green detail
- relevant hazards
- readable labels
- precise decision information

Information should appear because the view has reached the appropriate **semantic detail level**, not simply because a particular hole happens to be Overstone.

---

## 13. Bunkers need a universal relationship, not a universal position

A bunker can occur anywhere on any hole.

Therefore we do **not** define:

> Bunker label = X 72%, Y 42%

Instead we define a relationship such as:

```
Bunker
  ↓
Bunker geometry
  ↓
Determine course-side relationship
  ↓
Find usable polygon edge
  ↓
Place annotation outside bunker
  ↓
Apply standard screen-space breathing room
  ↓
Resolve collisions
```

The actual screen position is calculated dynamically.

---

## 14. Bunker LEFT/RIGHT is relative to the hole

Where verified, each bunker can have:

```
side = LEFT
```

or

```
side = RIGHT
```

This is relative to the hole's direction of play.

If explicit semantics are unavailable, geometry may be used to determine the relationship.

The renderer must never confuse:

- bunker side of hole
- screen side
- device side
- compass direction

---

## 15. Bunker labels belong to bunkers

A bunker label must remain associated with its bunker.

The relationship is more important than an absolute position.

Default principle:

> **Label outside the actual bunker polygon, attached to the nearest usable/appropriate edge, with consistent breathing room.**

If the player moves, the label may change screen position because the camera changes.

It must **not** change its relationship to the bunker.

---

## 16. Labels are presentation objects

Labels must never alter:

- bunker geometry
- green geometry
- fairway geometry
- player GPS position
- hole orientation

If a label is wrong, fix the annotation rule or renderer.

Do not modify course geometry to make the label look correct.

---

## 17. Annotation collision has priorities

When annotations compete for space, use a consistent priority system.

Initial priority:

1. Player
2. Green F/M/B
3. Relevant bunker information
4. Secondary annotations

Lower-priority annotations may:

- move
- reduce detail
- disappear

before higher-priority information is compromised.

---

## 18. Trees and other features need their own semantic rules

We should not assume every course feature needs a label.

For example:

- Trees generally provide visual context rather than labels.
- Bunkers may require yardage information.
- Water may require hazard identification.
- Greens require F/M/B.
- Tees establish the starting anchor.

Each feature type should eventually have a **universal annotation policy**.

The policy is attached to the feature type, not to a particular hole.

---

## 19. The UI rail is part of the screen composition

The right-hand information rail is a UI layer.

It is not part of the course.

The camera should understand the **usable playing area** created by the rail.

The course can visually continue underneath the rail, but important decision information should not be unintentionally hidden.

The storyboard therefore includes empty rail boxes to establish the physical UI footprint.

---

## 20. The same rules must survive different holes

A universal rule is not proven because it works on Overstone Hole 1.

The development sequence should be:

1. Define rule.
2. Test on Overstone.
3. Test on a materially different hole.
4. Test on another course.
5. Only then treat the rule as universal.

If the rule requires repeated hole-specific exceptions, the underlying rule should be reconsidered.

---

## 21. No implementation changes while defining a rule

During rule definition:

**Agreement first → implementation second.**

When we identify a problem:

1. Describe what is visually wrong.
2. Translate it into screen coordinates/relationships.
3. Agree the intended rule.
4. Record the rule.
5. Implement it.
6. Test it visually.
7. Test it on another hole/course.

This prevents repeated one-off camera and positioning patches.

---

## 22. Current storyboard test protocol

For a positioning question, the preferred evidence is:

### A. Screenshot

Shows what the user wants to see.

### B. Numeric specification

Shows the exact selected X/Y positions.

### C. Semantic relationships

For example:

```
Bunker 1
course side: LEFT
label relationship: OUTSIDE
label anchor: bunker edge
```

### D. Independent reproduction

The renderer recreates the specification without using the original positioning code.

This allows us to identify whether a mismatch comes from:

- user specification
- interpretation
- coordinate translation
- camera mathematics
- rendering

---

## 23. Source-of-truth hierarchy

When systems disagree:

1. Authoritative course model
2. Live GPS/player state
3. Camera state
4. Screen/UI presentation
5. Decorative/debug elements

A lower layer must never modify a higher layer to compensate for a presentation problem.

Example:

> A bunker label is wrong → change label placement.

Not:

> A bunker label is wrong → change bunker geometry.

---

## 24. Working language

For future UI discussions, prefer:

- **screen X/Y**
- **course LEFT/RIGHT**
- **direction of play**
- **player GPS position**
- **camera position**
- **camera scale/zoom**
- **annotation relationship**
- **safe UI area**

Avoid ambiguous instructions such as:

- move it left
- move it right
- move the hole
- move the camera left
- put it behind the player

unless the reference frame is explicitly stated.

---

## 25. Ground-rule principle

The overall UiDo approach is:

> **Define relationships, not one-off positions.**

Course geometry supplies the facts.

The player supplies the current position.

The camera supplies the view.

The UI supplies the safe screen area.

The renderer calculates where things appear.

The storyboard lets us verify that the calculated result matches the intended visual result.

---

## 26. Decisions still to be made

These are deliberately **not yet locked**:

- Exact initial hole-view framing.
- Exact safe playing area.
- Exact player screen anchor during GPS follow.
- Exact automatic zoom curve.
- Exact zoom/detail thresholds.
- Exact bunker-label offset.
- Full annotation collision algorithm.
- Exact behaviour after manual pan during GPS follow.
- Full feature-type annotation rules.
- Course-map navigation presentation.

These should be agreed one at a time rather than guessed in code.

