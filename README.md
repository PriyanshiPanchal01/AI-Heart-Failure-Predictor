# 🩺 AI Heart Failure Risk Predictor

An end-to-end Machine Learning web application built with **Django** and **XGBoost** to predict heart failure risk based on clinical records.

## 🚀 Features
- **High Accuracy:** Trained using XGBoost Classifier with 80%+ accuracy.
- **Professional Dashboard:** Clean medical UI built with Bootstrap 5.
- **Real-time Prediction:** Instant analysis of 12 clinical features like age, ejection fraction, and serum creatinine.

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **ML Model:** XGBoost, Scikit-learn
- **Frontend:** HTML5, Bootstrap 5
- **Data:** Heart Failure Clinical Records (Kaggle)

## 📂 Project Structure
- `predictor/`: Django app for handling user input and model logic.
- `ml_models/`: Contains the trained `heart_model.pkl`.
- `train.py`: Python script used to train the XGBoost model.