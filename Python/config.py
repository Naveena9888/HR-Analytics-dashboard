"""
Configuration settings for the HR Analytics & Employee Attrition Project.
Centralizes paths, plot aesthetics, column lists, and model parameters.
"""

from pathlib import Path

# Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "Dataset"
RAW_DATA_PATH = DATASET_DIR / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
CLEANED_DATA_PATH = DATASET_DIR / "HR_Cleaned.csv"

IMAGE_DIR = BASE_DIR / "Dashboard Images"
MODEL_DIR = BASE_DIR / "Python"
MODEL_PATH = MODEL_DIR / "attrition_model.joblib"
SCALER_PATH = MODEL_DIR / "scaler.joblib"
ENCODER_PATH = MODEL_DIR / "encoder.joblib"

# Ensure output directories exist
DATASET_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# Plot Aesthetic Settings
PLOT_STYLE = "seaborn-v0_8-whitegrid"
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
PALETTE = ["#2b5c8f", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02"]
ATTRITION_PALETTE = {"No": "#2b5c8f", "Yes": "#e74c3c"}
DPI = 300

# Columns definition
TARGET_COL = "Attrition"

CATEGORICAL_COLS = [
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime",
]

NUMERICAL_COLS = [
    "Age",
    "DailyRate",
    "DistanceFromHome",
    "Education",
    "EnvironmentSatisfaction",
    "HourlyRate",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "MonthlyIncome",
    "MonthlyRate",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]

CONSTANT_OR_ID_COLS = ["EmployeeCount", "EmployeeNumber", "Over18", "StandardHours"]
