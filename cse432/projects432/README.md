# CSE 432/532 — Machine Learning Semester Project

## Speech Emotion Recognition (SER) Using the RAVDESS Dataset

---

## 1. Project Overview

In this semester-long project, you will build an end-to-end **Speech Emotion Recognition (SER)** system. Starting from raw audio recordings of emotional speech, you will extract meaningful features, apply a range of machine learning algorithms to classify the expressed emotion, and write a technical report comparing your methods and results.

A unique component of this project is that you will develop your own lightweight ML toolkit — a Python package called **MiniLearn** — that implements core algorithms from scratch. You will use this package alongside scikit-learn in your SER experiments.

> **Important:** We are working exclusively with the **audio** portion of the RAVDESS dataset. You will **not** use any video or facial expression data. All your work should focus on extracting information from the audio signal only.

*NOTE: Some part of this readme may updated during the course. It's good idea to `git pull` on your local repo to get latest information.*

### Learning Objectives

By completing this project you will be able to:

- Work with a real-world audio dataset from download through analysis
- Extract and engineer features from audio signals
- Implement core ML algorithms from scratch inside a reusable library
- Apply and compare classical and modern classification techniques
- Perform model evaluation, cross-validation, and hyperparameter tuning
- Explore unsupervised learning (clustering) applied to the same problem
- Write a technical report with critical discussion of results
- Demonstrate deep understanding of every piece of code you submit

---

## 2. The Dataset — RAVDESS (Audio-Only)

**The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS)**

