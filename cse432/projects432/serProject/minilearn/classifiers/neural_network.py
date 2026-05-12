"""Small dense neural network classifier."""

import numpy as np

from minilearn.metrics import accuracy_score


class MLPClassifier:
    """One-hidden-layer neural network for multiclass classification."""

    def __init__(
        self,
        hidden_units=32,
        learning_rate=0.01,
        max_iter=200,
        batch_size=32,
        reg_strength=0.0,
        validation_split=0.0,
        shuffle=True,
        tol=0.0,
        random_state=None,
    ):
        self.hidden_units = hidden_units
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.reg_strength = reg_strength
        self.validation_split = validation_split
        self.shuffle = shuffle
        self.tol = tol
        self.random_state = random_state

        self.classes_ = None
        self.W1_ = None
        self.b1_ = None
        self.W2_ = None
        self.b2_ = None
        self.loss_history_ = []
        self.val_loss_history_ = []

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self._validate_fit_inputs(X, y)

        self.classes_, y_idx = np.unique(y, return_inverse=True)
        X_fit, y_fit_idx, X_val, y_val_idx = self._validation_split(X, y_idx)
        n_samples, n_features = X_fit.shape
        n_classes = len(self.classes_)

        rng = np.random.default_rng(self.random_state)
        self._init_weights(rng, n_features, n_classes)
        self.loss_history_ = []
        self.val_loss_history_ = []

        Y_fit = self._one_hot(y_fit_idx, n_classes)
        Y_val = self._one_hot(y_val_idx, n_classes) if X_val is not None else None
        last_loss = None

        for _ in range(self.max_iter):
            indices = np.arange(n_samples)
            if self.shuffle:
                rng.shuffle(indices)

            for start in range(0, n_samples, self.batch_size):
                batch_idx = indices[start : start + self.batch_size]
                self._update_batch(X_fit[batch_idx], Y_fit[batch_idx])

            loss = self._loss(X_fit, Y_fit)
            self.loss_history_.append(loss)
            if X_val is not None:
                self.val_loss_history_.append(self._loss(X_val, Y_val))

            if self.tol and last_loss is not None and abs(last_loss - loss) < self.tol:
                break
            last_loss = loss

        return self

    def predict_proba(self, X):
        if self.W1_ is None:
            raise ValueError("MLPClassifier has not been fit yet")
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        return self._forward(X)[2]

    def predict(self, X):
        probs = self.predict_proba(X)
        return self.classes_[np.argmax(probs, axis=1)]

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def architecture_summary(self):
        if self.W1_ is None:
            return {
                "input_features": None,
                "hidden_units": self.hidden_units,
                "output_classes": None,
                "hidden_activation": "ReLU",
                "output_activation": "softmax",
            }
        return {
            "input_features": self.W1_.shape[0],
            "hidden_units": self.W1_.shape[1],
            "output_classes": self.W2_.shape[1],
            "hidden_activation": "ReLU",
            "output_activation": "softmax",
        }

    def _validate_fit_inputs(self, X, y):
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if len(X) != len(y):
            raise ValueError("X and y have different lengths")
        if self.hidden_units < 1:
            raise ValueError("hidden_units must be at least 1")
        if self.max_iter < 1:
            raise ValueError("max_iter must be at least 1")
        if self.batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        if not 0 <= self.validation_split < 1:
            raise ValueError("validation_split must be in [0, 1)")

    def _validation_split(self, X, y_idx):
        if self.validation_split == 0:
            return X, y_idx, None, None

        rng = np.random.default_rng(self.random_state)
        train_parts = []
        val_parts = []
        for class_idx in np.unique(y_idx):
            class_rows = np.flatnonzero(y_idx == class_idx)
            rng.shuffle(class_rows)
            n_val = int(round(len(class_rows) * self.validation_split))
            n_val = min(max(1, n_val), len(class_rows) - 1)
            val_parts.append(class_rows[:n_val])
            train_parts.append(class_rows[n_val:])

        train_idx = np.concatenate(train_parts)
        val_idx = np.concatenate(val_parts)
        rng.shuffle(train_idx)
        rng.shuffle(val_idx)
        return X[train_idx], y_idx[train_idx], X[val_idx], y_idx[val_idx]

    def _init_weights(self, rng, n_features, n_classes):
        w1_scale = np.sqrt(2.0 / n_features)
        w2_scale = np.sqrt(2.0 / self.hidden_units)
        self.W1_ = rng.normal(0.0, w1_scale, size=(n_features, self.hidden_units))
        self.b1_ = np.zeros(self.hidden_units)
        self.W2_ = rng.normal(0.0, w2_scale, size=(self.hidden_units, n_classes))
        self.b2_ = np.zeros(n_classes)

    def _update_batch(self, X, Y):
        Z1, A1, probs = self._forward(X)
        n = X.shape[0]

        d_scores = (probs - Y) / n
        dW2 = A1.T @ d_scores + self.reg_strength * self.W2_
        db2 = d_scores.sum(axis=0)

        d_hidden = d_scores @ self.W2_.T
        dZ1 = d_hidden * (Z1 > 0)
        dW1 = X.T @ dZ1 + self.reg_strength * self.W1_
        db1 = dZ1.sum(axis=0)

        self.W1_ -= self.learning_rate * dW1
        self.b1_ -= self.learning_rate * db1
        self.W2_ -= self.learning_rate * dW2
        self.b2_ -= self.learning_rate * db2

    def _forward(self, X):
        Z1 = X @ self.W1_ + self.b1_
        A1 = np.maximum(0.0, Z1)
        scores = A1 @ self.W2_ + self.b2_
        probs = self._softmax(scores)
        return Z1, A1, probs

    def _loss(self, X, Y):
        probs = self._forward(X)[2]
        eps = 1e-12
        data_loss = -np.mean(np.sum(Y * np.log(probs + eps), axis=1))
        reg_loss = 0.5 * self.reg_strength * (
            np.sum(self.W1_ * self.W1_) + np.sum(self.W2_ * self.W2_)
        )
        return float(data_loss + reg_loss)

    @staticmethod
    def _one_hot(y_idx, n_classes):
        Y = np.zeros((len(y_idx), n_classes))
        Y[np.arange(len(y_idx)), y_idx] = 1.0
        return Y

    @staticmethod
    def _softmax(scores):
        scores = scores - scores.max(axis=1, keepdims=True)
        exp_scores = np.exp(scores)
        return exp_scores / exp_scores.sum(axis=1, keepdims=True)
