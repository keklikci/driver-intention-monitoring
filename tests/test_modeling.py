import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.pipeline import Pipeline

from driver_intention_monitoring.modeling import (
    anticipation_target,
    build_estimator,
    build_soft_voting_estimator,
)


@pytest.mark.parametrize(
    ("kind", "expected_type"),
    [
        ("random_forest", RandomForestClassifier),
        ("logistic_regression", Pipeline),
        ("linear_svm", Pipeline),
    ],
)
def test_build_estimator_returns_supported_baseline(
    kind: str, expected_type: type
) -> None:
    assert isinstance(build_estimator(kind), expected_type)


def test_build_soft_voting_estimator_uses_probability_voting() -> None:
    estimator = build_soft_voting_estimator()

    assert isinstance(estimator, VotingClassifier)
    assert estimator.voting == "soft"


def test_anticipation_target_marks_samples_before_lane_change() -> None:
    result = anticipation_target(np.array([False, False, False, True, True]), horizon=2)

    assert result.tolist() == [0, 1, 1, 0, 0]


def test_anticipation_target_returns_no_labels_without_lane_change() -> None:
    result = anticipation_target(np.array([False, False]), horizon=1)

    assert result.tolist() == [0, 0]
