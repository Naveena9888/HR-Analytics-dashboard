"""
Prediction module for evaluating individual employee attrition risk.
Loads saved model artifacts and makes inference on new employee profiles.
"""

import logging
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from config import MODEL_DIR, MODEL_PATH, SCALER_PATH

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def predict_employee_attrition(sample_data: dict) -> dict:
    """
    Predict attrition risk probability for a new employee.
    
    Args:
        sample_data: Dictionary containing employee attribute key-value pairs.
        
    Returns:
        Dictionary containing prediction result, probability, and risk level.
    """
    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        raise FileNotFoundError("Trained model artifacts not found. Please run main.py first.")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(MODEL_DIR / "feature_names.joblib")

    # Convert single dictionary record into DataFrame
    input_df = pd.DataFrame([sample_data])

    # Perform same dummy encoding
    encoded_df = pd.get_dummies(input_df)

    # Reindex columns to match exact feature names from training
    aligned_df = encoded_df.reindex(columns=feature_names, fill_value=0)

    # Scale numeric features
    X_scaled = scaler.transform(aligned_df)

    # Inference
    proba = model.predict_proba(X_scaled)[0, 1]
    prediction = int(proba >= 0.5)

    risk_level = "HIGH RISK" if proba >= 0.5 else ("MEDIUM RISK" if proba >= 0.3 else "LOW RISK")

    result = {
        "attrition_prediction": "Yes" if prediction == 1 else "No",
        "attrition_probability": round(float(proba) * 100, 2),
        "risk_level": risk_level,
    }

    return result


if __name__ == "__main__":
    # Example test record: High-risk profile (young, low pay, overtime, frequent travel, low satisfaction)
    sample_employee = {
        "Age": 24,
        "BusinessTravel": "Travel_Frequently",
        "DailyRate": 400,
        "Department": "Sales",
        "DistanceFromHome": 25,
        "Education": 2,
        "EducationField": "Marketing",
        "EnvironmentSatisfaction": 1,
        "Gender": "Male",
        "HourlyRate": 45,
        "JobInvolvement": 2,
        "JobLevel": 1,
        "JobRole": "Sales Representative",
        "JobSatisfaction": 1,
        "MaritalStatus": "Single",
        "MonthlyIncome": 2200,
        "MonthlyRate": 8000,
        "NumCompaniesWorked": 4,
        "OverTime": "Yes",
        "PercentSalaryHike": 12,
        "PerformanceRating": 3,
        "RelationshipSatisfaction": 2,
        "StockOptionLevel": 0,
        "TotalWorkingYears": 3,
        "TrainingTimesLastYear": 2,
        "WorkLifeBalance": 1,
        "YearsAtCompany": 1,
        "YearsInCurrentRole": 1,
        "YearsSinceLastPromotion": 0,
        "YearsWithCurrManager": 1,
    }

    print("\n--- SAMPLE EMPLOYEE ATTRITION RISK PREDICTION ---")
    res = predict_employee_attrition(sample_employee)
    print(f"Employee Age: {sample_employee['Age']} | Role: {sample_employee['JobRole']} | Dept: {sample_employee['Department']}")
    print(f"Monthly Income: ${sample_employee['MonthlyIncome']} | Overtime: {sample_employee['OverTime']} | Job Sat: {sample_employee['JobSatisfaction']}")
    print(f"-> Attrition Prediction: {res['attrition_prediction']}")
    print(f"-> Attrition Risk Score : {res['attrition_probability']}%")
    print(f"-> Risk Assessment Level: {res['risk_level']}")
    print("-------------------------------------------------\n")
