> **Note:** This is a fork of [marccass/Retail-Data-Warehousing-Project-Python-SQL](https://github.com/marccass/Retail-Data-Warehousing-Project-Python-SQL) (MIT licence). The original ETL pipeline and SQL analysis were written by marccass. My own additions are listed in the "My additions" section at the end of this README.
# End-to-End Retail Data Warehouse Pipeline

## 📌 Project Overview
This project simulates a real-world **Business Intelligence** environment. The goal is to transform raw sales data into a **Data Warehouse** optimized for business analytics.

I built a complete **ETL** (Extract, Transform, Load) pipeline using **Python** and modeled the data into a **Star Schema** architecture using **SQL**.

## 🛠 Tech Stack
* **Python:** Pandas (Data Cleaning), SQLAlchemy (ORM).
* **SQL:** SQLite, Window Functions, Joins, Aggregations.
* **Data Modeling:** Star Schema (Fact Table & Dimension Tables).
* **Visualization:** Matplotlib.

## 🏗 Architecture
Data is transformed from a flat file (`.csv`) into a relational model:
* **Fact Table:** `fact_vendes` (Transactions).
* **Dimensions:** `dim_clients` (Customers), `dim_productes` (Products), `dim_llocs` (Locations).

## 📊 Business Insights (Examples)
Leveraging advanced SQL queries, the analysis revealed that:
1.  The **Technology** category is the most profitable (17.4% margin).
2.  The **Furniture** category is critically underperforming (only 2.5% margin), suggesting potential issues with logistics costs.

## 🚀 How to Run
1.  Install dependencies: `pip install -r requirements.txt`
2.  Run ETL pipeline: `python scripts/etl_pipeline.py`
3.  Execute analysis: `python scripts/executar_sql.py`
