"""Feature scaling."""

import numpy as np


class StandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        self.scale_ = np.where(self.scale_ == 0, 1.0, self.scale_)
        return self

    def transform(self, X):
        if self.mean_ is None or self.scale_ is None:
            raise ValueError("StandardScaler has not been fit yet")
        X = np.asarray(X, dtype=float)
        return (X - self.mean_) / self.scale_

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, X):
        if self.mean_ is None or self.scale_ is None:
            raise ValueError("StandardScaler has not been fit yet")
        X = np.asarray(X, dtype=float)
        return X * self.scale_ + self.mean_
