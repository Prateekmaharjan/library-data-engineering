# Library Management System — Data Engineering Project

A complete data engineering project built on a Library Management System, 
demonstrating the full data pipeline from database design to automated 
ETL pipelines and data warehouse implementation.

---

## Tech Stack

- **Database:** MySQL
- **Languages:** Python, SQL
- **Data Processing:** pandas, PySpark (Apache Spark)
- **Pipeline Automation:** Apache Airflow
- **Libraries:** SQLAlchemy, mysql-connector-python, Faker
- **Environment:** Linux (WSL), Windows
- **Version Control:** Git

---

## Project Structure
library-data-engineering/
├── 01-database/          # Operational database design
├── 02-etl-pipeline/      # ETL scripts and data analysis
├── 03-data-warehouse/    # Star Schema warehouse and ETL
└── 04-airflow/           # Automated pipeline DAG

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
- `insert_fake_data.py` — generates 50+ realistic test records using Faker

---

## 02 — ETL Pipeline

Python scripts for extracting, transforming and loading library data:

- **`db_connection.py`** — MySQL connection setup
- **`etl_pipeline.py`** — main ETL pipeline with Extract, Transform, Load functions
- **`member_summary_etl.py`** — member borrowing summary report
- **`pyspark_analysis.py`** — large scale data analysis using PySpark
- **`library_borrow_summary_report.csv`** — sample ETL output report

**Key transformations:**
- Column renaming and standardization
- Overdue detection and days overdue calculation
- Borrowing status classification
- Automated CSV report generation

---

## 03 — Data Warehouse

Star Schema data warehouse design for analytical reporting:

**Fact Table:**
- `fact_borrow` — borrowing events with measurable metrics

**Dimension Tables:**
- `dim_member` — member details
- `dim_book` — book and author details (denormalized)
- `dim_date` — date dimension for time based analysis

**Key files:**
- `01_star_schema.sql` — warehouse schema (Snowflake Schema commented)
- `etl_to_warehouse.py` — ETL pipeline from operational DB to warehouse

---

## 04 — Airflow Automation

Apache Airflow DAG that automates the warehouse ETL pipeline:

- Scheduled daily execution
- Four tasks running in dependency order
- Dimension tables load before fact table
- Automatic retry on failure

**Task execution order:**
load_dim_member ──┐
load_dim_book  ──┼──→ load_fact_borrow
load_dim_date  ──┘

---

## Setup

### Prerequisites
- MySQL 8.0+
- Python 3.8+
- Apache Airflow (for automation)
- Java 17 (for PySpark)

### Environment Variables
Copy `.env.example` and set your values:
DB_PASSWORD=your_mysql_password
DB_HOST=localhost

### Database Setup
```sql
-- Run in order
01_schema.sql
02_constraints.sql
03_indexes.sql
insert_values.sql
```

### Running ETL Pipeline
```bash
python etl_pipeline.py
```

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

---

## Key Features

- ✅ Normalized relational database with constraints and indexes
- ✅ Python ETL pipeline with pandas and SQLAlchemy
- ✅ Star Schema data warehouse design
- ✅ Snowflake Schema alternative (commented in schema file)
- ✅ PySpark analysis for large scale data processing
- ✅ Apache Airflow automation with daily scheduling
- ✅ Data validation queries for quality assurance
- ✅ Automated report generation
