# Canonical model fixtures

Overstone Park and Poult Wood are the first two test fixtures.

Do not treat either existing acquisition output as the final schema. The fixture exercise is intended to expose missing fields and bad assumptions before the production acquisition pipeline is changed.

Required fixture coverage:

- course identity
- external source IDs
- course version
- 18-hole and non-18-hole structures where applicable
- tees
- per-hole yardage/par/SI
- fairway and green geometry
- bunkers/water/OB where evidence exists
- source provenance
- attribute-level confidence
- at least one example of conflicting evidence

The fixture test passes only when the canonical model can represent the evidence without losing provenance.
