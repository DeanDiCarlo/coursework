"""Week 6 MiniLearn baseline run."""

from pathlib import Path
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression as SkLogisticRegression

from minilearn.classifiers import LogisticRegression
from minilearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from minilearn.preprocessing import StandardScaler, train_test_split


ROOT = Path(__file__).resolve().parents[1]
FEATURE_PATH = ROOT / "features" / "features.csv"
RESULT_PATH = ROOT / "results" / "week6_initial_results.md"
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

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=432, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    mini = LogisticRegression(
        learning_rate=0.08,
        max_iter=1200,
        reg_strength=0.001,
        tol=1e-7,
    )

    start = time.perf_counter()
    mini.fit(X_train, y_train)
    mini_time = time.perf_counter() - start
    mini_pred = mini.predict(X_test)

    sk = SkLogisticRegression(max_iter=2000, C=1.0, solver="lbfgs")
    start = time.perf_counter()
    sk.fit(X_train, y_train)
    sk_time = time.perf_counter() - start
    sk_pred = sk.predict(X_test)

    lines = build_report(
        df=df,
        feature_count=len(feature_cols),
        y_test=y_test,
        mini_pred=mini_pred,
        mini_time=mini_time,
        mini_iters=len(mini.loss_history_),
        sk_pred=sk_pred,
        sk_time=sk_time,
    )

    RESULT_PATH.parent.mkdir(exist_ok=True)
    RESULT_PATH.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def build_report(
    df,
    feature_count,
    y_test,
    mini_pred,
    mini_time,
    mini_iters,
    sk_pred,
    sk_time,
):
    emotions = (
        df[["emotion_id", "emotion"]]
        .drop_duplicates()
        .sort_values("emotion_id")
        .set_index("emotion_id")["emotion"]
        .to_dict()
    )

    mini_acc = accuracy_score(y_test, mini_pred)
    mini_f1 = f1_score(y_test, mini_pred, average="macro")
    sk_acc = accuracy_score(y_test, sk_pred)
    sk_f1 = f1_score(y_test, sk_pred, average="macro")

    lines = [
        "# Week 6 Initial Results",
        "",
        "Goal: get the first MiniLearn classifier running on the extracted RAVDESS features.",
        "",
        "## Setup",
        "",
        f"- Rows: {len(df)}",
        f"- Feature columns: {feature_count}",
        "- Target: `emotion_id`",
        "- Split: stratified 80/20 train/test, random_state=432",
        "- Scaling: MiniLearn `StandardScaler`, fit on train only",
        "",
        "## Results",
        "",
        "| Model | Accuracy | Macro-F1 | Train time | Notes |",
        "|-------|----------|----------|------------|-------|",
        f"| MiniLearn LogisticRegression | {mini_acc:.3f} | {mini_f1:.3f} | {mini_time:.2f}s | {mini_iters} GD steps |",
        f"| sklearn LogisticRegression | {sk_acc:.3f} | {sk_f1:.3f} | {sk_time:.2f}s | lbfgs sanity check |",
        "",
        "## MiniLearn Per-Class F1",
        "",
        "| Emotion | F1 | Support |",
        "|---------|----|---------|",
    ]

    report = classification_report(y_test, mini_pred, labels=sorted(emotions))
    for label, name in emotions.items():
        row = report[label]
        lines.append(f"| {name} | {row['f1']:.3f} | {row['support']} |")

    lines.extend(
        [
            "",
            "## Confusion Matrix",
            "",
            "Rows are true labels, columns are predicted labels.",
            "",
            "```text",
            "labels: " + ", ".join(f"{k}={v}" for k, v in emotions.items()),
            str(confusion_matrix(y_test, mini_pred, labels=sorted(emotions))),
            "```",
            "",
            "## Notes",
            "",
            "- This is a first baseline, not tuned final performance.",
            "- Logistic regression is linear, so it gives us a decent pipeline check before KNN, Naive Bayes, trees, and SVM.",
            "- The sklearn number is not the goal; it is there to catch obvious bugs in the from-scratch version.",
        ]
    )
    return lines


if __name__ == "__main__":
    np.set_printoptions(linewidth=120)
    main()
