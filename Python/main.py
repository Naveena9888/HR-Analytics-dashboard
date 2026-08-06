"""
Main orchestration script for HR Analytics & Employee Attrition project.
Runs data cleaning, exploratory data analysis, chart generation, and ML model training end-to-end.
"""

import logging
import sys
from pathlib import Path

# Add Python module directory to path
sys.path.append(str(Path(__file__).resolve().parent))

from data_cleaning import run_data_pipeline
from eda import run_eda_pipeline
from ml_model import run_ml_pipeline
from predict import predict_employee_attrition

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    print("==========================================================================")
    print("      IBM HR ANALYTICS & EMPLOYEE ATTRITION PROJECT PIPELINE              ")
    print("==========================================================================")

    # 1. Data Cleaning & Feature Engineering
    logger.info("--- STEP 1: Running Data Cleaning & Preprocessing Pipeline ---")
    df_cleaned = run_data_pipeline()
    print(f"[SUCCESS] Data Pipeline Completed. Cleaned Dataset Shape: {df_cleaned.shape}")

    # 2. Exploratory Data Analysis & Visualizations
    logger.info("--- STEP 2: Running Exploratory Data Analysis & Visual Plotting ---")
    run_eda_pipeline(df_cleaned)
    print("[SUCCESS] EDA Visualizations Generated & Saved to 'Dashboard Images/'")

    # 3. Machine Learning Model Training & Evaluation
    logger.info("--- STEP 3: Training & Evaluating Machine Learning Models ---")
    results = run_ml_pipeline(df_cleaned)

    print("\n--- MODEL PERFORMANCE COMPARISON SUMMARY ---")
    print(f"{'Model Name':<22} | {'Accuracy':<9} | {'Precision':<9} | {'Recall':<9} | {'F1-Score':<9} | {'ROC-AUC':<9}")
    print("-" * 75)
    for model_name, metrics in results.items():
        print(
            f"{model_name:<22} | {metrics['Accuracy']:<9.4f} | {metrics['Precision']:<9.4f} | "
            f"{metrics['Recall']:<9.4f} | {metrics['F1-Score']:<9.4f} | {metrics['ROC-AUC']:<9.4f}"
        )
    print("-" * 75)

    # 4. Sample Inference Test
    logger.info("--- STEP 4: Testing Employee Risk Prediction Inference ---")
    sample_emp = {
        "Age": 26, "BusinessTravel": "Travel_Frequently", "DailyRate": 500, "Department": "Sales",
        "DistanceFromHome": 20, "Education": 2, "EducationField": "Marketing", "EnvironmentSatisfaction": 1,
        "Gender": "Female", "HourlyRate": 50, "JobInvolvement": 2, "JobLevel": 1,
        "JobRole": "Sales Representative", "JobSatisfaction": 1, "MaritalStatus": "Single",
        "MonthlyIncome": 2500, "MonthlyRate": 10000, "NumCompaniesWorked": 3, "OverTime": "Yes",
        "PercentSalaryHike": 11, "PerformanceRating": 3, "RelationshipSatisfaction": 1,
        "StockOptionLevel": 0, "TotalWorkingYears": 4, "TrainingTimesLastYear": 2,
        "WorkLifeBalance": 1, "YearsAtCompany": 1, "YearsInCurrentRole": 1,
        "YearsSinceLastPromotion": 0, "YearsWithCurrManager": 1
    }
    pred_res = predict_employee_attrition(sample_emp)
    print(f"Sample Test Prediction Result: {pred_res}")

    print("\n==========================================================================")
    print("      ALL PYTHON PIPELINE STEPS EXECUTED SUCCESSFULLY!                      ")
    print("==========================================================================")


if __name__ == "__main__":
    main()
