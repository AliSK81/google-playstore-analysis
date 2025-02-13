# Google Play Store Data Analysis

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
│   ├── api_models.py       # API data models
│   ├── database.py         # Database connection setup
│   ├── db_models.py        # SQLAlchemy models
│   ├── main.py             # FastAPI app entry point
│   └── requirements.txt    # Backend dependencies
│
│── frontend/               # Streamlit dashboard
│   ├── app.py              # Main app UI
│   ├── average_rating.py   # Rating analysis component
│   ├── data_fetcher.py     # Data fetching logic
│   ├── filters.py          # Filters for app data
│   ├── rating_distribution.py # Rating distribution chart
│   ├── release_trend.py    # Release trends chart
│   ├── requirements.txt    # Frontend dependencies
│   ├── search_apps.py      # Search apps functionality
│   └── update_trend.py     # Update trend chart
│
│── notebooks/              # Jupyter Notebooks for analysis
│   └── data_cleaning.ipynb # Data preprocessing
│
│── sql/                    # SQL scripts
│   ├── indexes.sql         # Index optimization scripts
│   └── schema.sql          # Database schema creation
│
├── .env                    # Environment variables for database connection
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
