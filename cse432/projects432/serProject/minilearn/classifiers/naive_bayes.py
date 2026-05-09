"""Gaussian Naive Bayes."""

import numpy as np

from minilearn.metrics import accuracy_score


class GaussianNaiveBayes:
    def __init__(self, var_smoothing=1e-9):
        self.var_smoothing = var_smoothing
        self.classes_ = None
        self.theta_ = None
        self.var_ = None
        self.class_prior_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if len(X) != len(y):
            raise ValueError("X and y have different lengths")

        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        n_features = X.shape[1]

        self.theta_ = np.zeros((n_classes, n_features))
        self.var_ = np.zeros((n_classes, n_features))
        self.class_prior_ = np.zeros(n_classes)

        eps = self.var_smoothing * np.var(X, axis=0).max()
        if eps == 0:
            eps = self.var_smoothing

        for i, cls in enumerate(self.classes_):
            Xc = X[y == cls]
            self.theta_[i] = Xc.mean(axis=0)
            self.var_[i] = Xc.var(axis=0) + eps
            self.class_prior_[i] = len(Xc) / len(X)

        return self

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_log_proba(X), axis=1)]

    def predict_log_proba(self, X):
        if self.classes_ is None:
            raise ValueError("GaussianNaiveBayes has not been fit yet")
        X = np.asarray(X, dtype=float)

        logs = []
        for i in range(len(self.classes_)):
            prior = np.log(self.class_prior_[i])
            var = self.var_[i]
            mean = self.theta_[i]
            density = -0.5 * np.sum(np.log(2.0 * np.pi * var))
            density -= 0.5 * np.sum(((X - mean) ** 2) / var, axis=1)
            logs.append(prior + density)

        raw = np.column_stack(logs)
        raw -= raw.max(axis=1, keepdims=True)
        denom = np.log(np.exp(raw).sum(axis=1, keepdims=True))
        return raw - denom

    def predict_proba(self, X):
        return np.exp(self.predict_log_proba(X))

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))


NaiveBayes = GaussianNaiveBayes
