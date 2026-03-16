# SER Project — Build Plan

## 1. Project Overview

Build an end-to-end **Speech Emotion Recognition (SER)** system using the RAVDESS dataset (2,452 audio files, 8 emotions, 24 actors). The project has three pillars:

1. **MiniLearn** — a from-scratch ML library (30 pts)
2. **Feature extraction + supervised classification** — audio features, classical + neural models (30 pts)
3. **Unsupervised clustering + evaluation + report** — K-Means, metrics, comparative analysis (40 pts)

**Dataset**: RAVDESS Audio-Only (speech + song). Already downloaded to `serProject/data/Actor_01-24/`. Filenames encode emotion, intensity, actor, etc. via a 7-part numeric ID (e.g., `03-01-05-01-02-01-12.wav` → emotion=angry).

---

## 2. MiniLearn Architecture

### Module Structure

```
minilearn/
├── __init__.py                  # Package root, version, public imports
├── classifiers/
│   ├── __init__.py
│   ├── logistic_regression.py   # LogisticRegression
│   ├── knn.py                   # KNearestNeighbors
│   ├── naive_bayes.py           # GaussianNaiveBayes
│   ├── decision_tree.py         # DecisionTreeClassifier (CART)
│   ├── svm.py                   # LinearSVM (optional: kernel trick)
│   └── neural_network.py        # ANNClassifier (dense network)
├── preprocessing/
│   ├── __init__.py
│   ├── scaler.py                # StandardScaler
│   ├── splitter.py              # train_test_split (stratified)
│   └── pca.py                   # PCA (eigendecomposition)
├── metrics/
│   ├── __init__.py
│   ├── classification.py        # accuracy, precision, recall, f1 (per-class + macro + weighted)
│   ├── confusion_matrix.py      # confusion_matrix + plotting helper
│   └── cross_validation.py      # k_fold_cross_validate (stratified)
└── ensemble/                    # Bonus
    ├── __init__.py
    ├── bagging.py               # BaggingClassifier
    └── random_forest.py         # RandomForestClassifier (wraps DecisionTree)
```

### Class Interface Convention

Every classifier follows scikit-learn's API:

```python
class Classifier:
    def __init__(self, **hyperparams): ...
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'Classifier': ...
    def predict(self, X: np.ndarray) -> np.ndarray: ...
    def predict_proba(self, X: np.ndarray) -> np.ndarray: ...  # where applicable
    def score(self, X: np.ndarray, y: np.ndarray) -> float: ...
```

### Implementation Order (with rationale)

| Order | Module | Why This Order |
|-------|--------|----------------|
| 1 | `metrics/classification.py` | Foundation — every model needs scoring to validate |
| 2 | `metrics/confusion_matrix.py` | Needed for evaluation from the start |
| 3 | `preprocessing/scaler.py` | StandardScaler is required before any model runs |
| 4 | `preprocessing/splitter.py` | train_test_split needed for all experiments |
| 5 | `classifiers/logistic_regression.py` | Simplest gradient-based classifier; validates the pipeline |
| 6 | `classifiers/naive_bayes.py` | Fast, no hyperparams — great sanity check baseline |
| 7 | `classifiers/knn.py` | Distance-based; tests scaler correctness |
| 8 | `classifiers/decision_tree.py` | CART is the most complex classical algo; build after simpler ones |
| 9 | `classifiers/svm.py` | Linear SVM via hinge loss + SGD |
| 10 | `preprocessing/pca.py` | Needed for clustering visualization + optional dim reduction |
| 11 | `metrics/cross_validation.py` | Needed for final evaluation; can test all models retroactively |
| 12 | `classifiers/neural_network.py` | Most complex; benefits from all prior infrastructure |
| 13 | `ensemble/` | Bonus — wraps DecisionTree, so build last |

---

## 3. Feature Extraction Pipeline

### Features to Extract

