"""Tiny PCA transformer."""

import numpy as np


class PCA:
    def __init__(self, n_components=None):
        self.n_components = n_components
        self.mean_ = None
        self.components_ = None
        self.explained_variance_ = None
        self.explained_variance_ratio_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")

        n_samples, n_features = X.shape
        n_components = self.n_components or min(n_samples, n_features)
        if not 1 <= n_components <= min(n_samples, n_features):
            raise ValueError("n_components is out of range")

        self.mean_ = X.mean(axis=0)
        Xc = X - self.mean_
        _, s, vt = np.linalg.svd(Xc, full_matrices=False)

        var = (s ** 2) / max(n_samples - 1, 1)
        self.components_ = vt[:n_components]
        self.explained_variance_ = var[:n_components]
        total = var.sum()
        self.explained_variance_ratio_ = (
            self.explained_variance_ / total if total > 0 else np.zeros(n_components)
        )
        return self

    def transform(self, X):
        if self.components_ is None:
            raise ValueError("PCA has not been fit yet")
        X = np.asarray(X, dtype=float)
        return (X - self.mean_) @ self.components_.T

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, X):
        if self.components_ is None:
            raise ValueError("PCA has not been fit yet")
        X = np.asarray(X, dtype=float)
        return X @ self.components_ + self.mean_
