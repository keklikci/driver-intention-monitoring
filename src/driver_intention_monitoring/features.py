"""Feature engineering helpers used by DIM experiments."""

import numpy as np
import pandas as pd

from .schema import SignalColumns


def add_vehicle_features(drive: pd.DataFrame, columns: SignalColumns) -> pd.DataFrame:
    """Add lateral deviation, relative yaw, and steering features."""
    required = [
        columns.lane_y_left,
        columns.lane_y_right,
        columns.steering_angle_deg,
    ]
    missing = set(required).difference(drive.columns)
    if missing:
        raise KeyError(f"missing required columns: {sorted(missing)}")

    result = drive.copy()
    result["lateral_deviation_m"] = (
        result[columns.lane_y_right] - result[columns.lane_y_left].abs()
    )
    result["driver_steering_angle_rad"] = np.deg2rad(result[columns.steering_angle_deg])
    return result


def add_steering_velocity(drive: pd.DataFrame, columns: SignalColumns) -> pd.DataFrame:
    """Add steering angle velocity in radians per second."""
    required = [columns.timestamp, columns.steering_angle_deg]
    missing = set(required).difference(drive.columns)
    if missing:
        raise KeyError(f"missing required columns: {sorted(missing)}")

    result = drive.copy()
    elapsed = result[columns.timestamp].diff()
    if (elapsed.iloc[1:] <= 0).any():
        raise ValueError("timestamps must be strictly increasing")
    velocity = np.deg2rad(result[columns.steering_angle_deg]).diff() / elapsed
    result[columns.steering_angle_velocity] = velocity.bfill()
    return result


def rolling_statistics(signal: pd.Series, window: int) -> pd.DataFrame:
    """Calculate descriptive rolling features for one signal."""
    if window < 1:
        raise ValueError("window must be positive")
    rolled = signal.rolling(window=window, min_periods=1)
    return pd.DataFrame(
        {
            "mean": rolled.mean(),
            "std": rolled.std().fillna(0.0),
            "median": rolled.median(),
            "kurtosis": rolled.kurt().fillna(0.0),
            "maximum": rolled.max(),
            "minimum": rolled.min(),
            "skew": rolled.skew().fillna(0.0),
        }
    )
