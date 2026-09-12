# UiDo Project State

**Current build:** v0.7 Integrated Round
**Updated:** 2026-09-12

## Canonical objective
Complete a real round in UiDo from New Round → hole navigation → pre-shot context → shot capture → scoring → scorecard → round finish → export, while preserving reliable before/after shot data.

## Current product position
UiDo is a proper golf app. The former live-test experience is the data-generation layer inside the product.

## Data rule
Do not ask for club before the shot. Record the actual club after the shot / in round review so UiDo can later compare its decision with what the player actually selected.

## Post-shot fields
- Shape: Hook, Draw, Straight, Fade, Slice
- Start line
- Lie
- Strike location: 3×3 face grid
- Strike quality: Heavy is a separate field
- Wind
- Actual club
- Shot distance

## Before-shot context
Capture automatic GPS latitude/longitude/accuracy/timestamp and heading where available, plus course/hole/par/green/yardages and player-confirmed pin, wind and lie. GPS confidence must be visible; never assume a poor fix is accurate.

## v0.7 priority
Wire the existing screens and data into one reliable integrated round. Do not add full decision-engine intelligence yet.

## APK
Android wrapper currently builds from `android/`, version code 8, version name `0.7-integrated-round`. GitHub Actions workflow builds the debug APK when `android/**` changes.
