"""
Unit tests for the data processing module.
"""
import sys
import os
import pandas as pd
import pytest

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_processing import load_and_clean_data, get_peer_group_analysis

@pytest.fixture
def cleaned_data():
    """Pytest fixture to load the cleaned data once for all tests."""
    return load_and_clean_data()

def test_data_loading_and_shape(cleaned_data):
    """
    Tests if the data is loaded correctly and has the expected shape.
    """
    assert isinstance(cleaned_data, pd.DataFrame)
    # The dataset should have 1000 rows and 21 columns
    assert cleaned_data.shape == (1000, 21)

def test_data_decoding(cleaned_data):
    """
    Tests if a known coded value is correctly decoded to its text representation.
    For example, 'A11' in 'checking_account_status' should become '< 0 DM'.
    """
    # The first row of the raw data has 'A11' for the first column.
    # Let's check if it was decoded correctly.
    assert cleaned_data.iloc[0]['checking_account_status'] == '< 0 DM'
    # The first row of the raw data has '1' for the risk column.
    assert cleaned_data.iloc[0]['risk'] == 'Good'

def test_peer_group_analysis(cleaned_data):
    """
    Tests the peer group analysis function with a known peer group.
    """
    # Find a peer group we can reasonably expect to exist
    analysis = get_peer_group_analysis(cleaned_data, age=35, housing='Own', job='Skilled')

    assert analysis is not None
    assert 'peer_count' in analysis
    assert 'default_rate' in analysis
    assert 'purpose_counts' in analysis
    assert analysis['peer_count'] > 0
