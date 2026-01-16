import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os

@st.cache_resource
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    model_path = os.path.join(script_dir, 'churn_model.pkl')
    scaler_path = os.path.join(script_dir, 'scaler.pkl')
    
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    with open(scaler_path, 'rb') as file:
        scaler = pickle.load(file)
        
    return model, scaler

try:
    model, scaler = load_data()
except FileNotFoundError as e:
    st.error(f"Error loading files. Please check the paths. \n\nDetails: {e}")
    st.stop()

expected_columns = [
    'SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
    'gender_Male', 'Partner_Yes', 'Dependents_Yes',
    'PhoneService_Yes', 'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year',
    'PaperlessBilling_Yes', 'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check'
]

st.title("Telco Customer Churn Predictor")
st.markdown("""
This app uses a machine learning model to predict whether a customer is likely to cancel their service (churn).
Adjust the values below to test different customer profiles.
""")

col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 70.0)
    total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0)
    senior_citizen = st.selectbox("Senior Citizen?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

with col2:
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    paperless = st.selectbox("Paperless Billing?", ["Yes", "No"])

if st.button("Predict Churn Risk"):
    input_data = {
        'SeniorCitizen': senior_citizen,
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges,
        'Contract_One year': 1 if contract == "One year" else 0,
        'Contract_Two year': 1 if contract == "Two year" else 0,
        'InternetService_Fiber optic': 1 if internet_service == "Fiber optic" else 0,
        'InternetService_No': 1 if internet_service == "No" else 0,
        'PaymentMethod_Electronic check': 1 if payment_method == "Electronic check" else 0,
        'PaymentMethod_Mailed check': 1 if payment_method == "Mailed check" else 0,
        'PaymentMethod_Credit card (automatic)': 1 if payment_method == "Credit card (automatic)" else 0,
        'PaperlessBilling_Yes': 1 if paperless == "Yes" else 0
    }
    
    input_df = pd.DataFrame([input_data])
    
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
            
    input_df = input_df[expected_columns]
    
    
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)
    probability = model.predict_proba(input_scaled)[0][1]
    
    st.divider()
    if prediction[0] == 1:
        st.error(f"**High Churn Risk** (Probability: {probability:.1%})")
        st.write("Suggestion: Offer this customer a discount or a longer-term contract immediately.")
    else:
        st.success(f"**Low Churn Risk** (Probability: {probability:.1%})")
        st.write("This customer is likely to stay loyal.")