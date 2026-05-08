# Week 6 Initial Results

Goal: get the first MiniLearn classifier running on the extracted RAVDESS features.

## Setup

- Rows: 2452
- Feature columns: 407
- Target: `emotion_id`
- Split: stratified 80/20 train/test, random_state=432
- Scaling: MiniLearn `StandardScaler`, fit on train only

## Results

| Model | Accuracy | Macro-F1 | Train time | Notes |
|-------|----------|----------|------------|-------|
| MiniLearn LogisticRegression | 0.689 | 0.681 | 2.54s | 1200 GD steps |
| sklearn LogisticRegression | 0.695 | 0.681 | 15.52s | lbfgs sanity check |

## MiniLearn Per-Class F1

| Emotion | F1 | Support |
|---------|----|---------|
| neutral | 0.667 | 38 |
| calm | 0.805 | 75 |
| happy | 0.730 | 75 |
| sad | 0.556 | 75 |
| angry | 0.797 | 75 |
| fearful | 0.614 | 75 |
| disgust | 0.650 | 38 |
| surprised | 0.625 | 38 |

## Confusion Matrix

Rows are true labels, columns are predicted labels.

```text
labels: 1=neutral, 2=calm, 3=happy, 4=sad, 5=angry, 6=fearful, 7=disgust, 8=surprised
[[24  3  0  8  1  0  0  2]
 [ 2 64  1  6  0  1  1  0]
 [ 1  5 54  1  3  6  0  5]
 [ 5  8  4 42  0 10  6  0]
 [ 0  0  2  2 59  2  4  6]
 [ 1  3  7 11  5 43  2  3]
 [ 0  1  2  3  5  0 26  1]
 [ 1  0  3  3  0  3  3 25]]
```

## Notes

- This is a first baseline, not tuned final performance.
- Logistic regression is linear, so it gives us a decent pipeline check before KNN, Naive Bayes, trees, and SVM.
- The sklearn number is not the goal; it is there to catch obvious bugs in the from-scratch version.
