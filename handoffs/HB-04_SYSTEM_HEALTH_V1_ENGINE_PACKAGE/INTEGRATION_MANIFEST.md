# HB-04 Integration Manifest

Future bounded integration target: `D:\RaspberryPi5\TANGRA\ACTIVE\DASHBOARD\TANGRA_DASHBOARD_2_1`.

Evidence basis: accepted Dashboard 2.1 architecture recovery identifies `dashboard.py`, `dashboard_state.py`, `runtime_state.py`, `pi_runtime_control.py`, `POST /api/ingest`, `GET /api/telemetry`, and `GET /api/pi/status` as existing telemetry/state surfaces.

## Intended attachment points
1. After `dashboard.py` produces the existing merged current telemetry object used by `GET /api/telemetry`, pass that object read-only to `SystemHealthV1Engine.normalize(...)`.
2. Reuse the current PC-side Runtime Controller status snapshot already obtained through `pi_runtime_control.py` / `GET /api/pi/status`; no new poll solely for System Health.
3. Instantiate one engine in Dashboard process scope so the authorized ephemeral Hailo last-valid-observation timestamp survives successive polls; no file/database persistence.
4. Attach returned `TANGRA_SYSTEM_HEALTH_V1` object to existing PC Dashboard state for later Settings/System Health UI consumption. Raw telemetry remains unchanged and authoritative as source facts.

## Explicit non-attachment points
- no `/api/set` use;
- no Pi/runtime endpoint change;
- no `POST /api/ingest` producer-contract change;
- no Communication Manager authority change;
- no CA/tracking/range/HOROS authority change;
- no command/IFF/readiness/actuation path.

## Future integration action
Copy `system_health_v1/` into the Dashboard COPY, import and instantiate `SystemHealthV1Engine` in the existing Dashboard backend layer, call `normalize()` where merged telemetry and current Runtime Controller status are already available, and expose only the normalized derived object through existing PC Dashboard state. Exact line-level insertion is deferred to later bounded integration against the then-current Dashboard COPY.
