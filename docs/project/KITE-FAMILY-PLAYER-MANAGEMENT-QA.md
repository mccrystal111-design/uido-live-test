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

### FQ-28 — Parent starts and manages rounds on the parent’s phone

**Confirmed 14 October 2026.** Round setup and starting should be handled by the parent on the parent’s phone. A junior signing in should not start a round themselves.

### FQ-29 — Junior sign-in is for the laptop dashboard only

**Confirmed 14 October 2026.** The junior uses their own sign-in for the laptop dashboard only. Round setup and play are managed by the parent on the parent’s phone.

### FQ-30 — Co-parent or guardian can help manage the family

**Confirmed 14 October 2026.** A co-parent or guardian can help manage the family account and junior profiles.

### FQ-31 — Co-parent has the same management access as the account owner

**Confirmed 14 October 2026.** A co-parent or guardian who is granted family access has the same management permissions as the account-owning parent.

### FQ-32 — Either parent can manage guardians

**Confirmed 14 October 2026.** Either the account-owning parent or an equally privileged co-parent can invite or remove a co-parent or guardian.

### FQ-33 — Co-parent access is granted immediately

**Confirmed 14 October 2026.** When a parent adds a co-parent or guardian, family access is granted immediately; the new co-parent does not need to accept an invitation first.

### FQ-34 — Co-parent can be created as a dashboard profile and linked to Kite account if needed

**Confirmed 14 October 2026.** A co-parent or guardian can be created as a parent profile within the family dashboard. That profile can be linked to a Kite account if needed.

### FQ-35 — Co-parent profile can be managed without a separate sign-in

**Confirmed 14 October 2026.** A co-parent profile in the family dashboard can be managed without linking it to a separate Kite sign-in.

### FQ-36 — Co-parent can link their own Kite account

**Confirmed 14 October 2026.** If a co-parent wants their own Kite sign-in later, they can connect their own Kite account to their existing family dashboard profile.

### FQ-37 — Family management access requires an existing Kite account

**Confirmed 14 October 2026.** An adult without a Kite profile is treated as a guest. An adult with an existing Kite account can be added to a family profile, which gives them access to manage the family profile. This clarifies the co-parent discussion: the earlier idea of an unlinked co-parent profile independently managing family data is superseded. Equal co-parent management access and guardian management apply once a Kite account is added to the family profile.

### FQ-38 — Guest players can be selected again by name

**Confirmed 14 October 2026.** A guest is a name that can be selected again as a previously selected player in a later round; the guest does not need a Kite account.

### FQ-39 — Parent can enter a guest’s handicap

**Confirmed 14 October 2026.** When adding a guest player to a round, the parent can enter that player’s handicap so the round scoring can use it.

### FQ-40 — Save guest handicap with reusable name

**Confirmed 14 October 2026.** Save a guest’s handicap with their reusable name so it is available for future rounds.

### FQ-41 — Saved guest name and handicap can be edited

**Confirmed 14 October 2026.** A saved guest entry includes the guest’s name and handicap, and both can be edited for future rounds.

### FQ-42 — Junior dashboard shows past rounds and scorecards

**Confirmed 14 October 2026.** The junior can view their own past rounds and scorecards on the laptop dashboard, in addition to points and badges.

### FQ-43 — Junior can see all players’ scores on mixed-round scorecards

**Confirmed 14 October 2026.** When viewing a mixed adult-and-junior round scorecard, the junior can see all players’ scores, not only their own.

## Open questions

1. Future “fun” scoring methods may be offered; their formats and rules have not yet been decided.
2. Continue one focused question at a time on adding, editing, switching, and managing family player profiles.
