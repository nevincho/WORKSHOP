"""Bounded TASK 6 review-correction checks. Requires exact frozen t1.py..t4.py materialized beside view_envelope_validation_harness.py."""
from view_envelope_validation_harness import Condition, run


def test_partial_silhouette_fails_closed() -> None:
    rows = [run(Condition(25.0, 20.0, 20.0, i, "KNOWN", partial=True)) for i in range(5)]
    assert all(r["candidate_count"] < 2 for r in rows)
    assert all(r["t3_error"] == "insufficient_independent_evidence" for r in rows)
    assert all(r["metric_usability"] != "VERIFIED" for r in rows)


if __name__ == "__main__":
    test_partial_silhouette_fails_closed()
    print("1/1 PASS")
