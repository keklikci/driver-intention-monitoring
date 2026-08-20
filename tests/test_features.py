import pandas as pd
import pytest

from driver_intention_monitoring import SignalColumns
from driver_intention_monitoring.features import (
    add_steering_velocity,
    add_vehicle_features,
    rolling_statistics,
)


def test_add_vehicle_features_converts_steering_angle() -> None:
    columns = SignalColumns()
    drive = pd.DataFrame(
        {
            columns.lane_y_left: [-2.0],
            columns.lane_y_right: [3.0],
            columns.steering_angle_deg: [180.0],
        }
    )

    result = add_vehicle_features(drive, columns)

    assert result["lateral_deviation_m"].tolist() == [1.0]
    assert result["driver_steering_angle_rad"].tolist() == [pytest.approx(3.14159)]


def test_add_steering_velocity_requires_increasing_timestamps() -> None:
    columns = SignalColumns()
    drive = pd.DataFrame(
        {columns.timestamp: [0.0, 0.0], columns.steering_angle_deg: [0.0, 1.0]}
    )

    with pytest.raises(ValueError, match="strictly increasing"):
        add_steering_velocity(drive, columns)


def test_rolling_statistics_has_no_initial_missing_values() -> None:
    result = rolling_statistics(pd.Series([1.0, 2.0, 3.0]), window=2)

    assert not result.isna().any().any()
    assert result["mean"].tolist() == [1.0, 1.5, 2.5]
