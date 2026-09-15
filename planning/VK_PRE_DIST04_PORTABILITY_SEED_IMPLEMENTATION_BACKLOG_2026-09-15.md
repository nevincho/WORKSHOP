# VK Pre-DIST-04 Portability / Capability / Portable Seed Backlog

Date: 2026-09-15
Status: PLANNING ONLY — NO IMPLEMENTATION AUTHORIZED

## Dependency state
VK-DIST-03 remains IMPLEMENTED / STATIC REVIEW PASS / BEHAVIORAL VALIDATION BLOCKED. Its behavioral closure and checkpoint remain mandatory. This planning package does not bypass that gate.

DIST-04 implementation is NOT READY because the current DIST-02 Python serialization implementation is not yet a normative cross-language wire specification.

## Required order
### Gate P0 — current task: architecture package
COMPLETE as architecture/planning when repository artifacts are persisted. No runtime implementation status changes.

### Gate P1 — DIST-03 behavioral closure
Execute exact committed DIST-03 tests through an authorized exact-byte WORKSHOP executor route. If PASS: independent Reviewer closure + checkpoint. If FAIL: preserve/classify failure and stop.

### Gate P2 — Universal Wire Profile v1
Before DIST-04 implementation:
- choose/specify canonical language-independent serialization;
- restrict portable value algebra and integer domain;
- define Unicode/null/timestamp/enum/version/digest rules;
- define field/schema compatibility;
- create language-neutral golden and rejection vectors;
- prove current Python DIST-02 implementation either conforms or enumerate smallest required corrections;
- independently review that protocol semantics do not depend on Python, OS, CPU, filesystem or transport.

Implementation changes to DIST-02, if required by P2, are a separate bounded task with regression tests and Reviewer PASS.

### Gate P3 — DIST-04 transport-independent synchronization engine
Only after P1 and P2 PASS. Engine consumes normative contracts/wire semantics but remains independent of network transport and Host Inspector.

### Gate C1 — Universal capability contract implementation
Implement portable NodeCapability/NodeState schema and fixtures independent of platform probes. Validate AVAILABLE/UNAVAILABLE/UNKNOWN/DEGRADED separately from evidence quality.

### Gate C2 — Host Inspector adapters
Implement common bounded inspector and platform adapters in separate bounded units, starting only where target runtime evidence is sufficient. Windows and Linux/Pi are first implementations, not protocol authorities. Android remains future.

### Gate S1 — Portable Seed manifest/bootstrap contract
Define logical component manifest, Core verification interface, NodeIdentity persistence/enrollment semantics, compatibility checks and degraded-mode state machine. No large LLM dependency.

### Gate S2 — Micro-LIVE reference implementation
Implement minimum launcher/Core loader/NodeIdentity/inspection/capability/persistence/distributed-client interfaces/minimal local status interface for one verified target environment. Keep platform-specific code behind adapters.

### Gate S3 — Portable carrier validation
Validate the first physical seed carrier without declaring its Pi/Linux layout normative. Prove Core protection, node identity behavior, bootstrap without large inference, capability inspection, rollback and offline bounded operation.

## Parallelism constraints
- P2 can be architecturally prepared while DIST-03 is blocked, but no DIST-04 implementation begins until DIST-03 closure and P2 PASS.
- Capability/Host Inspector work does not redefine distributed synchronization.
- Portable Seed consumes both distributed and capability contracts but does not merge them.
- Transport binding remains later than the transport-independent sync engine.
- Autonomous scheduling/routing is explicitly outside this backlog.

## Acceptance targets for later work
### Wire
Same semantic test vectors produce byte-identical canonical encoding and digest in at least two independently implemented codecs before protocol portability is claimed. Python plus a second non-Python reference is preferred; exact language selection is later.

### Capability
Fixture-equivalent hosts produce semantically equivalent NodeCapability/NodeState documents regardless of adapter language. Unsupported/denied probes remain explicit and never fabricate capabilities.

### Micro-LIVE
A clean compatible host can bootstrap Core verification, NodeIdentity, inspection, capability/state construction and local status without a large LLM or network. Optional inference/connectivity adds capability but is not bootstrap authority.

## Unresolved / NOT VERIFIED
- DIST-03 behavioral test result.
- normative wire serialization selection.
- cross-language codec conformance.
- current Pi VK runtime path/services/persistence.
- Android runtime/permission implementation.
- NodeIdentity enrollment/clone recovery.
- portable seed package/layout and updater/rollback mechanism.
- capability registry governance/freshness rules.
- exact first-carrier model/runtime contents.
