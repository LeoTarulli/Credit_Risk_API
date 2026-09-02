# Credit Risk Assessment System

An end-to-end machine learning application that predicts loan approval and credit risk classification (Good / Bad credit) based on applicant demographic and financial data. The project includes exploratory data analysis, pipeline preprocessing, model tuning, a FastAPI serving backend, and an interactive Streamlit frontend.

---

**Features**

* **Data Processing & Encoding:** Data cleaning, duplicate removal, category normalization, and one-hot encoding aligned across 36 feature columns.
* **Model Selection & Tuning:** Trained and evaluated multiple classification algorithms, selecting a **Gaussian Naive Bayes (`GaussianNB`)** classifier optimized for recall via `GridSearchCV`.
* **REST API (FastAPI):** Strict payload validation using Pydantic models and Enums, returning binary credit risk labels (`0: Good / Low Risk`, `1: Bad / High Risk`), approval decisions, and prediction probabilities.
* **Web Interface (Streamlit):** User-friendly dashboard for entering applicant parameters and viewing instant real-time risk scores.

---

**Project Structure**

```text
├── credit_customers.csv   # Raw dataset from Kaggle
├── credit_model.pkl       # Serialized GaussianNB model
├── model_columns.pkl      # Serialized feature column list
├── main.py                # FastAPI application & schema definitions
├── app.py                 # Streamlit UI dashboard
├── requirements.txt       # Project dependencies
└── README.md
