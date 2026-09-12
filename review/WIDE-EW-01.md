# WIDE-EW-01 — Independent Review

DATE: 2026-09-12
REVIEW_SCOPE: Contract + non-metric cue generator + deterministic tests + resource evidence
VERDICT: PASS

## Acceptance review

### Exact WideAcquisitionCue schema
PASS. Versioned schema is explicit and excludes target/class/range/XYZ/bearing/FC authority.

### Provenance/freshness semantics
PASS. Source is fixed to `WIDE_IMX708`; provenance is explicitly non-metric stable-background differencing; monotonic timestamp plus bounded max age is validated at consumer acceptance.

### Deterministic cue generation
PASS. Reference implementation is deterministic, non-neural and restricted to downscaled grayscale stable-background differencing.

### Temporal filtering
PASS after engineering correction. Initial frame-to-frame persistence could have treated appearance/disappearance of a large single-frame transient as two consecutive motion events. The final package uses a retained stable-background reference and refreshes it only on non-motion observations. Added large-transient adversarial test passes.

### Fail-closed behavior
PASS. Malformed frame/timestamp/schema/provenance/coordinates, insufficient area/persistence and stale cues all produce no acceptable cue. No fallback creates metric or command authority.

### Required deterministic tests
PASS.
- STATIC: PASS
- MOTION LEFT: PASS
- MOTION CENTER: PASS
- MOTION RIGHT: PASS
- TRANSIENT NOISE: PASS
- STALE CUE: PASS
Additional large-one-frame-transient and malformed-input cases: PASS.

### Resource evidence
PASS for Workshop engineering candidate selection, with explicit limitation. Hardened 160x90 implementation measured ~1.710 ms/sample over 1,000 processing calls in the available Workshop Python environment (~584.8 processing-only samples/s). At proposed 5 Hz cadence this is ~8.55 ms processing per wall-clock second on that host. This supports selection as a low-cost integration candidate but is not Pi5/runtime evidence and excludes capture/downscale cost. No production resource claim is authorized.

### Future MC1 ingress boundary
PASS. Boundary is explicit:
`WIDE latest frame -> WideCueGenerator -> WideAcquisitionCue -> acquisition bridge -> MC1 authority validation -> M1 acquisition decision`.
N1 is explicitly excluded pre-confirmation; no CurrentTarget/HOROS authority is created.

### Protected scope
PASS. Package modifies no HQ detector, NanoTracker, CA Kalman, CurrentTargetManager, HOROS, N1, M1, M2, M3, FC, command-send, Pi5 or production path.

## Review conclusion
The package satisfies WIDE-EW-01 acceptance as an independently reviewable engineering unit. It is suitable for the next bounded Workshop unit that defines/validates the acquisition bridge into MC1/M1, without runtime integration.

No Codex or production promotion is authorized by this PASS.
