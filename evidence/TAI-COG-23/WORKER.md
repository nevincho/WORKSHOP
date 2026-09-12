# TAI-COG-23 — WORKER EVIDENCE

Engineering repository: `nevincho/TANGRA-2.0`
Branch: `tai-cog-23`
Base: `5bdc25db69dbe0dc948a8ebe5a6b938247457c16`
Candidate head: `ca99a7d085d65acdee9cf99c27cb476cfa8b90cf`

Files added only under `TANGRA_2_0/00_FOUNDATION/TAI_COG_23/`:
- README.md
- fixtures/twin_policy.json
- tangra_digital_twin/__init__.py
- tangra_digital_twin/twin.py
- tests/test_twin.py

Implemented contracts:
DigitalTwinExperimentEngine, TwinExperimentRequest, TwinExperimentResult, TwinExperimentStatus, TwinMode, TwinFidelity, TwinOrigin, TwinScenario, TwinBaseline, TwinCandidate, TwinObservation, TwinProvenance, SyntheticCondition.

Policy evidence:
- REPLAY executable.
- SYNTHETIC executable.
- SHADOW -> NOT_EXECUTABLE_PHASE_A.
- Fidelity enum has exact L0..L4 vocabulary; L4 rejected in Phase A so implementation cannot overclaim validated physics.
- Every result/observation has explicit origin.
- Replay observations preserve historical evidence refs and are marked REPLAY.
- Synthetic observations are always SYNTHETIC and carry NOT_SENSED_NOT_REPLAYED limitation.
- Eight required synthetic condition classes supported.
- Baseline/candidate require identical evidence refs from supplied EvidencePacket.
- Candidate requires ValidatedConfigurationDescriptor with ValidationState.VALIDATED.
- COG-04 DeterministicEvaluator.compare is reused; no second evaluator.
- Four COG-04 ExperimentVerdict values preserved.
- Missing values/evidence -> INCONCLUSIVE.
- IMPROVED result adds explicit NOT_PRODUCTION_READINESS / NOT_PROMOTION limitations.
- MISSION_CONSTRAINED -> UNSUPPORTED_MODE.
- authority NONE / operational_authority [].
- no runtime mutation, command, SHADOW worker, subscription, callback, transport, ExperienceStore mutation, promotion, model/LLM.

Validation:
- py_compile PASS
- unittest: 41/41 PASS, failures 0, errors 0
- static surface review PASS
- forbidden import review PASS
- compare base..head: ahead_by=5, behind_by=0; changes confined to COG-23 package.

No COG-24 work performed.
