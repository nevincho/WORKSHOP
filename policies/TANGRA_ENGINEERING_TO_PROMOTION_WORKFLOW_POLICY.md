# TANGRA ENGINEERING → INTEGRATION → PROMOTION WORKFLOW POLICY

STATUS: MANDATORY FOR TANGRA CONTROL ROOM / AI WORKSHOP CAMPAIGNS

## Purpose

Separate engineering development from runtime integration and production promotion.

Default principle:

**AI WORKSHOP completes and reviews the engineering solution first. Codex later integrates reviewed units one at a time into an authorized development copy. Promotion occurs only after shadow, combined, real-copy runtime, and regression gates pass and the human explicitly authorizes promotion.**

## Roles

### Control Room
- Owns campaign sequence and acceptance gates.
- Defines one bounded WORKSHOP task at a time.
- Accepts, requests bounded correction, or blocks returned work.
- Does not implement and does not expose WORKSHOP internal routing.

### AI WORKSHOP
- Performs the engineering work.
- Produces implementation-ready software/packages/artifacts, tests, simulations/fixtures where applicable, and evidence.
- Resolves engineering issues before integration.
- Returns completed engineering units, not merely recommendations.

### Reviewer
- Independently validates completed WORKSHOP units using applicable static, contract, simulation, test, and regression evidence.
- Returns PASS / FAIL / BLOCKED with evidence.
- FAIL returns the affected unit for bounded correction.
- Reviewer PASS does not authorize runtime integration or promotion.

### Codex
- Is the bounded integration executor after the engineering campaign is ready for integration.
- Receives one reviewed integration unit at a time.
- Integrates only into the explicitly authorized TANGRA or Dashboard development copy.
- Executes only authorized bounded validation.
- Does not redesign accepted WORKSHOP engineering, broaden scope, or promote independently.

## Mandatory lifecycle

### Phase A — Engineering campaign

`Control Room -> WORKSHOP unit -> engineering artifact/software/tests/evidence -> independent Reviewer -> PASS -> next WORKSHOP unit`

Continue until all engineering units required by the campaign are complete and independently reviewed.

Default rule: **complete the software/engineering campaign before Codex integration begins.**

An early unit PASS is not an automatic Codex handoff. Early integration requires explicit human authorization.

### Phase B — Integration gate

Before Codex integration starts, establish:

- `ENGINEERING_COMPLETE = YES`
- `REVIEW_COMPLETE = YES`
- `REQUIRED_UNITS = COMPLETE`
- `KNOWN_BLOCKERS = NONE`

The campaign must also define:
- reviewed implementation-ready artifacts;
- integration order;
- protected components;
- expected interfaces;
- bounded tests per unit;
- combined regression requirements;
- rollback boundary.

Only then set `INTEGRATION_GATE = OPEN`.

### Phase C — Codex integration

For each reviewed unit:

`reviewed WORKSHOP artifact -> Codex integrates into authorized development COPY -> compile/import/static checks -> bounded integration test -> SHADOW validation where applicable -> PASS -> STOP`

Only after PASS may Control Room authorize the next integration unit.

Codex must not perform unrelated cleanup, redesign, broad discovery, protected-production modification, or autonomous promotion.

### Phase D — Combined shadow gate

After all individual units are integrated:

`ALL INTEGRATED UNITS -> COMBINED SHADOW TEST`

Validate applicable:
- interfaces and data flow;
- protected authority chain;
- regression behavior;
- failure isolation;
- performance/resource impact;
- side effects;
- campaign acceptance criteria.

Combined-shadow FAIL blocks promotion and returns only the affected unit(s) for bounded correction unless evidence invalidates the wider architecture.

### Phase E — Real development-copy runtime gate

After combined shadow PASS, run the complete integrated system on the authorized TANGRA/Dashboard copy under real runtime conditions.

Validate against the campaign acceptance criteria and protected baseline.

Required result:

`REAL_COPY_RUNTIME = PASS`

Simulation PASS and shadow PASS do not substitute for this gate.

### Phase F — Promotion gate

Promotion is eligible only when:

- `WORKSHOP_ENGINEERING = COMPLETE`
- `REVIEW = PASS`
- `INDIVIDUAL_INTEGRATION = PASS`
- `INDIVIDUAL_SHADOW = PASS` where applicable
- `COMBINED_SHADOW = PASS`
- `REAL_COPY_RUNTIME = PASS`
- `REGRESSION = PASS`
- `BLOCKERS = NONE`

Even then, promotion requires explicit human authorization.

**A test PASS never implies promotion authority.**

## Production protection

Default path:

`AI WORKSHOP -> REVIEW -> DEVELOPMENT COPY -> INDIVIDUAL SHADOW -> COMBINED SHADOW -> REAL COPY RUNTIME -> REGRESSION -> HUMAN PROMOTION DECISION -> PRODUCTION`

Forbidden shortcuts:

`IDEA -> CODEX -> PRODUCTION`

`WORKSHOP PASS -> PRODUCTION`

`SIMULATION PASS -> PRODUCTION`

## Failure loop

At any failed gate:

`FAIL -> identify smallest failed unit -> bounded correction -> repeat required validation -> continue only after PASS`

Do not restart or redesign the whole campaign unless evidence shows the failure invalidates the wider architecture.

## Relationship to Control Room task policy

The Control Room still issues one bounded WORKSHOP task at a time and remains operational/TASK-ONLY in user-facing communication.

This policy defines the **campaign lifecycle across engineering, integration, validation and promotion**. It does not require Control Room to narrate WORKSHOP internal Worker/Reviewer mechanics.

## Core rules

**WORKSHOP develops the solution.**

**Reviewer independently validates the prepared engineering unit before runtime integration.**

**Codex integrates reviewed units into a protected development copy one at a time.**

**Shadow proves integration without granting authority.**

**Combined shadow proves integrated units work together.**

**Real-copy runtime proves the complete candidate under actual execution.**

**Only the human authorizes promotion.**
