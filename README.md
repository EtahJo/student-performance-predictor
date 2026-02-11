# AI Student Performance Predictor

An end-to-end machine learning system that predicts student exam performance (A/B/C/D) based on historical quiz behavior.

---

## Built With

- **Django REST Framework** – Backend API  
- **Scikit-learn** – Model training  
- **NumPy & Pandas** – Feature processing  
- **Joblib** – Model persistence  
- **Next.js + Tailwind CSS** – Frontend UI  

---

## Project Overview

This project demonstrates how behavioral learning data can be transformed into predictive insights.

Each quiz attempt captures:

- Quiz score (0–100)
- Topic accuracy (0–1)
- Number of attempts
- Time spent (seconds)

Using supervised machine learning, the system predicts a student's expected final exam grade band.

---

##  Machine Learning Approach

- Multi-class classification using Logistic Regression  
- Feature standardization with `StandardScaler`  
- Stratified train/test split  
- Class balancing to prevent bias  
- Model persistence via `joblib`  
- REST API serving for real-time predictions  

---

## API Endpoint

### Predict Exam Band

**POST** `/api/predict/`

#### Request

```json
{
  "quiz_score": 75,
  "topic_accuracy": 0.7,
  "attempts": 2,
  "time_spent_sec": 900
}
