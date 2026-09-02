"""Dependency-free projections for latent-space artifacts."""

from __future__ import annotations

import numpy as np


def pca_project_2d(
    vectors: np.ndarray,
    *,
    source: str = "mean_q",
) -> tuple[np.ndarray, dict]:
    """Project vectors to two dimensions with deterministic PCA."""
    values = np.asarray(vectors, dtype=np.float32)
    if values.ndim != 2:
        raise ValueError(f"Expected a 2D vector matrix, got shape {values.shape}")
    if values.shape[0] == 0:
        raise ValueError("At least one vector is required for projection")

    centered = values.astype(np.float64) - values.mean(axis=0, keepdims=True)
    if values.shape[0] == 1:
        coordinates = np.zeros((1, 2), dtype=np.float32)
        explained_variance_ratio = [0.0, 0.0]
    else:
        _, singular_values, components = np.linalg.svd(centered, full_matrices=False)
        component_count = min(2, components.shape[0])
        coordinates = centered @ components[:component_count].T
        if component_count < 2:
            coordinates = np.pad(coordinates, ((0, 0), (0, 2 - component_count)))

        variances = singular_values ** 2
        variance_total = float(variances.sum())
        explained_variance_ratio = (
            (variances[:2] / variance_total).tolist()
            if variance_total > 0
            else [0.0, 0.0]
        )
        if len(explained_variance_ratio) < 2:
            explained_variance_ratio.extend([0.0] * (2 - len(explained_variance_ratio)))
        coordinates = coordinates.astype(np.float32)

    return coordinates, {
        "method": "pca",
        "source": source,
        "explained_variance_ratio": [
            round(float(value), 6) for value in explained_variance_ratio
        ],
    }
