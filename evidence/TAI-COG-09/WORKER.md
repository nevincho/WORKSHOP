# TAI-COG-09 WORKER EVIDENCE

Engineering repo: `nevincho/TANGRA-2.0`
Branch: `tai-cog-09`
Base: `ebd695a9081d9e47efe4e24d42f8927653e81292`
Candidate checkpoint: `1742232e9fbf1fc735254d974642afd00479ef5c`

Files added only under `TANGRA_2_0/00_FOUNDATION/TAI_COG_09/`:
- `README.md`
- `fixtures/sample_passive_observation.json`
- `tangra_passive_observer/__init__.py`
- `tangra_passive_observer/observer.py`
- `tests/test_passive_observer.py`

Validation performed locally against compatibility contracts matching consumed COG-00 StateEvent and COG-06 backend-health interfaces:
- `py_compile`: PASS
- deterministic unittest: 21/21 PASS

Validated behavior:
1. submit path uses non-blocking `queue.put_nowait` and does not call backend;
2. queue capacity bounded;
3. overflow/drop affects observer work only;
4. stale observations explicit;
5. NORMAL→REDUCED_SAMPLING→BACKEND_BYPASS→PAUSED covered;
6. PAUSED performs observer-local load shedding with explicit dropped count so Core never waits;
7. backend UNAVAILABLE/FAILED/exception/slow isolated to observer degradation;
8. disabled observer accepts/processes zero work;
9. operational authority remains empty;
10. source StateEvent remains unchanged after snapshot/output mutation;
11. explicit event/state-domain/claim-class filtering;
12. deterministic byte-identical observation output;
13. config/observation/health serialization round-trips;
14. no mission/target/config/command/remediation API;
15. invalid event fails open into observer-local drop.

No Pi5, Hailo, production runtime, real model, replay/Twin, STT/TTS or command-path execution was performed.
