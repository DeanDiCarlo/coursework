"""Multiclass logistic regression."""

import numpy as np

from minilearn.metrics import accuracy_score


class LogisticRegression:
    def __init__(
        self,
        learning_rate=0.1,
        max_iter=1000,
        reg_strength=0.0,
        fit_intercept=True,
        tol=1e-6,
    ):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.reg_strength = reg_strength
        self.fit_intercept = fit_intercept
        self.tol = tol

        self.classes_ = None
        self.weights_ = None
        self.loss_history_ = []

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        Xb = self._add_intercept(X)

        self.classes_, y_idx = np.unique(y, return_inverse=True)
        n_samples, n_features = Xb.shape
        n_classes = len(self.classes_)

        Y = np.zeros((n_samples, n_classes))
        Y[np.arange(n_samples), y_idx] = 1.0

        self.weights_ = np.zeros((n_features, n_classes))
        last_loss = None

        for _ in range(self.max_iter):
            probs = self._softmax(Xb @ self.weights_)
            error = probs - Y
            grad = (Xb.T @ error) / n_samples

            if self.reg_strength:
                reg = self.weights_.copy()
                if self.fit_intercept:
                    reg[0, :] = 0.0
                grad += self.reg_strength * reg

            self.weights_ -= self.learning_rate * grad
            loss = self._loss(Xb, Y)
            self.loss_history_.append(loss)

            if last_loss is not None and abs(last_loss - loss) < self.tol:
                break
            last_loss = loss

        return self

    def predict_proba(self, X):
        if self.weights_ is None:
            raise ValueError("LogisticRegression has not been fit yet")
        X = np.asarray(X, dtype=float)
        return self._softmax(self._add_intercept(X) @ self.weights_)

    def predict(self, X):
        probs = self.predict_proba(X)
        return self.classes_[np.argmax(probs, axis=1)]

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def _add_intercept(self, X):
        if not self.fit_intercept:
            return X
        return np.column_stack([np.ones(X.shape[0]), X])

    def _loss(self, X, Y):
        probs = self._softmax(X @ self.weights_)
        eps = 1e-12
        loss = -np.mean(np.sum(Y * np.log(probs + eps), axis=1))
        if self.reg_strength:
            weights = self.weights_[1:, :] if self.fit_intercept else self.weights_
            loss += 0.5 * self.reg_strength * np.sum(weights * weights)
        return float(loss)

    @staticmethod
    def _softmax(scores):
        scores = scores - scores.max(axis=1, keepdims=True)
        exp_scores = np.exp(scores)
        return exp_scores / exp_scores.sum(axis=1, keepdims=True)
