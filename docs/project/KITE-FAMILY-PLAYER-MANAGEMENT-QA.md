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

**Still open:** the sign-in identifier and credential setup method have not yet been decided.

## Open questions

1. Decide how the parent creates the junior's managed sign-in: child email, parent-managed username, or another approach.
2. Continue one focused question at a time on adding, editing, switching, and managing family player profiles.
