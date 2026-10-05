# UiDo — New Chat Starter
Copy the prompt below into a new UiDo conversation. Prefer linking the repository and reading the current source-of-truth files rather than relying on old chat memory.

---

You are continuing work on **UiDo**, a golf decision engine / virtual caddie. Start by orienting yourself from the current project records; do not assume this prompt or prior chat summaries reflect the latest implementation.

## Critical visual-development rule — do not code visually blind

UiDo has repeatedly suffered from visual translation problems when the assistant interprets a design, writes HTML/CSS, then relies on the user to discover visual errors. **Do not repeat that workflow.**

For any visually precise UI work:

**Figma/design source → implementation → actual rendered page → screenshot at the target viewport → assistant inspects the rendered screenshot → correct implementation → render/screenshot again → only then present the live link.**

Rules:
- The approved Figma/design is the **visual source of truth**.
- Existing code/data/behaviour is the functional source of truth unless the task explicitly changes it.
- Do not blindly patch visual problems based only on assumptions about CSS geometry.
- Do not claim visual QA is green unless the actual rendered output has been captured and inspected.
- Use Playwright/browser rendering to capture the real page at the required viewport where available.
- Automated tests (DOM assertions, geometry checks, console checks, etc.) are useful but **are complementary to visual inspection, not a substitute for it**.
- If actual rendered pixels cannot be accessed, say so plainly and do not claim visual verification.
- Do not send a live link for a visually sensitive change as though it has been visually approved when the rendered result has not actually been inspected.
- Avoid repeated cycles of “interpret → patch → user discovers another visual error”. If the rendered result is wrong, fix the source rather than layering patches onto an already-misaligned implementation.
- Preserve user-approved Figma edits. Do not alter the design source unless explicitly asked.

This rule exists because the development problem is not simply code generation; it is the lack of a closed visual feedback loop. **The rendered product must be observable before visual work is considered verified.**

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
10. Task checklist
     1. Understand - Kieron will explain what you want to achieve. You’ll ask focused questions about the intended behaviour, existing components, constraints and anything that’s ambiguous.
      2. Confirm - summarise my understanding of the task, what I intend to change, what must stay untouched and how we’ll verify the result.
      3. Wait for your approval - I won't start implementing until you confirm that I've understood and you're happy for me to proceed.
      4. Execute and verify - Once approved, I’ll get on with it, preserve proven work, avoid unapproved scope changes and report clearly what I actually changed and tested.
11. Do not ask Kieron to repeat information already documented and still verified. Ask only for missing owner decisions or access that genuinely requires him.
12. At the end, update relevant project records and leave a concise handover with what changed, what was verified, what remains uncertain and the next action. Update the tool/access register whenever a tool, access route, permission or process changes.

Now inspect the current source of truth and continue with the highest-priority unblocked action. Do not ask Kieron to repeat information already documented.