- **Source:** [https://zenodo.org/records/1188976](https://zenodo.org/records/1188976)
- **Citation (required in your report):** Livingstone SR, Russo FA (2018). *The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS): A dynamic, multimodal set of facial and vocal expressions in North American English.* PLoS ONE 13(5): e0196391. [https://doi.org/10.1371/journal.pone.0196391](https://doi.org/10.1371/journal.pone.0196391)

### What to Download

Download **only** the two **audio-only** zip files from the Zenodo page:

| File | Size | Contents |
|------|------|----------|
| `Audio_Speech_Actors_01-24.zip` | ~215 MB | 1,440 speech files (60 per actor × 24 actors) |
| `Audio_Song_Actors_01-24.zip` | ~198 MB | 1,012 song files (44 per actor × 23 actors*) |

*\*Actor 18 has no song files.*

All audio files are **16-bit, 48 kHz WAV** format. Do **not** download the video files.

### File Naming Convention

Each filename is a 7-part numerical identifier. For example: `03-01-05-01-02-01-12.wav`

| Position | Meaning | Values |
|----------|---------|--------|
| 1 | Modality | 01 = full-AV, 02 = video-only, **03 = audio-only** |
| 2 | Vocal channel | **01 = speech**, **02 = song** |
| 3 | **Emotion** | 01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised |
| 4 | Intensity | 01 = normal, 02 = strong (no strong for neutral) |
| 5 | Statement | 01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door" |
| 6 | Repetition | 01 = 1st, 02 = 2nd |
| 7 | Actor | 01–24 (odd = male, even = female) |

Your classification target is the **Emotion** (position 3). You must write code to parse these filenames and build a metadata table.

---

## 3. The MiniLearn Library

You will develop **MiniLearn** — your own mini scikit-learn–style Python package, implemented from scratch.

### Requirements

1. **Importable Python package.** You should be able to write statements like `from minilearn.classifiers import LogisticRegression` in your SER notebook.
2. **[optional]** Follow the scikit-learn API pattern. Each model must have `.fit(X, y)`, `.predict(X)`, and `.score(X, y)` methods.
3. **Required implementations** (from scratch, using only NumPy/SciPy for numerical operations):
   - Logistic Regression (with gradient descent)
   - k-Nearest Neighbors (KNN)
   - Gaussian Naive Bayes
   - Decision Tree (CART algorithm)
   - Evaluation metrics: accuracy, precision, recall, F1 score, confusion matrix
   - Preprocessing: feature standardization, train-test split
   - PCA for dimensionality reduction
   - SVM (simplified linear)
   - ANN
   - Cross-validation utility (k-fold)
   - Clustering (see section 6)
4. **Optional / Bonus:**
   - Ensemble method (e.g., bagging or random forest wrapper)

You must compare your MiniLearn implementations against the equivalent scikit-learn classes and **discuss** where they agree, where they diverge, and why.

> **Code Ownership:** There is an assessment for your project. You must be able to explain every function in your MiniLearn code. I reserve the right to ask you to walk through your code, explain design decisions, or modify it live during a scheduled walk-through. **Inability to explain your own code may result in a score of 0 for this section.**

---

## 4. Feature Extraction from Audio

Since this is a machine learning course (not a speech processing course), we provide guidance on audio feature extraction. Your job is to understand *what* these features capture and *why* they matter for emotion recognition, then to implement the extraction pipeline.

### 4.1 Hand-Crafted Features (Required)

You may use the `librosa` Python library. For each audio file, extract frame-level features and then compute **summary statistics** (mean, standard deviation, etc.) to produce a fixed-length feature vector.

| Feature | Description | Why It Matters for SER |
|---------|-------------|----------------------|
| **MFCCs** (Mel-Frequency Cepstral Coefficients) | Compact representation of the spectral envelope (typically 13 coefficients) | Gold standard in speech/audio ML; captures vocal tract characteristics |
| **MFCC Deltas** (1st and 2nd order) | Rate of change of MFCCs over time | Captures dynamic aspects of speech — how the sound *changes* |
| **Chroma Features** | 12-dimensional pitch class profile | Captures tonal content; useful for distinguishing emotions in song |
| **Mel Spectrogram** | Time-frequency representation on the Mel scale | Rich spectral information; good input for CNN-based approaches |
| **Zero Crossing Rate (ZCR)** | Rate at which signal changes sign | Indicates noisiness; excited emotions (angry, happy) tend to have higher ZCR |
| **RMS Energy** | Root mean square energy per frame | Loudness — directly related to emotional intensity |
| **Spectral Centroid** | "Center of mass" of the spectrum | Brightness of sound; higher for excited emotions |
| **Spectral Bandwidth** | Width of the spectral band | Spread of frequencies; varies with emotion |
| **Spectral Rolloff** | Frequency below which 85% of energy lies | Distinguishes harmonic vs. noisy signals |

**How to use `librosa`:** Each feature is computed per-frame (e.g., `librosa.feature.mfcc()` returns a matrix of shape `[n_mfcc, n_frames]`). Since each audio file has different length, you should compute **summary statistics** over the frames (mean, std, min, max, etc.) to get a single fixed-length vector per file.

Example for one feature:
```python
import librosa
import numpy as np

y, sr = librosa.load("path/to/file.wav", sr=48000)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)   # shape: (13, n_frames)
mfcc_mean = np.mean(mfcc, axis=1)                       # shape: (13,) — one mean per coefficient
mfcc_std = np.std(mfcc, axis=1)                         # shape: (13,)
```

Apply this pattern to **all** the features listed above. Concatenate everything into one feature vector per file, then store all vectors in a DataFrame and **save to CSV** so you don't have to re-extract every time.

### 4.2 Pre-Trained Embeddings (To boost the accuracy)

For more advanced experiments, you can extract embeddings from pre-trained audio neural networks (e.g., OpenL3, VGGish, wav2vec 2.0, or HuBERT via HuggingFace). These produce high-dimensional vectors that encode rich acoustic information. Compare the results with your hand-crafted features.

### 4.3 Feature Standardization

**Standardize your features before classification.** Audio features live on very different scales (e.g., MFCCs vs. spectral centroid in Hz vs. RMS energy). Apply standardization so that each feature has zero mean and unit variance.

Key rule: **fit the scaler on training data only**, then use the same fitted scaler to transform both training and test data. Never fit on test data. This is an important concept and violation of it in your results will result in major deduction in your score.

---

## 5. Supervised Learning — Classification

Apply the following classifiers to your extracted features. For every model, report the metrics specified in Section 7.

### 5.1 Classical Models (Required)

| Model | Course Chapter | What to Explore |
|-------|---------------|-----------------|
| Logistic Regression | Ch. 7 | Use **both** your MiniLearn version and scikit-learn. Compare results. |
| Gaussian Naive Bayes | Ch. 7 | Good fast baseline. |
| k-Nearest Neighbors | Ch. 7 | Try different values of *k*. Why does standardization matter here? |
| Support Vector Machine | Ch. 8 | Try linear, RBF, and polynomial kernels. Tune C and gamma. |
| Decision Tree | Ch. 9 | Visualize the tree. Discuss overfitting and pruning. |
| Random Forest | Ch. 10 | Compare with single Decision Tree. Why is it better? |
| Bagging / Voting Classifier | Ch. 10 | Combine your best models. |

### 5.2 Boosting Models (Optional)

| Model | What to Explore |
|-------|-----------------|
| AdaBoost | How does it focus on misclassified samples? |
| Gradient Boosting | Compare with AdaBoost on the same features. |
| XGBoost | Often a top performer on tabular data. Compare with Gradient Boosting. |

### 5.3 Neural Network Models (Required — At Least One)

| Model | Input Type | Notes |
|-------|-----------|-------|
| Dense Neural Network (DNN) | Feature vector | A few Dense layers with ReLU + softmax output. Start here. |
| 1D-CNN | Raw MFCC frames or Mel spectrogram | Captures local temporal patterns in audio. |
| LSTM / GRU | MFCC frame sequences | Captures sequential dependencies in speech over time. |

You can use `tensorflow`/`keras` or `pytorch` as well (since you're using a pre-trained model it would be a simple adaptation).

---

## 6. Unsupervised Learning — Clustering

Apply clustering to explore whether emotional categories emerge naturally from the features **without** using the labels.

### Requirements

1. Apply **K-Means** (with k = 8, matching the number of emotions) to your feature vectors.
2. (Optional) Apply **Agglomerative (Hierarchical) Clustering** and visualize the dendrogram.
3. (Optional) Try DBSCAN or Gaussian Mixture Models.

### Analysis Questions (Address in Your Report)

- Do the clusters correspond to true emotion labels? Quantify using **Adjusted Rand Index** and **Normalized Mutual Information**.
- Visualize clusters in 2D (using PCA or t-SNE), coloring points by (a) cluster assignment and (b) true emotion. Compare.
- Which emotions are most often confused/clustered together? Does this make intuitive sense?
- Is SER fundamentally better suited to supervised or unsupervised learning? Why?

---

## 7. Model Evaluation & Comparison

### 7.1 Required Metrics

For **every** supervised model, compute and report:

- **Accuracy**
- **Precision** (per-class and macro/weighted average)
- **Recall** (per-class and macro/weighted average)
- **F1 Score** (per-class and macro/weighted average)
- **Confusion Matrix** (visualize as a heatmap)
- **ROC Curve & AUC** (One-vs-Rest for multiclass)

### 7.2 Validation Strategy

- Use **Stratified K-Fold Cross-Validation** (k = 5 or 10).
- For neural networks, use a held-out validation split.
- Perform **hyperparameter tuning** (GridSearch or RandomizedSearch) on the training folds. Report the best parameters.
- Never evaluate on data the model has seen during training or tuning.

### 7.3 Comparative Analysis

Build a summary comparison table of all models (accuracy, macro-F1, AUC, best hyperparameters, training time) and discuss:

- Which model performed best and why?
- Did advanced models significantly outperform simple baselines?
- Which emotions are hardest to classify?
- Did your MiniLearn results match scikit-learn?
- How did different feature sets affect performance?

---

## 8. Weekly Roadmap (WIP: This will be updated)

| Week | Course Topic | Project Milestone | Deliverable |
|------|-------------|-------------------|-------------|
| **4** | Introduction to ML | Setup & Exploration: Download audio data, set up environment, parse filenames, build metadata table. | Notebook: data loading + class distribution plot |
| **4-5** | Data Wrangling | Data Cleaning: Verify file counts, check for corruption, organize by actor/emotion. | Notebook: data audit report |
| **4-5** | Data Exploration | Feature Extraction (Part 1): Extract MFCCs, ZCR, RMS, spectral features. Save to CSV. | Feature CSV + EDA notebook |
| **4-5** | Data Exploration (cont.) | Feature Extraction (Part 2) & EDA: Additional features, correlation analysis, visualizations. | Expanded features + analysis notebook |
| **6** | Regression / Classification | MiniLearn — Logistic Regression & Metrics: First from-scratch classifier + metric functions. | MiniLearn (partial) + initial results |
| **7** | Classification Models | MiniLearn — KNN & Naive Bayes: Apply all three classifiers. Compare with scikit-learn. | Updated MiniLearn + comparison notebook |
| **8** | SVMs | SVM Experiments: Linear, RBF, polynomial kernels. Hyperparameter tuning. | SVM results notebook |
| **9** | Decision Trees | MiniLearn — Decision Tree: Implement CART. Visualize. Discuss overfitting. | Updated MiniLearn + tree notebook |
| **10** | Ensemble Models | Ensembles: RF, AdaBoost, Gradient Boosting, XGBoost. | Ensemble results notebook |
| **11** | Model Evaluation | Comprehensive Evaluation: All metrics, ROC curves, comparison table. | Evaluation notebook |
| **12** | Model Validation | Cross-Validation & Tuning: Stratified K-Fold, finalized hyperparameters. | Validation notebook |
| **13** | Clustering | Unsupervised Analysis: K-Means, Hierarchical, PCA/t-SNE visualization. | Clustering notebook |
| **14** | Dimensionality Reduction | PCA & Feature Selection: Analyze explained variance, re-run classifiers. | Dimensionality reduction notebook |
| **14** | Neural Networks | Deep Models: DNN, CNN, or LSTM. Experiment with architectures. | Deep learning notebook |
| **15** | — | Final Report: Compile results, write discussion, clean repository. **Code walkthrough.** | Final report + clean repo |

---

## 9. Setup

### Required Python Packages

You will need: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `librosa`, `soundfile`, `xgboost`, 
   - Later you use a deep learning framework (`tensorflow` or `pytorch`).

### Dataset Download

Go to [https://zenodo.org/records/1188976](https://zenodo.org/records/1188976) and manually download the two audio-only zip files. Extract them into a `data/` folder in your project.

---

## 10. Report Requirements

Your final submission should be a well-organized Jupyter notebook (or set of notebooks) that reads like a technical report:

1. **Introduction** — What is SER? Why is it important? Describe the RAVDESS dataset.
2. **Data Exploration** — Class distributions, audio visualizations, summary statistics.
3. **Feature Engineering** — What features you extracted, why, and how they distribute across emotions.
4. **MiniLearn Library** — Description of your implementations and comparison with scikit-learn.
5. **Classification Results** — All models, all metrics, confusion matrices, ROC curves.
6. **Clustering Analysis** — Unsupervised results and comparison with true labels.
7. **Discussion** — Key findings, surprises, limitations, what you'd do differently.
8. **Conclusion** — Summary of best methods and practical takeaways.
9. **References** — Cite the RAVDESS paper, libraries, and any resources consulted.

> **Discuss, don't just display.** For every plot and table, write a paragraph explaining what it shows and what it means.

---

## 11. Rubric

### Total: 100 points

| Section | Points | Key Criteria |
|---------|--------|-------------|
| **A. Data Acquisition, Cleaning & Exploration** | 10 | Correct download, filename parsing, data audit, EDA visualizations, written discussion |
| **B. Feature Extraction** | 10 | Multiple feature types extracted, analysis/visualization, proper standardization |
| **C. MiniLearn Library** | 30 | Package structure, LR, KNN, NB, Decision Tree, metrics module — all from scratch |
| **D. Supervised Classification** | 20 | All classical + boosting + at least one NN model applied; MiniLearn vs sklearn comparison |
| **E. Model Evaluation & Validation** | 10 | All metrics reported, cross-validation, hyperparameter tuning |
| **F. Unsupervised / Clustering** | 10 | K-Means + Hierarchical applied, PCA/t-SNE visualization, ARI/NMI, written analysis |
| **G. Report Quality & Presentation** | 10 | Organization, writing quality, critical discussion, code cleanliness |

### Code Ownership (applies to all sections)

You must be able to explain every piece of code you submit. I reserve the right to conduct **individual code walkthroughs** at any time. Inability to explain your work will be treated as evidence that it is not your own and may result in a score of **0 for the affected sections**.

---

## 12. Academic Integrity

You may use AI tools for guidance, debugging, and learning concepts. However:

- You must **understand and be able to explain** every line of code and every result.
- Your Git history should show **incremental development**, not a single bulk commit.
- **Code walkthroughs are mandatory** — I will ask you to explain your work.
- Submitting code you cannot explain will be treated as an academic integrity violation.

---

## References

1. Livingstone SR, Russo FA (2018). *The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS).* PLoS ONE 13(5): e0196391. [https://doi.org/10.1371/journal.pone.0196391](https://doi.org/10.1371/journal.pone.0196391)
2. RAVDESS Dataset on Zenodo: [https://zenodo.org/records/1188976](https://zenodo.org/records/1188976)
3. McFee B, et al. *librosa: Audio and music signal analysis in Python.* [https://librosa.org](https://librosa.org)
4. Pedregosa F, et al. *Scikit-learn: Machine Learning in Python.* JMLR 12, 2011.