| Feature | Librosa Function | Raw Shape | Summary Stats | Final Dims |
|---------|-----------------|-----------|---------------|------------|
| **MFCCs** | `librosa.feature.mfcc(n_mfcc=13)` | (13, T) | mean, std, min, max, median | 65 |
| **MFCC Δ** | `librosa.feature.delta(mfcc)` | (13, T) | mean, std | 26 |
| **MFCC ΔΔ** | `librosa.feature.delta(mfcc, order=2)` | (13, T) | mean, std | 26 |
| **Chroma** | `librosa.feature.chroma_stft()` | (12, T) | mean, std | 24 |
| **Mel Spectrogram** | `librosa.feature.melspectrogram(n_mels=128)` | (128, T) | mean, std | 256 |
| **ZCR** | `librosa.feature.zero_crossing_rate()` | (1, T) | mean, std | 2 |
| **RMS Energy** | `librosa.feature.rms()` | (1, T) | mean, std | 2 |
| **Spectral Centroid** | `librosa.feature.spectral_centroid()` | (1, T) | mean, std | 2 |
| **Spectral Bandwidth** | `librosa.feature.spectral_bandwidth()` | (1, T) | mean, std | 2 |
| **Spectral Rolloff** | `librosa.feature.spectral_rolloff()` | (1, T) | mean, std | 2 |

**Total feature vector**: ~407 dimensions per audio file.

### Extraction Script Design

```python
# notebooks/02_feature_extraction.ipynb  OR  serProject/extract_features.py

def extract_features(file_path: str) -> np.ndarray:
    """Load one WAV, return a 1-D feature vector."""
    y, sr = librosa.load(file_path, sr=22050)  # resample to 22050 Hz
    # ... extract all features, compute summary stats, concatenate
    return feature_vector

def parse_filename(path: str) -> dict:
    """Parse RAVDESS filename → {modality, channel, emotion, intensity, statement, repetition, actor}."""
    parts = Path(path).stem.split('-')
    return {'emotion': int(parts[2]), 'actor': int(parts[6]), ...}
```

### Output Format

Save to `serProject/data/features.csv`:
- Columns: `file`, `emotion`, `actor`, `intensity`, `channel`, `mfcc_0_mean`, `mfcc_0_std`, ..., `rolloff_std`
- One row per audio file (2,452 rows)
- This prevents re-extraction on every run

### Critical Rule: Standardization

```
⚠️  Fit scaler on TRAINING data ONLY → transform both train and test.
     Never call scaler.fit() on test data. Major point deduction if violated.
```

---

## 4. Classification Workflow

### 4.1 Logistic Regression

**MiniLearn implementation**:
- Softmax (multinomial) for 8-class problem
- Gradient descent with configurable learning rate and max iterations
- L2 regularization (weight decay)

**Key hyperparameters**:
| Param | Search Range | Default |
|-------|-------------|---------|
| `learning_rate` | [0.001, 0.01, 0.1] | 0.01 |
| `max_iter` | [500, 1000, 2000] | 1000 |
| `reg_strength` | [0.0, 0.01, 0.1, 1.0] | 0.01 |

**Comparison**: Run both MiniLearn and `sklearn.linear_model.LogisticRegression` on same split. Report accuracy delta.

### 4.2 Gaussian Naive Bayes

**MiniLearn implementation**:
- Per-class mean/variance estimation (MLE)
- Log-probability trick to avoid underflow
- Variance smoothing (`var_smoothing=1e-9`)

**No hyperparameters to tune** — makes it the fastest baseline.

### 4.3 K-Nearest Neighbors

**MiniLearn implementation**:
- Euclidean distance (default), optionally Manhattan
- Brute-force search (no KD-tree needed for this dataset size)

**Key hyperparameters**:
| Param | Search Range |
|-------|-------------|
| `k` | [3, 5, 7, 9, 11, 15, 21] |
| `weights` | ['uniform', 'distance'] |

**Note**: KNN is very sensitive to feature scaling — this tests that StandardScaler works.

### 4.4 Decision Tree (CART)

**MiniLearn implementation**:
- Gini impurity criterion (optionally entropy)
- Recursive binary splitting
- Pre-pruning via `max_depth`, `min_samples_split`, `min_samples_leaf`

