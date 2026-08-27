import joblib
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel


# 1. Start FastAPI
app = FastAPI(
    title="Credit Risk API",
    description="API to predict whether a customer is a good or bad credit risk."
)


# 2. Load the trained model and scaler
model = joblib.load("credit_model.pkl")
scaler = joblib.load("scaler.pkl")


# 3. Define the input data
class CustomerInput(BaseModel):
    features: list[float]


# 4. Home endpoint
@app.get("/")
def home():
    return {
        "Message": "Credit Risk API is active. Go to /docs for testing."
    }


# 5. Prediction endpoint
@app.post("/predict")
def prediction(customer: CustomerInput):

    # Check that exactly 20 features were provided
    if len(customer.features) != 20:
        return {
            "error": f"20 features were expected, but received {len(customer.features)}."
        }

    # Convert input into NumPy array
    customer_data = np.array(customer.features).reshape(1, -1)

    # Apply the same scaler used during training
    scaled_data = scaler.transform(customer_data)

    # Predict class
    prediction = model.predict(scaled_data)[0]

    # Get probabilities
    probabilities = model.predict_proba(scaled_data)[0]

    good_probability = float(probabilities[0])
    bad_probability = float(probabilities[1])

    # Interpret prediction
    result = "Bad (High risk)" if prediction == 1 else "Good (Low risk)"

    # Loan decision
    approve_loan = prediction == 0

    return {
        "Result": result,
        "Good_probability": round(good_probability, 4),
        "Bad_probability": round(bad_probability, 4),
        "Approve_loan": approve_loan
    }