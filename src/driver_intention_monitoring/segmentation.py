"""Contiguous intervention event segmentation."""

import numpy as np
import pandas as pd


def contiguous_bounds(
    series: pd.Series, value: int | float = 1
) -> list[tuple[int, int]]:
    """Return inclusive positional bounds for each matching run."""
    matching = series.to_numpy() == value
    padded = np.pad(matching, (1, 1), constant_values=False)
    changes = np.flatnonzero(padded[1:] != padded[:-1])
    return [(int(start), int(end - 1)) for start, end in changes.reshape(-1, 2)]


def event_windows(
    drive: pd.DataFrame,
    warning_column: str,
    context: int = 0,
) -> list[pd.DataFrame]:
    """Return each intervention event with optional leading context."""
    if context < 0:
        raise ValueError("context must be non-negative")
    if warning_column not in drive:
        raise KeyError(f"missing required column: {warning_column}")
    return [
        drive.iloc[max(0, start - context) : end + 1].copy()
        for start, end in contiguous_bounds(drive[warning_column])
    ]
