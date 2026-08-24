import joblib
import numpy as np
from fastapi import FastAPI
from keras.models import load_model
from pydantic import BaseModel

# 1. Starting FastAPI
app = FastAPI(
    title="API - Testing Credit Risk",
    description="The purpose of this API is to predict if a customer is reliable for taking loans",
)

# 2. Importing the model and scaler model
model = load_model("credit_model.keras")
scaler = joblib.load("scaler.pkl")


# 3. Definir el esquema de datos de entrada (las 20 características)
# 3. Define the data schema for the entry (the 20 features)
class CustomerInput(BaseModel):
    features: list[float]  # Lista con los 20 valores numéricos del cliente


# 4. Ruta principal de prueba
@app.get("/")
def home():
    return {
        "Message": "Credit Risk API is active. Go to /docs for testing."
    }


# 5. Ruta de predicción
@app.post("/predict")
def prediction(cliente: CustomerInput):
    # Validar que ingresen exactamente 20 features
    if len(cliente.features) != 20:
        return {
            "error": f"20 characteristics were expected, but only received {len(cliente.features)}."
        }

    # 
    datos_cliente = np.array(cliente.features).reshape(1, -1)
    datos_escalados = scaler.transform(datos_cliente)

    # Predict
    prediccion_prob = model.predict(datos_escalados)[0][0]

    # Classification
    good = float(prediccion_prob) > 0.5
    resultado = "Good (Low risk)" if good else "Bad (High risk)"

    return {
        "Result": resultado,
        "Good_probabilities": round(float(prediccion_prob), 4),
        "Approve_loan": good,
    }