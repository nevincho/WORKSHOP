# TASK 3 — Sparse Geometry Range Mathematics / Architecture

Status: STANDALONE SHADOW / SYNTHETICALLY VALIDATED / NO PRODUCTION INTEGRATION

## Evidence boundary
Current baseline documents `HQ bbox + target_profiles.py dimensions + provisional intrinsics -> MONOCULAR_CLASS_SIZE -> LOS_RANGE -> HOROS XYZ`, but physical class-size accuracy remains open. Available repository evidence does not prove production numerical target-profile dimensions are exact TASK 1 silhouette-extrema correspondences. TASK 2 production CAL->AI transform A also remains NOT_VERIFIED. TASK 3 therefore imports no production dimensions and keeps production metric usability NOT_VERIFIED.

## Range model
For calibrated endpoints a=(u1,v1), b=(u2,v2):
`du=u2-u1`, `dv=v2-v1`, calibrated pixel length `s_px=sqrt(du^2+dv^2)`, and camera-normalized span
`q=sqrt((du/fx)^2+(dv/fy)^2)`.
The normalized form preserves anisotropic fx/fy instead of applying one scalar focal length to arbitrary 2D spans. For an explicitly corresponding physical span S and explicit orientation projection factor r in (0,1]:
`Z=(S*r)/q`.
The observation envelope is near top-down / mild oblique top-down. r is evidence-bearing configuration; it is not inferred/fabricated. Invalid orientation/correspondence rejects the candidate. Nonzero distortion fails closed unless coordinates are explicitly declared undistorted.

## Physical target profile contract
Each `PhysicalSpanSpec` names two semantic points, physical length and sigma, explicit `correspondence_verified`, `independence_group`, provenance, orientation projection factor and orientation uncertainty. Profile carries id/version/provenance and separate production-verification status. No span is created merely because two image points exist. All task fixtures are SYNTHETIC.

## Candidate evidence
Every candidate preserves span id/group/endpoints, `calibrated_length_px`, normalized calibrated span q, associated physical span/uncertainty, candidate range/uncertainty/confidence/validity/acceptance/rejection, and provenance including profile-span source, source geometry reference, calibration id, transform id/version and orientation factor.

## Uncertainty
Independent endpoint coordinate sigma p gives `sigma_du=sigma_dv=sqrt(2)*p`. First-order propagation derives sigma_q. Relative candidate range sigma combines physical-dimension, image-span, orientation-factor, calibration relative-scale and TASK 2 transform relative-scale uncertainties in quadrature. A configured relative floor avoids false precision.

## Robust fusion
Reject invalid/non-finite/near-zero candidates first. One best-information representative per independence group prevents correlated spans multiplying evidence. With >=3 groups, median-relative residual rejects bounded outliers. With exactly two groups, excessive pair disagreement fails closed. Fusion weight is confidence/sigma^2, one representative per group. Output sigma is max(formal fused sigma, weighted disagreement sigma, configured floor).

## Production metric gate
Production metric verification requires transform valid + production-verified, target profile production-verified, and camera calibration production-verified. Current evidence does not satisfy these production gates, so successful standalone observations remain DEGRADED / production metric NOT_VERIFIED.

## Existing range comparison
A passive DTO/function compares externally supplied existing range evidence (e.g. MONOCULAR_CLASS_SIZE) only when both sides are valid. It neither imports nor modifies the existing estimator and makes no superiority claim.
