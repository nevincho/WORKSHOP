# TAI-COG-14 WORKER EVIDENCE

Engineering repository: `nevincho/TANGRA-2.0`
Branch: `tai-cog-14`
Base: `d6dc0686f9238c2777c89425de7b088e30eb1c0e`
Engineering head: `36e92fefcd993fa5e4f556d82958dbeb02a2421a`

Implemented files: 5, all under `TANGRA_2_0/00_FOUNDATION/TAI_COG_14/`.

Implemented contracts: `ProposalAssuranceGate`, `ProposalAssuranceRequest`, `ProposalAssuranceResult`, `AssuranceStatus`, `AssuranceReason`, `AssuranceRule`, `AssuranceRuleSet`, `ProposalRiskClass`, `ProposalEligibility`, explicit provenance and deterministic serialization.

Deterministic default rule order: R01..R15 covering schema/type/evidence/bindings/causal safety/scenario-profile state/authority/approval/execution/provenance/voice trust/forbidden surface/proposal freshness/evidence freshness/blockers.

Risk mapping is fixed by COG-13 proposal type only. `ELIGIBLE_FOR_REVIEW` does not modify approval, execution, authority or operational authority.

Scenario/profile assurance is fail-closed: selection proposals require explicit `VALIDATED`; `NOT_VALIDATED` => INELIGIBLE; `UNKNOWN` => UNKNOWN. No implicit validated default.

Freshness is evaluated only when explicitly required. Missing required freshness metadata => UNKNOWN; stale proposal/evidence => INELIGIBLE.

Two defects were found during bounded local validation and corrected before review: default rule constructor field ordering; mutation snapshot using validating serialization. Final validation:
- `py_compile`: PASS
- `unittest`: 27/27 PASS
- failures: 0
- errors: 0

Validation used Phase-A compatibility modules matching consumed reviewed COG-00/13 contracts. No Pi5, production runtime, model, diagnostic/replay/Twin execution, activation, command or communications path was used.

Repository compare against base: ahead_by=5, behind_by=0, five added files only, COG-00..13 unchanged.
