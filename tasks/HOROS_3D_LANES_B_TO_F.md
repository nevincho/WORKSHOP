# HOROS / LOCAL 3D — CONTRACT-DRIVEN IMPLEMENTATION LANES

STATUS: READY_FOR_WORKER
PREREQUISITE: Phase A Independent Reviewer PASS
TARGET: nevincho/TANGRA-DOCS branch workshop-horos-3d
WRITE_SCOPE: Workshop/HOROS_3D/** only

## Lane 1 — time / geometry
Implement bounded observation synchronization, synthetic camera geometry adapter, explicit cross-camera association, fixed-baseline stereo evidence, carrier transforms and ego-motion helpers.

## Lane 2 — range / Local3D
Implement passive range hypothesis fusion and a downstream passive Local3D estimator using supplied contract objects. No baseline authority changes.

## Lane 3 — persistent local map
Implement versioned sparse map storage, landmarks, freshness/confidence/provenance, bounded merge policy, candidate selection/wrong-area rejection, map-derived constraint output and fail-open load behavior.

## Lane 4 — Mission Recorder / replay
Implement non-blocking bounded queue, deterministic overflow policy, bounded retained records, schema-versioned JSONL serialization, tolerant replay parser/reconstruction and explicit corrupt/schema-mismatch diagnostics.

## Lane 5 — replay model / diagnostics
Implement client-side-neutral data models for timeline/play/pause/scrub and renderable carrier/target/Kalman/HOROS/fused/landmark/health layers, plus prediction residual/error provenance/propagation/retraining-candidate preparation. No operational authority.

## Required tests
Synthetic/deterministic tests for aligned vs mismatched timestamps, wrong association, degenerate disparity, invalid geometry, static XYZ, constant velocity, moving carrier/stationary world target transform, range disagreement/no source/uncertainty degradation, map persistence/merge/wrong-area/revisit/failure isolation, recorder bounds/drop/serialization/corrupt/missing layer/schema/order, replay timeline behavior, residual/provenance/candidate selection.

## Evidence limits
Synthetic fixtures must be labelled SYNTHETIC. Physical metric claims and authoritative runtime integration remain NOT VERIFIED.
