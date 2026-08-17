# AI Assistant Working Agreement

The repository, not chat history, is the durable source of project state.

## For ChatGPT and Claude

- Read `AGENTS.md` and the named context documents before proposing architectural changes.
- Inspect current code/tests before stating that something is implemented.
- When proposing a material architectural change, update or add an ADR.
- Prefer small verifiable steps over large speculative rewrites.
- Run the narrowest relevant tests first, then the standard quality gate.
- Never make a test pass by deleting the property it was protecting without explicitly recording that decision.
- Leave the repository in a state another assistant can understand without the previous chat transcript.

## Handoff discipline

At the end of a substantial session, update `session-handoff.md` with:

- objective;
- changes made;
- tests/commands actually run and their result;
- decisions made;
- known defects or risks;
- exact next step.
