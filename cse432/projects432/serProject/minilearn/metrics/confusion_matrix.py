"""Confusion matrix helpers for MiniLearn."""

import numpy as np


def confusion_matrix(y_true, y_pred, labels=None, normalize=None):
    """Return counts where rows are true labels and columns are predictions."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}"
        )

    if labels is None:
        labels = sorted(set(y_true.tolist()) | set(y_pred.tolist()))
    else:
        labels = list(labels)

    n = len(labels)
    label_to_idx = {lbl: i for i, lbl in enumerate(labels)}

    try:
        true_idx = np.array([label_to_idx[t] for t in y_true.tolist()])
        pred_idx = np.array([label_to_idx[p] for p in y_pred.tolist()])
    except KeyError as err:
        raise ValueError(
            f"label {err.args[0]!r} appears in y_true/y_pred but not in `labels`"
        ) from err

    cm = np.zeros((n, n), dtype=int)
    np.add.at(cm, (true_idx, pred_idx), 1)

    if normalize is None:
        return cm

    cm = cm.astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        if normalize == "true":
            row_sums = cm.sum(axis=1, keepdims=True)
            cm = np.where(row_sums > 0, cm / row_sums, 0.0)
        elif normalize == "pred":
            col_sums = cm.sum(axis=0, keepdims=True)
            cm = np.where(col_sums > 0, cm / col_sums, 0.0)
        elif normalize == "all":
            total = cm.sum()
            cm = cm / total if total > 0 else cm
        else:
            raise ValueError(
                f"normalize must be None, 'true', 'pred', or 'all', got {normalize!r}"
            )
    return cm


def plot_confusion_matrix(cm, labels, ax=None, normalize=False, title=None, cmap="Blues"):
    """Draw a confusion matrix heatmap."""
    import matplotlib.pyplot as plt
    import seaborn as sns

    if ax is None:
        _, ax = plt.subplots(figsize=(7, 6))

    if normalize:
        row_sums = cm.sum(axis=1, keepdims=True)
        with np.errstate(invalid="ignore", divide="ignore"):
            cm_display = np.where(row_sums > 0, cm / row_sums, 0.0)
        fmt = ".2f"
    else:
        cm_display = cm
        fmt = "d" if np.asarray(cm).dtype.kind in "iu" else ".2f"

    sns.heatmap(
        cm_display,
        annot=True, fmt=fmt, cmap=cmap,
        xticklabels=labels, yticklabels=labels,
        ax=ax, cbar=True, square=True,
    )
    ax.set_xlabel("predicted")
    ax.set_ylabel("true")
    if title:
        ax.set_title(title)
    return ax


if __name__ == "__main__":
    import sklearn.metrics as sk

    rng = np.random.default_rng(28)
    y_true = rng.integers(0, 4, size=200)
    y_pred = rng.integers(0, 4, size=200)
    labels = [0, 1, 2, 3]

    cm_ours = confusion_matrix(y_true, y_pred, labels=labels)
    cm_sk = sk.confusion_matrix(y_true, y_pred, labels=labels)
    assert np.array_equal(cm_ours, cm_sk), "confusion_matrix disagrees with sklearn"

    for i, lbl in enumerate(labels):
        correct = ((y_true == lbl) & (y_pred == lbl)).sum()
        assert cm_ours[i, i] == correct

    cm_norm = confusion_matrix(y_true, y_pred, labels=labels, normalize="true")
    row_sums = cm_norm.sum(axis=1)
    nonzero_rows = row_sums[row_sums > 0]
    assert np.allclose(nonzero_rows, 1.0)

    try:
        confusion_matrix([0, 1, 99], [0, 1, 0], labels=[0, 1])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for unknown label")
