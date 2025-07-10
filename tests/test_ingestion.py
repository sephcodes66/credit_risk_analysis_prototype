"""
Tests for the data processing functions.
"""
import pandas as pd
import pytest
from src.data_processing import read_data, transform_data, get_column_names

@pytest.fixture
def raw_data():
    """Fixture to load the raw data for testing."""
    return read_data('data/german.data')

def test_read_data(raw_data):
    """Tests that the data is read correctly."""
    assert isinstance(raw_data, pd.DataFrame)
    assert len(raw_data) == 1000
    assert len(raw_data.columns) == 21
    assert raw_data.columns.tolist() == get_column_names()

def test_transform_data(raw_data):
    """Tests the data transformation logic."""
    transformed_data = transform_data(raw_data)

    # Test that the risk column is transformed correctly
    assert transformed_data['risk'].isin([0, 1]).all()

    # Test that categorical columns are decoded
    assert transformed_data['status_of_existing_checking_account'].iloc[0] == '< 0 DM'
    assert transformed_data['credit_history'].iloc[0] == 'critical account/ other credits existing (not at this bank)'

    # Test that data types are correct
    assert transformed_data['duration_in_month'].dtype == 'int64'
    assert transformed_data['credit_amount'].dtype == 'int64'
    assert transformed_data['risk'].dtype == 'int64'
