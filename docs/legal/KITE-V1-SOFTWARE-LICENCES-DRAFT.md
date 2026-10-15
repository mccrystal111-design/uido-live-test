# Kite V1 Software Licences — About Page Draft

**Draft status:** Licence-source inventory for the single read-only Software Licences page. Release notices are not complete until generated from the exact web and Android release contents.  
**Version:** 0.1  
**Last updated:** 15 October 2026

> Include only components actually distributed with or used to deliver Kite V1. The current repository contains prototypes, so a repository-wide search is not a substitute for a release dependency report.

## Confirmed font notice

### Space Grotesk

Space Grotesk is licensed under the SIL Open Font License, Version 1.1.  
Source: [Florian Karsten’s Space Grotesk project](https://github.com/floriankarsten/space-grotesk).

The repository includes `assets/fonts/space-grotesk-license.txt`, which identifies this license and source project. Before release, confirm the exact font files bundled by Kite and include the applicable complete OFL text and any required Reserved Font Name terms.

## Candidate software notices — confirm against the V1 release build

### Supabase JavaScript client

The prototype `hawk.html` references `@supabase/supabase-js@2` from jsDelivr. Upstream identifies the client as MIT-licensed: [license text](https://github.com/supabase/supabase-js/blob/master/LICENSE).

**Release action:** pin the exact shipped version and include its full copyright and MIT license notice only if that package is in V1.

### Leaflet

The prototype `home-preview.html` references Leaflet 1.9.4 from unpkg. Leaflet is licensed under the BSD 2-Clause License: [license text](https://github.com/Leaflet/Leaflet/blob/main/LICENSE).

**Release action:** confirm whether Leaflet ships in V1; if it does, include the complete BSD 2-Clause copyright, conditions and disclaimer.

### Oxanium font via Google Fonts

The prototype `index.html` imports Oxanium from Google Fonts.

**Release action:** confirm whether it ships in V1, pin the font/source/version and include the exact font license notice. Do not infer the license from the import URL alone.

## External map/data service — not a software license

The prototype `home-preview.html` requests ArcGIS World Imagery tiles from Esri. This is a map/data service rather than an open-source software license.

**Release action:** confirm whether the service is part of V1 and provide the required Esri/source attribution and comply with the applicable service terms. Keep these acknowledgements distinguishable from software license notices.

## Android and web release inventory

- The current Android Gradle module declares no third-party runtime dependencies, but this does not establish the final packaged WebView assets or a complete release software bill of materials.
- The repository does not currently identify a pinned, complete V1 dependency inventory.
- Prototype-only scripts, assets, fonts, map tiles and development tools must not be presented as shipped V1 dependencies without release-build evidence.

## Pre-release checklist

1. Build the exact V1 web and Android release artifacts.
2. Extract the transitive Android dependency/license report and enumerate all bundled or remotely loaded web packages, fonts, icons, map and data services.
3. Record package name, exact version, source URL, license identifier, required copyright notice and full license text.
4. Check required attribution for non-software assets/services separately.
5. Assemble the notices into this single read-only in-app page and keep a copy in the release bundle.
6. Verify displayed notices match the release artifacts and are reachable from Settings → Software Licences.
