#!/usr/bin/env python3
import json
from pathlib import Path
from evaluator import evaluate_fixture

ROOT = Path(__file__).parent
suite = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
cases = json.loads((ROOT / "synthetic_cases.json").read_text(encoding="utf-8"))["cases"]
fixtures = {x["id"]: x for x in suite["tests"]}


def run():
    rows = []
    for case in cases:
        result = evaluate_fixture(fixtures[case["fixture"]], case["output"])
        cats = {x["category"] for x in result["failures"]}
        assert result["pass"] == case["expected_pass"], (case["id"], result)
        if case["expected_failure"]:
            assert case["expected_failure"] in cats, (case["id"], cats)
        rows.append({"case":case["id"],"observed_pass":result["pass"],"failure_categories":sorted(cats)})

    malformed = evaluate_fixture(fixtures["T1"], {"test_id":"T1","claims":"bad"})
    assert "MALFORMED_STRUCTURED_OUTPUT" in {x["category"] for x in malformed["failures"]}
    rows.append({"case":"MALFORMED_CONTROL","observed_pass":False,"failure_categories":["MALFORMED_STRUCTURED_OUTPUT"]})

    # Explicit EXPECTED -> VERIFIED promotion control.
    promoted = {
        "test_id":"T1",
        "claims":[
            {"fact_id":"hailo_current","status":"VERIFIED","evidence_ids":["T1-E1","T1-E2"]},
            {"fact_id":"hq_camera_current","status":"NOT_VERIFIED","evidence_ids":["T1-E1","T1-E2"]}
        ],
        "distinctions":["expected_configuration_vs_current_evidence"],
        "summary":"Synthetic promotion control"
    }
    p = evaluate_fixture(fixtures["T1"], promoted)
    assert "EXPECTED_PROMOTED_TO_VERIFIED" in {x["category"] for x in p["failures"]}
    rows.append({"case":"EXPECTED_PROMOTION_CONTROL","observed_pass":False,"failure_categories":sorted({x["category"] for x in p["failures"]})})

    print(json.dumps({"pass": True, "cases": rows}, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
