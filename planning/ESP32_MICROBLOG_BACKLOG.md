# ESP32 MicroBlog + AGENT 32 — Proposed WORKSHOP Backlog

STATUS: PLANNED / NOT ACTIVE
SOURCE: `nevincho/nova:esp32-microblog-agent32/ESP32_MICROBLOG/`

This backlog is derived from the current project documentation. It does not activate execution and does not alter the existing WORKSHOP project priority order.

## TASK-045 — Canonical state reconciliation
Type: repository/local-state preparation
Goal: reconcile documentation branch with the authoritative local workspace before any source change. Verify exact v0.7 source location, current files, board/core/tool versions, COM port, and whether the 3.3.11 update completed. Record all unknowns as NOT VERIFIED.
Gate: local Windows execution route required for authoritative implementation-state claims.

## TASK-046 — Post-update minimal Wi-Fi toolchain diagnostic
Type: environment validation
Depends on: TASK-045
Goal: compile the same minimal Wi-Fi diagnostic that previously reproduced the stall, using the current post-update toolchain. This tests whether the blocker was actually removed before touching v0.7.
Acceptance: compile completes or produces a concrete reproducible environment error; exact Arduino CLI/core/toolchain versions recorded.

## TASK-047 — Exact v0.7 lean compile and resource measurement
Type: build validation
Depends on: TASK-046 PASS
Goal: compile the untouched exact v0.7 lean source and record application flash/RAM measurements.
Rule: do not change v0.7 unless this fresh compile identifies an implementation defect.

## TASK-048 — v0.7 physical upload and smoke test
Type: hardware validation
Depends on: TASK-047 PASS
Goal: upload the exact built v0.7 image to ESP32-WROOM-32 after re-detecting the physical COM port; verify boot, PocketNode AP, local site, 192.168.4.1, mDNS where supported, /admin auth, persistence, reset/reboot stability.
Human/live gate: REQUIRED.

## TASK-049 — AGENT 32 deterministic regression and safety suite
Type: functional validation
Depends on: TASK-048 PASS
Goal: validate retained Tech, Business, Nature and MicroBlog-help domains; verify deterministic intent/knowledge routing, low-confidence escalation, and safety refusals/escalations. Do not present AGENT 32 as an LLM.

## TASK-050 — Offline RC stress/regression gate
Type: release validation
Depends on: TASK-049 PASS
Goal: short stress/regression run covering local HTTP, AP stability, admin/persistence, repeated AGENT 32 use, restart/reconnect behavior, and absence of panic/brownout/reboot loops.
Outcome: decide whether Offline RC criteria are satisfied without Connected Mode/Web Search.

## TASK-051 — Reproducible release binary export
Type: release engineering
Depends on: TASK-050 PASS
Goal: export the exact validated merged firmware binary and hashes; record source fingerprint/toolchain versions/board target so the release artifact is traceable to the validated build.

## TASK-052 — Binary-only Windows customer installer/package
Type: implementation/package
Depends on: TASK-051 PASS
Goal: build the documented no-source customer package with standalone flashing tooling, COM selection, failure handling, warnings, QUICK_START/INSTALLATION/TROUBLESHOOTING, and SHA256SUMS. No Arduino IDE/Python/pip dependency for the customer.

## TASK-053 — Installer end-to-end acceptance
Type: hardware/customer-flow validation
Depends on: TASK-052
Goal: erase/flash a physical compatible ESP32 using only the actual customer package, then execute the customer quick-start path through PocketNode and admin access.
Human/live gate: REQUIRED.

## TASK-054 — Offline Edition release review
Type: independent release review
Depends on: TASK-053 PASS
Goal: independently verify that every advertised Offline Edition feature has evidence and that Connected Mode/Web Search are clearly excluded or marked unvalidated if still NOT VERIFIED.

## OPTIONAL TRACK — must not block Offline Edition

### TASK-055 — Connected Mode validation
Depends on: stable Offline RC
Verify WIFI_AP_STA join, PocketNode availability, bounded reconnect, Internet-loss behavior, credential handling and no reset/resource regression.

### TASK-056 — Narrow Web Search validation
Depends on: TASK-055 PASS
Verify configured provider/API handling, bounded structured result retrieval, failure behavior and no false claim of full web/LLM reasoning.

### TASK-057 — Full Edition release review
Depends on: TASK-056 PASS
Independent evidence review for advertised Connected Mode/Web Search features.

## Recommended sequencing
Do not start implementation expansion. The immediate engineering objective is to resolve the toolchain uncertainty and prove the exact v0.7 lean line. Offline RC should be pursued before optional online features.
