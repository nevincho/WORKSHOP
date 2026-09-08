# TASK 3 — Sparse Geometry Range Mathematics / Architecture

Status: STANDALONE SHADOW / SYNTHETICALLY VALIDATED / NO PRODUCTION INTEGRATION

## Evidence boundary
Current TANGRA baseline documents `HQ bbox + target_profiles.py dimensions + provisional intrinsics -> MONOCULAR_CLASS_SIZE -> LOS_RANGE -> HOROS XYZ`, while physical class-size accuracy remains open. Available repository documentation does not expose authoritative numerical target-profile dimensions together with proof that TASK 1 silhouette extrema are exact endpoints of those dimensions. TASK 3 therefore imports no production dimensions and keeps production metric usability NOT_VERIFIED.

TASK 2 production CAL->AI transform A remains NOT_VERIFIED. TASK 3 consumes calibrated geometry through an explicit contract and carries a separate transform-production-verification gate.

## Range model
For calibrated points a=(u1,v1), b=(u2,v2):
`q = sqrt(((u2-u1)/fx)^2 + ((v2-v1)/fy)^2)`.
This preserves anisotropic fx/fy rather than applying one scalar focal length to arbitrary 2D spans.
For an explicitly corresponding physical span S and explicit orientation projection factor r in (0,1]:
`Z = (S*r)/q`.
Assumptions: supplied points represent the physical span endpoints; operational envelope is near top-down / mild oblique top-down; r is evidence-bearing input and is never inferred or fabricated here. Invalid orientation/correspondence rejects the candidate. Nonzero distortion fails closed unless coordinates are explicitly declared undistorted.

## Physical target profile contract
Each `PhysicalSpanSpec` names two semantic points, physical length, physical sigma, `correspondence_verified`, an `independence_group`, provenance, orientation projection factor and orientation uncertainty. Profile has version/provenance and separate `production_verified`. No physical span is generated merely because two points exist. All test dimensions are SYNTHETIC.

## Candidate uncertainty
Endpoint sigma p gives `sigma_du=sigma_dv=sqrt(2)*p`. First-order propagation derives sigma_q from dq/du and dq/dv. Candidate relative range sigma combines in quadrature physical-dimension uncertainty, image-span uncertainty, orientation-factor uncertainty, calibration relative scale sigma and TASK 2 transform relative scale sigma. A configured relative floor prevents false precision.

## Robust fusion
Invalid/non-finite/near-zero candidates are rejected first. Robust center uses one best-information representative per `independence_group`, preventing correlated spans from multiplying evidence. With >=3 independent groups, bounded relative-residual outliers are rejected. With exactly two accepted independent groups, excessive pair disagreement fails closed. Final fusion uses confidence/sigma^2 weighting, one representative per group. Output sigma is max(formal fused sigma, weighted disagreement sigma, configured relative floor).

## Production metric gate
`production_metric_verified` requires: valid transform; transform explicitly production-verified; profile production-verified; calibration production-verified. Current evidence satisfies none of the missing production gates, so successful standalone/synthetic observations are DEGRADED with metric status NOT_VERIFIED rather than physical accuracy evidence.

## Existing range comparison
A passive comparison DTO/function accepts externally supplied existing range evidence such as MONOCULAR_CLASS_SIZE and returns absolute/relative delta only when both observations are valid. It does not import, modify, replace or rank the existing estimator and makes no superiority claim.
