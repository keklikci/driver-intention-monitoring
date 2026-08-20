"""Road geometry classification for DIM."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .schema import SignalColumns


@dataclass(frozen=True)
class GeometryThresholds:
    """Speed-dependent curvature thresholds for road classification."""

    speeds_kmph: tuple[float, ...]
    curvatures_radpm: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.speeds_kmph:
            raise ValueError("speed lookup must not be empty")
        if len(self.speeds_kmph) != len(self.curvatures_radpm):
            raise ValueError("speed and curvature lookup lengths must match")
        if tuple(sorted(self.speeds_kmph)) != self.speeds_kmph:
            raise ValueError("speed lookup must be sorted")

    def lookup(self, speed_kmph: float) -> float:
        """Return the piecewise threshold for a vehicle speed."""
        index = int(np.searchsorted(self.speeds_kmph, speed_kmph, side="right"))
        return self.curvatures_radpm[min(index, len(self.curvatures_radpm) - 1)]


def classify_geometry(
    drive: pd.DataFrame,
    columns: SignalColumns,
    thresholds: GeometryThresholds,
) -> pd.DataFrame:
    """Add curvature and straight or curve road geometry labels."""
    required = [columns.velocity_kmph, columns.curvature_left, columns.curvature_right]
    missing = set(required).difference(drive.columns)
    if missing:
        raise KeyError(f"missing required columns: {sorted(missing)}")

    result = drive.copy()
    curvature = (
        result[columns.curvature_left].abs() + result[columns.curvature_right].abs()
    ) / 2
    threshold = result[columns.velocity_kmph].map(thresholds.lookup)
    result["curvature_abs_avg_radpm"] = curvature
    result[columns.geometry] = np.where(curvature > threshold, "curve", "straight")
    return result
