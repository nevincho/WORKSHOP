# Agent Recovery Automation — idea for review

STATUS: PROPOSED / NOT ACTIVE
DATE: 2026-08-24

Purpose: provide a secondary recovery path for stranded/incomplete WORKSHOP role pipelines without replacing the Fresh Controller.

Proposed behavior:
- run approximately every 3 hours during active work periods;
- read current WORKSHOP state only;
- detect stranded work such as REVIEW without reviewer output, READY work with no progress after a reasonable interval, or incomplete role outputs;
- execute/retry only the missing role phase in its own automation run rather than attempting to mutate other chat sessions;
- preserve existing dependency rules, Codex Gate policy, protected components and project boundaries;
- do not create duplicate tasks or duplicate controller work;
- write recovery evidence/ledger entries to WORKSHOP;
- remain separate from the primary Fresh Controller so failures can be diagnosed independently.

Important limitation: direct scheduled injection of prompts into four existing agent chat threads is NOT VERIFIED. Preferred design is a recovery automation that performs the missing role itself against repository state.

Decision: discuss in the next Control Room before activation. Do not schedule or activate from this note alone.
