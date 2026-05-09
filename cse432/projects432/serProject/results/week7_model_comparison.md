# Week 7 Model Comparison

Goal: add the first two real Week 7 baselines to MiniLearn and compare them against sklearn on the same split.

## Setup

- Rows: 2452
- Feature columns: 407
- Target: `emotion_id` with 8 RAVDESS emotions
- Split: stratified 80/20 train/test, random_state=432
- Scaling: MiniLearn `StandardScaler`, fit on training rows only
- KNN tuning: tiny 3-fold CV on the training split only, distance weighting

## KNN Tune Check

| k | CV Accuracy | CV Macro-F1 |
|---|-------------|-------------|
| 3 | 0.635 | 0.627 |
| 5 | 0.596 | 0.585 |
| 7 | 0.582 | 0.564 |
| 9 | 0.560 | 0.542 |
| 11 | 0.551 | 0.534 |

Picked `k=3` for the final held-out test run.

## Held-Out Results

| Model | Accuracy | Macro-F1 | Weighted-F1 | Train s | Predict s | Notes |
|-------|----------|----------|-------------|---------|-----------|-------|
| MiniLearn LogisticRegression | 0.689 | 0.681 | 0.688 | 2.49 | 0.00 | softmax GD, same params as week 6 |
| sklearn LogisticRegression | 0.695 | 0.681 | 0.695 | 15.73 | 0.01 | library sanity check |
| MiniLearn GaussianNB | 0.434 | 0.415 | 0.425 | 0.02 | 0.01 | assumes feature independence, which is kinda fake for audio |
| sklearn GaussianNB | 0.434 | 0.415 | 0.425 | 0.01 | 0.01 | same simple baseline |
| MiniLearn KNN k=3 | 0.685 | 0.663 | 0.683 | 0.00 | 2.28 | 3-fold CV picked k on train only |
| sklearn KNN k=3 | 0.685 | 0.663 | 0.683 | 0.00 | 0.04 | same k/weights as MiniLearn |

## Per-Class F1

This table is from the test split. It is here because one overall accuracy number hides a lot with RAVDESS.

| Model | neutral | calm | happy | sad | angry | fearful | disgust | surprised | Macro avg |
|-------|---|---|---|---|---|---|---|---|---|
| MiniLearn LogisticRegression | 0.667 | 0.805 | 0.730 | 0.556 | 0.797 | 0.614 | 0.650 | 0.625 | 0.681 |
| sklearn LogisticRegression | 0.613 | 0.813 | 0.745 | 0.584 | 0.795 | 0.652 | 0.615 | 0.632 | 0.681 |
| MiniLearn GaussianNB | 0.383 | 0.589 | 0.438 | 0.283 | 0.583 | 0.313 | 0.343 | 0.387 | 0.415 |
| sklearn GaussianNB | 0.383 | 0.589 | 0.438 | 0.283 | 0.583 | 0.313 | 0.343 | 0.387 | 0.415 |
| MiniLearn KNN k=3 | 0.613 | 0.800 | 0.730 | 0.624 | 0.735 | 0.684 | 0.535 | 0.582 | 0.663 |
| sklearn KNN k=3 | 0.613 | 0.800 | 0.730 | 0.624 | 0.735 | 0.684 | 0.535 | 0.582 | 0.663 |

## Confusion Matrices

Rows are true labels, columns are predicted labels.

```text
labels: 1=neutral, 2=calm, 3=happy, 4=sad, 5=angry, 6=fearful, 7=disgust, 8=surprised

MiniLearn LogisticRegression
[[24  3  0  8  1  0  0  2]
 [ 2 64  1  6  0  1  1  0]
 [ 1  5 54  1  3  6  0  5]
 [ 5  8  4 42  0 10  6  0]
 [ 0  0  2  2 59  2  4  6]
 [ 1  3  7 11  5 43  2  3]
 [ 0  1  2  3  5  0 26  1]
 [ 1  0  3  3  0  3  3 25]]

sklearn LogisticRegression
[[23  3  1  8  1  0  0  2]
 [ 4 63  0  6  0  1  1  0]
 [ 1  3 57  2  2  6  0  4]
 [ 7  6  5 45  0  8  4  0]
 [ 0  0  2  1 58  2  6  6]
 [ 1  3  7 11  4 46  2  1]
 [ 0  2  2  4  5  0 24  1]
 [ 1  0  4  2  1  3  3 24]]

MiniLearn GaussianNB
[[18  3  6  4  0  2  3  2]
 [10 43  2  7  0  5  7  1]
 [ 2  1 30  4 14  5  8 11]
 [14 17 11 16  2  4  9  2]
 [ 0  1  5  0 51  2  5 11]
 [ 5  4  4  7 24 18 10  3]
 [ 2  2  2  0  4  3 18  7]
 [ 5  0  2  0  5  1  7 18]]

sklearn GaussianNB
[[18  3  6  4  0  2  3  2]
 [10 43  2  7  0  5  7  1]
 [ 2  1 30  4 14  5  8 11]
 [14 17 11 16  2  4  9  2]
 [ 0  1  5  0 51  2  5 11]
 [ 5  4  4  7 24 18 10  3]
 [ 2  2  2  0  4  3 18  7]
 [ 5  0  2  0  5  1  7 18]]

MiniLearn KNN k=3
[[23  9  1  2  1  1  0  1]
 [ 6 66  0  3  0  0  0  0]
 [ 1  3 50  2  5  3  4  7]
 [ 2 11  2 44  2  9  3  2]
 [ 0  0  3  1 57  4  5  5]
 [ 0  1  2  9  9 53  1  0]
 [ 2  0  1  4  4  5 19  3]
 [ 3  0  3  1  2  5  1 23]]

sklearn KNN k=3
[[23  9  1  2  1  1  0  1]
 [ 6 66  0  3  0  0  0  0]
 [ 1  3 50  2  5  3  4  7]
 [ 2 11  2 44  2  9  3  2]
 [ 0  0  3  1 57  4  5  5]
 [ 0  1  2  9  9 53  1  0]
 [ 2  0  1  4  4  5 19  3]
 [ 3  0  3  1  2  5  1 23]]
```

## Notes

- Logistic regression is still the best simple MiniLearn model here; the sklearn version is basically the ceiling for this linear setup.
- Gaussian NB runs instantly but the independence assumption is rough because the MFCC/mel summary features are obviously correlated.
- KNN gets a fairer shot only after scaling. Without scaling the big Hz-ish features would steamroll the distance calculation.
- This is not final model selection. It is the Week 7 checkpoint proving more MiniLearn pieces can run against the same SER table.
