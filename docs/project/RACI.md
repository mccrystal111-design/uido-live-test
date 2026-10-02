# UiDo RACI

Roles:
- Kieron (Product Owner): sets product intent, approves design/behaviour, manually triggers workflows, confirms outcomes.
- ChatGPT (Coordinator/Implementer): inspects source, implements agreed changes, maintains records, tests where possible and reports evidence/uncertainty.
- GitHub Actions/tooling: executes only when explicitly triggered by Kieron or an independently approved production design; it does not make decisions.

| Activity | ChatGPT | Kieron |
|---|---|---|
| Maintain action register/current state/handover | R | I |
| Inspect repo and dependencies | R | C |
| Implement agreed code/docs changes | R | I |
| Product scope and priority | C | A |
| Brand/design approval | C | A |
| Define geometry/product acceptance criteria | R | A |
| Manually trigger GitHub Actions | I | R/A |
| Inspect workflow results and diagnose defects | R | C |
| Approve design or release outcome | C | A |
| Confirm behaviour meets golfer needs | R | A |
| Approve production trigger semantics | R | A |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

ChatGPT may make reversible implementation choices within approved constraints and must record meaningful decisions. Kieron owns product trade-offs, visual approval, scope-changing priorities and production behaviour. Never imply approval without explicit evidence.
