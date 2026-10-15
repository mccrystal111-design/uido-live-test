# Kite Privacy Policy — V1 Draft

**Draft status:** Product-specific working draft. Do not publish until all `[OPEN]` items are answered and every statement is verified against the production app, backend configuration and supplier contracts.  
**Version:** 0.1  
**Last updated:** 15 October 2026  
**Launch market:** United Kingdom

> This is Kite’s authored privacy-content draft, not approved legal copy. Bracketed text marks a release blocker. The repository records a Core schema and prototypes; a schema field is not by itself proof that the live V1 collects that data.

## 1. Who is responsible for your information

The service provider is the individual operator of Kite in the United Kingdom, using the planned public-facing name **All Green Golf Company**.

**[OPEN: insert the operator’s full legal name. The company name is planned, not confirmed as incorporated.]**

Postal contact:
22 Landcross Drive, Northampton, NN3 3LS, United Kingdom  
Email: **support@kitegolf.com**

We are responsible for deciding why and how Kite uses personal information, subject to the actual contracts and roles of our service providers.

## 2. Who this policy covers

Kite V1 launches in the United Kingdom and includes adult and family features. Junior profiles are for players under 18, including children under 13. The parent or guardian manages the family account and creates the junior sign-in. A junior can use their own sign-in for the laptop dashboard; the parent manages round setup and play on the parent’s phone.

This information is for both adults and children. We will provide it in a clear, age-appropriate way so a junior can understand what information is used and how to ask for help.

**[OPEN: confirm the parent/guardian authority or verification method, age presentation, and the steps that allow an under-13 to be added. Align this with the shipped design and applicable requirements.]**

## 3. Information Kite may use

Depending on the features you use, Kite may process:

- **Account and sign-in details:** name or display name, email address, username and authentication/account identifiers. Passwords are handled by the authentication provider rather than stored in the Kite app database. Junior sign-in also has a parent-managed password and a four-animal PIN.
- **Player profile and preferences:** home course, preferred tees, yards/metres and other selected preferences.
- **Golf profile:** handicap information, club inventory, carry/total distance references, equipment and changes over time.
- **Rounds and scorecards:** course and course version, tee, round type, dates/times, hole scores, putts and round results.
- **Location and shot information:** GPS location when the relevant feature is used, plus shot details such as club, lie, wind, trajectory, shot shape, outcome and player notes.
- **Device and technical information:** device/app context needed to provide and troubleshoot the service.
- **Messages to support:** information you choose to include when you contact us.
- **Purchase information:** subscription status and related transaction identifiers from the purchase provider, if you buy Kite Family. Payment card or account details are handled by that provider, subject to confirmation of the V1 provider.

These categories are based on the current Core schema, UI decisions and prototype code. We will narrow or expand them to match the features and fields actually shipped in Kite V1.

**[OPEN: confirm actual V1 collection for every listed field; whether whole-round GPS paths are stored; exact device/diagnostic data; support ticket system; payment metadata; and whether analytics, advertising, or crash-reporting data are collected.]**

## 4. Why we use information

Kite may use information to:

- create and secure accounts and family profiles;
- provide the golf profile, round, scorecard, GPS and statistics features you choose to use;
- calculate or display golf distances, records and recommendations;
- allow parents/guardians to manage junior profiles and allow juniors to view their agreed dashboard information;
- process and manage Kite Family access;
- respond to support requests;
- keep the service secure, troubleshoot faults and maintain reliable records; and
- meet legal obligations and handle disputes.

**[OPEN: map each purpose to its UK GDPR lawful basis, separate essential service processing from optional uses, and confirm whether product analytics, advertising or personalised recommendations use personal information.]**

## 5. Location

If you grant location permission and use location-dependent golf features, Kite can receive precise device location. The Android prototype requests fine/coarse location and foreground-location capability. The Core schema supports round-start and shot locations.

**[OPEN: state exactly when location is collected (including whether the app may continue collecting when backgrounded), what is uploaded, what remains on the device, how location supports the product, and the retention period. Verify the released Android behavior before publication.]**

You can manage device location permission in your device settings. Turning it off may prevent location-dependent features from working; confirm the manual course/yardage fallback behavior in the release.

## 6. Junior information and family access

A parent or guardian creates a junior profile and manages its sign-in. The parent can view and manage the junior’s golf profile and history. A junior can view their own dashboard, handicap, past rounds and scorecards; the junior dashboard is view-only for saved scorecards. Family management access may also be granted to an adult Kite account added as a co-parent/guardian.

Junior profiles do not require the junior to have an email address. The junior chooses their four-animal PIN; the parent manages password/PIN resets and can manage family profiles. Adult conversion and profile deletion/retention follow the family-management flow.

**[OPEN: verify family access controls and authorization on the production backend; identify what account details parents and juniors can see; explain how a child may contact us or exercise privacy rights; and reconcile deletion/transfer behavior with the final retention policy.]**

We will not describe a child’s data as private from a parent where the confirmed family feature gives that parent access.

## 7. Who receives information

The current implementation evidence includes Supabase Auth/database services and prototypes that load software or data services from third parties. Their presence in a prototype does not prove they will be used in V1.

**[OPEN: publish the actual processor/recipient list and purpose for each provider, including hosting, authentication, database, map/course data, payments, email/support, analytics/diagnostics and any integrations. Confirm processing locations and any transfers outside the UK; identify safeguards where required.]**

Potential future integrations such as Garmin, TrackMan, WHS/GHIN are not to be described as active recipients unless they are included in the launched service.

## 8. How long we keep information

The Core Q&A records an idea of keeping a retired customer’s data recoverable for about five years and then anonymising useful statistics. The Core baseline says the final legal/privacy retention policy is still open. This is not yet a firm retention promise.

**[OPEN: choose and implement retention periods by data category, including active and deleted accounts, junior profiles, precise location, round/shot history, support messages, payment records, security logs and backups. Explain deletion/anonymisation timing and legal exceptions.]**

## 9. Your choices and rights

Depending on the circumstances, people may have rights to access, correct, delete or restrict use of their personal information, object to certain processing, and receive a portable copy. Children also have data protection rights. A parent or guardian may exercise rights on a child’s behalf where applicable, while the child should still receive clear information and an accessible way to seek help.

Contact **support@kitegolf.com** or write to the postal address in section 1 to make a request. **[OPEN: define identity/authority checks, response workflow, expected response information and escalation route. Add the correct UK supervisory-authority complaint details.]**

Account deletion is available as an App Settings action with confirmation.

**[OPEN: explain what deletion actually does, how it affects family players and saved scorecards, any retained/anonymised data, backups, and provider-side subscription cancellation.]**

## 10. Security

We use access controls intended to restrict customer-owned records to authorized accounts. The Core baseline describes row-level security policies based on the signed-in identity.

**[OPEN: verify production policies, staff access, backups, encryption, incident response and service-provider safeguards before describing the controls in more detail.]**

## 11. Changes to this policy

We will update this page when our data practices materially change and show the applicable version/date. **[OPEN: define in-app notice and consent/choice handling where required.]**

## 12. Contact

Privacy or support: **support@kitegolf.com**

Postal contact:
All Green Golf Company  
22 Landcross Drive  
Northampton  
NN3 3LS  
United Kingdom

**[OPEN: replace planned-name presentation with the accurate service-provider name and legal status before launch.]**

## Drafting references

- [ICO — the right to be informed](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/)
- [ICO — children’s data rights and privacy information](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/children-and-the-uk-gdpr/what-data-protection-rights-do-children-have/)
- [ICO — services covered by the Children’s Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/services-covered-by-this-code/)
