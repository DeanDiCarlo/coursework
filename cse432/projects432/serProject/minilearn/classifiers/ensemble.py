"""Small ensemble classifiers for MiniLearn."""

import numpy as np

from minilearn.classifiers.decision_tree import DecisionTreeClassifier
from minilearn.metrics import accuracy_score


class RandomForestClassifier:
    def __init__(
        self,
        n_estimators=25,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features="sqrt",
        bootstrap=True,
        max_samples=None,
        criterion="gini",
        random_state=None,
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.max_samples = max_samples
        self.criterion = criterion
        self.random_state = random_state

        self.classes_ = None
        self.estimators_ = []
        self.feature_indices_ = []
        self.bootstrap_indices_ = []
        self.n_features_in_ = None
        self.feature_importances_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if len(X) != len(y):
            raise ValueError("X and y have different lengths")
        if self.n_estimators < 1:
            raise ValueError("n_estimators must be at least 1")

        rng = np.random.default_rng(self.random_state)
        n_samples, n_features = X.shape
        n_tree_features = self._feature_count(n_features)
        sample_count = self._sample_count(n_samples)

        self.classes_ = np.unique(y)
        self.n_features_in_ = n_features
        self.estimators_ = []
        self.feature_indices_ = []
        self.bootstrap_indices_ = []
        self.feature_importances_ = np.zeros(n_features, dtype=float)

        for _ in range(self.n_estimators):
            if self.bootstrap:
                rows = rng.choice(n_samples, size=sample_count, replace=True)
            else:
                rows = rng.choice(n_samples, size=sample_count, replace=False)
            cols = rng.choice(n_features, size=n_tree_features, replace=False)

            tree = DecisionTreeClassifier(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf,
                criterion=self.criterion,
            )
            tree.fit(X[rows][:, cols], y[rows])

            self.estimators_.append(tree)
            self.feature_indices_.append(cols)
            self.bootstrap_indices_.append(rows)
            self.feature_importances_[cols] += tree.feature_importances_

        total = self.feature_importances_.sum()
        if total > 0:
            self.feature_importances_ = self.feature_importances_ / total
        return self

    def predict(self, X):
        if not self.estimators_:
            raise ValueError("RandomForestClassifier has not been fit yet")
        X = np.asarray(X, dtype=float)
        votes = np.zeros((len(X), len(self.classes_)), dtype=float)
        class_lookup = {cls: i for i, cls in enumerate(self.classes_)}

        for tree, cols in zip(self.estimators_, self.feature_indices_):
            pred = tree.predict(X[:, cols])
            for i, label in enumerate(pred):
                votes[i, class_lookup[label]] += 1
        return self.classes_[np.argmax(votes, axis=1)]

    def predict_proba(self, X):
        if not self.estimators_:
            raise ValueError("RandomForestClassifier has not been fit yet")
        X = np.asarray(X, dtype=float)
        proba = np.zeros((len(X), len(self.classes_)), dtype=float)
        class_lookup = {cls: i for i, cls in enumerate(self.classes_)}

        for tree, cols in zip(self.estimators_, self.feature_indices_):
            tree_proba = tree.predict_proba(X[:, cols])
            for j, label in enumerate(tree.classes_):
                proba[:, class_lookup[label]] += tree_proba[:, j]
        return proba / len(self.estimators_)

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def structure_summary(self, feature_names=None, max_trees=3, tree_depth=2):
        if not self.estimators_:
            raise ValueError("RandomForestClassifier has not been fit yet")
        if feature_names is None:
            feature_names = [f"x{i}" for i in range(self.n_features_in_)]

        lines = [
            "RandomForestClassifier",
            f"trees={len(self.estimators_)}, classes={list(self.classes_)}",
            f"bootstrap={self.bootstrap}, max_features={self.max_features}",
        ]
        for i, (tree, cols) in enumerate(
            zip(self.estimators_[:max_trees], self.feature_indices_[:max_trees]), start=1
        ):
            names = [feature_names[c] for c in cols[:8]]
            more = "..." if len(cols) > 8 else ""
            subset_names = [feature_names[c] for c in cols]
            lines.append(f"\ntree {i}: sampled_features={names}{more}")
            lines.append(tree.export_tree(feature_names=subset_names, max_depth=tree_depth))
        return "\n".join(lines)

    def _feature_count(self, n_features):
        if self.max_features == "sqrt":
            return max(1, int(np.sqrt(n_features)))
        if self.max_features == "log2":
            return max(1, int(np.log2(n_features)))
        if self.max_features is None:
            return n_features
        if isinstance(self.max_features, float):
            if not 0 < self.max_features <= 1:
                raise ValueError("float max_features must be in (0, 1]")
            return max(1, int(round(n_features * self.max_features)))
        if isinstance(self.max_features, int):
            if not 1 <= self.max_features <= n_features:
                raise ValueError("int max_features must be between 1 and n_features")
            return self.max_features
        raise ValueError("max_features must be 'sqrt', 'log2', None, float, or int")

    def _sample_count(self, n_samples):
        if self.max_samples is None:
            return n_samples
        if isinstance(self.max_samples, float):
            if not 0 < self.max_samples <= 1:
                raise ValueError("float max_samples must be in (0, 1]")
            return max(1, int(round(n_samples * self.max_samples)))
        if isinstance(self.max_samples, int):
            if not 1 <= self.max_samples <= n_samples:
                raise ValueError("int max_samples must be between 1 and n_samples")
            return self.max_samples
        raise ValueError("max_samples must be None, float, or int")


class AdaBoostClassifier:
    def __init__(
        self,
        n_estimators=30,
        learning_rate=1.0,
        max_depth=1,
        min_samples_leaf=1,
        criterion="gini",
        random_state=None,
    ):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.random_state = random_state

        self.classes_ = None
        self.estimators_ = []
        self.estimator_weights_ = []
        self.estimator_errors_ = []
        self.n_features_in_ = None
        self.feature_importances_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if X.ndim != 2:
            raise ValueError("X needs to be 2D")
        if len(X) != len(y):
            raise ValueError("X and y have different lengths")
        if self.n_estimators < 1:
            raise ValueError("n_estimators must be at least 1")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")

        rng = np.random.default_rng(self.random_state)
        n_samples, n_features = X.shape
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        if n_classes < 2:
            raise ValueError("AdaBoostClassifier needs at least two classes")

        weights = np.full(n_samples, 1.0 / n_samples)
        self.n_features_in_ = n_features
        self.estimators_ = []
        self.estimator_weights_ = []
        self.estimator_errors_ = []
        self.feature_importances_ = np.zeros(n_features, dtype=float)

        for _ in range(self.n_estimators):
            rows = rng.choice(n_samples, size=n_samples, replace=True, p=weights)
            tree = DecisionTreeClassifier(
                max_depth=self.max_depth,
                min_samples_split=2,
                min_samples_leaf=self.min_samples_leaf,
                criterion=self.criterion,
            )
            tree.fit(X[rows], y[rows])
            pred = tree.predict(X)
            wrong = pred != y
            err = float(np.dot(weights, wrong))
            err = np.clip(err, 1e-12, 1.0 - 1e-12)

            if err >= 1.0 - (1.0 / n_classes):
                if not self.estimators_:
                    self.estimators_.append(tree)
                    self.estimator_weights_.append(1.0)
                    self.estimator_errors_.append(err)
                break

            alpha = self.learning_rate * (
                np.log((1.0 - err) / err) + np.log(n_classes - 1.0)
            )
            self.estimators_.append(tree)
            self.estimator_weights_.append(float(alpha))
            self.estimator_errors_.append(err)
            self.feature_importances_ += alpha * tree.feature_importances_

            weights *= np.exp(alpha * wrong)
            weights /= weights.sum()

            if err <= 1e-12:
                break

        self.estimator_weights_ = np.asarray(self.estimator_weights_, dtype=float)
        self.estimator_errors_ = np.asarray(self.estimator_errors_, dtype=float)
        total = self.feature_importances_.sum()
        if total > 0:
            self.feature_importances_ = self.feature_importances_ / total
        return self

    def predict(self, X):
        scores = self._scores(X)
        return self.classes_[np.argmax(scores, axis=1)]

    def predict_proba(self, X):
        scores = self._scores(X)
        scores = scores - scores.max(axis=1, keepdims=True)
        exp = np.exp(scores)
        return exp / exp.sum(axis=1, keepdims=True)

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def structure_summary(self, feature_names=None, max_estimators=5, tree_depth=1):
        if not self.estimators_:
            raise ValueError("AdaBoostClassifier has not been fit yet")
        if feature_names is None:
            feature_names = [f"x{i}" for i in range(self.n_features_in_)]

        lines = [
            "AdaBoostClassifier",
            f"learners={len(self.estimators_)}, classes={list(self.classes_)}",
            f"learning_rate={self.learning_rate}, weak_tree_depth={self.max_depth}",
        ]
        for i, tree in enumerate(self.estimators_[:max_estimators], start=1):
            lines.append(
                f"\nlearner {i}: weight={self.estimator_weights_[i-1]:.3f}, "
                f"error={self.estimator_errors_[i-1]:.3f}"
            )
            lines.append(tree.export_tree(feature_names=feature_names, max_depth=tree_depth))
        return "\n".join(lines)

    def _scores(self, X):
        if not self.estimators_:
            raise ValueError("AdaBoostClassifier has not been fit yet")
        X = np.asarray(X, dtype=float)
        scores = np.zeros((len(X), len(self.classes_)), dtype=float)
        class_lookup = {cls: i for i, cls in enumerate(self.classes_)}

        for tree, alpha in zip(self.estimators_, self.estimator_weights_):
            pred = tree.predict(X)
            for i, label in enumerate(pred):
                scores[i, class_lookup[label]] += alpha
        return scores


RandomForest = RandomForestClassifier
AdaBoost = AdaBoostClassifier
