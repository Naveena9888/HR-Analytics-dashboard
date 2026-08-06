-- ============================================================================
-- HR ANALYTICS & EMPLOYEE ATTRITION PROJECT
-- SQL Script 2: 25 Production Business Analytical Queries
-- Target DBMS: ANSI SQL / PostgreSQL / MySQL / SQL Server
-- ============================================================================

USE HRAnalytics;

-- ----------------------------------------------------------------------------
-- Q1: Total Employee Count
-- ----------------------------------------------------------------------------
SELECT COUNT(*) AS total_employees
FROM employees;

-- ----------------------------------------------------------------------------
-- Q2: Overall Attrition Count and Attrition Rate (%)
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees;

-- ----------------------------------------------------------------------------
-- Q3: Department-wise Attrition Breakdown & Rate
-- ----------------------------------------------------------------------------
SELECT 
    department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS department_attrition_rate_pct
FROM employees
GROUP BY department
ORDER BY department_attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- Q4: Average Monthly Salary & Compensation Metrics by Department
-- ----------------------------------------------------------------------------
SELECT 
    department,
    COUNT(*) AS total_staff,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    MIN(monthly_income) AS min_monthly_income,
    MAX(monthly_income) AS max_monthly_income
FROM employees
GROUP BY department
ORDER BY avg_monthly_income DESC;

-- ----------------------------------------------------------------------------
-- Q5: Average Years at Company & Total Working Tenure by Job Role
-- ----------------------------------------------------------------------------
SELECT 
    job_role,
    ROUND(AVG(years_at_company), 1) AS avg_years_at_company,
    ROUND(AVG(total_working_years), 1) AS avg_total_working_years
FROM employees
GROUP BY job_role
ORDER BY avg_years_at_company DESC;

-- ----------------------------------------------------------------------------
-- Q6: Overtime Requirement Impact on Employee Attrition
-- ----------------------------------------------------------------------------
SELECT 
    over_time,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY over_time;

-- ----------------------------------------------------------------------------
-- Q7: Gender Demographics and Attrition Rate Analysis
-- ----------------------------------------------------------------------------
SELECT 
    gender,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS gender_attrition_rate_pct
FROM employees
GROUP BY gender;

-- ----------------------------------------------------------------------------
-- Q8: Attrition Rate by Education Level & Education Field
-- ----------------------------------------------------------------------------
SELECT 
    education_field,
    education_level_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY education_field, education_level_name
ORDER BY attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- Q9: Job Satisfaction Score vs Attrition Count & Percentage
-- ----------------------------------------------------------------------------
SELECT 
    job_satisfaction,
    job_satisfaction_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY job_satisfaction, job_satisfaction_name
ORDER BY job_satisfaction ASC;

-- ----------------------------------------------------------------------------
-- Q10: Performance Rating Analysis & Attrition Correlation
-- ----------------------------------------------------------------------------
SELECT 
    performance_rating,
    COUNT(*) AS employee_count,
    ROUND(AVG(percent_salary_hike), 2) AS avg_percent_salary_hike,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY performance_rating;

-- ----------------------------------------------------------------------------
-- Q11: Top 10 Highest-Paying Job Roles in the Organization
-- ----------------------------------------------------------------------------
SELECT 
    job_role,
    department,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income
FROM employees
GROUP BY job_role, department
ORDER BY avg_monthly_income DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q12: Salary Bands Distribution & Attrition Rate
-- ----------------------------------------------------------------------------
SELECT 
    salary_band,
    COUNT(*) AS employee_count,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY salary_band
ORDER BY MIN(monthly_income) ASC;

-- ----------------------------------------------------------------------------
-- Q13: Age Groups Attrition Rate Breakdown
-- ----------------------------------------------------------------------------
SELECT 
    age_group,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY age_group
ORDER BY age_group ASC;

-- ----------------------------------------------------------------------------
-- Q14: Employee Distribution Across Job Roles
-- ----------------------------------------------------------------------------
SELECT 
    job_role,
    COUNT(*) AS employee_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2) AS pct_of_total_workforce
FROM employees
GROUP BY job_role
ORDER BY employee_count DESC;

-- ----------------------------------------------------------------------------
-- Q15: Top 10 Employees with Longest Tenure at Company
-- ----------------------------------------------------------------------------
SELECT 
    employee_number,
    department,
    job_role,
    years_at_company,
    total_working_years,
    monthly_income,
    attrition
