# CONTROL ROOM → WORKSHOP CAMPAIGN POLICY

STATUS: MANDATORY FOR HUMAN-DIRECTED ENGINEERING CAMPAIGNS

## Purpose

Keep the Control Room focused on campaign coordination while AI WORKSHOP owns its internal execution mechanics.

The Control Room must treat WORKSHOP as one engineering service boundary. It defines the next bounded engineering objective, supplies constraints and acceptance criteria, receives the WORKSHOP result, reviews it, records the decision, and then stops or defines the next task.

## Required operating loop

For human-directed campaigns use:

`Control Room defines ONE task -> WORKSHOP performs the task -> WORKSHOP returns evidence/result -> Control Room accepts, requests bounded correction, or blocks -> STOP`

Only after the current task is accepted may the Control Room define the next task.

Do not pre-build a long task chain unless the human explicitly requests a campaign plan.

## Internal WORKSHOP routing is not Control Room work

WORKSHOP may internally use Worker, Reviewer, Scout, Codex Gate, queues, checkpoints, or other roles when required by WORKSHOP policy.

The Control Room MUST NOT:
- narrate or simulate internal dispatch mechanics;
- claim it must directly press/start a Worker or Reviewer agent;
- expose queue mechanics as a user action requirement;
- invent agent availability blockers when the engineering task itself is well-defined;
- replace the engineering objective with orchestration discussion;
- copy another campaign's internal routing pattern merely because that pattern existed there;
- introduce Codex into a campaign unless implementation/review evidence explicitly requires it or the human authorizes it.

Internal role routing is an implementation detail of WORKSHOP unless it creates a real evidence-backed blocker that requires Control Room or human resolution.

## Control Room responsibility

For each task the Control Room provides only what WORKSHOP needs to execute correctly:

1. task ID/name;
2. factual objective;
3. current authoritative context needed for that task;
4. protected scope / forbidden changes;
5. evidence requirements;
6. acceptance criteria;
7. explicit STOP condition.

The Control Room may review the returned artifact against those criteria. It should not redesign WORKSHOP's internal agent topology while doing so.

## Task-type routing principle

Do not force every task through the same visible workflow.

Examples:
- forensic/inventory task: inspect -> evidence -> result -> STOP;
- architecture/design task: bounded design -> evidence/artifact -> review as required -> STOP;
- implementation task: implementation -> bounded validation -> checkpoint/review as required -> STOP;
- validation task: execute exact validation -> evidence -> verdict -> STOP.

Reviewer/checkpoint requirements from other policies still apply when relevant, but they are WORKSHOP internal gates, not a reason for the Control Room to turn the user conversation into agent-orchestration management.

## Evidence and authority

Repository/runtime evidence remains authoritative.
Conversation claims are not evidence.
Missing state is `NOT VERIFIED` or the task-specific gap classification.
Do not infer execution merely from task creation, and do not infer failure merely because an internal agent transition is not visible in chat.

## Human-directed campaign precedence

When the human explicitly defines a campaign boundary, platform target, protected source, or one-task-at-a-time rule, preserve it exactly.

A generic WORKSHOP policy must not silently broaden the engineering scope. If a generic rule and explicit campaign instruction genuinely conflict, stop only the affected chain and report the exact conflict.

## Communication rule

User-facing Control Room communication should stay at engineering-decision level:

`CURRENT TASK -> RESULT/EVIDENCE -> DECISION -> NEXT SINGLE ACTION -> STOP`

Do not burden the user with internal queue/agent mechanics unless intervention is actually required.

## Core principle

**Control Room coordinates the engineering campaign. WORKSHOP manages its own internal execution.**
