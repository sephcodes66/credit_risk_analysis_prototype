"""
This script runs the Streamlit dashboard for the RITA Interactive Risk Calculator.
"""
import streamlit as st
import pandas as pd
from risk_model import get_risk_assessment
from data_processing import load_and_clean_data, get_peer_group_analysis

# --- App Configuration ---
st.set_page_config(
    page_title="RITA Risk Calculator",
    page_icon="🧮",
    layout="wide"
)

# --- Data Loading ---
@st.cache_data
def load_data():
    """Load and cache the cleaned historical data."""
    return load_and_clean_data()

historical_data = load_data()


# --- App Header ---
st.title("RITA: Loan Application Risk Assessment")
st.write(
    "This prototype demonstrates how a risk management application (RITA) can be used "
    "to assess loan applications. Enter the applicant's details below to get a risk score."
)
st.markdown("---")

# --- Input Form ---
with st.form("risk_assessment_form"):
    st.subheader("Applicant Details")

    # Layout columns for a cleaner look
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Applicant Age", min_value=18, max_value=100, value=30, step=1)
        credit_amount = st.number_input("Credit Amount (€)", min_value=250, max_value=25000, value=5000, step=100)
        duration = st.slider("Loan Duration (Months)", min_value=6, max_value=72, value=24)

    with col2:
        housing = st.selectbox("Housing Status", options=['Own', 'Rent', 'For Free'], index=1)
        job = st.selectbox("Job Type", options=['Skilled', 'Unskilled', 'Management'], index=0)

    # Submit button for the form
    submitted = st.form_submit_button("Calculate Risk Score")


# --- Calculation and Results ---
if submitted:
    st.markdown("---")
    st.subheader("Risk Assessment Result")

    # Get the assessment from the risk model
    assessment = get_risk_assessment(
        age=age,
        credit_amount=credit_amount,
        duration=duration,
        housing=housing,
        job=job
    )

    score = assessment["score"]
    category = assessment["category"]
    explanation = assessment["explanation"]

    # Display the result with a color-coded metric
    if category == "High Risk":
        st.metric(label="Risk Category", value=category, delta=f"{score} Points - Poor", delta_color="inverse")
    elif category == "Medium Risk":
        st.metric(label="Risk Category", value=category, delta=f"{score} Points - Average", delta_color="off")
    else: # Low Risk
        st.metric(label="Risk Category", value=category, delta=f"{score} Points - Good", delta_color="normal")


    # --- Transparency Feature ---
    with st.expander("Show how this was calculated"):
        for step in explanation:
            st.text(step)

    st.markdown("---")

    # --- Peer Group Analysis ---
    st.subheader("Historical Peer Group Analysis")
    peer_analysis = get_peer_group_analysis(historical_data, age, housing, job)

    if peer_analysis:
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label=f"Historical Default Rate for {peer_analysis['peer_count']} Similar Applicants",
                value=f"{peer_analysis['default_rate']:.1%}"
            )
            st.info("This is the percentage of similar individuals from the past who were classified as 'Bad' risk.")

        with col2:
            st.write("**Most Common Loan Purposes for this Peer Group:**")
            st.bar_chart(peer_analysis['purpose_counts'])
    else:
        st.warning("Could not find a large enough peer group in the historical data for a meaningful comparison.")
