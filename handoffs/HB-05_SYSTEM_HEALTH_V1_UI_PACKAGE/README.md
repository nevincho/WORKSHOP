# HB-05 — Settings / System Health v1 UI Package

Standalone integration-ready UI for the reviewed HB-04 normalized System Health contract.

Scope: read-only Settings UI. No health derivation, telemetry acquisition, Pi/runtime change, persistence, recovery or production integration.

Files:
- `ui/system_health_v1.js` — contract validator, display view-model, renderer and passive adapter.
- `ui/system_health_v1.css` — compact engineering diagnostic layout.
- `ui/system_health_v1.fragment.html` — Settings → Diagnostics → System Health fragment.
- `fixtures/*.json` — normalized HB-04 simulation outputs.
- `tests/test_ui.mjs` — contract-consumption/state/false-green tests.
- `INTEGRATION_MANIFEST.md` — intended Dashboard attachment points.
- `FILE_MANIFEST.md`, `ACCEPTANCE_EVIDENCE.md` — package evidence.

Test: `npm test` or `node --test tests/test_ui.mjs`.
