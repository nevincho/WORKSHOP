# TANGRA-COG-V1-PI-RUNTIME-01

- CHECKPOINT_ID: TANGRA-COG-V1-PI-RUNTIME-01
- PROJECT: TANGRA Cognitive V1
- TASK_ID: PI production chain / persistence / llama lifecycle / coexistence closure
- TIMESTAMP: 2026-09-27
- TARGET_REPOSITORY_OR_RUNTIME: `/home/khan/ai-drone/tangra` on Raspberry Pi 5
- BRANCH_OR_RUNTIME_CONTEXT: live production runtime; `tangra-droneguard-1-0.service`
- COMMIT_SHA / TAG / SNAPSHOT_REFERENCE: Git commit NOT VERIFIED for live Pi files. Bridge validated post-integration SHA256: `1272077469731093d06961712d68fba04d5bf1924d9129ea33c774e5d0ab1c18`. Durable Experience snapshot: `cognitive_backend/state/experience_store.json`.
- VALIDATION_EVIDENCE:
  - production typed chain completed: COG-02→16→18→19→20→RAW Experience→persist/reload→COG-26;
  - persisted Experience survived restart and reached COG-26 reference path;
  - persistent `llama-server` lifecycle validated start=1, repeated=1, stop=0, restart=1;
  - controlled stop 2.865 s, exit 0, no timeout/SIGKILL;
  - mission coexistence detection path showed no measured degradation;
  - observer-only boundary preserved with `authority=NONE`, `operational_authority=[]`.
- TESTS_RUN:
  - adapter compile PASS;
  - restart cycles PASS;
  - full Cognitive chain COMPLETED;
  - Experience persist/restart/load PASS;
  - single-owner server lifecycle PASS;
  - bounded mission coexistence detection measurement PASS within measured scope.
- PROTECTED_COMPONENT_STATUS:
  - Cognitive authority remains NONE;
  - operational authority remains [];
  - no command/mission/flight actions observed;
  - qualified Cognitive semantics/blobs not intentionally changed by the lifecycle/coexistence validation;
  - no new 317/317 regression claim.
- ROLLBACK_METHOD: production deployment reported a recoverable original bridge backup; exact backup pathname is NOT VERIFIED in this checkpoint. Qualified repository artifacts and the recorded bridge SHA256 identify the current known-good integration state. The systemd lifecycle change is isolated to `/etc/systemd/system/tangra-droneguard-1-0.service.d/95-cognitive-shutdown.conf` plus `cognitive_backend/package/adapter.py`.
- KNOWN_LIMITATIONS:
  - tracking coexistence NOT VALIDLY TESTED because `active_trackers=0` and no target stimulus was available;
  - HQ/WIDE cadence and explicit frame-age were not exposed;
  - coexistence gate did not create an equivalent current-runtime non-llama A/B because NO_CHANGE/read-only was enforced;
  - exact live Pi git commit for changed files NOT VERIFIED.
- REVIEW_VERDICT: PASS for typed chain, persistence and server lifecycle; TEMPORARY PASS WITH LIMITATION for mission coexistence; TRACKING COEXISTENCE DEFERRED.

Next required bounded validation: repeat coexistence during a real or controlled active-tracking workload with `active_trackers > 0`.
