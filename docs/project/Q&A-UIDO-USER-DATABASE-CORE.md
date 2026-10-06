# UiDo Core — User Database Q&A Log

**Purpose:** Durable decision log for the UiDo Core customer/user database.  
**Working mode:** Voice Q&A, one question at a time.  
**Principle:** UiDo Core is the complete customer/data model; Hawk is a simplified product variant that displays a subset of Core.

## Decisions

### Q1 — One permanent customer identity
**Decision:** YES — one permanent UiDo identity.

A customer has one account/identity that follows them through Hawk and full UiDo. Existing data remains attached to the same customer when they upgrade.

### Q2 — Core captures the full customer golf record
**Decision:** YES.

UiDo Core should aim to capture as much useful player data as reasonably possible. This includes the customer's home club, handicap information, shots, scorecards and other relevant golf data. Hawk will display only the subset appropriate to the simplified product.

### Q3 — Shot data
**Decision:** Capture the full UiDo shot-data flow, **if available**.

Relevant shot-event information can include GPS/location, club, lie, wind, trajectory, shape, outcome and other available inputs from the UiDo flow.

### Q4 — Free Aim / decision data
**Decision:** Capture additional decision information when relevant to Free Aim.

If a player selects **Free Aim** and then hits the shot, UiDo may prompt the player afterwards to confirm what happened / whether they decided something different. This should **not** be a prompt after every shot; it is specifically associated with Free Aim.

### Q5 — Official and UiDo handicaps
**Decision:** Core must support official handicap information and UiDo's own Practice Handicap separately.

UiDo should integrate with **WHS and GHIN** when the relevant APIs/integrations are available and display official handicap information. UiDo Practice Handicap is separately calculated/stored from UiDo round data. These values should not overwrite each other.

The database should be extensible for external handicap providers without requiring a later rebuild.

### Q6 — Future third-party integrations
**Decision:** YES — design Core to be integration-friendly.

Core should be flexible enough to accept future third-party data sources such as **TrackMan**, Garmin and other relevant services. External source data should retain its source identity rather than being destructively merged into UiDo's interpretation.

### Q7 — External source data and UiDo interpretation
**Decision:** Keep both.

Original user/device data supplied by external systems should be retained alongside the customer's Core data. UiDo's interpretation/calculations should be stored separately so the original source record is preserved.

### Q8 — Data deletion / retention
**Decision:** Retain useful statistical data; do not immediately destroy the golf history when a customer retires/deletes their active account.

The current direction is:
- Retain retired customer data in a recoverable state for approximately **5 years**
- Retain golf/statistical value for the decision engine
- After the 5-year recoverable period, **anonymize** the customer-linked data rather than simply deleting the useful statistical history
- If a customer returns within the recoverable period, their previous history should be capable of being restored to their account

Exact legal/privacy implementation and retention policy still needs to be finalized against applicable requirements.

### Q9 — Hawk versus Core
**Decision:** Core first, Hawk subset second.

The Core database should contain the complete UiDo customer/data model. Hawk should be defined afterwards as a simplified view/product variant that exposes only the fields and functionality appropriate to Hawk.

We should not constrain the Core database around Hawk's reduced feature set.

### Q10 — Entitlements / upgrade model
**Decision:** DEFERRED.

We do not need to finalize subscription/entitlement schema while defining the Core customer database. First define the complete Core model; then determine how Hawk maps onto it and add access/entitlement controls where necessary.

## Questions not yet answered

### Q11 — Core data-model versioning
**Status:** OPEN.

Question asked: should the Core data model/schema itself be versioned so schema changes are traceable, migrations are safer, and the evolution of Core is auditable?

### Other open database questions
Only genuine gaps should be added here. Previously settled UiDo product/UI/statistics decisions should be retrieved from the existing project documentation rather than re-asked during this Q&A.

## Working rules for future Q&A

1. Ask one genuine unresolved Core-database question at a time.
2. Do **not** re-ask previously settled UiDo product, UI, stats, handicap or shot-flow decisions.
3. If a question depends on an existing UiDo decision, retrieve/check the project source of truth first.
4. Record each confirmed answer in this log.
5. Keep Core comprehensive; define Hawk as a subset/variant after the Core model is established.
