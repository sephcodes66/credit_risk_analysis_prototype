"""
Unit tests for the risk model engine.
"""
import sys
import os
import pytest

# Add the 'src' directory to the Python path to allow importing the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from risk_model import get_risk_assessment

def test_high_risk_profile():
    """
    Tests a profile that should clearly result in a 'High Risk' assessment.
    - Young, renting, high credit amount, long duration, unskilled.
    """
    assessment = get_risk_assessment(
        age=24,
        credit_amount=15000,
        duration=48,
        housing='Rent',
        job='Unskilled'
    )
    assert assessment['category'] == 'High Risk'
    # Calculation: 50(base) + 10(age) + 10(housing) + 20(amount) + 15(duration) + 10(job) = 115
    assert assessment['score'] == 115

def test_low_risk_profile():
    """
    Tests a profile that should clearly result in a 'Low Risk' assessment.
    - Older, owns home, small credit amount, short duration, management job.
    """
    assessment = get_risk_assessment(
        age=50,
        credit_amount=1500,
        duration=12,
        housing='Own',
        job='Management'
    )
    assert assessment['category'] == 'Low Risk'
    # Calculation: 50(base) - 10(age) - 15(housing) - 5(amount) - 20(job) = 0
    assert assessment['score'] == 0

def test_edge_case_no_rules_apply():
    """
    Tests a profile where minimal rules should apply.
    """
    assessment = get_risk_assessment(
        age=30,
        credit_amount=5000,
        duration=24,
        housing='For Free', # No rule for 'For Free'
        job='Skilled'       # No rule for 'Skilled'
    )
    # Only the base score should be applied.
    assert assessment['score'] == 50
    assert assessment['category'] == 'Medium Risk'
