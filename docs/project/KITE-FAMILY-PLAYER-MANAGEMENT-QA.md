# Kite Family & Player Management Q&A

**Status:** In progress  
**Started:** 14 October 2026

## Scope

This Q&A records the family and multi-player management direction following the user's request to continue beyond the adult V1 Player Profile work. The project decision log previously kept junior/family UI as future scope for adult V1 curation. This Q&A does not, by itself, change that delivery scope or revise existing decisions.

Preserve the established product model: Kite is one app for adult and junior players; a family/account can contain multiple player profiles; the parent can switch between players and track a child's shots and rounds; the child can use the same app independently; do not create a separate kids mode.

## Confirmed decisions

### FQ-01 — Junior dashboard is under the parent's account and available on laptop

**Confirmed 14 October 2026.** The junior should be able to access a dashboard on a laptop to view their points, badges, and similar information. The junior's account/profile should remain under the parent's account.

### FQ-02 — Junior has a sign-in managed by the parent

**Confirmed 14 October 2026.** The junior should have their own sign-in, managed by the parent, while the junior account/profile remains under the parent's account.

### FQ-03 — Parent-created username; junior email not required

**Confirmed 14 October 2026.** The parent can create a username for the junior. The junior does not need their own email address.

### FQ-04 — Parent manages junior password changes and resets

**Confirmed 14 October 2026.** The parent manages all password changes and resets for the junior sign-in.

### FQ-05 — Use a chosen display name or nickname

**Confirmed 14 October 2026.** Show the junior's chosen display name or nickname in the family player list and junior dashboard.

### FQ-06 — Junior sign-in is restricted to its own player profile

**Confirmed 14 October 2026.** When signed in with the junior username, the junior can access only their own player profile and cannot switch to other family players.

### FQ-07 — Junior can change their own display name

**Confirmed 14 October 2026.** The junior can change their own chosen display name or nickname.

### FQ-08 — Junior mode is selected for the round and lasts until the round is saved

**Confirmed 14 October 2026.** When a junior is selected while adding a player, Kite switches into junior mode for that round. Junior mode remains in effect until that round is saved; it is not a persistent app-wide player context.

### FQ-09 — Adult and junior players can play in the same round

**Confirmed 14 October 2026.** A single round can include both adult and junior players.

### FQ-10 — Junior mode applies to the whole mixed round

**Confirmed 14 October 2026.** If adult and junior players are included together, junior mode applies to the entire round, not only the junior participant.

### FQ-11 — Each player in a mixed round chooses their own tee

**Confirmed 14 October 2026.** In a round with adults and juniors, each player can choose their own tee.

## Open questions

1. Decide whether Stroke Play / Stableford is chosen once for the whole round or separately by each player.
2. Continue one focused question at a time on adding, editing, switching, and managing family player profiles.
