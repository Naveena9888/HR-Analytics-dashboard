"""
Machine Learning Module for Employee Attrition Prediction.
Trains Logistic Regression, Random Forest, and Decision Tree classifiers.
Evaluates metrics (Accuracy, Precision, Recall, F1, ROC-AUC), exports feature importances, and saves model artifacts.
"""

import logging
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from config import ATTRITION_PALETTE, DPI, IMAGE_DIR, MODEL_DIR, MODEL_PATH, SCALER_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def preprocess_ml_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str], StandardScaler]:
    """
    Prepare feature matrix X and target vector y for machine learning.
    Encodes categoricals, drops identifier/derived helper columns, and scales numeric features.
    """
    ml_df = df.copy()

    # Drop non-predictive or helper derived columns
    drop_cols = [
        "EmployeeCount",
        "EmployeeNumber",
        "Over18",
        "StandardHours",
        "AgeGroup",
        "TenureGroup",
        "SalaryBand",
        "EducationLevelName",
        "JobSatisfactionName",
        "EnvironmentSatisfactionName",
        "WorkLifeBalanceName",
    ]
    ml_df = ml_df.drop(columns=[c for c in drop_cols if c in ml_df.columns])

    # Binary target encoding
    y = (ml_df["Attrition"] == "Yes").astype(int).values
    X_df = ml_df.drop(columns=["Attrition"])

    # One-Hot Encoding for categorical features
    X_encoded = pd.get_dummies(X_df, drop_first=True)
    feature_names = X_encoded.columns.tolist()

    # Feature Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_encoded)

    logger.info(f"ML Preprocessing complete. Feature matrix shape: {X_scaled.shape}")
    return X_scaled, y, feature_names, scaler


def train_and_evaluate_models(
    X: np.ndarray, y: np.ndarray, feature_names: list[str], output_dir: Path = IMAGE_DIR
) -> dict:
    """Train Logistic Regression, Random Forest, and Decision Tree models and report metrics."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=6),
    }

    results = {}
    best_f1 = -1.0
    best_model_name = None
    best_model_obj = None

    plt.figure(figsize=(15, 4))

    for idx, (name, model) in enumerate(models.items(), 1):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_proba)
        cm = confusion_matrix(y_test, y_pred)

        results[name] = {
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1-Score": f1,
            "ROC-AUC": roc_auc,
            "Confusion Matrix": cm,
            "Model": model,
        }

        logger.info(
            f"Model [{name}] -> Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | ROC-AUC: {roc_auc:.4f}"
        )

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_obj = model

        # Plot Confusion Matrix
        plt.subplot(1, 3, idx)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
        plt.title(f"{name}\nConfusion Matrix", fontweight="bold")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")

    plt.tight_layout()
    cm_path = output_dir / "10_confusion_matrix.png"
    plt.savefig(cm_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved confusion matrix chart to {cm_path}")

    # Plot Feature Importance for Random Forest
    rf_model = models["Random Forest"]
    importances = rf_model.feature_importances_
    feat_df = (
        pd.DataFrame({"Feature": feature_names, "Importance": importances})
        .sort_values(by="Importance", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(9, 5))
    ax = sns.barplot(
        data=feat_df, x="Importance", y="Feature", palette="Blues_r", hue="Feature", legend=False
    )
    plt.title("Top 10 Feature Importances (Random Forest)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Feature Importance Score", fontsize=11, fontweight="bold")
    plt.ylabel("Feature", fontsize=11, fontweight="bold")

    for p in ax.patches:
        width = p.get_width()
        ax.annotate(
            f"{width:.4f}",
            (width + 0.001, p.get_y() + p.get_height() / 2.0),
            ha="left",
            va="center",
            fontsize=9,
        )

    plt.tight_layout()
    feat_path = output_dir / "09_feature_importance.png"
    plt.savefig(feat_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved feature importance chart to {feat_path}")

    logger.info(f"Best performing model by F1-Score: {best_model_name} (F1: {best_f1:.4f})")
    return results, best_model_obj, best_model_name


def run_ml_pipeline(df: pd.DataFrame) -> dict:
    """Full execution of machine learning pipeline."""
    logger.info("Starting Machine Learning Pipeline...")
    X, y, feature_names, scaler = preprocess_ml_data(df)
    results, best_model, best_model_name = train_and_evaluate_models(X, y, feature_names)

    # Save artifacts for prediction script
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(feature_names, MODEL_DIR / "feature_names.joblib")
    logger.info(f"Saved trained model artifacts to {MODEL_PATH}")

    return results
