# LORA-05A File Manifest

- `README.md` — package scope/boundaries.
- `INTEGRATION_CONTRACT.md` — future real Dashboard binding contract; unresolved bindings explicitly `ADAPTER_MAPPING_REQUIRED`.
- `TEST_EVIDENCE.md` — deterministic validation/regression evidence.
- `dashboard_lora_ingress/models.py` — transport-neutral semantic update model including local LINK section.
- `dashboard_lora_ingress/semantic_mapper.py` — pure LORA-02 semantic message mapping.
- `dashboard_lora_ingress/ingress.py` — byte ingress using LORA-03 observer as packet-order/link authority.
- `dashboard_lora_ingress/dashboard_sink.py` — abstract sink + in-memory test sink.
- `dashboard_lora_ingress/__init__.py` — exports.
- `tests/test_dashboard_ingress.py` — deterministic ingress tests.
- `fixtures/fixture_manifest.json` — dependency commits/test-only clock thresholds.

The accepted LORA-02/LORA-03 implementations are dependencies and are not copied into this handoff package.
