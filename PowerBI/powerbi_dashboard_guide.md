# Power BI Dashboard Implementation Guide

## Executive HR Analytics & Employee Attrition Dashboard

This guide details the step-by-step procedure for assembling the executive Power BI dashboard using `Dataset/HR_Cleaned.csv` and `PowerBI/dax_measures.dax`.

---

## 1. Visual Layout Architecture

The report is structured into three interactive canvas pages:

### Page 1: Executive Attrition Overview
- **Top Header Bar**: Project Title, Corporate Logo, Date Slicer, and Dynamic Title Card (`[Dynamic KPI Title]`).
- **KPI Card Panel (Top Row)**:
  1. `Total Employees` (Card Visual)
  2. `Attrition Count` (Card Visual)
  3. `Attrition Rate %` (Card Visual with Conditional Formatting Red > 18%)
  4. `Average Salary` (Card Visual formatted as `$#,##0`)
  5. `Average Age` (Card Visual formatted as `0.0 Years`)
  6. `Average Tenure` (Card Visual formatted as `0.0 Years`)
- **Main Charts Panel**:
  - **Bar Chart**: `Attrition by Department` (X-axis: `Department`, Y-axis: `[Attrition Rate %]`).
  - **Horizontal Bar Chart**: `Attrition by Job Role` (Y-axis: `JobRole`, X-axis: `[Attrition Count]`).
  - **Donut Chart**: `Attrition by Gender` (Legend: `Gender`, Values: `[Attrition Count]`).
  - **Stacked Column Chart**: `Attrition by Education Field` (X-axis: `EducationField`, Legend: `Attrition`).
  - **Clustered Bar Chart**: `Attrition by OverTime` (X-axis: `OverTime`, Values: `[Attrition Count]`).

---

### Page 2: Compensation & Employee Satisfaction
- **Clustered Column Chart**: `Average Salary by Department & Job Level` (X-axis: `Department`, Legend: `JobLevel`, Y-axis: `[Average Salary]`).
- **Matrix / Heatmap Visual**: `Job Satisfaction vs Work-Life Balance` (Rows: `JobSatisfactionName`, Columns: `WorkLifeBalanceName`, Values: `[Attrition Rate %]`).
- **KDE / Histogram Chart**: `Monthly Income Distribution` (X-axis: `SalaryBand`, Legend: `Attrition`).
- **Pie Chart**: `Business Travel Breakdown` (Legend: `BusinessTravel`, Values: `[Total Employees]`).

---

### Page 3: Attrition Drivers & Risk Segmentation (Drill-Through Target)
- **Line & Clustered Column Chart**: `Age Group vs Attrition Rate & Avg Salary`.
- **Area Chart**: `Years at Company vs Attrition Count`.
- **Table Visual**: `High-Risk Employee Roster` (Columns: `EmployeeNumber`, `Department`, `JobRole`, `MonthlyIncome`, `OverTime`, `JobSatisfaction`, `YearsAtCompany`, `Attrition`).

---

## 2. Interactive Controls & Features

### Slicers Panel (Left Sidebar / Top Header)
Add single/multi-select slicers for:
1. `Department`
2. `Gender`
3. `Job Role`
4. `Education`
5. `Marital Status`
6. `OverTime`
7. `Business Travel`

### Dynamic Tooltips
- Create a tooltip page named `Employee Detail Tooltip`.
- Add cards for `MonthlyIncome`, `YearsSinceLastPromotion`, `PerformanceRating`, and `JobSatisfaction`.
- Set page type to **Tooltip** and link it to the main bar charts.

### Bookmarks & Page Navigation
- **Bookmark 1**: `Overview View` (Resets all slicer filters).
- **Bookmark 2**: `Overtime Risk Filter` (Pre-filters for `OverTime = Yes`).
- **Bookmark 3**: `Low Satisfaction Filter` (Pre-filters for `JobSatisfaction <= 2`).
- Add navigation buttons linking to these bookmarks in the top header.

---

## 3. Color Theme Palette Code

Configure Power BI Theme XML/JSON using these exact color codes:
- **Background**: `#F8FAFC` (Light Gray Slate)
- **Card Background**: `#FFFFFF` (Clean White)
- **Primary Accent**: `#1E3A8A` (Deep Navy)
- **Secondary Accent**: `#2563EB` (Royal Blue)
- **High Risk / Attrition Yes**: `#EF4444` (Crimson Red)
- **Low Risk / Attrition No**: `#10B981` (Emerald Green)
- **Text Color**: `#0F172A` (Dark Charcoal)
