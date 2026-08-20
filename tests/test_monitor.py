import pandas as pd
import pytest

from driver_intention_monitoring import DimMonitor, MonitorThresholds, SignalColumns


def synthetic_thresholds() -> MonitorThresholds:
    """Return a non-calibrated configuration for tests."""
    return MonitorThresholds(
        speeds_mps=(5.0, 10.0),
        steering_moment_nm=(0.5, 0.4),
        acceleration_mps2=(0.3, 0.2),
        deceleration_mps2=(0.4, 0.3),
        steering_velocity_radps=(0.6, 0.5),
    )


def test_monitor_marks_only_the_start_of_a_suppressed_event() -> None:
    columns = SignalColumns()
    drive = pd.DataFrame(
        {
            columns.timestamp: [0.0, 0.1, 0.2, 0.3, 0.4],
            columns.velocity_kmph: [72.0] * 5,
            columns.acceleration: [0.1] * 5,
            columns.steering_moment: [0.1] * 5,
            columns.steering_angle_deg: [0.0] * 5,
            columns.lane_departure_warning: [0, 0, 1, 1, 0],
            columns.geometry: ["straight"] * 5,
        }
    )

    result = DimMonitor(synthetic_thresholds(), columns, tolerance_samples=2).run(drive)

    assert result[columns.output].tolist() == [0, 0, 1, 0, 0]


def test_monitor_does_not_mark_an_event_when_input_is_large() -> None:
    columns = SignalColumns()
    drive = pd.DataFrame(
        {
            columns.timestamp: [0.0, 0.1, 0.2],
            columns.velocity_kmph: [72.0] * 3,
            columns.acceleration: [2.0] * 3,
            columns.steering_moment: [0.1] * 3,
            columns.steering_angle_deg: [0.0] * 3,
            columns.lane_departure_warning: [0, 1, 1],
            columns.geometry: ["curve"] * 3,
        }
    )

    result = DimMonitor(synthetic_thresholds(), columns).run(drive)

    assert result[columns.output].sum() == 0


def test_monitor_requires_caller_supplied_thresholds() -> None:
    with pytest.raises(TypeError):
        DimMonitor()
