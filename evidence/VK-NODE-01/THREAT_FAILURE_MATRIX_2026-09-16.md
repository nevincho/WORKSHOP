# VK-NODE-01 — Threat / Failure Decision Matrix

Date: 2026-09-16
Authority: `decisions/VK_NODE_IDENTITY_ENROLLMENT_TRUST_CLONE_RECOVERY_CONTRACT_2026-09-16.md`

| Case | Condition / evidence | Decision | Identity action | History / provenance | Replication | Recovery / escalation |
|---|---|---|---|---|---|---|
| Normal returning node | Accepted enrollment; valid node-key proof; ACTIVE; no revocation/conflict | AUTHORIZED | Continue same NodeIdentity | Preserve; continue own origin_sequence | Eligible under DIST-04 policy | None |
| New node | No accepted enrollment yet | NOT_AUTHORIZED | Fresh key + NodeIdentity; obtain LEA enrollment | Existing history unchanged; bootstrap only after enrollment | Ineligible until ACTIVE | Owner enrollment |
| Interrupted enrollment | Request/key exists but no durably accepted signed enrollment | NOT_AUTHORIZED | Remain UNENROLLED; safely retry; identical accepted record idempotent | No fabricated provenance | Ineligible | Retry with LEA |
| SSD clone | Same NodeIdentity/key appears in independent incarnations | CLONE_CONFLICT | Freeze lineage; owner resolves or authorized split | Preserve both histories/evidence; no winner | Withheld | Owner resolution |
| Portable Seed clone | Two media copies; same node secret concurrently used | CLONE_CONFLICT; copied media without identity authority is NOT_AUTHORIZED on a new host | New host enrolls new identity or authenticated migration/recovery | Preserve copied valid history unchanged | Withheld until resolved | Enrollment/split/recovery |
| VM clone | Same NodeIdentity/key duplicated and independently active | CLONE_CONFLICT | No automatic winner | Preserve divergent evidence | Withheld | Owner resolution/split |
| Directory clone | Runtime/identity directory copied | NOT_AUTHORIZED until exclusive authority; CLONE_CONFLICT if duplicate lineage active | New identity or authorized migration | Preserve valid history | Withheld unless exclusively authorized | Enrollment/migration |
| Simultaneous duplicate NodeIdentity | Two live valid proofs without exclusive handoff | CLONE_CONFLICT | Suspend ordinary continuation | Preserve all valid evidence | Withheld | Explicit owner resolution |
| Intentional migration | Signed exclusive handoff; old host continuation closed; verified frontier | AUTHORIZED at target | Same NodeIdentity remains ACTIVE; old host incarnation migration-closed | Preserve; continue same origin_sequence from frontier | Target eligible | None after completion |
| Old machine returning | Migration-closed old incarnation presents copied key | NOT_AUTHORIZED; CLONE_CONFLICT if competing continuation exists | NodeIdentity remains at authorized target; old host cannot continue | Historical records remain valid | Old host ineligible | Owner inspection if divergence |
| Lost node | Node unavailable/lost and future possession untrusted | NOT_AUTHORIZED after revocation; may first be SUSPENDED | Revoke or recover/replace | Preserve history | Ineligible | LEA revocation/recovery |
| Portable Seed recovery | Seed restores code/history; separate recovery authority exists | RECOVERY_REQUIRED until recovery accepted; then AUTHORIZED | Same identity recovery or replacement enrollment | Preserve; same identity sequence only if proven | Withheld during recovery | Recovery authority |
| Missing recovery material | Identity known but valid key/recovery authority absent | RECOVERY_REQUIRED | Do not synthesize identity | Preserve history | Ineligible | Restore protected authority |
| Revoked reconnect | Old key valid but authenticated revocation applies | NOT_AUTHORIZED | Remain REVOKED | Historical valid provenance remains | Ineligible | Replacement identity if desired |
| Unknown node claiming LogicalIdentity | Claim only; no accepted enrollment | NOT_AUTHORIZED | Remain UNENROLLED | No history authority granted | Ineligible | Owner enrollment if legitimate |
| Legitimate hardware change | Same lineage; valid proof; no competitor | AUTHORIZED | No identity change | Preserve/continue | Eligible | None; hardware non-authoritative |
| Corrupted identity metadata | Binding/key/frontier incomplete or inconsistent | RECOVERY_REQUIRED | Reconstruct only via authenticated recovery | Preserve independently valid history | Withheld | Recovery authority |
| Divergent clone history | Same NodeIdentity has incompatible future sequence claims | CLONE_CONFLICT | Freeze lineage; no timestamp winner | Preserve both branches | Withheld | Owner split/recovery/revocation |
| Two legitimate concurrent nodes | Different enrolled NodeIdentities; both ACTIVE | AUTHORIZED for each | Separate node lineages | Preserve separate provenance/origin namespaces | Eligible independently | Normal reconciliation |
| Android node enrollment | Fresh Android keypair/NodeIdentity; portable LEA enrollment verified | AUTHORIZED after accepted enrollment | OS keystore optional protection, not authority | Bootstrap shared history; new origin namespace | Eligible | Standard enrollment |
| Offline enrollment | LEA/delegated signer and required policy evidence locally available | AUTHORIZED after accepted signed enrollment; otherwise NOT_AUTHORIZED | Deterministic offline enrollment only with full authority | Preserve history | Eligible only after enrollment | Later reconcile control evidence without timestamp winner |
| Offline recovery | Recovery authority, non-conflict evidence and frontier locally available | RECOVERY_REQUIRED until accepted, then AUTHORIZED; otherwise RECOVERY_REQUIRED | Same/replacement recovery per contract | Preserve history | Withheld until completion | Wait for authority if insufficient |
| Seed copied but no node secret | Bootstrap media/history duplicated; identity absent | NOT_AUTHORIZED | Fresh enrollment | Copied valid shared history remains valid | Ineligible before enrollment | Owner enrollment |
| Identity key copied secretly | Same private key used by second incarnation | CLONE_CONFLICT when duplicate continuation credible | Rotate/recover or revoke; establish one continuation | Preserve historical evidence | Withheld | Security recovery |
| Suspended returning node | Valid proof but SUSPENDED | NOT_AUTHORIZED for ordinary replication | Owner/policy may restore ACTIVE | Preserve history | Ineligible | Validate then restore |
| Retired node reconnect | Valid historical key but NodeIdentity RETIRED | NOT_AUTHORIZED | Remain RETIRED | Preserve historical provenance | Ineligible | New NodeIdentity if desired |

## Determinism notes
The decision procedure never uses newest timestamp, newest hardware, hostname, MAC, IP, disk path, OS identity, uptime, or last-seen ordering as authority. Device/environment facts are diagnostic only. Competing valid same-NodeIdentity continuation is `CLONE_CONFLICT` until explicit authority establishes a safe lineage outcome.
