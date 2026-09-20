# PEX v0.1 — Project Execution Language

Status: INITIAL / EXPERIMENTAL  
Scope: universal execution shorthand for Codex/engineering agents across projects.

## Purpose

PEX compresses execution prompts while preserving task boundaries, validation, acceptance criteria and reporting semantics. Project-specific terms belong in project profiles, not PEX Core.

## Core syntax

```text
@PEX/0.1 PROJECT=<PROJECT> TASK=<TASK>
SRC>DST
+X
-X
DO=X|Y
RUN=X|Y
KEEP=X|Y
TEST=X|Y
PASS=X|Y
FAIL=>X|Y
OUT=X|Y
```

## Semantics

- `SRC>DST` — source to target.
- `+X` — require/add/enable X.
- `-X` — prohibit/remove/disable X.
- `DO=` — required actions.
- `RUN=` — execution/runtime constraints.
- `KEEP=` — preserve unchanged.
- `TEST=` — mandatory verification.
- `PASS=` — acceptance gate.
- `FAIL=>` — required failure action.
- `OUT=` — final output contract.
- `RUN+=` — append runtime constraints without replacing prior RUN terms.

## Reserved Core tokens

- `STRICT` — obey declared boundaries exactly.
- `SILENT` — no progress narration or running commentary.
- `FACTS` — report evidence/results only.
- `DISCOVER` — inspect actual state; do not assume.
- `CURRENT` — currently verified target/state.
- `ALL` — every declared requirement.
- `RB` — rollback task mutations.
- `STOP!` — stop on genuine blocker or boundary violation.
- `REGRESS` — regression validation.
- `PERSIST` — write → terminate → restart → restore validation.
- `ISOLATE` — prove isolation from protected paths/components.
- `NO_REGRESSION` — no demonstrated regression in protected behavior.

## Resolution rule

Unknown token MUST NOT be guessed.

Resolution order:
1. PEX Core.
2. Active project profile.
3. Repository-persistent project documentation.
4. `DISCOVER` from actual target state.
5. If still unresolved: `STOP!`.

## Profiles

PEX Core is project-neutral. Project profiles may define domain tokens such as:

- TANGRA: `AUTH0`, `SHADOW`, `HOROS`, `COG`, `PI`, `PROD`.
- VK: `NODE`, `IDENTITY`, `LIFECYCLE`.
- ESP32: `FLASH`, `SERIAL`, `SMOKE`.

Profile tokens MUST have one stable repository-persistent meaning.

## Example

```text
@PEX/0.1 PROJECT=TANGRA TASK=COG-PI-SHADOW
RUN=STRICT|SILENT|DISCOVER
STAGE>PI:CURRENT
+COG*|PERSIST|LFM
RUN+=SHADOW|AUTH0|PASSIVE
KEEP=PROD|PI_DELTA
-DESIGN|-PERSONALITY|-CTRL
TEST=CHAIN|PERSIST|LFM|ISOLATE|RES|REGRESS
PASS=ALL|NO_REGRESSION
FAIL=>RB|STOP!
OUT=FACTS
```

## Versioning rule

PEX v0.1 stays deliberately small. Add syntax/tokens only when repeated real project use demonstrates a need. Do not expand the Core with project-specific vocabulary.
