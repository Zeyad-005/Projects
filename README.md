# Welcome to the Dual ML Project! 🚀

This repository contains two distinct machine learning projects that demonstrate fundamental skills in both **Classification** and **Regression**.

-----------------------------------------------------------------

## 📁 Project 1: MAGIC Gamma Telescope Classification

### Overview
This project tackles a classic classification problem using the **MAGIC Gamma Telescope** dataset. The goal is to distinguish high-energy gamma particles (signal) from hadronic particles (background) captured by the telescope.

### Objectives
1. Balance the dataset by randomly putting aside the extra readings for the gamma “g” class to make both classes equal in size.
2. Split the dataset randomly so that the training set would form 70%, for the validation set 15% and 15% for the testing set.
3. Apply K-NN Classifier to the data Manually (Without Scikit- Learn) once (i.e. create functions for distance calculation, finding K-nearest neighbors & making predictions based on majority vote or any other implementation)
4. Re-apply K-NN Classifier to the data by using Scikit-Learn.
5. Apply different k values to get the best results in both cases.
6. Plot validation accuracy vs. k values for both implementation and identify optimal k-value and discuss overfitting/underfitting trends.
7. Report final trained model’s accuracy, precision, recall and f-score as well as confusion matrix for both cases and compare between them.

### Dataset
**Name:** MAGIC Gamma Telescope Data  
**Source:** [UCI Machine Learning Repository] --> (https://archive.ics.uci.edu/ml/datasets/MAGIC+Gamma+Telescope)  
**Target Variable:** Class (g for gamma, h for hadron)

### Key Steps
1.  Data Loading & Cleaning
2.  Exploratory Data Analysis (EDA)
3.  Feature Engineering & Selection
4.  Model Training and Hyperparameter Tuning
5.  Model Evaluation using Accuracy, Precision, Recall, F1-Score, and ROC-AUC

----------------------------------------------------------------------

## 📁 Project 2: California Housing Price Prediction (Regression)

### Overview
This project addresses a regression problem using the **California Census Data**. The goal is to build a model that can predict the median house value for any district in California.

### Objectives
1. Split your dataset randomly so that the training set would form 70%, for the validation set 15% and 15% for the testing set.
2. Apply linear, lasso and ridge regression to the data to predict the median house value Implement from scratch using matrix operations.
3. Calculate weights using normal equation: w = (X^T X)^(-1) X^T y) and apply Gradient descent as an alternative optimization approach and comment on the two results.
4. Apply L2 Regularization (Ridge Regression) and L1 Regularization (Lasso Regression) and try different regularization parameters & plot validation error vs. regularization parameter
5. Re-apply these steps again using Scikit- Learn and compare both results.
6. Report Mean Square Error and Mean Absolute Errors for all models.
7. Add comments on the results and compare between the models.

### Dataset
**Name:** California Housing Prices  
**Source:** [Popular dataset from StatLib] --> (https://www.kaggle.com/camnugent/california-housing-prices) OR (via `sklearn.datasets.fetch_california_housing`)  
**Target Variable:** `MedHouseVal` (Median House Value)

### Key Steps
1.  Data Loading & Inspection
2.  Handling Missing Values and Scaling Features
3.  Exploratory Data Analysis (EDA) and Visualizing Geospatial Data
4.  Model Training and Hyperparameter Tuning
5.  Model Evaluation using MSE, RMSE, MAE, and R² Score

---------------------------------------------------------------------
