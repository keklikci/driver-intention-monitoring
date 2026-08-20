import numpy as np
import pytest

from driver_intention_monitoring.transforms import (
    continuous_wavelet_transform,
    gaussian_spectrogram,
    smoothed_fft,
)


def test_continuous_wavelet_transform_returns_scale_by_sample_matrix() -> None:
    result = continuous_wavelet_transform(np.array([0.0, 1.0, 0.0, -1.0]))

    assert result.shape == (4, 4)


def test_gaussian_spectrogram_returns_square_matrix() -> None:
    result = gaussian_spectrogram(np.array([0.0, 1.0, 0.0]), sigma=1.0)

    assert result.shape == (3, 3)
    assert (result >= 0).all()


def test_smoothed_fft_rejects_multidimensional_signal() -> None:
    with pytest.raises(ValueError, match="one-dimensional"):
        smoothed_fft(np.zeros((2, 2)), sigma=1.0)
