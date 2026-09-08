# Reviewer Handoff — TASK 2 AI→Calibrated HQ Geometry Adapter

Status: REVIEW READY / STANDALONE COORDINATE ADAPTER ONLY

Reviewer must verify:
- A and A^-1 semantics and numerical correctness;
- finite/invertible affine validation and fail-closed output;
- crop+resize and padding/letterbox fixtures;
- explicit integer-pixel-center continuous coordinate convention;
- bbox corner transform;
- TASK 1 equivalent sparse geometry compatibility;
- invalid/null points never gain coordinates;
- K_AI=A*K_CAL mathematical consistency;
- no concrete production transform fabricated;
- no TASK 1 or protected runtime modification;
- complete deterministic tests;
- benchmark claim limited to host coordinate-only microbenchmark.

Production transform is intentionally NOT_VERIFIED because available repository evidence did not establish the complete live HQ preprocessing transform. This is not a blocker to the generic implementation-ready adapter; it is a gate for future production integration.

Do not start TASK 3.
