"""Train/test splitting."""

import numpy as np


def train_test_split(*arrays, test_size=0.2, random_state=None, shuffle=True, stratify=None):
    if not arrays:
        raise ValueError("at least one array is required")

    n = len(arrays[0])
    if any(len(a) != n for a in arrays):
        raise ValueError("all arrays must have the same length")

    rng = np.random.default_rng(random_state)

    if stratify is None:
        indices = np.arange(n)
        if shuffle:
            rng.shuffle(indices)
        split = n - _test_count(n, test_size)
        train_idx, test_idx = indices[:split], indices[split:]
    else:
        train_parts = []
        test_parts = []
        stratify = np.asarray(stratify)
        if len(stratify) != n:
            raise ValueError("stratify must have the same length as the arrays")

        for label in np.unique(stratify):
            label_idx = np.flatnonzero(stratify == label)
            if shuffle:
                rng.shuffle(label_idx)
            n_test = _test_count(len(label_idx), test_size)
            test_parts.append(label_idx[:n_test])
            train_parts.append(label_idx[n_test:])

        train_idx = np.concatenate(train_parts)
        test_idx = np.concatenate(test_parts)
        if shuffle:
            rng.shuffle(train_idx)
            rng.shuffle(test_idx)

    out = []
    for arr in arrays:
        arr = np.asarray(arr)
        out.extend([arr[train_idx], arr[test_idx]])
    return tuple(out)


def _test_count(n, test_size):
    if isinstance(test_size, float):
        if not 0 < test_size < 1:
            raise ValueError("float test_size must be between 0 and 1")
        return max(1, int(round(n * test_size)))
    if isinstance(test_size, int):
        if not 0 < test_size < n:
            raise ValueError("int test_size must be between 1 and n - 1")
        return test_size
    raise TypeError("test_size must be a float or int")