**Key hyperparameters**:
| Param | Search Range |
|-------|-------------|
| `max_depth` | [5, 10, 15, 20, None] |
| `min_samples_split` | [2, 5, 10] |
| `min_samples_leaf` | [1, 2, 5] |
| `criterion` | ['gini', 'entropy'] |

**Deliverable**: Visualize a shallow tree (depth≤4) to show what features it splits on — likely MFCCs.

### 4.5 Support Vector Machine

**MiniLearn implementation** (linear only):
- Hinge loss + L2 regularization, optimized via SGD
- One-vs-Rest wrapper for multiclass

**Sklearn comparison**: Use `sklearn.svm.SVC` with kernels:
| Kernel | Tune |
|--------|------|
| `linear` | C ∈ [0.1, 1, 10] |
| `rbf` | C ∈ [0.1, 1, 10], gamma ∈ ['scale', 'auto', 0.01, 0.001] |
| `poly` | degree ∈ [2, 3], C ∈ [0.1, 1, 10] |

**Expectation**: RBF kernel SVM will likely be a top performer on this feature set.

### 4.6 Random Forest (sklearn or bonus MiniLearn)

**Key hyperparameters**:
| Param | Search Range |
|-------|-------------|
| `n_estimators` | [100, 200, 500] |
| `max_depth` | [10, 20, None] |
| `max_features` | ['sqrt', 'log2'] |

**Deliverable**: Feature importance plot — which audio features matter most.

### 4.7 Boosting Models (optional but worth points)

- **XGBoost**: Already in requirements.txt. Use `XGBClassifier`.
- Tune `n_estimators`, `max_depth`, `learning_rate`, `subsample`.
- XGBoost will likely be the best classical model.

### 4.8 Neural Network (required — at least one)

See Section 7 for detailed architecture.

---

## 5. Clustering Section

### K-Means (Required, k=8)

1. Standardize features (same scaler, fit on full dataset for unsupervised)
2. Apply PCA → reduce to 50 components (speeds up K-Means, reduces noise)
3. Run K-Means with `k=8` (matching 8 emotions)
4. Also run with `k` ∈ [2, 4, 6, 8, 10, 12] and plot elbow curve (inertia vs k)

### Visualization Strategy

| Plot | Method | Purpose |
|------|--------|---------|
| **2D scatter (clusters)** | PCA or t-SNE → 2D | Color by K-Means cluster assignment |
| **2D scatter (true labels)** | Same projection | Color by true emotion label |
| **Side-by-side comparison** | Subplots | Visual alignment of clusters vs truth |
| **Elbow curve** | Inertia vs k | Justify k=8 or show natural grouping |
| **Silhouette plot** | Per-sample silhouette | Cluster quality per emotion |

### Evaluation Metrics

- **Adjusted Rand Index (ARI)**: Measures agreement between clusters and true labels, adjusted for chance. Range: [-1, 1], 1 = perfect.
- **Normalized Mutual Information (NMI)**: Information-theoretic measure of cluster-label correspondence. Range: [0, 1].

### Discussion Points to Address

1. Do clusters naturally separate by emotion? (Probably partially — calm/neutral will merge, angry/happy may overlap)
2. Which emotions cluster together? Why? (Valence-arousal model: high-arousal emotions may group)
3. Is SER better suited to supervised or unsupervised? (Supervised — emotions are subtle, labeled data is essential)

### Optional: Hierarchical Clustering

- Agglomerative with Ward linkage
- Dendrogram visualization (truncated to ~20 leaves)
- Compare with K-Means assignments

---

## 6. Evaluation Framework

### Per-Model Metrics (compute for every supervised model)

```
Accuracy
Precision  (per-class, macro-avg, weighted-avg)
Recall     (per-class, macro-avg, weighted-avg)
F1 Score   (per-class, macro-avg, weighted-avg)
Confusion Matrix (8×8 heatmap)
ROC Curve + AUC (One-vs-Rest, per-class)
Training Time (wall clock)
```

