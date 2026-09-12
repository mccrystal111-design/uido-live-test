# UiDo Build Log

## 2026-09-12

### v0.7 Integrated Round started
- Android version bumped from v0.6 sharper imagery to v0.7 integrated round (version code 8).
- Added canonical project-state documentation.
- Added canonical design-decision documentation.
- Android GitHub Actions build workflow now triggers for `android/**` and `gps.html` changes.
- Integrated the new UiDo home, course selection, on-course map, pre-shot context, shot capture, scoring, round review, scorecard and export screens into `gps.html`.
- Triggered a fresh Android build by making a no-op functional UI-file change after fixing the workflow trigger.
- Next step: verify the new GitHub Actions run and APK artifact, then test the integrated flow on-device.
