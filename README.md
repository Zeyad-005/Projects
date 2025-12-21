
## 📁 Welcome to "MAGIC Gamma Telescope Classification" Project

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
