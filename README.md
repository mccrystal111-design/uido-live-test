# UiDo — Live Test Repository

## Project control centre

**[Open the live project dashboard](https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html)** — read-only live summary of GitHub issues, pull requests and recent workflow runs.

Start at [docs/project/README.md](docs/project/README.md).

- [UiDo Project Brief](docs/project/PROJECT-BRIEF.md) — stable orientation for any new chat.
- [New Chat Starter](docs/project/NEW-CHAT-STARTER.md) — copy/paste prompt to get a fresh conversation up to speed.

- [Current state and next action](docs/project/CURRENT-STATE.md)
- [Master action register](docs/project/ACTION-REGISTER.md)
- [Dependencies](docs/project/DEPENDENCIES.md)
- [RACI](docs/project/RACI.md)
- [Decision log](docs/project/DECISION-LOG.md)
- [Change log](docs/project/CHANGELOG.md)
- [Session handover](docs/project/SESSION-HANDOVER.md)
- [Dashboard design in Figma](https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI)

## Operating rules
1. Read the control pack before project work.
2. Choose the next unblocked, highest-priority action.
3. Record acceptance criteria and evidence; intention is not completion.
4. Update current state, action register, decisions, changelog and handover after work.
5. Let configured GitHub Actions triggers run normally for code changes, tests and deployments. Use manual dispatch/reruns when useful; do not duplicate automatic runs unnecessarily.
6. Live-product triggers must represent real golfer activity, relevant real-world conditions, or justified supporting processes. Isolate development/QA activity from live golfer behaviour.

The dashboard reads public repository data in the browser. It does not require a token and does not trigger workflows.