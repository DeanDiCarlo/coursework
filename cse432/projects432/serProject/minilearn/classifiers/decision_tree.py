"""CART decision tree classifier."""

from dataclasses import dataclass

import numpy as np

from minilearn.metrics import accuracy_score


@dataclass
class _Node:
    prediction: object
    proba: np.ndarray
    impurity: float
    samples: int
    feature_index: int = None
    threshold: float = None
    left: object = None
    right: object = None

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


class DecisionTreeClassifier:
    def __init__(
        self,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        criterion="gini",
    ):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion

        self.classes_ = None
        self.root_ = None
        self.n_features_in_ = None
        self.feature_importances_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if len(X) != len(y):
            raise ValueError("X and y have different lengths")
        if self.criterion not in ("gini", "entropy"):
            raise ValueError("criterion must be 'gini' or 'entropy'")
        if self.min_samples_split < 2:
            raise ValueError("min_samples_split must be at least 2")
        if self.min_samples_leaf < 1:
            raise ValueError("min_samples_leaf must be at least 1")

        self.classes_, y_idx = np.unique(y, return_inverse=True)
        self.n_features_in_ = X.shape[1]
        self.feature_importances_ = np.zeros(self.n_features_in_, dtype=float)
        self.root_ = self._grow(X, y_idx, depth=0)

        total = self.feature_importances_.sum()
        if total > 0:
            self.feature_importances_ = self.feature_importances_ / total
        return self

    def predict(self, X):
        if self.root_ is None:
            raise ValueError("DecisionTreeClassifier has not been fit yet")
        X = np.asarray(X, dtype=float)
        return np.array([self._predict_one(row).prediction for row in X])

    def predict_proba(self, X):
        if self.root_ is None:
            raise ValueError("DecisionTreeClassifier has not been fit yet")
        X = np.asarray(X, dtype=float)
        return np.vstack([self._predict_one(row).proba for row in X])

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def export_tree(self, feature_names=None, class_names=None, max_depth=3):
        if self.root_ is None:
            raise ValueError("DecisionTreeClassifier has not been fit yet")
        if feature_names is None:
            feature_names = [f"x{i}" for i in range(self.n_features_in_)]
        if class_names is None:
            class_names = {cls: str(cls) for cls in self.classes_}
        elif not isinstance(class_names, dict):
            class_names = {cls: name for cls, name in zip(self.classes_, class_names)}

        lines = []
        self._tree_lines(self.root_, feature_names, class_names, max_depth, 0, lines)
        return "\n".join(lines)

    def _grow(self, X, y, depth):
        counts = np.bincount(y, minlength=len(self.classes_))
        proba = counts / counts.sum()
        impurity = self._impurity(counts)
        prediction = self.classes_[np.argmax(counts)]
        node = _Node(prediction, proba, impurity, len(y))

        if self._should_stop(y, depth):
            return node

        split = self._best_split(X, y, impurity)
        if split is None:
            return node

        feature, threshold, gain, left_mask = split
        node.feature_index = feature
        node.threshold = threshold
        self.feature_importances_[feature] += gain * len(y)
        node.left = self._grow(X[left_mask], y[left_mask], depth + 1)
        node.right = self._grow(X[~left_mask], y[~left_mask], depth + 1)
        return node

    def _should_stop(self, y, depth):
        if len(np.unique(y)) == 1:
            return True
        if self.max_depth is not None and depth >= self.max_depth:
            return True
        if len(y) < self.min_samples_split:
            return True
        if len(y) < 2 * self.min_samples_leaf:
            return True
        return False

    def _best_split(self, X, y, parent_impurity):
        n_samples, n_features = X.shape
        best_gain = 0.0
        best_feature = None
        best_threshold = None
        best_left_mask = None
        n_classes = len(self.classes_)

        for feature in range(n_features):
            order = np.argsort(X[:, feature], kind="mergesort")
            values = X[order, feature]
            labels = y[order]

            if values[0] == values[-1]:
                continue

            one_hot = np.eye(n_classes)[labels]
            left_counts = np.cumsum(one_hot, axis=0)[:-1]
            total_counts = left_counts[-1] + one_hot[-1]
            right_counts = total_counts - left_counts

            left_n = np.arange(1, n_samples)
            right_n = n_samples - left_n
            valid = (
                (left_n >= self.min_samples_leaf)
                & (right_n >= self.min_samples_leaf)
                & (values[:-1] != values[1:])
            )
            if not valid.any():
                continue

            left_imp = self._impurity_many(left_counts)
            right_imp = self._impurity_many(right_counts)
            child_imp = (left_n * left_imp + right_n * right_imp) / n_samples
            gains = parent_impurity - child_imp
            gains = np.where(valid, gains, -np.inf)

            idx = int(np.argmax(gains))
            gain = float(gains[idx])
            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_threshold = (values[idx] + values[idx + 1]) / 2.0

        if best_feature is None:
            return None

        best_left_mask = X[:, best_feature] <= best_threshold
        return best_feature, best_threshold, best_gain, best_left_mask

    def _impurity(self, counts):
        total = counts.sum()
        if total <= 0:
            return 0.0
        p = counts[counts > 0] / total
        if self.criterion == "entropy":
            return float(-np.sum(p * np.log2(p)))
        return float(1.0 - np.sum(p * p))

    def _impurity_many(self, counts):
        totals = counts.sum(axis=1, keepdims=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            p = np.where(totals > 0, counts / totals, 0.0)
        if self.criterion == "entropy":
            logs = np.zeros_like(p)
            positive = p > 0
            logs[positive] = np.log2(p[positive])
            return -np.sum(p * logs, axis=1)
        return 1.0 - np.sum(p * p, axis=1)

    def _predict_one(self, row):
        node = self.root_
        while not node.is_leaf:
            if row[node.feature_index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node

    def _tree_lines(self, node, feature_names, class_names, max_depth, depth, lines):
        indent = "  " * depth
        pred = class_names.get(node.prediction, str(node.prediction))
        if node.is_leaf or depth >= max_depth:
            lines.append(
                f"{indent}leaf: class={pred}, samples={node.samples}, impurity={node.impurity:.3f}"
            )
            return

        name = feature_names[node.feature_index]
        lines.append(
            f"{indent}if {name} <= {node.threshold:.4f}: "
            f"samples={node.samples}, impurity={node.impurity:.3f}"
        )
        self._tree_lines(node.left, feature_names, class_names, max_depth, depth + 1, lines)
        lines.append(f"{indent}else:")
        self._tree_lines(node.right, feature_names, class_names, max_depth, depth + 1, lines)


DecisionTree = DecisionTreeClassifier
