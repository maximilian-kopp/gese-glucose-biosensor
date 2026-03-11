"""
Signal Processing Utilities for Polarimetric Biosensor
======================================================
Preprocessing, filtering, and analysis of raw optical signals
from GeSe photodetector arrays.

Author: Maximilian Kopp
"""

import numpy as np
from scipy import signal as sig


def bandpass_filter(
    data: np.ndarray,
    low_freq: float,
    high_freq: float,
    sampling_rate: float,
    order: int = 4,
) -> np.ndarray:
    """Apply Butterworth bandpass filter to signal.

    Parameters
    ----------
    data : np.ndarray
        Input signal (1D or 2D with channels as columns).
    low_freq : float
        Lower cutoff frequency in Hz.
    high_freq : float
        Upper cutoff frequency in Hz.
    sampling_rate : float
        Sampling rate in Hz.
    order : int
        Filter order.

    Returns
    -------
    np.ndarray
        Filtered signal.
    """
    nyq = 0.5 * sampling_rate
    b, a = sig.butter(order, [low_freq / nyq, high_freq / nyq], btype="band")
    return sig.filtfilt(b, a, data, axis=0)


def compute_rotation_angle(
    intensity_0: np.ndarray,
    intensity_90: np.ndarray,
) -> np.ndarray:
    """Compute optical rotation angle from orthogonal polarization channels.

    Uses the ratio of two orthogonal polarization intensities to
    determine the rotation induced by optically active glucose molecules.

    Parameters
    ----------
    intensity_0 : np.ndarray
        Signal from 0-degree polarization channel.
    intensity_90 : np.ndarray
        Signal from 90-degree polarization channel.

    Returns
    -------
    np.ndarray
        Estimated rotation angle in degrees.
    """
    ratio = np.clip(intensity_0 / (intensity_90 + 1e-12), 1e-6, 1e6)
    return np.degrees(0.5 * np.arctan(ratio))


def remove_baseline_drift(data: np.ndarray, window_size: int = 101) -> np.ndarray:
    """Remove baseline drift using moving median subtraction.

    Parameters
    ----------
    data : np.ndarray
        Input signal.
    window_size : int
        Window size for median filter (must be odd).

    Returns
    -------
    np.ndarray
        Baseline-corrected signal.
    """
    if window_size % 2 == 0:
        window_size += 1
    baseline = sig.medfilt(data, kernel_size=window_size)
    return data - baseline


def snr_estimate(data: np.ndarray, noise_segment: np.ndarray) -> float:
    """Estimate signal-to-noise ratio in dB.

    Parameters
    ----------
    data : np.ndarray
        Signal of interest.
    noise_segment : np.ndarray
        Segment containing only noise.

    Returns
    -------
    float
        SNR in dB.
    """
    signal_power = np.mean(data**2)
    noise_power = np.mean(noise_segment**2)
    return 10 * np.log10(signal_power / (noise_power + 1e-12))
