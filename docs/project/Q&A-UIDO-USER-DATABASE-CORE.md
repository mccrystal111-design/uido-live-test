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

### Q11 — Multiple rounds on the same day
**Decision:** YES.

A customer can play multiple rounds or sessions on the same day. Each completed round/session is captured separately with its own start/end boundaries and unique Round ID.

### Q12 — Course and course-version linkage
**Decision:** YES.

Each round gets a unique, permanent **Round ID** and stores the **canonical Course ID** and the **Course Version ID** used for that round. New rounds can use the current course version; historical rounds retain the version used when they were played.

### Q13 — Practice rounds and practice sessions
**Decision:** YES.

Core should distinguish practice activity from rounds intended as scored/official golf. Practice sessions can be fully logged, including shots and results, without being treated as official handicap rounds.

This also supports practice such as playing only three holes or repeatedly hitting shots from a particular position. The customer should be able to review those practice shots and their results.

WHS/GHIN treatment of official rounds remains governed by the relevant external rules/integration and should not be hard-coded into the basic Core data model.

### Q14 — Course-independent sessions
**Decision:** DEFERRED.

The normal round flow is course-linked because the course is needed for yardages and decision support. A course-independent practice/session mode may be useful later, particularly for offline or specialized practice, but no final database requirement was set.

### Q15 — Round start GPS
**Decision:** YES / implicit.

When a round is started and the app has GPS, the round should capture the start location as part of the round record.

### Q16 — Manual course selection / GPS fallback / offline mode
**Decision:** YES for manual selection; offline mode remains a product requirement to investigate.

When GPS is working, the nearest appropriate course can be presented for confirmation. The customer must also be able to manually select a course if GPS is unavailable or incorrect.

The round/session should retain how the course was selected.

A paid/offline-capable product may later allow course data to be stored locally so the app can operate without a live data connection. This is primarily a product/storage decision rather than a blocker for the Core customer schema.

### Q17 — Tee selection and round conditions
**Decision:** YES — log the customer's selections.

Core must store the tee selected for each round because tee selection affects handicap calculations and course rating/slope. Relevant course/tee rating information should remain associated with the round so the historical context is preserved.

### Q18 — Device information
**Decision:** YES.

Core should record the device/context used to capture a round or session. This can support product improvement, understanding transitions between phone/watch/other devices, customer research, and future device/integration opportunities.

Device information should be treated as useful customer/product telemetry and retained appropriately.

### Q19 — Customer preferences/settings
**Decision:** YES — keep preferences/settings conceptually separate from historical player data.

Customer preferences may change independently of historical golf records. Examples include units, notifications, preferred/default tees and other app settings.

A default tee preference can be stored, but the customer's actual tee choice for each round must be recorded independently. UiDo should not dictate which tee a customer plays based solely on history; conditions, season, course availability, competitions and personal practice goals can change the appropriate choice.

### Q20 — Equipment history
**Decision:** YES — retain history, not just the current bag.

Core should store equipment changes over time so UiDo can eventually help customers understand whether improvement is associated with equipment changes, practice, or player development.

### Q21 — Club inventory and carry distances
**Decision:** YES.

Core should store the customer's club inventory and typical/known carry distances. This is part of the data available to UiDo's decision engine.

### Q22 — Core data-model versioning
**Status:** OPEN / not yet decided.

Question: should the Core data model/schema itself be versioned so schema changes are traceable, migrations are safer, and the evolution of Core is auditable?

## Working rules for future Q&A

1. Ask one genuine unresolved Core-database question at a time.
2. Do **not** re-ask previously settled UiDo product, UI, stats, handicap or shot-flow decisions.
3. If a question depends on an existing UiDo decision, retrieve/check the project source of truth first.
4. Record each confirmed answer in this log.
5. Keep Core comprehensive; define Hawk as a subset/variant after the Core model is established.
6. Where the user has made a product decision rather than a database decision, record the database implication without unnecessarily forcing a schema decision.
