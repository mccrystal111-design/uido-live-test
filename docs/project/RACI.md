# UiDo RACI

Roles:
- Kieron (Product Owner): sets product intent, approves design/behaviour, confirms outcomes.
- ChatGPT (Coordinator/Implementer): inspects source, implements agreed changes, maintains records, tests where possible and reports evidence/uncertainty.
- GitHub Actions/tooling: runs according to configured push, schedule, dispatch or other approved triggers; it does not make product decisions.

| Activity | ChatGPT | Kieron |
|---|---|---|
| Maintain action register/current state/handover | R | I |
| Inspect repo and dependencies | R | C |
| Implement agreed code/docs changes | R | I |
| Product scope and priority | C | A |
| Brand/design approval | C | A |
| Define geometry/product acceptance criteria | R | A |
| Configure and maintain workflow triggers | R | A/C |
| Monitor workflow results and diagnose defects | R | C |
| Inspect workflow results and diagnose defects | R | C |
| Approve design or release outcome | C | A |
| Confirm behaviour meets golfer needs | R | A |
| Approve production trigger semantics | R | A |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

ChatGPT may make reversible implementation choices within approved constraints and must record meaningful decisions. Kieron owns product trade-offs, visual approval, scope-changing priorities and production behaviour. Never imply approval without explicit evidence.
