# TANGRA — Error Tactics / Shadow Twin Research Seed

**Status:** IDEA CAPTURE / RESEARCH SEED  
**Date:** 2026-09-19  
**Project:** TANGRA  
**Authority:** research/planning only — no runtime, command, flight-control, readiness, IFF, LoRa, or actuator authority  
**Runtime state:** respect current WORKSHOP `TANGRA: OFFLINE_HOLD`

## Purpose

Preserve a future TANGRA research line before implementation work begins.

The research has two connected objectives:

1. Build a **TANGRA Failure Knowledge Model** from post-freeze heavy/endurance/fault-injection runs.
2. Study the strategic concept presented in Gordon R. Dickson's *Tactics of Mistake* / Bulgarian edition *Тактика на грешките*, then derive an original, explicitly TANGRA-specific mathematical formalization suitable for bounded defensive Shadow Twin scenario analysis.

The source book was supplied by the project owner for research. **The book itself is not stored in WORKSHOP.** Any later research artifact must distinguish source-derived concepts from TANGRA interpretation or mathematical invention and must not reproduce substantial copyrighted text.

## A. Failure Knowledge Model

After package reorganization and a temporary feature/module freeze, execute controlled heavy system runs to discover and classify real failure modes.

Each validated failure class should receive a stable machine-searchable code, for example:

- `TNG-CAM-###` — camera/acquisition
- `TNG-VIS-###` — vision/inference
- `TNG-TRK-###` — tracking/identity
- `TNG-RNG-###` — range/geometry
- `TNG-HOR-###` — HOROS/spatial
- `TNG-TEL-###` — telemetry/API
- `TNG-HW-###` — hardware/communications
- `TNG-COG-###` — Cognitive Layer/backend
- `TNG-CFG-###` — configuration/runtime contradiction

Candidate record structure:

`code → symptom → evidence → cause status → affected subsystem → severity → safe response → diagnostic procedure → proven recovery → regression test → occurrence history`

Epistemic state must remain explicit: `VERIFIED / PROBABLE / NOT_VERIFIED`.

Goal: future diagnostics can map an observed signature to a known failure class and retrieve an evidenced recovery path instead of restarting investigation from zero.

## B. Error Tactics research

Do **not** assume the novel contains a ready mathematical equation.

Research sequence:

1. Extract the passages/scenes in which the concept is explained, demonstrated, or strategically applied.
2. Separate:
   - what Dickson/Cletus actually states or demonstrates;
   - the inferred logical principle;
   - TANGRA's own mathematical formalization;
   - proposed Shadow Twin use.
3. Identify recurring variables such as:
   - system/opponent state;
   - observation and uncertainty;
   - action/reaction;
   - local error or deviation;
   - accumulation/path dependence;
   - consequence/cost;
   - available future actions;
   - confidence in the internal model.
4. Derive candidate formal models only after source analysis.

A provisional research form, **not attributed to Dickson**, is:

```
S_(t+1) = F(S_t, A_t, O_t, E_t)
```

where a small error `E_t` changes the state from which subsequent observations, reactions, and errors arise. The research question is therefore not simple arithmetic error accumulation, but **path-dependent cascading error and reaction**.

## C. Shadow Twin connection

The Cognitive Layer's future Shadow Twin/scenario capability is the intended experimental consumer.

Candidate defensive question:

> Given the current evidence and uncertainty, which apparently reasonable response becomes unsafe if one or more of our assumptions are wrong?

The Shadow Twin may compare bounded hypothetical trajectories:

```
S_t --A1--> S_(t+1)^1
S_t --A2--> S_(t+1)^2
S_t --A3--> S_(t+1)^3
```

and examine how observation error, model error, delayed reaction, or incorrect assumptions alter later states.

This remains **analysis/proposal only**. It must not create operational authority.

## D. Relationship between the two research lines

The intended long-term loop is:

```
real heavy-run failures
    -> coded Failure Knowledge Base
    -> Cognitive Layer evidence
    -> Shadow Twin scenarios
    -> cascading-error / assumption-failure analysis
    -> defensive proposal
    -> human/authorized deterministic gate
```

