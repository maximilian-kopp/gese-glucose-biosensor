"""
ML Calibration Pipeline for GeSe-Based Glucose Biosensor
=========================================================
Supervised regression model for predicting glucose concentration
from optical polarimetric signals.

Author: Maximilian Kopp
"""

import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error


def extract_features(signal: np.ndarray, sampling_rate: float) -> np.ndarray:
    """Extract features from raw polarimetric signal.

    Parameters
    ----------
    signal : np.ndarray
        Raw photodetector signal array (N_samples x N_channels).
    sampling_rate : float
        Acquisition sampling rate in Hz.

    Returns
    -------
    np.ndarray
        Feature vector for ML calibration.
    """
    features = []
    for ch in range(signal.shape[1]):
        ch_signal = signal[:, ch]
        features.extend([
            np.mean(ch_signal),
            np.std(ch_signal),
            np.max(ch_signal) - np.min(ch_signal),
            np.median(ch_signal),
            _spectral_centroid(ch_signal, sampling_rate),
        ])
    return np.array(features)


def _spectral_centroid(signal: np.ndarray, fs: float) -> float:
    """Compute spectral centroid of a signal."""
    fft_vals = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal), d=1.0 / fs)
    return np.sum(freqs * fft_vals) / (np.sum(fft_vals) + 1e-12)


def cross_validate(X: np.ndarray, y: np.ndarray, model, n_splits: int = 5):
    """K-fold cross-validation for glucose calibration model.

    Parameters
    ----------
    X : np.ndarray
        Feature matrix (N_samples x N_features).
    y : np.ndarray
        Reference glucose concentrations (mg/dL).
    model : sklearn estimator
        Regression model with fit/predict interface.
    n_splits : int
        Number of CV folds.

    Returns
    -------
    dict
        Cross-validation results with R², MAE per fold and overall.
    """
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    scaler = StandardScaler()

    r2_scores = []
    mae_scores = []

    for train_idx, test_idx in kf.split(X):
        X_train = scaler.fit_transform(X[train_idx])
        X_test = scaler.transform(X[test_idx])
        y_train, y_test = y[train_idx], y[test_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2_scores.append(r2_score(y_test, y_pred))
        mae_scores.append(mean_absolute_error(y_test, y_pred))

    return {
        "r2_mean": np.mean(r2_scores),
        "r2_std": np.std(r2_scores),
        "mae_mean": np.mean(mae_scores),
        "mae_std": np.std(mae_scores),
        "r2_folds": r2_scores,
        "mae_folds": mae_scores,
    }
