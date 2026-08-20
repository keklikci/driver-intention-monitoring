"""Rule-based driver intention monitoring implementation."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .features import add_steering_velocity
from .schema import SignalColumns
from .segmentation import contiguous_bounds


@dataclass(frozen=True)
class MonitorThresholds:
    """Speed-dependent thresholds for the DIM prototype."""

    speeds_mps: tuple[float, ...]
    steering_moment_nm: tuple[float, ...]
    acceleration_mps2: tuple[float, ...]
    deceleration_mps2: tuple[float, ...]
    steering_velocity_radps: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.speeds_mps:
            raise ValueError("speed lookup must not be empty")
        if tuple(sorted(self.speeds_mps)) != self.speeds_mps:
            raise ValueError("speed lookup must be sorted")
        values = (
            self.steering_moment_nm,
            self.acceleration_mps2,
            self.deceleration_mps2,
            self.steering_velocity_radps,
        )
        if any(len(value) != len(self.speeds_mps) for value in values):
            raise ValueError("threshold lookup lengths must match the speed lookup")

    def lookup(self, values: tuple[float, ...], speed_mps: float) -> float:
        """Interpolate a threshold and clamp outside the lookup range."""
        return float(np.interp(speed_mps, self.speeds_mps, values))


class DimMonitor:
    """Run the rule-based DIM prototype on one preprocessed drive."""

    def __init__(
        self,
        thresholds: MonitorThresholds,
        columns: SignalColumns | None = None,
        tolerance_samples: int = 6,
        curve_tolerance_samples: int = 16,
        smoothing_factor: float = 0.8,
    ) -> None:
        if tolerance_samples < 0 or curve_tolerance_samples < 0:
            raise ValueError("tolerances must be non-negative")
        if not 0.0 <= smoothing_factor <= 1.0:
            raise ValueError("smoothing factor must be between zero and one")
        self.columns = columns or SignalColumns()
        self.thresholds = thresholds
        self.tolerance_samples = tolerance_samples
        self.curve_tolerance_samples = curve_tolerance_samples
        self.smoothing_factor = smoothing_factor

    def run(self, drive: pd.DataFrame) -> pd.DataFrame:
        """Return one DIM decision at the start of each intervention event."""
        columns = self.columns
        required = {
            columns.timestamp,
            columns.velocity_kmph,
            columns.acceleration,
            columns.steering_moment,
            columns.steering_angle_deg,
            columns.lane_departure_warning,
            columns.geometry,
        }
        missing = required.difference(drive.columns)
        if missing:
            raise KeyError(f"missing required columns: {sorted(missing)}")

        result = add_steering_velocity(drive, columns)
        result = result.reset_index(drop=True)
        result[columns.steering_moment] = self._smooth(result[columns.steering_moment])
        result[columns.steering_angle_velocity] = self._smooth(
            result[columns.steering_angle_velocity]
        )
        candidates = result.apply(self._is_suppression_candidate, axis=1)
        result[columns.output] = 0

        for start, _end in contiguous_bounds(result[columns.lane_departure_warning]):
            geometry = result.at[start, columns.geometry]
            tolerance = (
                self.curve_tolerance_samples
                if geometry == "curve"
                else self.tolerance_samples
            )
            lower = max(0, start - tolerance)
            if candidates.iloc[lower : start + 1].any():
                result.at[start, columns.output] = 1

        return result

    def _smooth(self, signal: pd.Series) -> pd.Series:
        """Apply the recursive signal smoother from the prototype."""
        return signal.ewm(alpha=self.smoothing_factor, adjust=False).mean()

    def _is_suppression_candidate(self, row: pd.Series) -> bool:
        """Evaluate the pointwise rule-based suppression condition."""
        columns = self.columns
        speed = row[columns.velocity_kmph] / 3.6
        acceleration = row[columns.acceleration]
        acceleration_thresholds = (
            self.thresholds.deceleration_mps2
            if acceleration < 0
            else self.thresholds.acceleration_mps2
        )
        acceleration_ok = abs(acceleration) < self.thresholds.lookup(
            acceleration_thresholds, speed
        )
        if row[columns.geometry] == "curve":
            geometry_ok = abs(row[columns.steering_moment]) < self.thresholds.lookup(
                self.thresholds.steering_moment_nm, speed
            )
        else:
            geometry_ok = abs(
                row[columns.steering_angle_velocity]
            ) < self.thresholds.lookup(self.thresholds.steering_velocity_radps, speed)
        return bool(acceleration_ok and geometry_ok)
