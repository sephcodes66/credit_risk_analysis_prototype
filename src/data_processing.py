import pandas as pd

def get_column_names():
    """Returns the column names for the german credit dataset."""
    return [
        'status_of_existing_checking_account',
        'duration_in_month',
        'credit_history',
        'purpose',
        'credit_amount',
        'savings_account_bonds',
        'present_employment_since',
        'installment_rate_in_percentage_of_disposable_income',
        'personal_status_and_sex',
        'other_debtors_guarantors',
        'present_residence_since',
        'property',
        'age_in_years',
        'other_installment_plans',
        'housing',
        'number_of_existing_credits_at_this_bank',
        'job',
        'number_of_people_being_liable_to_provide_maintenance_for',
        'telephone',
        'foreign_worker',
        'risk'
    ]

def read_data(file_path):
    """Reads the german credit data from the specified path."""
    df = pd.read_csv(file_path, sep=r'\s+', header=None, names=get_column_names())
    return df

def transform_data(df):
    """Decodes categorical features and standardizes the target variable."""
    # A11: < 0 DM, A12: 0 <= ... < 200 DM, etc.
    status_map = {'A11': '< 0 DM', 'A12': '0 <= ... < 200 DM', 'A13': '>= 200 DM / salary assignments for at least 1 year', 'A14': 'no checking account'}
    df['status_of_existing_checking_account'] = df['status_of_existing_checking_account'].map(status_map)

    # A30: no credits taken, A31: all credits at this bank paid back, etc.
    credit_history_map = {'A30': 'no credits taken/ all credits paid back duly', 'A31': 'all credits at this bank paid back duly', 'A32': 'existing credits paid back duly till now', 'A33': 'delay in paying off in the past', 'A34': 'critical account/ other credits existing (not at this bank)'}
    df['credit_history'] = df['credit_history'].map(credit_history_map)

    # A40: car (new), A41: car (used), etc.
    purpose_map = {'A40': 'car (new)', 'A41': 'car (used)', 'A42': 'furniture/equipment', 'A43': 'radio/television', 'A44': 'domestic appliances', 'A45': 'repairs', 'A46': 'education', 'A47': 'vacation', 'A48': 'retraining', 'A49': 'business', 'A410': 'others'}
    df['purpose'] = df['purpose'].map(purpose_map)

    # A61: < 100 DM, A62: 100 <= ... < 500 DM, etc.
    savings_map = {'A61': '< 100 DM', 'A62': '100 <= ... < 500 DM', 'A63': '500 <= ... < 1000 DM', 'A64': '>= 1000 DM', 'A65': 'unknown/ no savings account'}
    df['savings_account_bonds'] = df['savings_account_bonds'].map(savings_map)

    # A71: unemployed, A72: < 1 year, etc.
    employment_map = {'A71': 'unemployed', 'A72': '< 1 year', 'A73': '1 <= ... < 4 years', 'A74': '4 <= ... < 7 years', 'A75': '>= 7 years'}
    df['present_employment_since'] = df['present_employment_since'].map(employment_map)

    # A91: male : divorced/separated, A92: female : divorced/separated/married, etc.
    personal_status_map = {'A91': 'male : divorced/separated', 'A92': 'female : divorced/separated/married', 'A93': 'male : single', 'A94': 'male : married/widowed', 'A95': 'female : single'}
    df['personal_status_and_sex'] = df['personal_status_and_sex'].map(personal_status_map)

    # A101: none, A102: co-applicant, etc.
    other_debtors_map = {'A101': 'none', 'A102': 'co-applicant', 'A103': 'guarantor'}
    df['other_debtors_guarantors'] = df['other_debtors_guarantors'].map(other_debtors_map)

    # A121: real estate, A122: building society savings agreement/ life insurance, etc.
    property_map = {'A121': 'real estate', 'A122': 'if not A121 : building society savings agreement/ life insurance', 'A123': 'if not A121/A122 : car or other, not in attribute 6', 'A124': 'unknown / no property'}
    df['property'] = df['property'].map(property_map)

    # A141: bank, A142: stores, etc.
    other_installment_plans_map = {'A141': 'bank', 'A142': 'stores', 'A143': 'none'}
    df['other_installment_plans'] = df['other_installment_plans'].map(other_installment_plans_map)

    # A151: rent, A152: own, etc.
    housing_map = {'A151': 'rent', 'A152': 'own', 'A153': 'for free'}
    df['housing'] = df['housing'].map(housing_map)

    # A171: unemployed/ unskilled, A172: unskilled - resident, etc.
    job_map = {'A171': 'unemployed/ unskilled - non-resident', 'A172': 'unskilled - resident', 'A173': 'skilled employee / official', 'A174': 'management/ self-employed/ highly qualified employee/ officer'}
    df['job'] = df['job'].map(job_map)

    # A191: none, A192: yes
    telephone_map = {'A191': 'none', 'A192': 'yes, registered under the customers name'}
    df['telephone'] = df['telephone'].map(telephone_map)

    # A201: yes, A202: no
    foreign_worker_map = {'A201': 'yes', 'A202': 'no'}
    df['foreign_worker'] = df['foreign_worker'].map(foreign_worker_map)

    # The original dataset uses 1 for Good and 2 for Bad. We map to 0 and 1.
    df['risk'] = df['risk'].map({1: 0, 2: 1})

    return df

def feature_engineering(df):
    """Engineers new features for the analysis."""
    # Create age groups
    age_bins = [0, 25, 60, 100]
    age_labels = ['Young', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['age_in_years'], bins=age_bins, labels=age_labels, right=False)

    # Calculate a 'payment pressure' metric. Add epsilon to avoid division by zero.
    df['payment_pressure'] = df['credit_amount'] / (df['duration_in_month'] + 1e-6)

    return df
