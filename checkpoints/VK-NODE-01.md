# VK-NODE-01 Checkpoint

Date: 2026-09-16
Status: `COMPLETE / ARCHITECTURE_PASS / REVIEWER_PASS`

## Prerequisites verified on WORKSHOP main
- VK-DIST-03: COMPLETE / BEHAVIORAL_PASS / REVIEWER_PASS
- VK-DIST-04: COMPLETE / BEHAVIORAL_PASS / REVIEWER_PASS
- VK-WIRE-02: COMPLETE / BEHAVIORAL_PASS / REVIEWER_PASS
- VK-WIRE-05: COMPLETE / CPP_PASS / CROSS_LANGUAGE_CONFORMANCE_PASS / REVIEWER_PASS

No prerequisite was reopened or re-executed.

## Accepted artifacts
- Contract: `decisions/VK_NODE_IDENTITY_ENROLLMENT_TRUST_CLONE_RECOVERY_CONTRACT_2026-09-16.md`
- Threat/failure matrix: `evidence/VK-NODE-01/THREAT_FAILURE_MATRIX_2026-09-16.md`
- Backlog: `planning/VK_NODE_01_IMPLEMENTATION_CONFORMANCE_BACKLOG_2026-09-16.md`
- Independent review: `review/VK-NODE-01.md` — PASS

## Accepted model
`LogicalIdentity != NodeIdentity`; one LogicalIdentity may have many explicitly enrolled NodeIdentities. Owner-controlled LEA authorizes durable enrollment. Per-node cryptographic identity uses portable Ed25519 baseline. Lifecycle states are UNENROLLED, ACTIVE, SUSPENDED, RECOVERY_REQUIRED, CLONE_CONFLICT, REVOKED, RETIRED. Portable Seed is never NodeIdentity. SECRETS are never SHARED_REPLICATED. DIST-04 consumes four-way identity authorization and is not enrollment authority.

## Wire consequence
NodeEnrollmentRecord, NodeRevocationRecord, NodeMigrationRecord and NodeRecoveryRecord each require a separately gated bounded Wire extension. Wire Profile v1 and existing vectors remain unchanged.

## Protected scope
No LIVE runtime change. No DIST-04 change. No Wire/vector change. No NODE-02. No transport. No Windows-Pi communication. No Codex.

## Next gate
`VK-NODE-WIRE-01` — bounded lifecycle control-record Wire extension specification/conformance design. It is NOT started by this checkpoint.
