# HB-05 Integration Manifest

Package consumes the reviewed HB-04 normalized object only. It does not accept raw Pi telemetry and does not contain health derivation rules.

## Intended Dashboard 2.1 attachment points
- Settings shell: `dashboard.py`, existing **Diagnostics** Settings group. Add the supplied `system_health_v1.fragment.html` as the System Health page/panel.
- Existing Settings polling/render path: after the Dashboard backend has attached the HB-04 `TANGRA_SYSTEM_HEALTH_V1` object to PC Dashboard state, pass that object to `attachSystemHealthView({root, getHealthSnapshot})` or `renderSystemHealth(root, healthObject)`.
- Styles: include `system_health_v1.css`; variables intentionally reuse generic Dashboard panel/text/status variables when present and provide dark fallback values.
- No dedicated network request is required by this UI package. It must reuse the existing Dashboard state/poll cycle that receives the HB-04 normalized object.

## Integration contract
- Input schema: `TANGRA_SYSTEM_HEALTH_V1`.
- Exact concepts: 12 canonical HB-04 concepts, ordered and validated.
- State strings are displayed verbatim: `NOMINAL`, `DEGRADED`, `FAULT`, `STALE`, `UNAVAILABLE`, `NOT_VERIFIED`.
- Reason codes are displayed verbatim.
- Diagnostic values are selected for readability only; values never change health state.
- Missing/invalid HB-04 contract renders `System Health unavailable` plus contract errors; UI must not synthesize substitute concepts or green states.

## Explicit non-attachment points
- no `/api/set`;
- no Pi/runtime endpoint;
- no `POST /api/ingest` producer change;
- no direct EDGE LINK polling;
- no command/IFF/readiness/actuation path;
- no new telemetry, thresholds, history, persistence, restart or recovery.

Exact line-level insertion is intentionally deferred to later bounded integration against the authorized Dashboard COPY.
