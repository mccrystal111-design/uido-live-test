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

### FQ-12 — Mixed round uses one scoring format

**Confirmed 14 October 2026.** All players in a mixed adult-and-junior round use the same scoring format, such as Stroke Play or Stableford.

### FQ-13 — Standard formats use each player's own handicap

**Confirmed 14 October 2026.** In standard Stroke Play or Stableford, apply each player's own handicap to their score. Future “fun” scoring methods may be offered; their formats and rules remain undecided.

### FQ-14 — Parent can create a junior profile while adding them to a round

**Confirmed 14 October 2026.** The parent can create a junior profile inline as part of adding a player to a round, rather than needing to create it beforehand in family/player management.

### FQ-15 — Parent sets the initial junior password

**Confirmed 14 October 2026.** When creating the junior sign-in, the parent sets its initial password. The parent also manages later password changes and resets.

### FQ-16 — Animal PIN is an additional junior sign-in element

**Confirmed 14 October 2026.** Use an animal-based PIN where each animal represents a number. The animal PIN is used in addition to the regular password; it does not replace the password.

### FQ-17 — Junior profile persists if the round is cancelled

**Confirmed 14 October 2026.** If a parent creates a junior profile during round setup and then cancels the round, keep the junior profile in the family account.

### FQ-18 — Junior enters the animal PIN at every sign-in

**Confirmed 14 October 2026.** The junior enters their animal PIN every time they sign in, alongside the regular password.

### FQ-19 — Animal PIN contains four animals

**Confirmed 14 October 2026.** The junior animal PIN uses a sequence of four animals, with each animal representing a number.

### FQ-20 — Junior chooses their animal PIN

**Confirmed 14 October 2026.** The junior chooses their four-animal PIN sequence. The parent remains responsible for managing PIN resets.

### FQ-21 — Parent can choose how to remove a junior profile

**Confirmed 14 October 2026.** When removing a junior from family management, give the parent options to disable/remove the junior sign-in while keeping their round history, or delete the profile and its history.

### FQ-22 — Parent alone can change a junior’s handicap

**Confirmed 14 October 2026.** Only the parent can change the junior’s handicap.

### FQ-23 — Junior uses parent-chosen username and animal PIN

**Confirmed 14 October 2026.** The junior signs in with a username chosen by the parent and the four-animal PIN. The username is not animal-themed.

### FQ-24 — Both parent and junior can change the display name

**Confirmed 14 October 2026.** The junior can change their own display name, and the parent can change it as well.

### FQ-25 — Both parent and junior can manage clubs and carry distances

**Confirmed 14 October 2026.** Both the parent and junior can manage the junior’s club list and carry distances.

### FQ-26 — Both parent and junior can change home course and preferred tees

**Confirmed 14 October 2026.** Both the parent and junior can change the junior’s home course and preferred tees.

### FQ-27 — Both parent and junior can change junior app preferences

**Confirmed 14 October 2026.** Both the parent and junior can change the junior’s app preferences, including units such as yards or metres.

## Open questions

1. Future “fun” scoring methods may be offered; their formats and rules have not yet been decided.
2. Continue one focused question at a time on adding, editing, switching, and managing family player profiles.