### Cross-Validation

- **Stratified 5-fold CV** for all classical models
- Report mean ± std for accuracy and macro-F1
- Use `cross_val_score` from sklearn AND MiniLearn's own implementation — compare

### Hyperparameter Tuning

- Use `GridSearchCV` or `RandomizedSearchCV` on training folds
- Report best params per model
- Never tune on the held-out test set

### Comparison Table Template

| Model | Accuracy | Macro-F1 | Weighted-F1 | AUC (macro) | Best Hyperparams | Train Time |
|-------|----------|----------|-------------|-------------|------------------|------------|
| Logistic Regression (MiniLearn) | | | | | | |
| Logistic Regression (sklearn) | | | | | | |
| Gaussian Naive Bayes | | | | | | |
| KNN | | | | | | |
| Decision Tree | | | | | | |
| SVM (RBF) | | | | | | |
| Random Forest | | | | | | |
| XGBoost | | | | | | |
| Dense NN | | | | | | |

### MiniLearn vs Sklearn Comparison

For each MiniLearn classifier, run the equivalent sklearn model on the same data split and compare:
- Accuracy difference (should be small — within 1-3%)
- Training time difference
- If large gap exists, debug the MiniLearn implementation

### Error Analysis

- Which emotions are hardest to classify? (Expect: calm vs neutral, happy vs surprised)
- Per-class F1 breakdown
- Confusion matrix analysis: where are the biggest off-diagonal values?

---

## 7. Neural Network Section

### Recommended Architecture: Dense NN (start here)

This is the simplest NN to implement and meets the "at least one" requirement.

```
Input (407 features)
  → Dense(256, ReLU) → BatchNorm → Dropout(0.3)
  → Dense(128, ReLU) → BatchNorm → Dropout(0.3)
  → Dense(64, ReLU)  → Dropout(0.2)
  → Dense(8, Softmax)
```

**Training config**:
| Param | Value |
|-------|-------|
| Optimizer | Adam, lr=0.001 |
| Loss | CrossEntropyLoss |
| Batch size | 32 |
| Epochs | 100-200 |
| Early stopping | patience=15 on val_loss |
| Validation split | 15% of training data |

**Framework**: Use PyTorch or TensorFlow/Keras — whichever you're more comfortable with. Keras is simpler for this.

### MiniLearn ANN (from-scratch, simpler)

For the MiniLearn `neural_network.py`, implement a simpler version:
- 2-3 fully connected layers
- ReLU activation, softmax output
- Backpropagation with SGD or mini-batch SGD
- No BatchNorm or Dropout needed (keep it simple)
- This will underperform Keras, and that's expected — discuss why in the report

### Optional Stretch: 1D-CNN

If time allows, a 1D-CNN on raw MFCC frames (not summary stats) can capture temporal patterns:

```
Input (13 × T MFCC frames, zero-padded to fixed length)
  → Conv1D(64, kernel=3) → ReLU → MaxPool
  → Conv1D(128, kernel=3) → ReLU → MaxPool
  → Flatten → Dense(128, ReLU) → Dropout(0.3)
  → Dense(8, Softmax)
```

This requires storing per-frame MFCCs (not just summary stats). Save as `.npy` files.

---

## 8. Algorithmic Recommendations

### Expected Performance Ranking (best → worst)

| Rank | Model | Expected Accuracy | Why |
|------|-------|------------------|-----|
| 1 | **XGBoost** | 65-75% | Best classical model for tabular features; handles feature interactions well |
| 2 | **SVM (RBF)** | 60-70% | Strong on medium-sized datasets with good features; kernel trick captures nonlinearities |
| 3 | **Random Forest** | 58-68% | Robust ensemble; good feature importance insights |
| 4 | **Dense NN (Keras)** | 55-68% | Can learn complex boundaries but may overfit on 2,452 samples |
| 5 | **KNN (k=7, distance)** | 50-60% | Decent with standardized features; struggles in high dimensions |
| 6 | **Logistic Regression** | 45-55% | Linear boundary is too simple for 8-class emotion recognition |
| 7 | **Decision Tree** | 40-55% | Prone to overfitting without ensemble |
| 8 | **Naive Bayes** | 35-50% | Feature independence assumption is heavily violated |

