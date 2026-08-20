"""Classical machine-learning utilities used in DIM experiments."""

from collections.abc import Sequence

import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def build_estimator(
    kind: str, random_state: int = 42
) -> Pipeline | RandomForestClassifier:
    """Build a reproducible baseline classifier for a DIM experiment."""
    if kind == "random_forest":
        return RandomForestClassifier(n_estimators=100, random_state=random_state)
    if kind == "logistic_regression":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(random_state=random_state)),
            ]
        )
    if kind == "linear_svm":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    SVC(kernel="linear", probability=True, random_state=random_state),
                ),
            ]
        )
    raise ValueError(f"unknown estimator kind: {kind}")


def build_soft_voting_estimator(random_state: int = 42) -> VotingClassifier:
    """Build the calibrated ensemble used for DIM classification experiments."""
    return VotingClassifier(
        estimators=[
            ("random_forest", build_estimator("random_forest", random_state)),
            ("linear_svm", build_estimator("linear_svm", random_state)),
        ],
        voting="soft",
    )


def anticipation_target(
    lane_change: Sequence[bool] | np.ndarray,
    horizon: int,
) -> np.ndarray:
    """Label samples in the horizon immediately before the first lane change."""
    if horizon < 1:
        raise ValueError("horizon must be positive")
    values = np.asarray(lane_change, dtype=bool)
    target = np.zeros(values.size, dtype=int)
    indices = np.flatnonzero(values)
    if indices.size:
        event_start = int(indices[0])
        target[max(0, event_start - horizon) : event_start] = 1
    return target
