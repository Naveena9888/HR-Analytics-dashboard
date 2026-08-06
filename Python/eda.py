"""
Exploratory Data Analysis (EDA) & Visualization module.
Generates statistical summaries, outlier reports, and saves publication-quality visualization charts.
"""

import logging
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from config import ATTRITION_PALETTE, DPI, IMAGE_DIR, PALETTE, PLOT_STYLE

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Set global seaborn/matplotlib style
plt.style.use("default")
sns.set_theme(style="whitegrid")


def generate_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Generate summary statistics for numerical variables."""
    stats = df.describe().T
    stats["skewness"] = df.select_dtypes(include=[np.number]).skew()
    logger.info("Descriptive statistics generated.")
    return stats


def detect_outliers_iqr(df: pd.DataFrame, columns: list[str]) -> dict:
    """Detect outliers using the Interquartile Range (IQR) method."""
    outlier_summary = {}
    for col in columns:
        if col in df.columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_summary[col] = {
                "count": len(outliers),
                "percentage": round(len(outliers) / len(df) * 100, 2),
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
            }
            logger.info(f"Outliers in {col}: {len(outliers)} ({outlier_summary[col]['percentage']}%)")
    return outlier_summary


def plot_attrition_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 1: Overall Attrition Count & Percentage Distribution."""
    plt.figure(figsize=(7, 5))
    ax = sns.countplot(
        data=df, x="Attrition", palette=ATTRITION_PALETTE, hue="Attrition", legend=False
    )
    plt.title("Employee Attrition Distribution", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Attrition Status", fontsize=11, fontweight="bold")
    plt.ylabel("Number of Employees", fontsize=11, fontweight="bold")

    total = len(df)
    for p in ax.patches:
        height = p.get_height()
        percentage = f"{100 * height / total:.1f}%"
        ax.annotate(
            f"{int(height)}\n({percentage})",
            (p.get_x() + p.get_width() / 2.0, height / 2.0),
            ha="center",
            va="center",
            fontsize=11,
            color="white",
            fontweight="bold",
        )

    plt.tight_layout()
    file_path = output_dir / "01_attrition_distribution.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def plot_department_attrition(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 2: Department-wise Attrition Distribution."""
    plt.figure(figsize=(9, 5))
    ax = sns.countplot(
        data=df, x="Department", hue="Attrition", palette=ATTRITION_PALETTE
    )
    plt.title("Department-wise Employee Attrition", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Department", fontsize=11, fontweight="bold")
    plt.ylabel("Employee Count", fontsize=11, fontweight="bold")
    plt.legend(title="Attrition", frameon=True)

    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f"{int(height)}",
                (p.get_x() + p.get_width() / 2.0, height + 5),
                ha="center",
                va="bottom",
                fontsize=9,
            )

    plt.tight_layout()
    file_path = output_dir / "02_department_attrition.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def plot_monthly_income_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 3: Monthly Income Distribution by Attrition."""
    plt.figure(figsize=(9, 5))
    sns.kdeplot(
        data=df,
        x="MonthlyIncome",
        hue="Attrition",
        common_norm=False,
        palette=ATTRITION_PALETTE,
        fill=True,
        alpha=0.4,
        linewidth=2,
    )
    plt.title("Monthly Income Distribution by Attrition", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Monthly Income ($)", fontsize=11, fontweight="bold")
    plt.ylabel("Density", fontsize=11, fontweight="bold")

    plt.tight_layout()
    file_path = output_dir / "03_monthly_income_distribution.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def plot_job_satisfaction_attrition(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 4: Job Satisfaction Rating vs Attrition Rate."""
    plt.figure(figsize=(8, 5))
    sat_df = (
        df.groupby("JobSatisfaction")["Attrition"]
        .apply(lambda x: (x == "Yes").sum() / len(x) * 100)
        .reset_index()
    )
    sat_df["Satisfaction_Label"] = sat_df["JobSatisfaction"].map(
        {1: "1 - Low", 2: "2 - Medium", 3: "3 - High", 4: "4 - Very High"}
    )

    ax = sns.barplot(
        data=sat_df, x="Satisfaction_Label", y="Attrition", palette="Reds_r", hue="Satisfaction_Label", legend=False
    )
    plt.title("Attrition Rate by Job Satisfaction Level", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Job Satisfaction Rating", fontsize=11, fontweight="bold")
    plt.ylabel("Attrition Rate (%)", fontsize=11, fontweight="bold")

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(
            f"{height:.1f}%",
            (p.get_x() + p.get_width() / 2.0, height + 0.5),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    plt.tight_layout()
    file_path = output_dir / "04_job_satisfaction_attrition.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def plot_overtime_vs_attrition(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 5: Overtime vs Attrition Rate."""
    plt.figure(figsize=(7, 5))
    ax = sns.countplot(
        data=df, x="OverTime", hue="Attrition", palette=ATTRITION_PALETTE
    )
    plt.title("Impact of Overtime on Employee Attrition", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Overtime Requirement", fontsize=11, fontweight="bold")
    plt.ylabel("Employee Count", fontsize=11, fontweight="bold")
    plt.legend(title="Attrition")

    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f"{int(height)}",
                (p.get_x() + p.get_width() / 2.0, height + 5),
                ha="center",
                va="bottom",
                fontsize=9,
            )

    plt.tight_layout()
    file_path = output_dir / "05_overtime_vs_attrition.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def plot_gender_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 6: Gender Distribution & Attrition Breakdown."""
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(
        data=df, x="Gender", hue="Attrition", palette=ATTRITION_PALETTE
    )
    plt.title("Gender Breakdown by Attrition Status", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Gender", fontsize=11, fontweight="bold")
    plt.ylabel("Employee Count", fontsize=11, fontweight="bold")
    plt.legend(title="Attrition")

    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f"{int(height)}",
                (p.get_x() + p.get_width() / 2.0, height + 5),
                ha="center",
                va="bottom",
                fontsize=9,
            )

    plt.tight_layout()
    file_path = output_dir / "06_gender_distribution.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 7: Correlation Heatmap for Key Numerical Metrics."""
    plt.figure(figsize=(10, 8))
    numeric_cols = [
        "Age",
        "DistanceFromHome",
        "JobLevel",
        "MonthlyIncome",
        "NumCompaniesWorked",
        "PercentSalaryHike",
        "TotalWorkingYears",
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsSinceLastPromotion",
        "YearsWithCurrManager",
    ]
    corr = df[numeric_cols].corr()

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )
    plt.title("Correlation Matrix of Key HR Numerical Metrics", fontsize=14, fontweight="bold", pad=15)

    plt.tight_layout()
    file_path = output_dir / "07_correlation_heatmap.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def plot_age_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Chart 8: Age Distribution by Attrition."""
    plt.figure(figsize=(9, 5))
    sns.histplot(
        data=df,
        x="Age",
        hue="Attrition",
        bins=20,
        kde=True,
        palette=ATTRITION_PALETTE,
        element="step",
        alpha=0.5,
    )
    plt.title("Age Distribution by Attrition Status", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Age (Years)", fontsize=11, fontweight="bold")
    plt.ylabel("Employee Count", fontsize=11, fontweight="bold")

    plt.tight_layout()
    file_path = output_dir / "08_age_distribution.png"
    plt.savefig(file_path, dpi=DPI)
    plt.close()
    logger.info(f"Saved: {file_path}")


def run_eda_pipeline(df: pd.DataFrame, output_dir: Path = IMAGE_DIR) -> None:
    """Execute all EDA visualizations and statistical checks."""
    logger.info("Starting EDA & Visualization Pipeline...")
    generate_descriptive_stats(df)
    detect_outliers_iqr(df, ["MonthlyIncome", "Age", "TotalWorkingYears", "YearsAtCompany"])
    
    plot_attrition_distribution(df, output_dir)
    plot_department_attrition(df, output_dir)
    plot_monthly_income_distribution(df, output_dir)
    plot_job_satisfaction_attrition(df, output_dir)
    plot_overtime_vs_attrition(df, output_dir)
    plot_gender_distribution(df, output_dir)
    plot_correlation_heatmap(df, output_dir)
    plot_age_distribution(df, output_dir)
    logger.info("EDA Pipeline completed successfully.")