**Note**: These are rough estimates. RAVDESS is a controlled lab dataset, so accuracies may be higher than real-world SER.

### Key Insights to Discuss in Report

1. **Feature importance**: MFCCs (especially deltas) and spectral features will dominate. ZCR and energy are weaker but still useful.
2. **Class imbalance**: Neutral has no "strong" intensity variant → slightly fewer samples. Not severe but worth noting.
3. **Speaker independence**: For a stronger evaluation, split by actor (leave-actor-out CV) rather than random splits. This tests generalization to unseen speakers.
4. **Song vs speech**: Consider training separate models or using channel as a feature. Emotions manifest differently in speech vs song.

---

## 9. Phased Implementation Order

### Phase 1: Foundation (Do First)
- [ ] **1.1** Parse all filenames → build metadata DataFrame (emotion, actor, channel, intensity)
- [ ] **1.2** EDA notebook: class distributions, actor balance, audio waveform/spectrogram plots
- [ ] **1.3** Implement `minilearn/metrics/classification.py` (accuracy, precision, recall, F1)
- [ ] **1.4** Implement `minilearn/metrics/confusion_matrix.py`
- [ ] **1.5** Implement `minilearn/preprocessing/scaler.py` (StandardScaler)
- [ ] **1.6** Implement `minilearn/preprocessing/splitter.py` (train_test_split)

### Phase 2: Feature Extraction
- [ ] **2.1** Build feature extraction function (all 10 feature types)
- [ ] **2.2** Run extraction on all 2,452 files → save to `features.csv`
- [ ] **2.3** Feature EDA: distributions per emotion, correlation matrix, PCA variance explained
- [ ] **2.4** Verify features load correctly and standardize properly

### Phase 3: Classical Classifiers (MiniLearn)
- [ ] **3.1** Logistic Regression (MiniLearn) — validate on features
- [ ] **3.2** Gaussian Naive Bayes (MiniLearn)
- [ ] **3.3** KNN (MiniLearn)
- [ ] **3.4** Decision Tree / CART (MiniLearn)
- [ ] **3.5** Linear SVM (MiniLearn)
- [ ] **3.6** Run sklearn equivalents for comparison

### Phase 4: Advanced Models
- [ ] **4.1** Random Forest (sklearn)
- [ ] **4.2** XGBoost
- [ ] **4.3** Hyperparameter tuning (GridSearch) for top 3 models

### Phase 5: Neural Network
- [ ] **5.1** Dense NN in Keras/PyTorch — train, evaluate
- [ ] **5.2** MiniLearn ANN (from-scratch backprop) — simpler architecture
- [ ] **5.3** Compare MiniLearn ANN vs Keras NN

### Phase 6: Evaluation & Clustering
- [ ] **6.1** Implement `minilearn/metrics/cross_validation.py`
- [ ] **6.2** Run stratified 5-fold CV on all models
- [ ] **6.3** Build comparison table with all metrics
- [ ] **6.4** ROC curves (One-vs-Rest) for top models
- [ ] **6.5** K-Means clustering (k=8) + elbow curve
- [ ] **6.6** Implement `minilearn/preprocessing/pca.py`
- [ ] **6.7** PCA/t-SNE visualization of clusters vs true labels
- [ ] **6.8** ARI and NMI computation

### Phase 7: Report & Polish
- [ ] **7.1** Consolidate notebooks into clean report structure
- [ ] **7.2** Write discussion sections (every plot gets a paragraph)
- [ ] **7.3** Error analysis: hardest emotions, confusion patterns
- [ ] **7.4** Conclusion with practical takeaways
- [ ] **7.5** Add references (RAVDESS paper, librosa, etc.)
- [ ] **7.6** Code cleanup, docstrings, final review
