# Library Management System — Data Engineering Project

A complete data engineering project built on a Library Management System,
demonstrating the full data pipeline from database design to automated
ETL pipelines, analytical report generation, and data warehouse implementation.

---

## Tech Stack

- **Database:** MySQL 8.4
- **Languages:** Python 3, SQL
- **Data Processing:** pandas, PySpark (Apache Spark 3.5.3)
- **Pipeline Automation:** Apache Airflow
- **Libraries:** SQLAlchemy, mysql-connector-python, Faker, python-dotenv
- **Environment:** Linux (WSL), Windows
- **Version Control:** Git

---

## Project Structure

```
library-data-engineering/
├── 01-database/          # Operational database design
├── 02-etl-pipeline/      # ETL scripts and analytical reports
├── 03-data-warehouse/    # Star Schema warehouse and ETL
└── 04-airflow/           # Automated pipeline DAG
```

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

## 02 — ETL Pipeline

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
```
load_dim_member ──┐
load_dim_book   ──┼──→ load_fact_borrow
load_dim_date   ──┘
```

---

## Setup

### Prerequisites
- MySQL 8.4
- Python 3.8+
- Apache Spark / PySpark (for PySpark analysis)
- Apache Airflow (for pipeline automation)
- Java 17 (for PySpark)

### Environment Variables
Copy `.env.example` and fill in your values:
```
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
```

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

---

## Key Features

- ✅ Normalized relational database with constraints, indexes and stored procedures
- ✅ Python ETL pipeline generating 3 analytical reports across 1000+ records
- ✅ Star Schema data warehouse with fact and 3 dimension tables
- ✅ Snowflake Schema alternative design documented
- ✅ PySpark analysis using both DataFrame API and Spark SQL
- ✅ Apache Airflow DAG with 4 tasks, dependency ordering and retry logic
- ✅ SQL data validation — NULL checks, duplicate detection, logical date validation
- ✅ Secure credential management using python-dotenv