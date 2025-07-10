#!/bin/bash
# This script activates the virtual environment and runs the Streamlit application.

# Set the PYTHONPATH to include the src directory
export PYTHONPATH=$(pwd)/src

# Activate the virtual environment
source .venv/bin/activate

# Run the Streamlit app
streamlit run src/app.py