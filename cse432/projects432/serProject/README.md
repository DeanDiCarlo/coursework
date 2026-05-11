# SER Project — Speech Emotion Recognition with MiniLearn

A complete Speech Emotion Recognition system built on the RAVDESS dataset,
featuring **MiniLearn** — a from-scratch mini scikit-learn library.

This is being built in passes instead of one giant dump. The point is to get
one small piece working, compare it against a known library when possible, and
then move to the next piece.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download RAVDESS audio-only data
python download_data.py

# 4. Extract features
# e.g. python extract_features.py --data_dir data/ --output features.csv

# 5. Open the classification notebook
jupyter notebook notebooks/01_classification.ipynb
```

## Project Structure

```
SER_Project/
├── minilearn/                  # From-scratch ML library
│   ├── classifiers/            # LR, KNN, NB, SVM, trees, ensembles
│   ├── clustering/             # K-Means
│   ├── preprocessing/          # StandardScaler, train_test_split
│   └── metrics/                # accuracy, precision, recall, F1, confusion matrix
├── notebooks/
│   └── 01_classification.ipynb # End-to-end SER classification demo
├── benchmarks/
│   ├── week6_initial_results.py
│   └── week7_model_comparison.py
├── results/
│   └── week6_initial_results.md
├── extract_features.py         # Audio → feature CSV pipeline
├── download_data.py            # Dataset download helper
├── requirements.txt            # Python dependencies (one example)
└── README.md
```

## Dataset

RAVDESS Audio-Only — 2,452 files (1,440 speech + 1,012 song) from 24 actors,
8 emotions: neutral, calm, happy, sad, angry, fearful, disgust, surprised.

Source: https://zenodo.org/records/1188976

## MiniLearn

Import it like scikit-learn:

```python
from minilearn.classifiers import LogisticRegression, KNN, GaussianNaiveBayes, LinearSVM, DecisionTreeClassifier, RandomForestClassifier, AdaBoostClassifier
from minilearn.preprocessing import StandardScaler, train_test_split
from minilearn.metrics import accuracy_score, f1_score, confusion_matrix
```

Right now the MiniLearn slice includes:

- `accuracy_score`
- `precision_score`
- `recall_score`
- `f1_score`
- `classification_report`
- `confusion_matrix`
- `plot_confusion_matrix`
- `k_fold_cross_validate`
- `StandardScaler`
- `train_test_split`
- `PCA`
- `LogisticRegression`
- `GaussianNaiveBayes`
- `KNN`
- `LinearSVM`
- `DecisionTreeClassifier`
- `RandomForestClassifier`
- `AdaBoostClassifier`
- `KMeans`

The metrics files also have quick `__main__` checks against scikit-learn so
they can be tested before the classifiers are written.

```bash
cd serProject
PYTHONPATH=. python -W ignore::RuntimeWarning -m minilearn.metrics.confusion_matrix
PYTHONPATH=. python -W ignore::RuntimeWarning -m minilearn.metrics.classification
PYTHONPATH=. python benchmarks/week6_initial_results.py
PYTHONPATH=. python benchmarks/week7_model_comparison.py
```

## Build Strategy

### Pass 1 - Data sanity

Get the files into a shape the rest of the project can trust.

- Download only the RAVDESS audio-only speech and song zip files.
- Extract them under `data/`.
- Parse filenames into `metadata.csv`.
- Check counts by actor, emotion, channel, and intensity.
- Make a few basic plots in the data check notebook.

This pass is mostly about proving the labels are correct before training
anything.

### Pass 2 - Feature table

Turn every WAV file into one row of numbers.

- Extract MFCCs, MFCC deltas, chroma, mel spectrogram summaries, ZCR, RMS,
  centroid, bandwidth, and rolloff.
- Save the result once in `features/features.csv`.
- Keep the target columns beside the feature columns so notebooks do not have
  to re-parse filenames.
- Do quick checks for missing values and weird ranges.

The big rule here is to never standardize before splitting for supervised
models. Fit the scaler on the training split only.

### Pass 3 - MiniLearn foundation

Build the parts every later model will reuse.

- Metrics: done for the first pass.
- `StandardScaler`: done for the first pass.
- `train_test_split`: done, including stratified splits.
- Logistic regression: done as the first real classifier.

The goal is not to make the fanciest library first. It is to get a tiny
pipeline running end to end, then replace or improve pieces.

### Pass 4 - Baselines

Train simple models before chasing bigger ones.

- MiniLearn logistic regression vs sklearn logistic regression.
- Gaussian Naive Bayes.
- KNN with standardized features.
- Decision tree after the simpler classifiers work.

Each model should produce the same basic output: accuracy, macro-F1, weighted
F1, a classification report, and a confusion matrix.

### Pass 5 - Stronger models

Once the baselines are honest, use sklearn models for performance.

- SVM with linear/RBF/poly kernels.
- Random forest.
- XGBoost if the environment cooperates.
- A small dense neural network.

These models are mainly for final comparison and discussion. The MiniLearn
versions are for showing understanding.

### Pass 6 - Validation and report

Clean up the evaluation so the final writeup is not just random notebook
outputs.

- Stratified cross-validation.
- Hyperparameter tuning on training folds only.
- One summary table for every model.
- ROC/AUC for top supervised models.
- K-Means clustering with ARI/NMI and PCA or t-SNE plots.
- Short discussion under every plot instead of just screenshots.

## Current Checkpoint

Finished or partly finished:

- RAVDESS data is present under `data/`.
- Feature outputs exist under `features/`.
- MiniLearn package shell exists.
- MiniLearn metrics have sklearn sanity checks.
- MiniLearn preprocessing has a scaler and stratified train/test split.
- MiniLearn logistic regression, Gaussian NB, KNN, linear SVM, and Decision Tree run on the extracted features.
- MiniLearn Random Forest and AdaBoost run as the first ensemble models.
- Week 6 initial results are saved in `results/week6_initial_results.md`.
- Week 7 comparisons are saved in `results/week7_model_comparison.md`.
- The comparison workbook is `notebooks/3_week7_model_comparison.ipynb`.
- The SVM workbook is `notebooks/4_week8_svm.ipynb`.
- The tree workbook is `notebooks/5_week9_decision_tree.ipynb`.
- The ensemble workbook is `notebooks/6_week10_ensemble_models.ipynb`.
- The comprehensive evaluation workbook is `notebooks/7_comprehensive_model_evaluation.ipynb`.
- The validation/tuning workbook is `notebooks/8_model_validation_tuning.ipynb`.
- The clustering workbook is `notebooks/9_topic13_clustering.ipynb`.

Next build chunk:

1. Add ANN if we keep pushing the from-scratch library.
2. Tighten final report language around the validated model comparison.
