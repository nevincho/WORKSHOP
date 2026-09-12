# TANGRA — WORKSHOP Project Profile

PRIORITY: 1 — HIGHEST WHEN ACTIVE
CANONICAL REPOSITORY: `nevincho/TANGRA-DOCS`
PROJECT_STATE: LIMITED_REACTIVATION
ACTIVE_CAMPAIGNS:
- WIDE-EW
- TAI
REACTIVATED: 2026-09-12
REACTIVATION_AUTHORITY: Vlad explicit Control Room authorization

## Campaign isolation

WIDE-EW and TAI are independent bounded campaigns. Activating TAI does not invalidate, rewrite, supersede or silently alter WIDE-EW state, evidence, decisions or history.

## WIDE-EW campaign

SCOPE: WIDE V3 Early-Warning / WIDE-EW campaign.

WORKSHOP may create, queue, execute, test, review, checkpoint and persist repository-safe engineering artifacts required by this campaign. Production/Pi5 integration remains prohibited unless separately authorized.

HQ remains sole authoritative vision chain:
`HQ -> Hailo detector -> NanoTracker -> CA Kalman -> CurrentTargetManager -> HOROS`.

WIDE has no authority for target detection/confirmation, tracking, metric range, HOROS target XYZ, navigation or mission authority except as separately reviewed/authorized by the campaign.

## TAI campaign

TAI_CAMPAIGN_STATE: ACTIVE
TAI_PHASE: PHASE_A_STANDALONE_ENGINEERING
TAI_WORKSHOP_ENGINEERING_AUTHORITY: AUTHORIZED_PHASE_A_BOUNDED
TAI_PI5_REQUIRED_PHASE_A: NO
TAI_PRODUCTION_AUTHORITY: NONE
TAI_CODEX_AUTHORITY: NONE
TAI_DESIGN_AUTHORITY: `nevincho/TANGRA-DOCS`, branch `TAI`
TAI_ENGINEERING_REPOSITORY: `nevincho/TANGRA-2.0` (private, repository-safe Phase A implementation artifacts)

WORKSHOP may, one bounded TAI unit at a time:
- create implementation-ready software/packages;
- create schemas/contracts;
- create deterministic fixtures/simulations;
- create unit tests;
- perform bounded repository-side engineering validation;
- perform independent review/checkpoint work;
- persist implementation artifacts in the private engineering repository and evidence/review/handoffs in WORKSHOP.

TAI Phase A forbids:
- integration into `/home/khan/ai-drone/droneguard_1_0`;
- production modification/promotion;
- modification/redesign of protected HQ/Hailo/NanoTracker/CA Kalman/CurrentTargetManager/HOROS authority behaviour;
- FC/carrier/actuation activation;
- Codex dispatch/integration;
- runtime parameter changes unless explicitly authorized in a later phase.

Codex integration requires a later explicit human authorization after:
`ENGINEERING_COMPLETE = YES`, `REVIEW_COMPLETE = YES`, `REQUIRED_UNITS = COMPLETE`, `KNOWN_BLOCKERS = NONE`.

## Agent rules

- Inspect current canonical repository/runtime evidence before conclusions.
- Preserve validated/production components and interfaces.
- Do not infer Pi5 production/runtime paths from memory.
- Do not convert repository/simulation validation into current runtime state.
- Detect phase mismatch, duplicate work and invalid validation methodology before implementation.
- Missing evidence is `NOT VERIFIED` / `UNKNOWN` / `SOURCE_GAP` as defined by the active contract.
- STOP between Control Room bounded units.

## Runtime/host

Production/Pi5 runtime actions remain prohibited for current WIDE-EW and TAI Phase A engineering. Repository-safe engineering and deterministic local/repository tests are permitted.

## Codex

No Codex work is authorized for either current TAI Phase A engineering or WIDE-EW unless a separate explicit human gate opens it.
