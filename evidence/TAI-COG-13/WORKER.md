# TAI-COG-13 WORKER EVIDENCE

Engineering repository: `nevincho/TANGRA-2.0`
Branch: `tai-cog-13`
Base: `3b24753a21a6c42f70b160001c0e24376993a6be`
Engineering head: `d6dc0686f9238c2777c89425de7b088e30eb1c0e`

Files added only under `TANGRA_2_0/00_FOUNDATION/TAI_COG_13/`.

Implemented:
- `CognitiveProposal`, `CognitiveProposalBuilder`, `CognitiveProposalResult`;
- `ProposalStatus`, `ProposalType`, `ProposalEvidenceBinding`, `ProposalProvenance`;
- evidence-bound actionable proposals;
- deterministic SHA-256 proposal IDs and canonical JSON;
- validated ScenarioDescriptor / ValidatedConfigurationDescriptor catalog gating;
- voice-origin UNTRUSTED preservation;
- NOT_APPROVED / NOT_EXECUTED / authority NONE / operational_authority empty invariants.

Validation executed locally against compatibility contracts matching consumed COG-00 definitions:
- `py_compile`: PASS;
- `unittest`: 24/24 PASS;
- failures/errors: 0/0.

Negative tests cover missing evidence, confidence-without-evidence, unvalidated scenario/profile IDs, arbitrary scenario use, backend VERIFIED_CAUSE manufacture, HYPOTHESIS promotion, voice trust escalation, execution/activation surface absence, malformed authority, invalid proposal type.

Repository compare base→head: ahead 5, behind 0, exactly 5 added files under TAI_COG_13; COG-00..12 unchanged.

No Pi5, production runtime, model, diagnostic/replay/Twin execution, command/dispatch, mission/target/config mutation or COG-14 work performed.
