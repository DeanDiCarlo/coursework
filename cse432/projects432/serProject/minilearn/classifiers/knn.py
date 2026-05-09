"""Brute force k-nearest neighbors."""

import numpy as np

from minilearn.metrics import accuracy_score


class KNearestNeighbors:
    def __init__(self, k=5, weights="uniform", metric="euclidean"):
        self.k = k
        self.weights = weights
        self.metric = metric
        self.X_train_ = None
        self.y_train_ = None
        self.classes_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if len(X) != len(y):
            raise ValueError("X and y have different lengths")
        if self.k < 1:
            raise ValueError("k must be at least 1")
        if self.weights not in ("uniform", "distance"):
            raise ValueError("weights must be 'uniform' or 'distance'")
        if self.metric not in ("euclidean", "manhattan"):
            raise ValueError("metric must be 'euclidean' or 'manhattan'")

        self.X_train_ = X
        self.y_train_ = y
        self.classes_ = np.unique(y)
        return self

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

    def predict_proba(self, X):
        if self.X_train_ is None:
            raise ValueError("KNearestNeighbors has not been fit yet")
        X = np.asarray(X, dtype=float)
        k = min(self.k, len(self.X_train_))
        out = np.zeros((len(X), len(self.classes_)))
        class_to_i = {cls: i for i, cls in enumerate(self.classes_)}

        for row_i, row in enumerate(X):
            d = self._distances(row)
            nn = np.argpartition(d, k - 1)[:k]
            nn = nn[np.argsort(d[nn])]
            labels = self.y_train_[nn]

            if self.weights == "distance":
                zero = d[nn] == 0
                if zero.any():
                    labels = labels[zero]
                    vote_weight = np.ones(len(labels))
                else:
                    vote_weight = 1.0 / (d[nn] + 1e-12)
            else:
                vote_weight = np.ones(len(labels))

            for lbl, wt in zip(labels, vote_weight):
                out[row_i, class_to_i[lbl]] += wt

        row_sums = out.sum(axis=1, keepdims=True)
        return np.where(row_sums > 0, out / row_sums, 0.0)

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def _distances(self, row):
        diff = self.X_train_ - row
        if self.metric == "manhattan":
            return np.abs(diff).sum(axis=1)
        return np.sqrt((diff * diff).sum(axis=1))


KNN = KNearestNeighbors
