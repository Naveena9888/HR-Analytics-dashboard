# 📊 HR Analytics & Employee Attrition Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-ANSI%20%2F%20PostgreSQL-orange.svg)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Executive_Dashboard-yellow.svg)](https://powerbi.microsoft.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-green.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

An end-to-end data analytics and predictive modeling project designed to analyze employee retention drivers, identify key factors triggering workplace turnover, and predict employee attrition risk using the **IBM HR Analytics Employee Attrition dataset**.

---

## 🎯 Business Problem Statement

Human capital turnover imposes substantial replacement costs, loss of organizational knowledge, and operational disruption. Organizations struggle to pinpoint early warning signs of attrition before top talent leaves.

This project delivers an executive-grade analytics platform that:
1. **Identifies core root causes** of employee turnover across departments, compensation tiers, and demographic groups.
2. **Provides 25+ SQL analytical business queries** for deep-dive workforce management reporting.
3. **Presents an executive Power BI dashboard** for interactive decision-making.
4. **Deploys Machine Learning classification models** (Logistic Regression, Random Forest, Decision Tree) to predict at-risk employees and score flight probabilities.

---

## 📁 Repository Structure

```text
HR-Analytics-Dashboard/
│── Dataset/
│   ├── WA_Fn-UseC_-HR-Employee-Attrition.csv   # Raw IBM HR Dataset
│   └── HR_Cleaned.csv                           # Preprocessed Clean Dataset
│── Python/
│   ├── config.py                                # Configuration & Plot Aesthetics
│   ├── data_cleaning.py                         # Cleaning, Missing Value & Derived Fields
│   ├── eda.py                                   # Exploratory Analysis & Visualization Plotter
│   ├── ml_model.py                              # ML Model Training, Evaluation & Importances
│   ├── predict.py                               # Inference Script for New Employee Records
│   └── main.py                                  # Pipeline Orchestration Script
│── SQL/
│   ├── 01_schema_setup.sql                      # DDL Database Schema & Indexing
│   └── 02_business_queries.sql                  # 25 Analytical SQL Business Queries
│── PowerBI/
│   ├── dax_measures.dax                         # Complete Power BI DAX Formulas Library
│   └── powerbi_dashboard_guide.md               # Visual Blueprint & Dashboard Assembly Guide
│── Dashboard Images/                            # Exported Data Visualization Plots & Charts
│   ├── 01_attrition_distribution.png
│   ├── 02_department_attrition.png
│   ├── 03_monthly_income_distribution.png
│   ├── 04_job_satisfaction_attrition.png
│   ├── 05_overtime_vs_attrition.png
│   ├── 06_gender_distribution.png
│   ├── 07_correlation_heatmap.png
│   ├── 08_age_distribution.png
│   ├── 09_feature_importance.png
│   └── 10_confusion_matrix.png
│── requirements.txt                             # Python Package Dependencies
│── .gitignore                                  # Git Exclusion Rules
└── README.md                                    # Master Documentation
```

---

## ⚙️ Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Naveena9888/HR-Analytics-dashboard.git
cd HR-Analytics-dashboard
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the End-to-End Python Pipeline
```bash
python Python/main.py
```
*Executes cleaning, generates visualizations in `Dashboard Images/`, saves `Dataset/HR_Cleaned.csv`, trains ML models, and evaluates sample employee predictions.*

### 4. Test Single Employee Attrition Risk Prediction
```bash
python Python/predict.py
```

---

## 🔍 Data Pipeline & Exploratory Analysis Highlights

### Visual Artifacts Generated in `Dashboard Images/`
| Chart | File Name | Analytics Focus |
|---|---|---|
| 01 | `01_attrition_distribution.png` | Overall attrition count and percentage split |
| 02 | `02_department_attrition.png` | Departmental turnover comparison (Sales vs R&D vs HR) |
| 03 | `03_monthly_income_distribution.png` | Income density curve contrasting active vs departed staff |
| 04 | `04_job_satisfaction_attrition.png` | Turn-over percentage per job satisfaction tier (1-4) |
| 05 | `05_overtime_vs_attrition.png` | Comparative impact of overtime requirements |
| 06 | `06_gender_distribution.png` | Attrition rate across male and female employees |
| 07 | `07_correlation_heatmap.png` | Correlation matrix across numerical HR metrics |
| 08 | `08_age_distribution.png` | Turnover vulnerability across age brackets |
| 09 | `09_feature_importance.png` | Top 10 predictive drivers derived via Random Forest |
| 10 | `10_confusion_matrix.png` | Confusion matrix grid comparing classifier models |

---

## 🗄️ SQL Analytics Query Suite

`SQL/02_business_queries.sql` contains **25 production-ready analytical SQL queries**, including:
- **Core Workforce KPIs**: Total Staff, Attrition Rate %, Average Monthly Income, Average Tenure.
- **Demographic & Role Segmentation**: Department turnover, Job Role distribution, Gender & Age band analysis.
- **Compensation & Retention**: Department salary ranking (`DENSE_RANK() OVER (...)`), promotion lag (`YearsSinceLastPromotion`), salary band attrition rate.
- **Flight Risk Detection**: High-risk segment identification combining Overtime = 'Yes', Low Job Satisfaction (<=2), and Monthly Income < $3,500.

---

## 🤖 Machine Learning Model Comparison

Three classification algorithms were trained to predict employee attrition:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Logistic Regression** | **0.8673** | **0.6842** | **0.3421** | **0.4561** | **0.8125** |
| **Random Forest** | 0.8571 | 0.6429 | 0.2368 | 0.3462 | 0.7950 |
| **Decision Tree** | 0.8163 | 0.3750 | 0.2368 | 0.2903 | 0.6284 |

### Key Predictive Features:
1. `OverTime_Yes` (Strongest positive predictor of attrition)
2. `MonthlyIncome` (Lower salary strongly correlates with early turnover)
3. `TotalWorkingYears` & `Age` (Younger, early-career staff exhibit higher mobility)
4. `JobSatisfaction` & `EnvironmentSatisfaction`

---

## 📈 Key Business Insights & Recommendations

1. **Overtime is the Single Largest Driver**: Employees working overtime demonstrate an attrition rate nearly **3x higher** than non-overtime staff.
   - *Recommendation*: Implement mandatory cap on consecutive overtime hours and evaluate staffing capacity in bottleneck roles.
2. **Compensation Vulnerability in Entry-Level Roles**: Sales Representatives and Laboratory Technicians earning under $3,500/month display the highest turnover rate.
   - *Recommendation*: Review market compensation alignment for junior roles and establish transparent merit-based promotion pathways.
3. **Satisfaction & Environment Ratings Matter**: Over 50% of departed employees reported Job Satisfaction ratings of 1 or 2.
   - *Recommendation*: Conduct quarterly pulse surveys and empower managers with stay-interviews for employees showing satisfaction drop.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).

---

## ✍️ Author & Contact

**Naveena Indukuri**  
- **GitHub**: [@Naveena9888](https://github.com/Naveena9888)  
- **Project Repository**: [HR-Analytics-dashboard](https://github.com/Naveena9888/HR-Analytics-dashboard.git)
