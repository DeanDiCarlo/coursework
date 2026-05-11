"""Tiny K-Means clustering."""

import numpy as np


class KMeans:
    def __init__(self, n_clusters=8, max_iter=100, tol=1e-4, n_init=5, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.n_init = n_init
        self.random_state = random_state

        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if not 1 <= self.n_clusters <= len(X):
            raise ValueError("n_clusters must be between 1 and n_samples")
        if self.max_iter < 1:
            raise ValueError("max_iter must be at least 1")
        if self.n_init < 1:
            raise ValueError("n_init must be at least 1")

        rng = np.random.default_rng(self.random_state)
        best = None
        for _ in range(self.n_init):
            centers, labels, inertia, n_iter = self._single_run(X, rng)
            if best is None or inertia < best[2]:
                best = (centers, labels, inertia, n_iter)

        self.cluster_centers_, self.labels_, self.inertia_, self.n_iter_ = best
        return self

    def predict(self, X):
        if self.cluster_centers_ is None:
            raise ValueError("KMeans has not been fit yet")
        X = np.asarray(X, dtype=float)
        return self._closest(X, self.cluster_centers_)

    def fit_predict(self, X):
        return self.fit(X).labels_

    def transform(self, X):
        if self.cluster_centers_ is None:
            raise ValueError("KMeans has not been fit yet")
        X = np.asarray(X, dtype=float)
        return self._distances(X, self.cluster_centers_)

    def _single_run(self, X, rng):
        centers = self._init_centers(X, rng)
        old_inertia = None

        for n_iter in range(1, self.max_iter + 1):
            labels = self._closest(X, centers)
            new_centers = centers.copy()
            for cluster in range(self.n_clusters):
                members = X[labels == cluster]
                if len(members) == 0:
                    far = np.argmax(np.min(self._distances(X, centers), axis=1))
                    new_centers[cluster] = X[far]
                else:
                    new_centers[cluster] = members.mean(axis=0)

            inertia = self._inertia(X, new_centers)
            shift = np.sqrt(((new_centers - centers) ** 2).sum(axis=1)).max()
            centers = new_centers
            if old_inertia is not None and abs(old_inertia - inertia) <= self.tol:
                break
            if shift <= self.tol:
                break
            old_inertia = inertia

        labels = self._closest(X, centers)
        inertia = self._inertia(X, centers)
        return centers, labels, inertia, n_iter

    def _init_centers(self, X, rng):
        centers = np.empty((self.n_clusters, X.shape[1]), dtype=float)
        first = rng.integers(len(X))
        centers[0] = X[first]

        closest_dist = self._distances(X, centers[:1]).ravel() ** 2
        for i in range(1, self.n_clusters):
            total = closest_dist.sum()
            if total == 0:
                idx = rng.integers(len(X))
            else:
                idx = rng.choice(len(X), p=closest_dist / total)
            centers[i] = X[idx]
            closest_dist = np.minimum(
                closest_dist, self._distances(X, centers[i : i + 1]).ravel() ** 2
            )
        return centers

    def _closest(self, X, centers):
        return np.argmin(self._distances(X, centers), axis=1)

    def _distances(self, X, centers):
        return np.sqrt(((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2))

    def _inertia(self, X, centers):
        d = self._distances(X, centers)
        return float(np.min(d * d, axis=1).sum())
