# 🍷 Welcome to "Wine Quality Classification - Gaussian Discriminant Analysis from Scratch" Project (Classification)

## Overview
This project addresses a multi-class classification problem using the Wine Quality Dataset. The goal is to build a Gaussian Discriminant Analysis (GDA) model from scratch for classifying wine quality based on continuous features.

## Objectives
- **Data Loading & Inspection**: Load the dataset from the UCI repository and perform initial inspection.
- **Exploratory Data Analysis (EDA)**: Derive visuals to check Gaussian assumptions and class separability (histograms, scatter plots, etc.).
- **Data Pre-Processing & Feature Engineering**: Select continuous features, handle outliers, and apply standardization.
- **Feature Scaling**: Scale numerical features to meet GDA assumptions.
- **Data Splitting**: Split your dataset randomly for training, validation, and testing with stratification.
- **Model Building & Training**: Implement GDA from scratch with both shared and individual covariance matrices.
- **Hyperparameter Tuning**: Compare shared vs. individual covariance assumptions.
- **Model Evaluation**: Report accuracy, confusion matrix, and class-wise performance.
- **Results Analysis**: Analyze the impact of feature correlation and Gaussian assumption violations.
- **Comparison with Sklearn**: Compare results with sklearn's LDA and QDA.

## Dataset
- **Name**: Wine Quality Dataset
- **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- **Target Variable**: Quality (multi-class)

## Key Steps
1. Loading Dataset from UCI Repository
2. EDA and Visualizing Feature Distributions & Class Separability
3. Data Pre-Processing (Feature Selection, Outlier Handling, Standardization)
4. Data Splitting (Training, Validation, Testing Sets)
5. Model Building (GDA from Scratch with Shared/Individual Covariance)
6. Training the Model and Covariance Analysis
7. Model Evaluation using Accuracy and Confusion Matrix
8. Gaussian Assumption Testing
9. Comparison with Sklearn's LDA & QDA
