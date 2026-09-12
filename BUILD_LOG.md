# UiDo Build Log

## 2026-09-12

### v0.7 Integrated Round started
- Android version bumped from v0.6 sharper imagery to v0.7 integrated round (version code 8).
- Added canonical project-state documentation.
- Added canonical design-decision documentation.
- Existing Android GitHub Actions build workflow is configured to build a debug APK when `android/**` changes.
- Next build step: let GitHub Actions produce the v0.7 debug APK, then verify the resulting artifact before testing on-device.
