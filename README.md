# Credit Risk Analysis Prototype

## 1. Project Goal

The objective of this project is to develop a fully functional, interactive prototype for credit risk analysis. This project serves as a tangible demonstration of skills in Python, data engineering (ETL), data analysis, interactive visualization, and professional software development practices.

## 2. Architecture

The project is structured as follows:

-   **Data Ingestion & ETL (`src/ingest_data.py`):** A Python script to extract the raw "German Credit Data" from its source, transform it by decoding categorical variables and standardizing the target variable, and (intended to) load it into a PostgreSQL database.
-   **Database Schema (`src/schema.sql`):** A SQL script to create the `german_credit_data` table in a PostgreSQL database.
-   **Interactive Dashboard (`src/app.py`):** A Streamlit application that provides an interactive dashboard for exploring the credit risk data. It currently reads from the local data file but is designed to connect to the PostgreSQL database.
-   **Environment Management:** The project uses a Python virtual environment (`.venv`) and a `requirements.txt` file to manage dependencies. Database credentials are managed securely using a `.env` file.

## 3. How to Use the Tool

### Prerequisites

-   Python 3.9+
-   PostgreSQL (Optional, for full functionality)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate the virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Set up the PostgreSQL database:**
    -   Create a PostgreSQL database named `credit_risk_analysis`.
    -   Execute the `src/schema.sql` script to create the `german_credit_data` table.
    -   Update the `.env` file with your database credentials.

5.  **(Optional) Load the data into the database:**
    -   If you have set up the database, you can run the ETL script:
    ```bash
    python3 src/ingest_data.py
    ```

### Running the Application

To start the interactive dashboard, run the following command:

```bash
./run_app.sh
```

The application will open in your web browser. You can then navigate between the "Portfolio Overview" and "Risk Factor Deep Dive" pages to explore the data.

## 4. What the Tool Does

The Credit Risk Analysis Prototype provides two main views:

-   **Portfolio Overview:** This page gives a high-level overview of the credit portfolio, including key metrics like the total loan amount, the overall default rate, and the average loan duration. It also visualizes the composition of good vs. bad risk and the distribution of loan purposes.
-   **Risk Factor Deep Dive:** This page allows for a more detailed analysis of the factors affecting credit risk. You can use the interactive filters in the sidebar to slice the data by age, credit amount, loan purpose, job type, and housing status. The visualizations on this page will update dynamically based on your selections.
