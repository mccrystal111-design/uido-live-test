# UiDo Decisions

## v0.7 Integrated Round

- UiDo is the product; the live-test flow is the embedded data-generation layer.
- Before-shot and after-shot data remain explicitly separated.
- Club is never requested before the shot; actual club is recorded after the shot.
- Shot shape is exactly five options: Hook, Draw, Straight, Fade, Slice. Slight Draw and Slight Fade are removed.
- Strike location is a 3×3 club-face grid.
- Heavy is a separate `strike_quality` value, not a face-location option.
- GPS accuracy/confidence must be displayed and captured with the position.
- The pre-shot context should be auditable: distance, GPS accuracy, heading, lie, wind and pin can be shown for confirmation/editing before capture.
- v0.7 is focused on reliable data capture and round completion, not full AI decision intelligence.
- 2026-09-12: Integrated the new UiDo home, course selection, on-course map, pre-shot context, shot capture, scoring, round review and scorecard screens into `gps.html`, which is the screen loaded by the Android wrapper.
