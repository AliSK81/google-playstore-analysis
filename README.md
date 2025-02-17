# Google Play Store Data Analysis

**[Watch the Demo](https://drive.google.com/file/d/1r8GfgGVyj56qIhsO5HK8IE80V5kjlx4d/view?usp=sharing)**  

## Project Overview

This project focuses on analyzing **Google Play Store** app data to derive insights on market trends, app ratings, and
installation patterns. Key components include:

- **Data Preprocessing** (Cleaning and Formatting)
- **Database Management** (PostgreSQL)
- **Backend API** (FastAPI)
- **Interactive Dashboard** (Streamlit)
- **Query Optimization** (Performance Benchmarking)

---

## Project Structure

```
google-playstore-analysis/
│── backend/                # FastAPI backend
│   ├── venv/               # Virtual environment for backend dependencies
│   ├── database.py         # Database connection setup
│   ├── entities.py         # SQLAlchemy models for database tables
│   ├── main.py             # FastAPI app entry point
│   ├── models.py           # API data models (Pydantic)
│   └── requirements.txt    # Backend dependencies
│
│── frontend/               # Streamlit dashboard
│   ├── venv/               # Virtual environment for frontend dependencies
│   ├── app.py              # Main app UI
│   ├── average_rating_page.py   # Rating analysis component
│   ├── client_api.py       # Data fetching logic (API calls)
│   ├── filters.py          # Filters for app data
│   ├── manage_apps_page.py # Manage apps (create, update, delete)
│   ├── manage_categories_page.py # Manage categories (create, update, delete)
│   ├── manage_developers_page.py # Manage developers (create, update, delete)
│   ├── rating_distribution_page.py # Rating distribution chart
│   ├── release_trend_page.py    # Release trends chart
│   ├── requirements.txt    # Frontend dependencies
│   ├── search_apps_page.py # Search apps functionality
│   └── update_trend_page.py     # Update trend chart
│
│── notebooks/              # Jupyter Notebooks for analysis
│   └── data_cleaning.ipynb # Data preprocessing and cleaning notebook
│
│── sql/                    # SQL scripts
│   ├── indexes.sql         # Index optimization scripts
│   └── schema.sql          # Database schema creation
│
│── docs/                   # Documentation files
│   ├── report.docx         # Final project report
│   └── report.pdf          # PDF version of the report
│
│── data/                   # Processed and raw data
│   ├── cleaned_apps.csv    # Cleaned app data
│   ├── cleaned_categories.csv # Cleaned category data
│   ├── cleaned_developers.csv # Cleaned developer data
│   └── Google-Playstore.csv  # Raw dataset
│
├── .env                    # Environment variables for database connection
├── .gitignore              # Git ignore file
└── README.md               # Setup and usage guide
```

---

## Installation Guide

### Prerequisites

- **Python 3.10+**
- **PostgreSQL**
- **Pip (Package Manager)**
- **Jupyter Notebook** (for analysis)

### 1. Clone the Repository

```sh
git clone https://github.com/alisk81/google-playstore-analysis.git
cd google-playstore-analysis
```

### 2. Set Up PostgreSQL Database

1. Create the database:
   ```sh
   createdb playstore
   ```
2. Run the schema and indexing scripts:
   ```sh
   psql -d playstore -f sql/schema.sql
   psql -d playstore -f sql/indexes.sql
   ```

### 3. Set Up Environment Variables

Create a `.env` file with the following content:

```
DB_NAME=playstore
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Data Preprocessing and Import

To clean and process the data before inserting it into PostgreSQL:

```sh
cd notebooks
jupyter notebook data_cleaning.ipynb
```

This will produce cleaned data ready for import into PostgreSQL.

---

## Running the Project

### 1. Run the Backend (FastAPI)

```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

- **API Base URL:** `http://127.0.0.1:8000`

### 2. Run the Frontend (Streamlit)

```sh
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

- The dashboard will launch at **`http://localhost:8501`**.
