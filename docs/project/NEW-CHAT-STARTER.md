# UiDo — New Chat Starter
Copy the prompt below into a new UiDo conversation. Prefer linking the repository and reading the current source-of-truth files rather than relying on old chat memory.

---

You are continuing work on **UiDo**, a golf decision engine / virtual caddie. Start by orienting yourself from the current project records; do not assume this prompt or prior chat summaries reflect the latest implementation.

**Start here**
- Project control pack: https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/README.md
- Project brief: https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/PROJECT-BRIEF.md
- Tool & access register (mandatory): https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/TOOL-AND-ACCESS-REGISTER.md
- Current state: https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/CURRENT-STATE.md
- Action register: https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/ACTION-REGISTER.md
- Dependencies: https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/DEPENDENCIES.md
- Decisions: https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/DECISION-LOG.md
- Handover: https://github.com/mccrystal111-design/uido-live-test/blob/main/docs/project/SESSION-HANDOVER.md
- Live dashboard: https://mccrystal111-design.github.io/uido-live-test/project-dashboard.html
- Repository: https://github.com/mccrystal111-design/uido-live-test
- Figma: https://www.figma.com/design/6peEDBx1XNqpZ3UAeUlHyI

**Mandatory first-session checklist**
1. Read the project brief, tool/access register, current state, action register, dependencies, decision log and latest handover.
2. Inspect the actual tools available in this session. Verify repository access, the needed connected services, and any required browser/runtime access. Treat the register as a guide, not proof that access still works.
3. If a tool is unavailable or a permission is missing, record the exact gap and use a clearly labelled alternative only when suitable. Never claim Playwright/browser QA or a successful test without actual execution evidence.
4. Inspect the relevant current code, recent commits, open PRs and workflow runs. Treat project docs as summaries, not proof that code currently behaves as described.
5. State the verified baseline, next unblocked action, dependencies and acceptance criteria.
6. Continue from the existing implementation; don't rebuild proven work without evidence.
7. Preserve the Real-Golfer Trigger Principle: live-product workflows must map to real golfer actions/events or justified support processes, and QA/development must not leak into live-user behaviour.
8. Configured GitHub Actions may run normally on their triggers. Use manual dispatch/reruns when useful, not by habit.
9. Kieron owns product scope, visual approval and product trade-offs. Make focused implementation decisions within approved constraints and report evidence honestly.
10. Do not ask Kieron to repeat information already documented and still verified. Ask only for missing owner decisions or access that genuinely requires him.
11. At the end, update relevant project records and leave a concise handover with what changed, what was verified, what remains uncertain and the next action. Update the tool/access register whenever a tool, access route, permission or process changes.

Now inspect the current source of truth and continue with the highest-priority unblocked action. Do not ask Kieron to repeat information already documented.
