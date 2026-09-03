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
    duration = st.slider("Duration of the loan (Months)", 1, 36, 12)

    credit_amount = st.number_input("Total requested (€)", min_value=100.0, value=2500.0, step=100.0)
    
    installment_commitment = st.slider("Monthly installment burden (% of disposable income)", 
                                    min_value=1,
                                    max_value= 4,
                                    value=2,
                                    help="1 = Lowest share of income (<25%)\n\n 4 = Heavy share of income (>35%)")

    # Mapping checking status
    checking_status_mapping = {
            "No checking account": "no checking",
            "Overdrawn / In debt (<0)":"<0",
            "Less than 200€": "0<=x<200",
            "200€ or more": ">=200"
    }

    # Showing labels 
    selected_checking_label = st.selectbox( "Money in current account", options=list(checking_status_mapping.keys()))

    # Obtaining the value to send to the API
    checking_status = checking_status_mapping[selected_checking_label]


    # Mapping saving account
    saving_account_mapping = {
            "No savings": "no known savings",
            "Less than 100€":"<100",
            "Between 500€ and 1000€": "500<=X<1000",
            "More than 1000": ">=1000"
    }

    # Showing labels
    selected_savings_status = st.selectbox("Money in your saving accounts", options=list(saving_account_mapping.keys()))

    # Obtaining the value to send to the API
    savings_status = saving_account_mapping[selected_savings_status]



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
        "Age:", min_value=18, max_value=100, value=35)
    
    personal_status = st.selectbox(
        "marital status: ",
        ["male single", "female div/dep/mar", "male mar/wid", "male div/sep"],)

    # Mapping employment

    employment_mapping = {
        "Unemployed":"unemployed",
        "Less than a year":"<1",
        "Between 1 and 4 years":"1<=X<4",
        "Between 4 and 7 years": "4<=X<7",
        "More than 7 years": ">=7"
    }

    # YOE stands for years of employment
    selected_YOE = st.selectbox(
        "How many years of employment do you currently have?",
        options=list(employment_mapping.keys()))

    employment = employment_mapping[selected_YOE]
    
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