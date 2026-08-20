import pandas as pd

from driver_intention_monitoring.segmentation import contiguous_bounds, event_windows


def test_contiguous_bounds_finds_each_event() -> None:
    result = contiguous_bounds(pd.Series([0, 1, 1, 0, 1, 0]))

    assert result == [(1, 2), (4, 4)]


def test_event_windows_adds_leading_context() -> None:
    drive = pd.DataFrame({"warning": [0, 0, 1, 1, 0, 1]})

    windows = event_windows(drive, "warning", context=1)

    assert [window["warning"].tolist() for window in windows] == [[0, 1, 1], [0, 1]]
