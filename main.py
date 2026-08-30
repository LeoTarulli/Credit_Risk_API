from enum import Enum
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API - German Credit Risk Assessment",
    description="Predicción interactiva de riesgo crediticio basada en el dataset German Credit",
    version="1.0.0",
)

model = joblib.load("credit_model.pkl")
model_columns = joblib.load("model_columns.pkl")


class CheckingStatusEnum(str, Enum):
    no_checking = "no checking"
    less_0 = "<0"
    zero_to_200 = "0<=X<200"
    greater_200 = ">=200"


class CreditHistoryEnum(str, Enum):
    existing_paid = "existing paid"
    critical_other = "critical/other existing credit"
    delayed_previously = "delayed previously"
    all_paid = "all paid"
    no_credits_all_paid = "no credits/all paid"


class PurposeEnum(str, Enum):
    radio_tv = "radio/tv"
    new_car = "new car"
    furniture_equipment = "furniture/equipment"
    used_car = "used car"
    business = "business"
    education = "education"
    repairs = "repairs"
    domestic_appliance = "domestic appliance"
    other = "other"
    retraining = "retraining"


class SavingsStatusEnum(str, Enum):
    less_100 = "<100"
    no_known_savings = "no known savings"
    onehundred_to_500 = "100<=X<500"
    fivehundred_to_1000 = "500<=X<1000"
    greater_1000 = ">=1000"


class EmploymentEnum(str, Enum):
    one_to_4 = "1<=X<4"
    greater_7 = ">=7"
    four_to_7 = "4<=X<7"
    less_1 = "<1"
    unemployed = "unemployed"


class PersonalStatusEnum(str, Enum):
    male_single = "male single"
    female_div_dep_mar = "female div/dep/mar"
    male_mar_wid = "male mar/wid"
    male_div_sep = "male div/sep"


class OtherPartiesEnum(str, Enum):
    none = "none"
    guarantor = "guarantor"
    co_applicant = "co applicant"


class PropertyMagnitudeEnum(str, Enum):
    car = "car"
    real_estate = "real estate"
    life_insurance = "life insurance"
    no_known_property = "no known property"


class OtherPaymentPlansEnum(str, Enum):
    none = "none"
    bank = "bank"
    stores = "stores"


class HousingEnum(str, Enum):
    own = "own"
    rent = "rent"
    for_free = "for free"


class JobEnum(str, Enum):
    skilled = "skilled"
    unskilled = "unskilled"
    highqualif_selfemp = "highqualif / selfemp"
    unemp_unsk_nonres = "unemp/unsk/ nonres"


class OwnTelephoneEnum(str, Enum):
    none = "none"
    yes = "yes"


class ForeignWorkerEnum(str, Enum):
    yes = "yes"
    no = "no"



class CustomerData(BaseModel):
    # Numeric features
    duration: int = Field(..., ge=1, le=100, example=24)
    credit_amount: float = Field(..., gt=0, example=2500.0)
    installment_commitment: int = Field(..., ge=1, le=4, example=2)
    residence_since: int = Field(..., ge=1, le=4, example=2)
    age: int = Field(..., ge=18, le=100, example=35)
    existing_credits: int = Field(..., ge=1, le=4, example=1)
    num_dependents: int = Field(..., ge=1, le=2, example=1)

    # String features // The 3 points makes the campus mandatory
        # En ... → Define que el campo es obligatorio.
        # . → Accede a una categoría específica dentro de la clase Enum.
        # example=... → Define el ejemplo visual que muestra la documentación.
        
    checking_status: CheckingStatusEnum = Field(
        ..., example=CheckingStatusEnum.no_checking
    )
    credit_history: CreditHistoryEnum = Field(
        ..., example=CreditHistoryEnum.existing_paid
    )
    purpose: PurposeEnum = Field(..., example=PurposeEnum.radio_tv)
    savings_status: SavingsStatusEnum = Field(
        ..., example=SavingsStatusEnum.less_100
    )
    employment: EmploymentEnum = Field(..., example=EmploymentEnum.one_to_4)
    personal_status: PersonalStatusEnum = Field(
        ..., example=PersonalStatusEnum.male_single
    )
    other_parties: OtherPartiesEnum = Field(
        ..., example=OtherPartiesEnum.none
    )
    property_magnitude: PropertyMagnitudeEnum = Field(
        ..., example=PropertyMagnitudeEnum.car
    )
    other_payment_plans: OtherPaymentPlansEnum = Field(
        ..., example=OtherPaymentPlansEnum.none
    )
    housing: HousingEnum = Field(..., example=HousingEnum.own)
    job: JobEnum = Field(..., example=JobEnum.skilled)
    own_telephone: OwnTelephoneEnum = Field(
        ..., example=OwnTelephoneEnum.none
    )
    foreign_worker: ForeignWorkerEnum = Field(
        ..., example=ForeignWorkerEnum.yes
    )

# 4. API

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "API de Credit Risk activa. Accede a /docs para realizar pruebas.",
    }


@app.post("/predict")
def predict(customer: CustomerData):
    try:
        # 1. Transforming the input into a DataFrame
        df_input = pd.DataFrame([customer.model_dump()])

        # 2. Apply get_dummies
        df_encoded = pd.get_dummies(df_input)

        # 3. Aling exactly as the 36 columns which the model was trained
        df_final = df_encoded.reindex(columns=model_columns, fill_value=0)

        # 4. Predictting with the GaussianNB Model 
        pred = int(model.predict(df_final)[0])
        probabilities = model.predict_proba(df_final)[0]

        # Potential outcomes: 0 (Good - Low risk) and 1 (Bad - High risk)
        good_prob = float(probabilities[0])
        bad_prob = float(probabilities[1])

        status_label = "Good (Low risk)" if pred == 0 else "Bad (High risk)"
        approve_loan = bool(pred == 0)

        return {
            "prediction": pred,
            "status": status_label,
            "loan_approved": approve_loan,
            "confidence_probabilities": {
                "good_credit": round(good_prob, 4),
                "bad_credit": round(bad_prob, 4),
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error durante la predicción: {str(e)}"
        )