# Jannell's Car Sales

## Overview

This project demonstrates the implementation of a complete data engineering pipeline for Jannell's Car Sales. The goal was to integrate data from multiple sources, design a normalized database schema, and generate actionable insights for stakeholders. The project was part of a team project for the Data Engineering Bootcamp with Nashville Software School. I worked with my teammates [Andrew Gerhold](https://github.com/acgerhold) and [Rosemary Chadwick](https://github.com/Rosemary-Chadwick) and [Alison](https://github.com/AlisonCG1)

## Key Features

### 1. API Integration

- Authenticated with the API using a token-based system using python.
- Retrieved paginated data and dynamically created database tables to store the data.
- Automated the ingestion process using Python and SQLAlchemy.

---

### 2. CSV Data

- Loaded the csv data using pandas and sqlalchemy into the PostgreSQL database.

---

### 3. Database Design

- Designed an ER Diagram to connect the CSV data (`client_contact_status.csv`) with the API data.
- Created new tables and inserted data into them with stored procedures in PostgreSQL.
- Transformations were done to load into the database while maintaining referential integrity.

- Extended the database schema to include normalized tables in accordance with best practices.

---

### 4. Data Validation

- Initial validation with SQL queries
- Wrote Python scripts to validate data between the API, and database.

### 5. Business Reporting

- Created a consolidated view (`client_contact_status_view`) by joining multiple tables.
- Queried the database to extract insights based on business requirements.
- Exported the results to a CSV file and designed an Excel report for stakeholders.

- **Outcome**: Delivered a stakeholder-friendly report with actionable insights.

---

## Skills learned

- **Data Engineering**:
  - API integration, data transformation, and database design.
- **Database Management**:
  - PostgreSQL schema design, query optimization, and stored procedures.
- **Python Programming**:
  - Automating workflows with libraries like `requests`, `pandas`, and `sqlalchemy`.
- **Data Validation**:
  - Ensuring data consistency across multiple sources.
- **Reporting**:
  - Creating stakeholder-friendly reports in Excel.

---

## Future Improvements

- Automate the data validation as the data is loaded to database.
- Implement more robust error handling for API responses.
