from fastapi.testclient import TestClient
from main import app

# Initialize test client pointing directly to the FastAPI app instance
client = TestClient(app)

# Test 1: Verify API documentation endpoint responds with HTTP 200 OK
def test_docs_status():
    response = client.get("/docs")
    assert response.status_code == 200

# Test 2: Send a complete and valid payload; expect HTTP 200 and boolean inference
def test_predict_valid_payload():
    payload = {
        "checking_status": "no checking",
        "duration": 24,
        "credit_history": "existing paid",
        "purpose": "radio/tv",
        "credit_amount": 2500,
        "savings_status": "<100",
        "employment": "1<=X<4",
        "installment_commitment": 2,
        "personal_status": "male single",
        "other_parties": "none",
        "residence_since": 2,
        "property_magnitude": "car",
        "age": 35,
        "other_payment_plans": "none",
        "housing": "own",
        "existing_credits": 1,
        "job": "skilled",
        "num_dependents": 1,
        "own_telephone": "yes",
        "foreign_worker": "yes"
    }
    
    response = client.post("/predict", json=payload)
    
    # Assert successful status code
    assert response.status_code == 200
    
    data = response.json()
    # Assert the expected key exists and maps to a boolean value
    assert "loan_approved" in data
    assert isinstance(data["loan_approved"], bool)

# Test 3: Send an invalid payload; expect Pydantic validation failure (HTTP 422)
def test_predict_invalid_payload():
    invalid_payload = {
        "duration": "invalid_string_instead_of_int"
    }
    
    response = client.post("/predict", json=invalid_payload)
    
    # Pydantic schema validation should reject bad types with 422 Unprocessable Entity
    assert response.status_code == 422