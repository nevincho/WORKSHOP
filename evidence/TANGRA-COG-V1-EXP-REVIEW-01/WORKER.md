# TANGRA-COG-V1-EXP-REVIEW-01 — Worker Evidence

DATE: 2026-09-26
STATE: IMPLEMENTED / QUALIFICATION_PASS / REVIEW_REQUIRED

TARGET_REPOSITORY: nevincho/TANGRA-2.0
BASE: tangra-cog-v1-exp-life-01@b6db74d02365ccf2aad5e1a6e755525233c51584
CANDIDATE: tangra-cog-v1-exp-review-01@249234f5265a9ae4595fbcfc8b91ef82efc353a8

ARCHITECTURE_CONTRACT:
WORKSHOP/decisions/TANGRA_COG_V1_RAW_CANDIDATE_REVIEW_CONTRACT_2026-09-26.md

## Final repository delta

Exactly two files differ from the qualified EXP-LIFE-01 base:
- TAI_COGNITIVE_INTEGRATION_PACKAGE/integration/cognitive_experience_candidate_review_contract.py
  - blob 691378fdbf35181e66da17acde5c710995c6c5ed
- TAI_COGNITIVE_INTEGRATION_PACKAGE/tests/integration/test_cognitive_experience_candidate_review_contract.py
  - blob 2066909692b735b146264efa1e28ac887014013a

Temporary qualification workflow was restored byte-for-byte:
- .github/workflows/cognitive-bridge-qualification.yml
- baseline blob 9d28f0fd44886b7901f061258b5f028deab4bd8b

Protected blobs unchanged:
- EXP-LIFE-01 adapter: b7573bce130aa9dd2827142d5c63d1190126d28e
- EXP-PERSIST-01 adapter: efcfbf1cefa028efe40735835f25f2c86b8cb812
- EXP-01 adapter: f8d4e425347c0aca842064dffa7eb2de4f9dd21f
- reviewed COG-22 store: 0707f718b07b5fa1730a02c07aeb197078b67154
- reviewed COG-30 lifecycle: 97e942f01288b5153f0795633b870f531588e590
- Cognitive Bridge: 5f4a6346fa70e369452067d9d96f776a84468a64

## Implementation

Added immutable additive contract:
- ReviewDecision: APPROVE / REJECT only.
- RawCandidateReview fields:
  review_ref, source_experience_id, reviewer_id, decision, evidence_refs, reason, authority, operational_authority.
- deterministic canonical JSON and SHA-256 canonical review hash.
- RawCandidateReviewStatus:
  AUTHORIZED, REJECTED, INVALID_REVIEW, SOURCE_NOT_FOUND, SOURCE_NOT_RAW, SOURCE_NOT_ACTIVE, EVIDENCE_NOT_BOUND, REVIEW_CONFLICT.
- RawCandidateReviewValidator requires the same reviewed COG-22 store used by the reviewed COG-30 policy.

Validation:
- source must exist;
- source lifecycle must be RAW_EVIDENCE;
- COG-30 disposition must be ACTIVE;
- all review evidence refs must already be bound to that exact ExperienceRecord;
- explicit REJECT returns REJECTED;
- explicit APPROVE returns AUTHORIZED;
- identical same-review_ref replay returns the exact previously recorded semantic result;
- same review_ref with different canonical payload returns REVIEW_CONFLICT;
- result authority is NONE and operational authority empty.

Containment:
- validator does not call ExperienceStore.append();
- does not call any lifecycle promotion/transition method;
- does not create CANDIDATE_LESSON;
- does not mutate COG-22 or COG-30;
- no persistence, model, command, configuration, mission or target surface.

Reviewer identity:
- contract requires explicit non-empty reviewer_id;
- reserved model/backend identities/prefixes are rejected;
- reviewer identity authentication infrastructure is intentionally outside the approved architecture scope and is NOT VERIFIED by this task.

## Executed qualification

GitHub Actions run: 36266776690
Executed head: d4a41e8913f94fa00c0cd48c73d15aeb52a82155

PASS:
- Cognitive Bridge: 17/17
- DIAG-01 adapter: 15/15
- CORR-01 integration: 12/12
- HYP-01 integration: 13/13
- INT-01 integration: 13/13
- EXP-01 integration: 13/13
- EXP-PERSIST-01 integration: 13/13
- EXP-LIFE-01 integration: 8/8
- EXP-REVIEW-01 integration: 12/12
- current reviewed COG-22 source tests: 36/36
- reviewed COG-30 lifecycle tests: 15/15

Bounded total: 167 PASS / 0 FAIL.

Final implementation/test blobs equal the blobs executed in the passing run. Later candidate commit only restored the qualification workflow.

## Qualified behavior

- explicit APPROVE can yield AUTHORIZED for one exact active RAW_EVIDENCE source with bound evidence;
- AUTHORIZED is only authorization eligibility and performs no transition;
- explicit REJECT yields REJECTED and no mutation;
- unbound evidence cannot authorize;
- missing/non-active source cannot authorize;
- same-review_ref identical replay is idempotent;
- conflicting same-review_ref payload is REVIEW_CONFLICT;
- contract contains no confidence/count/time/score/model authorization fields;
- COG-22 store and COG-30 policy remain unchanged by validation.

## Limitations / NOT VERIFIED

- reviewer identity authentication is NOT VERIFIED and was explicitly excluded from the architecture task;
- durable review-ledger persistence is NOT IMPLEMENTED;
- cross-review conflict resolution for different review_ref values is NOT IMPLEMENTED;
- RAW_EVIDENCE -> CANDIDATE_LESSON transition is NOT EXECUTED / NOT IMPLEMENTED;
- CANDIDATE_LESSON -> VALIDATED_EXPERIENCE remains out of scope;
- historical Cognitive Bridge cumulative 317-test regression remains NOT EXECUTED.

CODEX: NOT USED
PI_CHANGES: NONE
