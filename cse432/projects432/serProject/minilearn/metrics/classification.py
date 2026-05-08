"""Basic classification metrics for MiniLearn."""

import numpy as np

from .confusion_matrix import confusion_matrix


def accuracy_score(y_true, y_pred):
    """Return the fraction of correct predictions."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}"
        )
    return float((y_true == y_pred).mean())


def _per_class_prf_support(y_true, y_pred, labels=None):
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    tp = np.diag(cm)
    fp = cm.sum(axis=0) - tp
    fn = cm.sum(axis=1) - tp
    support = cm.sum(axis=1)

    with np.errstate(divide="ignore", invalid="ignore"):
        precision = np.where(tp + fp > 0, tp / (tp + fp), 0.0)
        recall = np.where(tp + fn > 0, tp / (tp + fn), 0.0)
        denom = precision + recall
        f1 = np.where(denom > 0, 2 * precision * recall / denom, 0.0)

    return precision, recall, f1, support


def _aggregate(per_class_values, support, average):
    if average is None:
        return per_class_values
    if average == "macro":
        return float(per_class_values.mean())
    if average == "weighted":
        if support.sum() == 0:
            return 0.0
        return float(np.average(per_class_values, weights=support))
    raise ValueError(
        f"average must be None, 'macro', or 'weighted', got {average!r}"
    )


def precision_score(y_true, y_pred, labels=None, average="macro"):
    """Precision score. average can be None, 'macro', or 'weighted'."""
    precision, _, _, support = _per_class_prf_support(y_true, y_pred, labels=labels)
    return _aggregate(precision, support, average)


def recall_score(y_true, y_pred, labels=None, average="macro"):
    """Recall score. average can be None, 'macro', or 'weighted'."""
    _, recall, _, support = _per_class_prf_support(y_true, y_pred, labels=labels)
    return _aggregate(recall, support, average)


def f1_score(y_true, y_pred, labels=None, average="macro"):
    """F1 score. average can be None, 'macro', or 'weighted'."""
    _, _, f1, support = _per_class_prf_support(y_true, y_pred, labels=labels)
    return _aggregate(f1, support, average)


def classification_report(y_true, y_pred, labels=None):
    """Return a small sklearn-ish report as nested dictionaries."""
    precision, recall, f1, support = _per_class_prf_support(
        y_true, y_pred, labels=labels
    )

    if labels is None:
        labels_used = sorted(
            set(np.asarray(y_true).tolist()) | set(np.asarray(y_pred).tolist())
        )
    else:
        labels_used = list(labels)

    report = {}
    for i, lbl in enumerate(labels_used):
        report[lbl] = {
            "precision": float(precision[i]),
            "recall": float(recall[i]),
            "f1": float(f1[i]),
            "support": int(support[i]),
        }

    report["accuracy"] = accuracy_score(y_true, y_pred)
    report["macro avg"] = {
        "precision": _aggregate(precision, support, "macro"),
        "recall": _aggregate(recall, support, "macro"),
        "f1": _aggregate(f1, support, "macro"),
        "support": int(support.sum()),
    }
    report["weighted avg"] = {
        "precision": _aggregate(precision, support, "weighted"),
        "recall": _aggregate(recall, support, "weighted"),
        "f1": _aggregate(f1, support, "weighted"),
        "support": int(support.sum()),
    }
    return report


if __name__ == "__main__":
    import sklearn.metrics as sk

    rng = np.random.default_rng(28)
    y_true = rng.integers(0, 4, size=400)
    y_pred = y_true.copy()
    flip = rng.choice(400, size=120, replace=False)
    y_pred[flip] = rng.integers(0, 4, size=120)

    assert abs(accuracy_score(y_true, y_pred) - sk.accuracy_score(y_true, y_pred)) < 1e-12

    for avg in ("macro", "weighted"):
        ours_p = precision_score(y_true, y_pred, average=avg)
        ours_r = recall_score(y_true, y_pred, average=avg)
        ours_f = f1_score(y_true, y_pred, average=avg)
        sk_p = sk.precision_score(y_true, y_pred, average=avg, zero_division=0)
        sk_r = sk.recall_score(y_true, y_pred, average=avg, zero_division=0)
        sk_f = sk.f1_score(y_true, y_pred, average=avg, zero_division=0)
        assert abs(ours_p - sk_p) < 1e-12, f"precision({avg}) mismatch"
        assert abs(ours_r - sk_r) < 1e-12, f"recall({avg}) mismatch"
        assert abs(ours_f - sk_f) < 1e-12, f"f1({avg}) mismatch"

    p_ours = precision_score(y_true, y_pred, average=None)
    p_sk = sk.precision_score(y_true, y_pred, average=None, zero_division=0)
    assert np.allclose(p_ours, p_sk)

    y_true_edge = np.array([0, 0, 1, 1])
    y_pred_edge = np.array([0, 0, 0, 0])
    p_edge = precision_score(y_true_edge, y_pred_edge, labels=[0, 1], average=None)
    assert p_edge[1] == 0.0, "precision should be 0 (not NaN) when a class has no predictions"
