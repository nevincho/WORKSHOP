# HUMAN GATE POLICY

STATUS: MANDATORY
APPLIES TO: ALL AUTONOMOUS WORK

Autonomous work must stop only the affected dependency chain and request Control Room review when any of the following applies:

- protected VK Core, canonical personality or approved-memory mutation;
- destructive or irreversible operation;
- architectural contradiction or scope conflict;
- missing credentials, hardware, network path or required execution access;
- validation cannot establish the claimed objective;
- task requires unsupported scope expansion;
- prerequisite is absent or contradicted by repository/runtime evidence;
- security-sensitive or production-critical change exceeds current authorization;
- target project policy explicitly requires human approval.

Independent eligible work may continue when it does not depend on the blocked chain.

A human gate record must contain:
- task id;
- exact blocker;
- evidence;
- affected dependency chain;
- smallest decision required from Vlad/Control Room;
- safe current checkpoint;
- allowed independent work that may continue.

Do not convert uncertainty into approval. Use NOT VERIFIED where evidence is unavailable.