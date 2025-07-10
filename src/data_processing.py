"""
This module handles loading and processing the historical German Credit Data.
"""
import os
import pandas as pd

# Define the path to the data file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'german.data')

# Define the column names as per the dataset documentation
COLUMN_NAMES = [
    'checking_account_status', 'duration_months', 'credit_history', 'purpose',
    'credit_amount', 'savings_account', 'employment_duration', 'installment_rate',
    'personal_status_sex', 'other_debtors', 'present_residence_since', 'property',
    'age_years', 'other_installment_plans', 'housing', 'existing_credits', 'job',
    'dependents', 'telephone', 'foreign_worker', 'risk'
]

# Define the mapping for categorical variables from codes to human-readable text
# Based on the dataset documentation from UCI Machine Learning Repository
DECODING_MAP = {
    'checking_account_status': {'A11': '< 0 DM', 'A12': '0 - 200 DM', 'A13': '>= 200 DM', 'A14': 'No Account'},
    'credit_history': {'A30': 'No Credits/All Paid', 'A31': 'All Credits Paid', 'A32': 'Existing Credits Paid', 'A33': 'Past Delay', 'A34': 'Critical Account'},
    'purpose': {'A40': 'Car (New)', 'A41': 'Car (Used)', 'A42': 'Furniture/Equipment', 'A43': 'Radio/TV', 'A44': 'Appliances', 'A45': 'Repairs', 'A46': 'Education', 'A48': 'Retraining', 'A49': 'Business', 'A410': 'Other'},
    'savings_account': {'A61': '< 100 DM', 'A62': '100 - 500 DM', 'A63': '500 - 1000 DM', 'A64': '>= 1000 DM', 'A65': 'Unknown/No Savings'},
    'employment_duration': {'A71': 'Unemployed', 'A72': '< 1 Year', 'A73': '1 - 4 Years', 'A74': '4 - 7 Years', 'A75': '>= 7 Years'},
    'personal_status_sex': {'A91': 'Male: Divorced', 'A92': 'Female: Divorced/Married', 'A93': 'Male: Single', 'A94': 'Male: Married/Widowed', 'A95': 'Female: Single'},
    'other_debtors': {'A101': 'None', 'A102': 'Co-applicant', 'A103': 'Guarantor'},
    'property': {'A121': 'Real Estate', 'A122': 'Savings Agreement/Insurance', 'A123': 'Car or Other', 'A124': 'No Property'},
    'other_installment_plans': {'A141': 'Bank', 'A142': 'Stores', 'A143': 'None'},
    'housing': {'A151': 'Rent', 'A152': 'Own', 'A153': 'For Free'},
    'job': {'A171': 'Unemployed/Unskilled NR', 'A172': 'Unskilled Resident', 'A173': 'Skilled', 'A174': 'Management/Self-employed'},
    'telephone': {'A191': 'None', 'A192': 'Yes'},
    'foreign_worker': {'A201': 'Yes', 'A202': 'No'},
    'risk': {1: 'Good', 2: 'Bad'}
}

def load_and_clean_data():
    """
    Loads the raw german.data file, assigns column names, and decodes
    the categorical variables into a clean, human-readable DataFrame.

    Returns:
        pandas.DataFrame: The cleaned and decoded dataset.
    """
    # Load the data, specifying no header and space as the delimiter
    df = pd.read_csv(DATA_PATH, header=None, sep=r'\s+')
    df.columns = COLUMN_NAMES

    # Apply the decoding map to each relevant column
    for col, mapping in DECODING_MAP.items():
        df[col] = df[col].map(mapping)

    return df

def get_peer_group_analysis(df, age, housing, job):
    """
    Filters the historical data to find a peer group and calculates key metrics.

    Args:
        df (pandas.DataFrame): The cleaned historical data.
        age (int): The applicant's age.
        housing (str): The applicant's housing status ('Own', 'Rent', 'For Free').
        job (str): The applicant's job type ('Skilled', 'Unskilled', 'Management').

    Returns:
        dict: A dictionary containing the peer group's historical default rate
              and a breakdown of their loan purposes. Returns None if no peers found.
    """
    # Create an age bracket for more effective filtering
    age_bracket_min = age - 5
    age_bracket_max = age + 5

    # Map the app's simple job titles to the more detailed ones in the data
    job_mapping = {
        'Skilled': 'Skilled',
        'Unskilled': 'Unskilled Resident',
        'Management': 'Management/Self-employed'
    }
    mapped_job = job_mapping.get(job, 'Skilled') # Default to skilled if not found

    # Filter the DataFrame to find the peer group
    peer_group = df[
        (df['age_years'] >= age_bracket_min) &
        (df['age_years'] <= age_bracket_max) &
        (df['housing'] == housing) &
        (df['job'] == mapped_job)
    ]

    if peer_group.empty:
        return None

    # Calculate metrics
    default_rate = (peer_group['risk'] == 'Bad').mean()
    purpose_counts = peer_group['purpose'].value_counts()

    return {
        "peer_count": len(peer_group),
        "default_rate": default_rate,
        "purpose_counts": purpose_counts
    }
