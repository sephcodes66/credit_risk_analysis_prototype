"""
This module contains the core logic for the RITA Risk Calculator.
It functions as a generic rule engine that reads its logic from an
external configuration file.
"""
import os
import json

# Define the path to the rules configuration file
RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'rules.json')

def _load_rules():
    """Loads the rules from the JSON configuration file."""
    with open(RULES_PATH, 'r') as f:
        return json.load(f)

def get_risk_assessment(age, credit_amount, duration, housing, job):
    """
    Calculates a risk score by dynamically applying rules from a config file.

    Args:
        age (int): Applicant's age in years.
        credit_amount (float): The amount of credit requested.
        duration (int): The loan duration in months.
        housing (str): The applicant's housing status ('Own', 'Rent', 'Free').
        job (str): The applicant's job type ('Skilled', 'Unskilled', 'Management').

    Returns:
        dict: A dictionary containing the final score, the risk category,
              and a detailed log of the calculation steps.
    """
    config = _load_rules()
    score = config['base_score']
    explanation = [f"Base Score: {score} points"]

    # Create a dictionary of the applicant's data to easily access fields
    applicant_data = {
        "age": age,
        "credit_amount": credit_amount,
        "duration": duration,
        "housing": housing,
        "job": job
    }

    # --- Rule Engine Logic ---
    for rule in config['rules']:
        field = rule['field']
        applicant_value = applicant_data.get(field)

        if applicant_value is None:
            continue

        for condition in rule['conditions']:
            eval_type = condition['type']
            compare_value = condition['value']
            points = condition['points']
            label = condition['label']

            match = False
            if eval_type == 'less_than' and applicant_value < compare_value:
                match = True
            elif eval_type == 'greater_than' and applicant_value > compare_value:
                match = True
            elif eval_type == 'equals' and applicant_value == compare_value:
                match = True

            if match:
                score += points
                explanation.append(f"{label} ({points:+} points). Current Score: {score}")
                # A field can only match one condition in a rule set
                break

    # --- Determine Risk Category ---
    category = "Low Risk" # Default category
    for cat in sorted(config['risk_categories'], key=lambda x: x['threshold'], reverse=True):
        if score >= cat['threshold']:
            category = cat['category']
            break

    explanation.append(f"Final Score: {score} -> {category}")

    return {
        "score": score,
        "category": category,
        "explanation": explanation
    }
