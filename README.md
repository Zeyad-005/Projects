# 🧬 Welcome to "Breast Cancer Wisconsin - Dimensionality Reduction & Clustering Analysis" Project (Unsupervised Learning)

## Overview
This project addresses an unsupervised learning problem using the Breast Cancer Wisconsin (Diagnostic) dataset. The goal is to implement PCA and K-Means clustering from scratch to identify inherent patterns in the data and evaluate the impact of dimensionality reduction on clustering performance.

## Objectives
- **Data Loading & Inspection**: Load the dataset from Kaggle and perform initial inspection.
- **Data Pre-Processing**: Handle missing values, scale features, and prepare data for unsupervised analysis.
- **Principal Component Analysis (PCA)**: Implement PCA from scratch using NumPy.
- **Dimensionality Reduction**: Experiment with different numbers of principal components.
- **K-Means Clustering**: Implement K-Means clustering from scratch using NumPy.
- **Elbow Method**: Apply the elbow method to determine optimal number of clusters.
- **Visualization**: Visualize clustering results in 2D/3D using principal components.
- **Performance Evaluation**: Compare sum of squared errors with and without PCA.
- **Label Comparison**: Compare clustering results with original diagnostic labels.

## Dataset
- **Name**: Breast Cancer Wisconsin (Diagnostic) Dataset
- **Source**: [Kaggle - Breast Cancer Wisconsin Dataset](https://www.kaggle.com/datasets/ucimi/breast-cancer-wisconsin-data)
- **Features**: 30 numerical features computed from digitized images of FNA
- **Target Variable**: Diagnosis (M = malignant, B = benign) - *Used only for validation, not for clustering*

## Key Steps
1. Loading Dataset from Kaggle
2. Data Pre-Processing (Handling Missing Values, Feature Scaling)
3. **Experiment 1**: K-Means Clustering on Original Data
   - Implement K-Means from scratch
   - Apply elbow method to find optimal k
   - Calculate sum of squared errors
4. **Experiment 2**: PCA + K-Means Clustering
   - Implement PCA from scratch
   - Reduce dimensionality with different numbers of components
   - Apply K-Means on reduced data
   - Apply elbow method to find optimal k
   - Calculate sum of squared errors
5. Visualization of Clustering Results
6. Performance Comparison Between Experiments
7. Analysis and Documentation of Findings

## Implementation Requirements
- ✅ Implement PCA using NumPy (no sklearn)
- ✅ Implement K-Means using NumPy (no sklearn)
- ✅ Apply elbow method in both experiments
- ✅ Compare SSE (sum of squared errors) between experiments
- ✅ Experiment with different numbers of principal components
- ✅ Visualize clustering results against original labels
- ✅ Provide detailed analysis and observations
