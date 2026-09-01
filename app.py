import requests
import streamlit as st

# ------------------------------------
# Visual page settings
st.set_page_config(
    page_title="Credit Risk Test",
    page_icon="💳",
    layout="centered",
)

st.title("💳 Credit Risk Test")
st.write("Fill out all the fields in the form to check your status.")

st.divider()

# ------------------------------------
# Data Form

col1, col2 = st.columns(2)

with col1:
    st.subheader("Financials and loans")
    duration = st.slider("Duration of the loan (Months)", 1, 72, 24)

    credit_amount = st.number_input("Total requested (€)", min_value=100.0, value=2500.0, step=100.0)
    
    installment_commitment = st.slider("Installment rate (% of income)", 1, 4, 2)

    checking_status = st.selectbox( "Current Account Status", 
                                   ["no checking", "<0", "0<=X<200", ">=200"],)
    
    savings_status = st.selectbox("Saving Account Status",
                                   ["<100", "no known savings", "100<=X<500", "500<=X<1000", ">=1000"],
    )
    credit_history = st.selectbox(
        "Credit History",
        [
            "existing paid",
            "critical/other existing credit",
            "delayed previously",
            "all paid",
            "no credits/all paid",
        ],
    )
    purpose = st.selectbox(
        "Purpose of the loan",
        [
            "radio/tv",
            "new car",
            "furniture/equipment",
            "used car",
            "business",
            "education",
            "repairs",
            "domestic appliance",
            "other",
            "retraining",
        ],
    )
    other_payment_plans = st.selectbox(
        "Other's payment plans", ["none", "bank", "stores"]
    )

with col2:
    st.subheader("Personal details")
    age = st.number_input(
        "Age:", min_value=18, max_value=100, value=35
    )
    personal_status = st.selectbox(
        "marital status: ",
        ["male single", "female div/dep/mar", "male mar/wid", "male div/sep"],
    )
    employment = st.selectbox(
        "Employment: ", ["1<=X<4", ">=7", "4<=X<7", "<1", "unemployed"]
    )
    job = st.selectbox(
        "Job type: ",
        ["skilled", "unskilled", "highqualif / selfemp", "unemp/unsk/ nonres"],
    )
    housing = st.selectbox("Housing: ", ["own", "rent", "for free"])

    property_magnitude = st.selectbox(
        "Properties: ",
        ["car", "real estate", "life insurance", "no known property"],
    )
    residence_since = st.slider("Total years in the same address", 1, 4, 2)
    existing_credits = st.slider("Existing loans in this bank", 1, 4, 1)
    num_dependents = st.selectbox("Children: ", [1, 2])
    other_parties = st.selectbox(
        "3rd Parties: ", ["none", "guarantor", "co applicant"]
    )
    own_telephone = st.selectbox("Phone number: ", ["none", "yes"])
    foreign_worker = st.selectbox("Foreign worker: ", ["yes", "no"])

st.divider()

# ------------------------------------
# Execute evaluation

if st.button("Check results", type="primary", use_container_width=True):
    # Build the playload JSON
    payload = {
        "duration": duration,
        "credit_amount": credit_amount,
        "installment_commitment": installment_commitment,
        "residence_since": residence_since,
        "age": age,
        "existing_credits": existing_credits,
        "num_dependents": num_dependents,
        "checking_status": checking_status,
        "credit_history": credit_history,
        "purpose": purpose,
        "savings_status": savings_status,
        "employment": employment,
        "personal_status": personal_status,
        "other_parties": other_parties,
        "property_magnitude": property_magnitude,
        "other_payment_plans": other_payment_plans,
        "housing": housing,
        "job": job,
        "own_telephone": own_telephone,
        "foreign_worker": foreign_worker,
    }

    # Send data to FastAPLI
    try:
        response = requests.post("https://credit-risk-api-bpn4.onrender.com/predict", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.subheader("Analysis results:")

            if result["loan_approved"]:
                st.success("✅ **Loan Approved: The applicant is ELEGIBLE.**")
            else:
                st.error(
                    "❌ **Loan Denied: High risk applicant.**"
                )

            # Mostrar métricas de probabilidad
            prob_good = result["confidence_probabilities"]["good_credit"] * 100
            prob_bad = result["confidence_probabilities"]["bad_credit"] * 100

            st.write(f"**Level of low risk:** {prob_good:.1f}%")
            st.progress(int(prob_good))

        else:
            st.error(
                f"Error in the: {response.status_code} - {response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Not possible to connect with the API.")