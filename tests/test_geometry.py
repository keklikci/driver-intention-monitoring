import pandas as pd
import pytest

from driver_intention_monitoring import (
    GeometryThresholds,
    SignalColumns,
    classify_geometry,
)


def test_geometry_threshold_lookup_uses_expected_speed_bin() -> None:
    thresholds = GeometryThresholds(
        speeds_kmph=(10.0, 20.0), curvatures_radpm=(0.03, 0.01)
    )

    assert thresholds.lookup(9.9) == 0.03
    assert thresholds.lookup(10.0) == 0.01
    assert thresholds.lookup(30.0) == 0.01


def test_classify_geometry_adds_curvature_and_labels() -> None:
    columns = SignalColumns()
    drive = pd.DataFrame(
        {
            columns.velocity_kmph: [5.0, 30.0],
            columns.curvature_left: [0.001, 0.0003],
            columns.curvature_right: [0.001, 0.0003],
        }
    )

    thresholds = GeometryThresholds(
        speeds_kmph=(10.0, 20.0), curvatures_radpm=(0.002, 0.0002)
    )

    result = classify_geometry(drive, columns, thresholds)

    assert result["curvature_abs_avg_radpm"].tolist() == [0.001, 0.0003]
    assert result[columns.geometry].tolist() == ["straight", "curve"]


def test_classify_geometry_requires_signal_columns() -> None:
    with pytest.raises(KeyError, match="missing required columns"):
        classify_geometry(
            pd.DataFrame(),
            SignalColumns(),
            GeometryThresholds(speeds_kmph=(10.0,), curvatures_radpm=(0.01,)),
        )


def test_geometry_thresholds_require_caller_supplied_values() -> None:
    with pytest.raises(TypeError):
        GeometryThresholds()
