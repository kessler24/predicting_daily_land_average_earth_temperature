"""
Unit Tests for the Temperature Anomaly Forecasting Pipeline

This test suite validates critical functionality of the `ml_modelling.py` pipeline.

Test Coverage:
--------------
1. Input validation: ensures the input CSV contains required columns.
2. Train/test split behavior: validates error handling for invalid cutoff years.
3. Full pipeline execution: ensures the pipeline runs without errors and produces output files.
4. Forecast output correctness: checks the forecast CSV for correct number of rows/columns and numeric types.

How to Run:
------------
# From the project root, run all tests:
pytest tests/ml_test.py -v

# Run a single test function:
pytest tests/ml_test.py::test_full_pipeline_runs -v

# Notes:
# - The `tmp_path` fixture in pytest creates a temporary directory for isolated file testing.
# - The pipeline is invoked using `ml.main.callback(...)` to simulate command-line execution.
"""

import os
import sys
import pandas as pd
import pytest

# Ensure the 'scripts' folder is in the Python path so we can import the pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Import the pipeline module
import scripts.ml_modelling as ml


# -------------------------------------------------------------------
# Helper function: create a minimal valid dataset
# -------------------------------------------------------------------
def make_valid_df():
    """
    Generates a minimal valid dataset suitable for pipeline testing.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: 'Year', 'Month', 'Day', 'Anomaly'.
        Contains 4 rows of example anomalies.
    """
    return pd.DataFrame({
        "Year": [2010, 2010, 2011, 2011],
        "Month": [1, 1, 1, 1],
        "Day": [1, 2, 1, 2],
        "Anomaly": [0.2, 0.3, 0.4, 0.5]
    })


# -------------------------------------------------------------------
# TEST 1: Input validation for missing columns
# -------------------------------------------------------------------
def test_missing_required_columns(tmp_path):
    """
    Ensures the pipeline raises a ValueError if required columns are missing.
    
    - Missing 'Anomaly' column triggers an error.
    """
    df = pd.DataFrame({
        "Year": [2010],
        "Month": [1],
        "Day": [1]
        # 'Anomaly' column is intentionally missing
    })
    test_csv = tmp_path / "bad.csv"
    df.to_csv(test_csv, index=False)

    with pytest.raises(ValueError) as err:
        ml.main.callback(
            input_path=str(test_csv),
            output_dir=str(tmp_path),
            cutoff_year=2010
        )

    # Verify the error message mentions missing columns
    assert "must contain columns" in str(err.value)


# -------------------------------------------------------------------
# TEST 2: Invalid cutoff year handling
# -------------------------------------------------------------------
def test_invalid_cutoff_split(tmp_path):
    """
    Ensures the pipeline raises a ValueError if the train/test split is empty.
    
    - Using a cutoff_year larger than any dataset year results in an empty test set.
    """
    df = make_valid_df()
    test_csv = tmp_path / "data.csv"
    df.to_csv(test_csv, index=False)

    with pytest.raises(ValueError) as err:
        ml.main.callback(
            input_path=str(test_csv),
            output_dir=str(tmp_path),
            cutoff_year=3000  # deliberately too high
        )

    assert "Train or Test split is empty" in str(err.value)


# -------------------------------------------------------------------
# TEST 3: Full pipeline execution and output files
# -------------------------------------------------------------------
def test_full_pipeline_runs(tmp_path):
    """
    Tests that the full pipeline executes without errors and generates all expected output files:
    
    - model_results.csv
    - forecast_2030.csv
    - forecast_plot.png
    """
    df = make_valid_df()
    test_csv = tmp_path / "data.csv"
    df.to_csv(test_csv, index=False)

    outdir = tmp_path / "results"

    # Execute the pipeline
    ml.main.callback(
        input_path=str(test_csv),
        output_dir=str(outdir),
        cutoff_year=2010
    )

    # Check that all expected files were created
    assert (outdir / "model_results.csv").exists()
    assert (outdir / "forecast_2030.csv").exists()
    assert (outdir / "forecast_plot.png").exists()


# -------------------------------------------------------------------
# TEST 4: Forecast output correctness (shape and numeric types)
# -------------------------------------------------------------------
def test_forecast_value_shape(tmp_path):
    """
    Validates the forecast CSV output from the pipeline:

    1. Shape: expected 1 row, 4 columns (CSV index + Year, Temperature, Anomaly)
    2. Data types: 'Anomaly' and 'Temperature' must be numeric

    Note:
    - The CSV includes an index column by default, which is why there are 4 columns instead of 3.
    """
    df = make_valid_df()
    test_csv = tmp_path / "data.csv"
    df.to_csv(test_csv, index=False)

    outdir = tmp_path / "results"

    # Run the pipeline
    ml.main.callback(
        input_path=str(test_csv),
        output_dir=str(outdir),
        cutoff_year=2010
    )

    # Read forecast CSV
    forecast = pd.read_csv(outdir / "forecast_2030.csv")

    # Verify shape
    expected_shape = (1, 4)  # includes index
    assert forecast.shape == expected_shape, f"Expected shape {expected_shape}, got {forecast.shape}"

    # Verify numeric types
    assert pd.api.types.is_numeric_dtype(forecast["Anomaly"]), "Anomaly column must be numeric"
    assert pd.api.types.is_numeric_dtype(forecast["Temperature"]), "Temperature column must be numeric"
