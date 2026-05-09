"""Small cross validation helpers."""

import numpy as np

from minilearn.preprocessing import StandardScaler
from .classification import accuracy_score, f1_score


def stratified_k_fold_indices(y, n_splits=5, shuffle=True, random_state=None):
    y = np.asarray(y)
    if n_splits < 2:
        raise ValueError("n_splits must be at least 2")

    rng = np.random.default_rng(random_state)
    folds = [[] for _ in range(n_splits)]

    for cls in np.unique(y):
        idx = np.flatnonzero(y == cls)
        if len(idx) < n_splits:
            raise ValueError("each class needs at least n_splits samples")
        if shuffle:
            rng.shuffle(idx)
        for fold_i, item in enumerate(idx):
            folds[fold_i % n_splits].append(item)

    all_idx = np.arange(len(y))
    out = []
    for fold in folds:
        test_idx = np.array(sorted(fold))
        train_mask = np.ones(len(y), dtype=bool)
        train_mask[test_idx] = False
        train_idx = all_idx[train_mask]
        out.append((train_idx, test_idx))
    return out


def k_fold_cross_validate(model_factory, X, y, n_splits=5, random_state=None, scale=True):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)

    rows = []
    for fold_i, (train_idx, test_idx) in enumerate(
        stratified_k_fold_indices(y, n_splits=n_splits, random_state=random_state),
        start=1,
    ):
        X_train = X[train_idx]
        X_test = X[test_idx]
        if scale:
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        model = model_factory()
        model.fit(X_train, y[train_idx])
        pred = model.predict(X_test)
        rows.append(
            {
                "fold": fold_i,
                "accuracy": accuracy_score(y[test_idx], pred),
                "macro_f1": f1_score(y[test_idx], pred, average="macro"),
                "weighted_f1": f1_score(y[test_idx], pred, average="weighted"),
            }
        )
    return rows
