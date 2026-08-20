"""Signal transforms used in thesis experiments."""

import numpy as np
import pywt
from scipy.ndimage import gaussian_filter1d


def continuous_wavelet_transform(
    signal: np.ndarray,
    scales: np.ndarray | None = None,
    wavelet: str = "mexh",
) -> np.ndarray:
    """Compute a continuous wavelet transform for a one-dimensional signal."""
    array = np.asarray(signal, dtype=float)
    if array.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    scales = np.arange(1, array.size + 1) if scales is None else np.asarray(scales)
    coefficients, _ = pywt.cwt(array, scales, wavelet)
    return coefficients


def gaussian_spectrogram(signal: np.ndarray, sigma: float) -> np.ndarray:
    """Compute a gaussian-windowed Fourier magnitude matrix."""
    array = np.asarray(signal, dtype=float)
    if array.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    timestamps = np.arange(array.size)
    output = np.empty((array.size, array.size))
    for index, timestamp in enumerate(timestamps):
        kernel = np.exp(-((timestamps - timestamp) ** 2) / (2 * sigma**2))
        output[:, index] = np.abs(np.fft.fftshift(np.fft.fft(array * kernel)))
    return output


def smoothed_fft(signal: np.ndarray, sigma: float) -> np.ndarray:
    """Compute the Fourier magnitude after gaussian smoothing."""
    array = np.asarray(signal, dtype=float)
    if array.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    return np.abs(np.fft.fftshift(np.fft.fft(gaussian_filter1d(array, sigma=sigma))))
