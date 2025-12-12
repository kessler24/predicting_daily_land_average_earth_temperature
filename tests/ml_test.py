"""
Unit tests for the Temperature Anomaly Forecasting Pipeline

This test suite validates key functionalities of the `ml_modelling.py` pipeline,
including:

1. Input validation (required columns)
2. Train/test split behavior
3. Full pipeline execution and output file generation
4. Forecast output correctness (shape and types)

Usage (from project root):
--------------------------
# Install required dependencies
pip install -r requirements.txt

# Run all tests with pytest
pytest tests/test_ml.py -v

# Run a single test function
pytest tests/test_ml.py::test_full_pipeline_runs -v
"""

import os
import sys
import pandas as pd
import pytest

# Ensure scripts folder is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Import the pipeline module
import scripts.ml_modelling as ml


# -------------------------------------------------------------------
# Helper: create minimal valid dataframe for testing
# -------------------------------------------------------------------
def make_valid_df():
    """
    Generates a minimal valid dataset to test the pipeline.

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns: Year, Month, Day, Anomaly
        Contains 4 rows of sample anomalies.
    """
    return pd.DataFrame({
        "Year": [2010, 2010, 2011, 2011],
        "Month": [1, 1, 1, 1],
        "Day": [1, 2, 1, 2],
        "Anomaly": [0.2, 0.3, 0.4, 0.5]
    })


# -------------------------------------------------------------------
# TEST 1: Missing required columns raises ValueError
# -------------------------------------------------------------------
def test_missing_required_columns(tmp_path):
    """
    Tests that the pipeline raises a ValueError if the input CSV
    does not contain all required columns.
    """
    df = pd.DataFrame({
        "Year": [2010],
        "Month": [1],
        "Day": [1],
        # Missing "Anomaly"
    })
    test_csv = tmp_path / "bad.csv"
    df.to_csv(test_csv, index=False)

    with pytest.raises(ValueError) as err:
        ml.main.callback(
            input_path=str(test_csv),
            output_dir=str(tmp_path),
            cutoff_year=2010
        )

    assert "must contain columns" in str(err.value)


# -------------------------------------------------------------------
# TEST 2: Invalid cutoff year causes empty split
# -------------------------------------------------------------------
def test_invalid_cutoff_split(tmp_path):
    """
    Tests that the pipeline raises a ValueError if the cutoff_year
    results in an empty train or test set.
    """
    df = make_valid_df()
    test_csv = tmp_path / "data.csv"
    df.to_csv(test_csv, index=False)

    # cutoff_year too high → all data in training, test = empty
    with pytest.raises(ValueError) as err:
        ml.main.callback(
            input_path=str(test_csv),
            output_dir=str(tmp_path),
            cutoff_year=3000
        )

    assert "Train or Test split is empty" in str(err.value)


# -------------------------------------------------------------------
# TEST 3: Full pipeline runs and outputs files
# -------------------------------------------------------------------
def test_full_pipeline_runs(tmp_path):
    """
    Tests that the full pipeline runs without errors and generates
    all expected output files: model_results.csv, forecast_2030.csv, forecast_plot.png
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

    # Check existence of output files
    assert (outdir / "model_results.csv").exists()
    assert (outdir / "forecast_2030.csv").exists()
    assert (outdir / "forecast_plot.png").exists()


# -------------------------------------------------------------------
# TEST 4: Check model forecast output shape and types
# -------------------------------------------------------------------
def test_forecast_value_shape(tmp_path):
    """
    Validates that the forecast CSV contains the expected number of rows/columns
    and that numeric columns are correctly typed.

    Note: Currently forecast_2030.csv includes the CSV index, resulting in 4 columns.
    """
    df = make_valid_df()
    test_csv = tmp_path / "data.csv"
    df.to_csv(test_csv, index=False)

    outdir = tmp_path / "results"

    # Run pipeline
    ml.main.callback(
        input_path=str(test_csv),
        output_dir=str(outdir),
        cutoff_year=2010
    )

    # Read forecast output
    forecast = pd.read_csv(outdir / "forecast_2030.csv")

    # Check shape: 1 row, 4 columns (includes index)
    assert forecast.shape == (1, 4), f"Expected shape (1,4), got {forecast.shape}"

    # Check numeric types for Anomaly and Temperature
    assert pd.api.types.is_numeric_dtype(forecast["Anomaly"]), "Anomaly column must be numeric"
    assert pd.api.types.is_numeric_dtype(forecast["Temperature"]), "Temperature column must be numeric"
