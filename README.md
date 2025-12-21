
## 📁 Welcome to "California Housing Price Prediction" Project (Regression)

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

