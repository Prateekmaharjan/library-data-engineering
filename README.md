# Library Management System — Data Analytics & Engineering Project

Analyzes library operations data to uncover borrowing trends, member activity patterns, and overdue risk — delivered through analytical reports and an interactive Tableau dashboard. Built on a full data pipeline covering database design, ETL, a Star Schema data warehouse, and dbt-based transformation and testing.

---

## Tech Stack

- **Database:** MySQL 8.4
- **Languages:** Python 3, SQL
- **Data Processing:** pandas, PySpark (Apache Spark 3.5.3)
- **Pipeline Automation:** Apache Airflow
- **Transformation Framework:** dbt Core 1.7 (with dbt-mysql adapter)
- **Visualization:** Tableau
- **Libraries:** SQLAlchemy, mysql-connector-python, Faker, python-dotenv
- **Environment:** Linux (WSL), Windows
- **Version Control:** Git
- **CI/CD:** GitHub Actions

---

## Project Structure

library-data-engineering/
├── 01-database/ # Operational database design
├── 02-etl-pipeline/ # ETL scripts and analytical reports
├── 03-data-warehouse/ # Star Schema warehouse and ETL
├── 04-airflow/ # Automated pipeline DAG
└── dbt-medallion/ # dbt medallion architecture implementation


---

## 01 — Database Design

Relational database schema for a library management system managing:
- Books and authors (many-to-many relationship)
- Members and borrowing records
- Book copies and availability tracking

**Key files:**
- `01_schema.sql` — table definitions
- `02_constraints.sql` — foreign keys and unique constraints
- `03_indexes.sql` — performance indexes
- `04_stored_procedures.sql` — reusable procedures
- `05_sample_queries.sql` — analytical queries
- `insert_fake_data.py` — generates 500+ realistic test records using Faker

---

## 02 — ETL Pipeline & Analytical Reports

Python ETL pipeline extracting, transforming and loading library data into
3 purpose-built analytical reports covering 1000+ borrow records:

- **`etl_pipeline.py`** — main ETL pipeline generating 3 analytical CSV reports
- **`pyspark_analysis.py`** — large scale data analysis using PySpark DataFrame API and Spark SQL

**Analytical Reports Generated:**

| Report | Description |
|--------|-------------|
| `report_most_borrowed_books.csv` | Books ranked by borrow count with author and availability status |
| `report_member_activity.csv` | Member borrow totals, return rates and activity level classification |
| `report_overdue_analysis.csv` | Overdue records with days overdue and severity rating (Low/Medium/High) |

**Key transformations:**
- Multi-table JOIN queries across 5 tables for book and member aggregations
- Activity level classification (High/Medium/Low) based on borrow frequency
- Overdue severity scoring using DATEDIFF calculations
- Automated report generation with report date stamping

---

## 03 — Data Warehouse

Star Schema data warehouse design for analytical reporting:

**Fact Table:**
- `fact_borrow` — borrowing events with measurable metrics (days borrowed, is_returned, is_overdue)

**Dimension Tables:**
- `dim_member` — member details
- `dim_book` — book and author details (denormalized)
- `dim_date` — date dimension for time based analysis

**Key files:**
- `01_star_schema.sql` — warehouse schema (Snowflake Schema commented as alternative design)
- `etl_to_warehouse.py` — ETL pipeline loading operational DB into Star Schema warehouse

---

## 04 — Airflow Automation

Apache Airflow DAG automating the full warehouse ETL pipeline:

- Scheduled daily execution
- 4 tasks running in dependency order with retry logic
- 3 dimension tables load in parallel before fact table

**Task execution order:**

load_dim_member ──┐
load_dim_book ──┼──→ load_fact_borrow
load_dim_date ──┘


---

## 05 — dbt Medallion Architecture

Alternative transformation approach using dbt, demonstrating medallion
architecture (bronze → silver → gold) on the same library dataset,
with automated data quality testing.

**Architecture:**

library_db (bronze — raw source)
↓
Staging models as views (silver — cleaned and standardized)
↓
Warehouse models as tables (gold — analytics ready)


**Silver Layer (views — no storage overhead):**
- `stg_members` — cleaned member data with standardized column names
- `stg_books` — books with author names concatenated using GROUP_CONCAT
- `stg_borrow_records` — borrow records with calculated metrics (days_borrowed, is_returned, is_overdue)

**Gold Layer (tables — stored in library_dw_dbt):**
- `dim_member` — member dimension table
- `dim_book` — book dimension with denormalized author data
- `dim_date` — date dimension generated for 2024–2026
- `fact_borrow` — fact table joining borrow records with book and date dimensions

**Data Quality Tests (10 automated tests):**

| Test | Column | Result |
|------|--------|--------|
| not_null | member_id | PASS |
| unique | member_id | PASS |
| not_null | member_name | PASS |
| unique | email | PASS |
| not_null | book_id | PASS |
| unique | book_id | PASS |
| not_null | title | PASS |
| not_null | borrow_id | PASS |
| unique | borrow_id | PASS |
| not_null | member_id (borrow) | PASS |

**Running dbt:**
```bash
cd dbt-medallion/library_dw
dbt run      # builds all models
dbt test     # runs all 10 data quality tests
```

---

## Setup

### Prerequisites
- MySQL 8.4
- Python 3.8+
- Apache Spark / PySpark (for PySpark analysis)
- Apache Airflow (for pipeline automation)
- Java 17 (for PySpark)
- dbt Core with dbt-mysql adapter (for medallion architecture)

### Environment Variables
Copy `.env.example` and fill in your values:

DB_PASSWORD=your_mysql_password
DB_HOST=localhost


### Database Setup
```sql
-- Run in order
01_schema.sql
02_constraints.sql
03_indexes.sql
```

### Running ETL Pipeline & Reports
```bash
python etl_pipeline.py
```
Generates 3 analytical CSV reports in the same directory.

### Running Data Warehouse ETL
```bash
python etl_to_warehouse.py
```

### Running PySpark Analysis
```bash
python pyspark_analysis.py
```

### Starting Airflow
```bash
airflow standalone
```

### Running dbt Medallion Pipeline
```bash
pip install dbt-mysql
cd dbt-medallion/library_dw
dbt run
dbt test
```

---

## Key Features

- ✅ Interactive Tableau dashboard visualizing borrowing trends and member activity
- ✅ Python ETL pipeline generating 3 analytical reports across 1000+ records
- ✅ Normalized relational database with constraints, indexes and stored procedures
- ✅ Star Schema data warehouse with fact and 3 dimension tables
- ✅ Snowflake Schema alternative design documented
- ✅ PySpark analysis using both DataFrame API and Spark SQL
- ✅ Apache Airflow DAG with 4 tasks, dependency ordering and retry logic
- ✅ dbt medallion architecture — bronze, silver and gold layers with 10 automated data quality tests
- ✅ SQL data validation — NULL checks, duplicate detection, logical date validation
- ✅ Secure credential management using python-dotenv
- ✅ CI/CD pipeline via GitHub Actions