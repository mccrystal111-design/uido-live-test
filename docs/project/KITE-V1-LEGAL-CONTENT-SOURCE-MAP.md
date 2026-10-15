# Kite V1 Legal Content — Source Map and Drafting Inputs

**Status:** Engineering inventory; not legal copy or a release-ready disclosure  
**Reviewed:** 2026-10-15  
**Repository baseline:** `main` at `34d01d206ed0dc3bd2c9555c18f3500adc98d9c8`

This document records what the repository currently supports as evidence for Kite V1 Terms of Use, Privacy Policy and Software Licences. It distinguishes documented product intent, schema/code evidence, and unresolved launch facts. Legal copy should describe the shipped V1 product, not every future UiDo Core capability or experimental prototype.

## Product and data facts evidenced in the repository

| Area | Evidence | Drafting implication |
|---|---|---|
| Account and sign-in | `hawk.html` uses Supabase Auth through `@supabase/supabase-js@2` from jsDelivr. The UI collects a name, email and password. Its text says password handling is by Supabase Auth and passwords are not stored in the app database. | Explain account credentials and the identity/authentication provider accurately for the shipped client. Verify final sign-in providers and auth configuration before publication. |
| Player profile and preferences | `database/schema/uido-core-user-data-v1.sql`: profile, home course, lifecycle/retention metadata; preferences include yards/metres, default tee and notifications. Profile identity is linked to `auth.users`. | Potential data categories: account/profile identifiers and user-selected preferences. Do not claim notification preferences are exposed in V1 Settings unless product scope changes. |
| Handicap, equipment and bag | Schema tables `uido_handicap_records`, `uido_equipment`, and `uido_clubs` preserve provider/type/effective dates, equipment details, club names/categories and carry-distance history. | Explain these as player-provided or service-derived golf profile data only to the extent the V1 flows actually collect them. |
| Rounds and scorecards | `uido_rounds` stores course/course-version, tee, session type/status/times, start location, course-selection method and device context. `uido_round_holes` stores hole number, score, putts and net score. | Potential data categories include round history, scores, tee/course choice and round-start location. Confirm which are actually collected and whether location is retained for the whole round before describing it. |
| Shot and location data | `uido_shots` has a location field and club, lie, wind, trajectory, shape, outcome, free-aim/decision note, source data, interpretation and device context. Android manifest requests coarse/fine location and foreground-location service permissions; `MainActivity.java` requests precise location and streams GPS updates while active. | Be transparent about location use, when it is collected, what it is used for, and how long it is retained. Schema alone does not prove every field is collected by V1. |
| External records | `uido_external_records` can preserve provider, record type, external ID, observed/received times, raw payload and separate interpretation. Project notes describe Garmin, TrackMan, WHS/GHIN as future/possible integrations. | Treat those providers as future unless V1 actually connects them. Inventory active integrations before naming recipients or data sources. |
| Security model | Core baseline says customer-owned tables have RLS and owner policies based on `auth.uid()`. | Describe safeguards concretely only after implementation/configuration is verified. Avoid a blanket security guarantee. |
| Retention and deletion | Core Q&A proposes about five years of recoverable retired-account data followed by anonymisation, while the baseline explicitly says final legal/privacy implementation remains open. Profile schema has active/retired/anonymized status and timestamps. | This is a proposal, not a publishable retention promise. Decide and implement retention/deletion behaviour before the Privacy Policy states a period. |
| Junior/family accounts | `docs/project/KITE-FAMILY-PLAYER-MANAGEMENT-QA.md` records V1 family/junior requirements, including parent-managed junior sign-in, junior dashboard and parent/guardian controls. Screen implementation is deferred in the current build slice. | A junior-facing product requires age-appropriate transparency and a clear parent/junior data-rights and account-management explanation. Policy and consent flow must match the actual shipped implementation. |
| Location permission | `android/app/src/main/AndroidManifest.xml` includes coarse and fine location plus foreground location service permissions. | Permission declarations show capability, not actual collection scope. Confirm foreground/background behavior, purpose and control before publishing. |

## Third-party notices evidenced by current source

| Component/source | Repository evidence | Notice status |
|---|---|---|
| Space Grotesk font | `assets/fonts/space-grotesk-license.txt` states SIL Open Font License 1.1 and identifies the source project. | License text/source are documented. Confirm which font files are actually shipped, then include the required OFL notice and any reserved font name condition. |
| Supabase JavaScript client | `hawk.html` loads `@supabase/supabase-js@2` from jsDelivr. Upstream project identifies MIT License. | Candidate for a notice if included in the distributed V1 bundle; pin the exact version and capture its complete license text in the shipped notices. |
| Leaflet | `home-preview.html` loads Leaflet 1.9.4 from unpkg. Upstream repository identifies BSD 2-Clause. | Prototype evidence only. Include only if it ships in V1; retain copyright/license/disclaimer text. |
| Esri World Imagery | `home-preview.html` uses ArcGIS World Imagery tile service. | This is a map/data service, not a software license notice. Confirm whether it is part of V1 and satisfy the current service attribution/terms. |
| Google Fonts / Oxanium | `index.html` imports Oxanium from Google Fonts. | Prototype evidence only. Confirm shipped use and obtain the exact typeface license/source before listing. |
| Android build | Gradle declares Android Gradle Plugin 8.13.0 and the app module has no declared third-party runtime dependencies. | Generate the final Android third-party notices from the actual release build/dependency graph; the current repository does not establish a complete release bill of materials. |