FROM employees
ORDER BY years_at_company DESC, total_working_years DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q16: Monthly Income Summary Statistics across Departments
-- ----------------------------------------------------------------------------
SELECT 
    department,
    MIN(monthly_income) AS min_income,
    MAX(monthly_income) AS max_income,
    ROUND(AVG(monthly_income), 2) AS avg_income,
    ROUND(STDDEV(monthly_income), 2) AS stddev_income
FROM employees
GROUP BY department;

-- ----------------------------------------------------------------------------
-- Q17: Department Salary Ranking using Window Functions
-- ----------------------------------------------------------------------------
SELECT 
    employee_number,
    department,
    job_role,
    monthly_income,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY monthly_income DESC) AS dept_salary_rank
FROM employees
ORDER BY department, dept_salary_rank ASC;

-- ----------------------------------------------------------------------------
-- Q18: Stagnation & Promotion Delay Analysis (Years Since Last Promotion)
-- ----------------------------------------------------------------------------
SELECT 
    years_since_last_promotion,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY years_since_last_promotion
ORDER BY years_since_last_promotion ASC;

-- ----------------------------------------------------------------------------
-- Q19: Business Travel Frequency Impact on Attrition Rate
-- ----------------------------------------------------------------------------
SELECT 
    business_travel,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY business_travel
ORDER BY attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- Q20: Marital Status & Demographics vs Attrition
-- ----------------------------------------------------------------------------
SELECT 
    marital_status,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY marital_status
ORDER BY attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- Q21: High-Risk Employee Segment Identification
-- Criteria: OverTime='Yes', Low Job Satisfaction (<=2), Monthly Income < $3,500
-- ----------------------------------------------------------------------------
SELECT 
    employee_number,
    department,
    job_role,
    age,
    monthly_income,
    over_time,
    job_satisfaction,
    attrition
FROM employees
WHERE over_time = 'Yes' 
  AND job_satisfaction <= 2 
  AND monthly_income < 3500
ORDER BY monthly_income ASC;

-- ----------------------------------------------------------------------------
-- Q22: Work-Life Balance Rating Impact on Staff Retention
-- ----------------------------------------------------------------------------
SELECT 
    work_life_balance,
    work_life_balance_name,
    COUNT(*) AS employee_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY work_life_balance, work_life_balance_name
ORDER BY work_life_balance ASC;

-- ----------------------------------------------------------------------------
-- Q23: Distance From Home vs Attrition Rate (Commute Impact)
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN distance_from_home <= 5 THEN 'Near (0-5 km)'
        WHEN distance_from_home BETWEEN 6 AND 15 THEN 'Moderate (6-15 km)'
        ELSE 'Far (>15 km)'
    END AS commute_distance_category,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY 
    CASE 
        WHEN distance_from_home <= 5 THEN 'Near (0-5 km)'
        WHEN distance_from_home BETWEEN 6 AND 15 THEN 'Moderate (6-15 km)'
        ELSE 'Far (>15 km)'
    END
ORDER BY attrition_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- Q24: Job Level vs Salary & Attrition Correlation
-- ----------------------------------------------------------------------------
SELECT 
    job_level,
    COUNT(*) AS employee_count,
    ROUND(AVG(monthly_income), 2) AS avg_monthly_income,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) AS attrition_rate_pct
FROM employees
GROUP BY job_level
ORDER BY job_level ASC;

-- ----------------------------------------------------------------------------
-- Q25: Comprehensive Retention Risk Index Query
-- Calculates composite risk score based on high-risk factors
-- ----------------------------------------------------------------------------
SELECT 
    employee_number,
    department,
    job_role,
    monthly_income,
    over_time,
    job_satisfaction,
    (
        (CASE WHEN over_time = 'Yes' THEN 30 ELSE 0 END) +
        (CASE WHEN job_satisfaction <= 2 THEN 30 ELSE 0 END) +
        (CASE WHEN monthly_income < 3500 THEN 25 ELSE 0 END) +
        (CASE WHEN business_travel = 'Travel_Frequently' THEN 15 ELSE 0 END)
    ) AS flight_risk_score,
    attrition
FROM employees
ORDER BY flight_risk_score DESC, monthly_income ASC
LIMIT 20;
