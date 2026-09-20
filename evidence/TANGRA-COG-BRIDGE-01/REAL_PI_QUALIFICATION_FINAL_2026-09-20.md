# TANGRA-COG-BRIDGE-01 — Real Pi Qualification Final Evidence, 2026-09-20

RESULT: PASS
TASK: TANGRA-COG-BRIDGE-01
RUNTIME: /home/khan/ai-drone/tangra
COGNITIVE_RUNTIME: /home/khan/ai-drone/tangra/cognitive_backend
CANDIDATE_HEAD: bd11d92f396b68de00a0f3636ae49ed8310ce420
QUALIFIED_BRIDGE_BLOB: 5f4a6346fa70e369452067d9d96f776a84468a64

## Final human-run Codex report

FILES_CHANGED:
- main.py
- core/config.py
- cognitive/bridge_runtime.py
- exact cognitive_bridge.py blob 5f4a6346...
- Cognitive substrate contracts
- persistence state

TESTS:
- py_compile PASS
- bridge identity PASS
- 2 controlled restarts PASS

LIVE_RESULT:
- service active
- COG-20 COMPLETED
- persistence restored=true
- Hailo active
- CA Kalman primary
- HOROS errors=0
- observed 41.40 FPS
- WIDE unchanged

CONTROL_STATE:
- CONTROL_ENABLED=false
- AUTHORITY=NONE
- operational_authority=[]

RESULT:
PASS

## Historical first precheck

The first real-Pi attempt stopped safely before production mutation because the execution handoff expected a dedicated WIDE detector path while the actual Pi baseline used the current WIDE capture/motion-cue path. That result was BLOCKED_BASELINE_MISMATCH and explicitly not a bridge defect. The successful integration subsequently preserved the actual current WIDE behavior.

## Regression accounting

The earlier repository-side cumulative 317-test regression remains NOT EXECUTED due to the documented WORKSHOP execution-environment acquisition/persistence limitation.

317/317 PASS is NOT claimed.

The real-Pi qualification PASS therefore means the qualified bridge was integrated and the reported target-environment checks above passed; it does not rewrite the historical cumulative-regression record.

## Rollback

Verified pre-change backup retained:
- /home/khan/ai-drone/backups/COG-BRIDGE-01-20260920T1730/prechange.tgz
- SHA256 68ddf4a1e8408b2060e7323b35086db9d585dc93451213ad6f0ae69f50c37062