### Notice-source references

- [Space Grotesk source project](https://github.com/floriankarsten/space-grotesk)
- [Supabase JavaScript client license](https://github.com/supabase/supabase-js/blob/master/LICENSE)
- [Leaflet license](https://github.com/Leaflet/Leaflet/blob/main/LICENSE)
- [Leaflet guidance on attribution and tile-provider terms](https://github.com/Leaflet/Leaflet/blob/main/FAQ.md)
- [Esri World Imagery service](https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer)

## Known Settings decisions

- Terms of Use and Privacy Policy open as read-only pages inside Kite.
- Software Licences opens one read-only page with licence notices.
- App Version is an inline value, “V1”.
- Account settings include email/password management, linked sign-in providers, Log Out and Delete Account with confirmation.
- Adult V1 Settings includes yards/metres and Celsius/Fahrenheit; no notifications, language, or handedness controls.
- V1 is English-only.

## Inputs still required before release-ready legal copy

### Service operator and contact
- **Confirmed by the product owner:** Kite is currently provided by the owner personally as an individual service provider operating in the UK.
- Planned public-facing name: **All Green Golf Company** (an eventual company name; incorporation/legal-entity status is not confirmed).
- Postal service address supplied for the published contact details: **22 Landcross Drive, Northampton, NN3 3LS**. Do not label it a registered office unless company formation and registration confirm that status.
- **Confirmed by the product owner:** use `support@kitegolf.com` as the shared public support and privacy-request contact.
- Complaint/escalation route and operational response process still need to be defined.
- Governing-law and court/jurisdiction approach for Terms, while preserving mandatory consumer rights.
- User-facing privacy/data-protection contact and support contact; complaint/escalation route.
- Governing-law and court/jurisdiction approach for Terms, while preserving mandatory consumer rights.

### Product scope and commercial terms
- **Confirmed by the product owner:** Kite V1 launches in the UK only.
- **Confirmed by the product owner:** junior profiles are for all users under 18, including under-13s.
- The account eligibility and parent-consent/authority flow still needs to match this age range and be verified against implementation.
- Whether V1 is free, paid, trialled, or offers Kite Family subscription; price, billing provider, renewal/cancellation/refund mechanics.
- Precisely which features are advisory (GPS distances, caddie recommendations, handicap/statistics) and any availability or accuracy limits.

### Data practices to verify against the release build and service configuration
- Final list of data collected, purpose and lawful basis for each purpose; distinguish required from optional.
- Location collection boundaries, foreground/background operation, retention and use in analytics or recommendations.
- Production processor/subprocessor and hosting-region list, international transfers, and any map/weather/handicap/account-provider recipients.
- Analytics, crash reporting, diagnostics, advertising and tracking SDKs, including whether any are present in V1.
- Actual round/shot/profile retention, export, account deletion, backup expiry and anonymisation behaviour.
- Junior age bands and parent authority/verification model; how children receive age-appropriate privacy information and use data rights.
- Whether junior dashboard/profile data are visible only to the junior and authorized family adults, and the effective access controls.
- Data breach contact and operational rights-request path.

### Release dependency inventory
- Pin exact package/CDN versions and distinguish bundled libraries from prototype-only libraries.
- Produce an Android release dependency/license report and web asset inventory.
- Confirm external map/tile/data licenses and required attribution for assets shipped in V1.
- Store complete third-party license texts/notices in the app bundle; verify the read-only Software Licences view contains the same notices.

## Implementation note

The repository contains useful product decisions and a Git-backed Core schema, but it does not yet establish the final release data flows, complete production processor list, final retention policy, or operator/legal contact details. The Terms, Privacy Policy and notices should be authored as versioned product content, then rendered in the Settings destinations already agreed in `docs/project/KITE-UI-QA-MEMORY.md`. Update the sources and policy version/date together when any relevant implementation changes.

For the UK junior experience, privacy information must be clear and accessible to both children and parents. The ICO explains that services likely to be accessed by children may fall within the Children’s Code and that children should receive age-appropriate transparency: [ICO — services covered by the Children’s Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/services-covered-by-this-code/), [ICO — children’s data rights and privacy information](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-data-protection-rights-do-children-have/).
