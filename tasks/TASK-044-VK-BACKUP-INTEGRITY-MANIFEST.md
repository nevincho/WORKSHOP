# TASK-044 — VK Backup / Integrity Manifest + Restore Simulation

TASK_ID: TASK-044
PROJECT: VK
STATUS: READY_FOR_WORKER
TYPE: REPOSITORY / SIMULATION PREPARATION
CODEX: HUMAN-GATED; DO NOT AUTO-INVOKE

## Objective
Prepare the smallest backup/integrity manifest and simulated restore-verification procedure consistent with VK durability and Canonical Minimal State principles, without touching the live Core.

## Basis
VK architecture requires backup/migration, reconstructability and portable durable state. Canonical foundation requires work -> validation -> canonical promotion -> cleanup and integrity/lineage preservation.

## Allowed work
Define manifest fields, hashes/version/source classification, mock backup set and restore-verification simulation using non-sensitive fixtures only. Reuse existing mechanisms where repository evidence supports them.

## Acceptance
- manifest distinguishes canonical/required/reproducible-temp/unknown or compatible existing classes;
- integrity verification and rollback/restore simulation are deterministic;
- no assumption that a successful manifest test proves live Core backup health;
- no secrets/raw private memory committed;
- evidence + independent review.

## Non-goals
No live `D:\Store\AI` backup, no Core mutation, no encryption-key handling, no production restore.