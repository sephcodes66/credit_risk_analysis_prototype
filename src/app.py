"""
This script runs the Streamlit dashboard for credit risk analysis.
"""
import streamlit as st
import os
import plotly.express as px
from src.data_processing import read_data, transform_data, feature_engineering

# Path to the data file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'german.data')

@st.cache_data
def load_data():
    """Loads, transforms, and engineers features from the german credit data."""
    raw_data = read_data(DATA_PATH)
    transformed_data = transform_data(raw_data)
    featured_data = feature_engineering(transformed_data)
    return featured_data

def portfolio_overview(df):
    """Displays the portfolio overview page."""
    st.title("Portfolio Overview")
    st.write("High-level overview of the credit portfolio.")

    # KPIs
    total_loan_amount = df['credit_amount'].sum()
    overall_default_rate = df['risk'].mean()
    average_loan_duration = df['duration_in_month'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Loan Amount", f"{total_loan_amount:,.0f} DM")
    col2.metric("Overall Default Rate", f"{overall_default_rate:.2%}")
    col3.metric("Average Loan Duration", f"{average_loan_duration:.1f} months")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Composition")
        risk_counts = df['risk'].value_counts().reset_index()
        risk_counts.columns = ['risk', 'count']
        risk_counts['risk'] = risk_counts['risk'].map({0: 'Good', 1: 'Bad'})
        fig = px.pie(risk_counts, values='count', names='risk', title='Good vs. Bad Risk', hole=0.3,
                     color_discrete_map={'Good': 'green', 'Bad': 'red'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Loan Purposes")
        purpose_counts = df['purpose'].value_counts().reset_index()
        purpose_counts.columns = ['purpose', 'count']
        st.bar_chart(purpose_counts.set_index('purpose'))

def risk_factor_deep_dive(df):
    """Displays the risk factor deep dive page."""
    st.title("Risk Factor Deep Dive")
    st.write("A deep dive into the factors affecting credit risk.")

    # Filters
    st.sidebar.header("Filters")
    age_range = st.sidebar.slider("Age Range", int(df['age_in_years'].min()), int(df['age_in_years'].max()), (int(df['age_in_years'].min()), int(df['age_in_years'].max())))
    credit_amount_range = st.sidebar.slider("Credit Amount Range", int(df['credit_amount'].min()), int(df['credit_amount'].max()), (int(df['credit_amount'].min()), int(df['credit_amount'].max())))
    
    purpose_options = df['purpose'].unique()
    selected_purposes = st.sidebar.multiselect("Loan Purpose", purpose_options, default=purpose_options)

    job_options = df['job'].unique()
    selected_jobs = st.sidebar.multiselect("Job Type", job_options, default=job_options)

    housing_options = df['housing'].unique()
    selected_housing = st.sidebar.multiselect("Housing Status", housing_options, default=housing_options)

    # Apply filters
    filtered_df = df[
        (df['age_in_years'] >= age_range[0]) & (df['age_in_years'] <= age_range[1]) &
        (df['credit_amount'] >= credit_amount_range[0]) & (df['credit_amount'] <= credit_amount_range[1]) &
        (df['purpose'].isin(selected_purposes)) &
        (df['job'].isin(selected_jobs)) &
        (df['housing'].isin(selected_housing))
    ]

    st.subheader("Filtered Data")
    st.write(f"{len(filtered_df)} records found.")

    if len(filtered_df) > 0:
        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Risk Distribution")
            risk_counts = filtered_df['risk'].value_counts().reset_index()
            risk_counts.columns = ['risk', 'count']
            risk_counts['risk'] = risk_counts['risk'].map({0: 'Good', 1: 'Bad'})
            fig = px.bar(risk_counts, x='risk', y='count', title='Good vs. Bad Risk', color='risk',
                         color_discrete_map={'Good': 'green', 'Bad': 'red'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Age, Credit Amount, and Risk")
            fig = px.scatter(filtered_df, x='age_in_years', y='credit_amount', color='risk',
                             title='Age vs. Credit Amount by Risk',
                             color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data matches the selected filters.")


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(layout="wide")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Portfolio Overview", "Risk Factor Deep Dive"])

    data = load_data()

    if page == "Portfolio Overview":
        portfolio_overview(data)
    elif page == "Risk Factor Deep Dive":
        risk_factor_deep_dive(data)

if __name__ == "__main__":
    main()
