"""Simple linear support vector machine."""

import numpy as np

from minilearn.metrics import accuracy_score


class LinearSVM:
    def __init__(
        self,
        learning_rate=0.001,
        max_iter=1000,
        reg_strength=0.01,
        fit_intercept=True,
        random_state=None,
    ):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.reg_strength = reg_strength
        self.fit_intercept = fit_intercept
        self.random_state = random_state

        self.classes_ = None
        self.weights_ = None
        self.loss_history_ = []

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if len(X) != len(y):
            raise ValueError("X and y have different lengths")

        Xb = self._add_intercept(X)
        self.classes_ = np.unique(y)
        n_samples, n_features = Xb.shape
        n_classes = len(self.classes_)

        rng = np.random.default_rng(self.random_state)
        self.weights_ = rng.normal(0.0, 0.01, size=(n_features, n_classes))

        for _ in range(self.max_iter):
            scores = Xb @ self.weights_
            Y = np.where(y[:, None] == self.classes_[None, :], 1.0, -1.0)
            margins = 1.0 - Y * scores
            active = margins > 0

            grad = np.zeros_like(self.weights_)
            for class_i in range(n_classes):
                if active[:, class_i].any():
                    grad[:, class_i] = (
                        -(Xb[active[:, class_i]].T @ Y[active[:, class_i], class_i])
                        / n_samples
                    )

            reg = self.weights_.copy()
            if self.fit_intercept:
                reg[0, :] = 0.0
            grad += self.reg_strength * reg

            self.weights_ -= self.learning_rate * grad
            self.loss_history_.append(self._loss(Xb, Y))

        return self

    def decision_function(self, X):
        if self.weights_ is None:
            raise ValueError("LinearSVM has not been fit yet")
        X = np.asarray(X, dtype=float)
        return self._add_intercept(X) @ self.weights_

    def predict(self, X):
        scores = self.decision_function(X)
        return self.classes_[np.argmax(scores, axis=1)]

    def predict_proba(self, X):
        scores = self.decision_function(X)
        scores = scores - scores.max(axis=1, keepdims=True)
        exp_scores = np.exp(scores)
        return exp_scores / exp_scores.sum(axis=1, keepdims=True)

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def _add_intercept(self, X):
        if not self.fit_intercept:
            return X
        return np.column_stack([np.ones(X.shape[0]), X])

    def _loss(self, X, Y):
        scores = X @ self.weights_
        margins = np.maximum(0.0, 1.0 - Y * scores)
        weights = self.weights_[1:, :] if self.fit_intercept else self.weights_
        return float(margins.mean() + 0.5 * self.reg_strength * np.sum(weights * weights))