Real TANGRA failures provide empirical cases; the Error Tactics research provides a possible reasoning framework for studying how small errors and reasonable reactions can compound across a trajectory.


## E. Conditional ETM mode and controlled strategic deviation

ETM is **not** intended as a normal or continuously active TANGRA strategy. Under nominal conditions, when the current deterministic/authorized strategy is working, there is no reason to invoke it.

Candidate conceptual state progression:

```
NORMAL -> ADAPTIVE -> ETM
```

ETM becomes a research candidate only after bounded trigger conditions indicate that normal behavior is becoming ineffective, repetitive, or exploitable. Example evidence may include repeated escape/reaction patterns, repeated strategic failure, or sufficient observed behavioral regularity. Activation criteria are **not yet defined** and require later formalization and simulation.

A central distinction is:

```
E_accidental != E_controlled
```

- `E_accidental`: an actual unplanned failure/deviation.
- `E_controlled`: a deliberately selected, bounded local deviation from the otherwise locally optimal response, considered only after scenario evaluation predicts a better later trajectory.

The research hypothesis is that an action may be locally worse while still producing a better bounded trajectory. This must be evaluated over the trajectory, not by immediate outcome alone.

An accidental failure should also be treated as potential behavioral evidence rather than wasted information. If another actor repeatedly obtains success using the same observable response, TANGRA may update the probability that the response will recur. The model must remain behavioral and evidence-based; it must **not** assert unobserved mental states such as confidence, intent, or psychology as facts.

Candidate loop:

```
operational failure
    -> observed external response
    -> behavioral evidence/history update
    -> recurrence hypothesis with explicit confidence
    -> Shadow Twin trajectory comparison
    -> reduced probability of repeating the same strategic error
```

A future ETM simulation may consider a controlled deviation only when all later-defined safety and evidence gates are satisfied. Every such scenario must include both the expected-response branch and an unexpected-response recovery branch:

```
E_controlled
    -> expected response   -> planned continuation
    -> other response      -> abort / recovery trajectory
```

This produces a stricter research question:

> Under what evidence, uncertainty, safety bounds, and recovery conditions can a locally suboptimal controlled deviation improve the expected future trajectory without creating unacceptable downside if the predicted response does not occur?

The intended interpretation is therefore **conditional contingency reasoning**, not routine deliberate error. Any future implementation remains Shadow Twin analysis/proposal only and does not itself authorize operational execution.

## Research gates

This seed does not authorize implementation.

Suggested future bounded campaign:

1. **ETM-01 — Source Extraction:** evidence-backed concept map from the supplied novel.
2. **ETM-02 — Formalization:** original mathematical/state-transition model with assumptions and limits.
3. **ETM-03 — TANGRA Mapping:** map variables to existing Cognitive Layer / Digital Twin / Shadow contracts without changing authority.
4. **ETM-04 — Simulation:** synthetic defensive scenarios only.
5. **FKM-01 — Failure Taxonomy:** define stable failure-code namespace and record schema.
6. **FKM-02 — Heavy-Run Plan:** define post-freeze endurance/fault-injection campaign.
7. **FKM-03 — Knowledge Integration:** only after real failure evidence exists.

Each gate remains independently reviewable. No promotion to runtime follows from this planning artifact.

## Protected boundaries

- Preserve current TANGRA deterministic/runtime authority.
- Cognitive authority remains `NONE` unless separately authorized by a future campaign.
- Shadow Twin output is hypothetical analysis, not command authority.
- Do not modify protected production while TANGRA is `OFFLINE_HOLD`.
- Do not treat fictional strategy as validated engineering evidence.
- Do not attribute TANGRA-derived mathematics to Gordon R. Dickson.
- Keep source evidence, inference, and original TANGRA formalization explicitly separated.

## Current decision

**CAPTURE NOW; IMPLEMENT LATER.**

Priority remains current package reorganization / system stabilization. This research seed exists so the idea is repository-persistent and can be resumed after the planned software freeze without relying on conversation memory.
