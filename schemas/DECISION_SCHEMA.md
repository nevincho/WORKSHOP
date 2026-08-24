# WORKSHOP Human Decision Schema

STATUS: MANDATORY FORMAT

Use for Control Room / Vlad decisions that change task authorization, architecture, protected scope, priority, execution route or blocker resolution.

Required fields:
- DECISION_ID
- TIMESTAMP
- PROJECT
- TASK_ID if applicable
- QUESTION_OR_GATE
- VERIFIED_CONTEXT
- OPTIONS_CONSIDERED
- DECISION
- AUTHORIZED_SCOPE
- PROHIBITED_SCOPE
- EFFECTIVE_FROM
- AFFECTED_DEPENDENCIES
- REQUIRED_FOLLOW_UP
- EVIDENCE_REFERENCES

A decision does not alter target-project implementation state by itself. Agents must still verify current target state before execution.