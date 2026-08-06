-- ============================================================================
-- HR ANALYTICS & EMPLOYEE ATTRITION PROJECT
-- SQL Script 1: Database Setup, Schema Creation & Data Ingestion
-- Target DBMS: PostgreSQL / MySQL / SQL Server compatible
-- ============================================================================

-- 1. Database Creation
CREATE DATABASE HRAnalytics;
USE HRAnalytics;

-- 2. Employee Table Schema Definition
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_number INT PRIMARY KEY,
    age INT NOT NULL,
    attrition VARCHAR(5) NOT NULL,
    business_travel VARCHAR(30) NOT NULL,
    daily_rate INT,
    department VARCHAR(50) NOT NULL,
    distance_from_home INT,
    education INT,
    education_field VARCHAR(50),
    employee_count INT DEFAULT 1,
    environment_satisfaction INT,
    gender VARCHAR(10) NOT NULL,
    hourly_rate INT,
    job_involvement INT,
    job_level INT,
    job_role VARCHAR(50) NOT NULL,
    job_satisfaction INT,
    marital_status VARCHAR(20),
    monthly_income INT NOT NULL,
    monthly_rate INT,
    num_companies_worked INT,
    over_18 VARCHAR(2) DEFAULT 'Y',
    over_time VARCHAR(5) NOT NULL,
    percent_salary_hike INT,
    performance_rating INT,
    relationship_satisfaction INT,
    standard_hours INT DEFAULT 80,
    stock_option_level INT,
    total_working_years INT,
    training_times_last_year INT,
    work_life_balance INT,
    years_at_company INT,
    years_in_current_role INT,
    years_since_last_promotion INT,
    years_with_curr_manager INT,
    -- Derived Analytical Columns (From Cleaned Dataset)
    age_group VARCHAR(20),
    tenure_group VARCHAR(20),
    salary_band VARCHAR(30),
    education_level_name VARCHAR(30),
    job_satisfaction_name VARCHAR(20),
    environment_satisfaction_name VARCHAR(20),
    work_life_balance_name VARCHAR(20)
);

-- Indexing for Query Performance Optimization
CREATE INDEX idx_department ON employees(department);
CREATE INDEX idx_attrition ON employees(attrition);
CREATE INDEX idx_job_role ON employees(job_role);
CREATE INDEX idx_salary ON employees(monthly_income);

-- 3. Data Ingestion Statements
-- For PostgreSQL:
-- \copy employees FROM '../Dataset/HR_Cleaned.csv' WITH (FORMAT csv, HEADER true);

-- For MySQL:
-- LOAD DATA LOCAL INFILE '../Dataset/HR_Cleaned.csv'
-- INTO TABLE employees
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- For SQL Server:
-- BULK INSERT employees
-- FROM 'C:\Users\induk\Desktop\Project\HRAnalytics-dashboard\Dataset\HR_Cleaned.csv'
-- WITH (FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');
