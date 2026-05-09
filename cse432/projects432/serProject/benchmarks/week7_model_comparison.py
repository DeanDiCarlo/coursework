"""Week 7 MiniLearn vs sklearn benchmark."""

from pathlib import Path
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression as SkLogisticRegression
from sklearn.naive_bayes import GaussianNB as SkGaussianNB
from sklearn.neighbors import KNeighborsClassifier

from minilearn.classifiers import GaussianNaiveBayes, KNN, LogisticRegression
from minilearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    k_fold_cross_validate,
)
from minilearn.preprocessing import StandardScaler, train_test_split


ROOT = Path(__file__).resolve().parents[1]
FEATURE_PATH = ROOT / "features" / "features.csv"
RESULT_DIR = ROOT / "results"
CSV_PATH = RESULT_DIR / "week7_model_comparison.csv"
MD_PATH = RESULT_DIR / "week7_model_comparison.md"

META_COLS = {
    "filename",
    "emotion",
    "emotion_id",
    "actor",
    "gender",
    "vocalchannel",
    "intensity",
    "statement",
    "repetition",
    "duration",
}


def main():
    df = pd.read_csv(FEATURE_PATH)
    feature_cols = [c for c in df.columns if c not in META_COLS]

    X = df[feature_cols].to_numpy(dtype=float)
    y = df["emotion_id"].to_numpy()
    labels = sorted(df["emotion_id"].unique())
    emotions = (
        df[["emotion_id", "emotion"]]
        .drop_duplicates()
        .sort_values("emotion_id")
        .set_index("emotion_id")["emotion"]
        .to_dict()
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=432, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    k_rows = []
    for k in [3, 5, 7, 9, 11]:
        folds = k_fold_cross_validate(
            lambda k=k: KNN(k=k, weights="distance"),
            X_train,
            y_train,
            n_splits=3,
            random_state=432,
            scale=True,
        )
        k_rows.append(
            {
                "k": k,
                "cv_macro_f1": float(np.mean([r["macro_f1"] for r in folds])),
                "cv_accuracy": float(np.mean([r["accuracy"] for r in folds])),
            }
        )
    best_k = max(k_rows, key=lambda row: (row["cv_macro_f1"], row["cv_accuracy"]))["k"]

    models = [
        (
            "MiniLearn LogisticRegression",
            LogisticRegression(
                learning_rate=0.08,
                max_iter=1200,
                reg_strength=0.001,
                tol=1e-7,
            ),
            "softmax GD, same params as week 6",
        ),
        (
            "sklearn LogisticRegression",
            SkLogisticRegression(max_iter=2000, C=1.0, solver="lbfgs"),
            "library sanity check",
        ),
        (
            "MiniLearn GaussianNB",
            GaussianNaiveBayes(),
            "assumes feature independence, which is kinda fake for audio",
        ),
        ("sklearn GaussianNB", SkGaussianNB(), "same simple baseline"),
        (
            f"MiniLearn KNN k={best_k}",
            KNN(k=best_k, weights="distance"),
            "3-fold CV picked k on train only",
        ),
        (
            f"sklearn KNN k={best_k}",
            KNeighborsClassifier(n_neighbors=best_k, weights="distance"),
            "same k/weights as MiniLearn",
        ),
    ]

    rows = []
    reports = {}
    cms = {}
    for name, model, note in models:
        start = time.perf_counter()
        model.fit(X_train_s, y_train)
        train_time = time.perf_counter() - start
        start = time.perf_counter()
        pred = model.predict(X_test_s)
        pred_time = time.perf_counter() - start

        rows.append(
            {
                "model": name,
                "accuracy": accuracy_score(y_test, pred),
                "macro_f1": f1_score(y_test, pred, average="macro"),
                "weighted_f1": f1_score(y_test, pred, average="weighted"),
                "train_seconds": train_time,
                "predict_seconds": pred_time,
                "notes": note,
            }
        )
        reports[name] = classification_report(y_test, pred, labels=labels)
        cms[name] = confusion_matrix(y_test, pred, labels=labels)

    RESULT_DIR.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(CSV_PATH, index=False)
    MD_PATH.write_text(
        build_markdown(df, feature_cols, rows, reports, cms, emotions, k_rows, best_k)
    )
    print(MD_PATH.read_text())


def build_markdown(df, feature_cols, rows, reports, cms, emotions, k_rows, best_k):
    lines = [
        "# Week 7 Model Comparison",
        "",
        "Goal: add the first two real Week 7 baselines to MiniLearn and compare them against sklearn on the same split.",
        "",
        "## Setup",
        "",
        f"- Rows: {len(df)}",
        f"- Feature columns: {len(feature_cols)}",
        "- Target: `emotion_id` with 8 RAVDESS emotions",
        "- Split: stratified 80/20 train/test, random_state=432",
        "- Scaling: MiniLearn `StandardScaler`, fit on training rows only",
        "- KNN tuning: tiny 3-fold CV on the training split only, distance weighting",
        "",
        "## KNN Tune Check",
        "",
        "| k | CV Accuracy | CV Macro-F1 |",
        "|---|-------------|-------------|",
    ]
    for row in k_rows:
        lines.append(f"| {row['k']} | {row['cv_accuracy']:.3f} | {row['cv_macro_f1']:.3f} |")

    lines.extend(
        [
            "",
            f"Picked `k={best_k}` for the final held-out test run.",
            "",
            "## Held-Out Results",
            "",
            "| Model | Accuracy | Macro-F1 | Weighted-F1 | Train s | Predict s | Notes |",
            "|-------|----------|----------|-------------|---------|-----------|-------|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['model']} | {row['accuracy']:.3f} | {row['macro_f1']:.3f} | "
            f"{row['weighted_f1']:.3f} | {row['train_seconds']:.2f} | "
            f"{row['predict_seconds']:.2f} | {row['notes']} |"
        )

    lines.extend(
        [
            "",
            "## Per-Class F1",
            "",
            "This table is from the test split. It is here because one overall accuracy number hides a lot with RAVDESS.",
            "",
            "| Model | "
            + " | ".join(emotions.values())
            + " | Macro avg |",
            "|-------|"
            + "|".join(["---"] * (len(emotions) + 1))
            + "|",
        ]
    )
    for model, report in reports.items():
        vals = [f"{report[label]['f1']:.3f}" for label in emotions]
        vals.append(f"{report['macro avg']['f1']:.3f}")
        lines.append(f"| {model} | " + " | ".join(vals) + " |")

    lines.extend(
        [
            "",
            "## Confusion Matrices",
            "",
            "Rows are true labels, columns are predicted labels.",
            "",
            "```text",
            "labels: " + ", ".join(f"{k}={v}" for k, v in emotions.items()),
        ]
    )
    for model, cm in cms.items():
        lines.append("")
        lines.append(model)
        lines.append(str(cm))
    lines.extend(
        [
            "```",
            "",
            "## Notes",
            "",
            "- Logistic regression is still the best simple MiniLearn model here; the sklearn version is basically the ceiling for this linear setup.",
            "- Gaussian NB runs instantly but the independence assumption is rough because the MFCC/mel summary features are obviously correlated.",
            "- KNN gets a fairer shot only after scaling. Without scaling the big Hz-ish features would steamroll the distance calculation.",
            "- This is not final model selection. It is the Week 7 checkpoint proving more MiniLearn pieces can run against the same SER table.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    np.set_printoptions(linewidth=120)
    main()
