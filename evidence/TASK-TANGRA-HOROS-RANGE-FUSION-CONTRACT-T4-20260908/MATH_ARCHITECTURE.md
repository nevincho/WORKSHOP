# TASK 4 — HOROS Range Fusion Contract Architecture

Status: STANDALONE / SHADOW / NO PRODUCTION INTEGRATION.

Boundary: source estimator -> RangeEvidence -> HorosRangeFusionContract -> HorosRangeObservation -> future LOS_RANGE ingress adapter.
Source-specific mathematics remain outside this contract.

Common evidence carries source/version, frame/timestamp/target refs, range/sigma/confidence, validity, metric usability, calibration/transform status, provenance, reason, and independence group.

Fusion policy:
- invalid/non-finite/non-positive/missing evidence fails closed;
- metric UNUSABLE is rejected; NOT_VERIFIED may remain SHADOW evidence but can never become VERIFIED from agreement;
- correlated evidence is reduced to one deterministic representative per independence group;
- one independent source passes through with preserved provenance;
- compatible independent sources use confidence-adjusted inverse-variance fusion;
- disagreement contributes to output uncertainty;
- material conflict produces CONFLICT with no selected range;
- no source authority is invented.

Effective sigma is sigma/sqrt(confidence), so reduced confidence cannot create precision. Fused uncertainty is max(formal independent-fusion sigma, weighted disagreement spread, relative floor).

LOS_RANGE compatibility is intentionally range-only. Bearing/LOS fields remain null when not supplied; TASK 4 does not fabricate camera rays.

Production gate: multiple NOT_VERIFIED sources remain NOT_VERIFIED even if numerically consistent.
