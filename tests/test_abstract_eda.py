"""

FUNCTION TO GRADE FOR TESTING: test_viz_mean_temp_years()

The following script tests the exploratory data analysis (EDA) script functions from 
abstract_eda.py. Testing should be running using the $ pytest or $ pytest -v in the 
project environment from the repo root.

Parameters
----------
None
    This script takes no arguments, test data is generated from within the script by the 
    create_test_data() function below.

Returns
-------
None
    Prints the passed/failed tests in the terminal when using the $ pytest command.

Examples
--------
    $ pytest    (for concise output, from repo root)
    >>> collected 8 items

        tests/test_abstract_eda.py ........
                                                                                                                                                                                                                                                                           
        ======================= 8 passed in 4.80s =======================

    $ pytest -v     (for verbose output, from repo root) 
    >>> collected 8 items

        tests/test_abstract_eda.py::test_increment_filename PASSED
        tests/test_abstract_eda.py::test_add_prefix_to_increment PASSED
        tests/test_abstract_eda.py::test_read_clean_data PASSED
        tests/test_abstract_eda.py::test_viz_tabular_stats PASSED
        tests/test_abstract_eda.py::test_viz_mean_temp_years PASSED
        tests/test_abstract_eda.py::test_viz_linear_regression PASSED
        tests/test_abstract_eda.py::test_viz_seasonal_lines PASSED
        tests/test_abstract_eda.py::test_viz_density_dists PASSED

        ======================= 8 passed in 5.04s =======================

"""

# -----------------------------
# import libraries/packages
# -----------------------------
import pandas as pd
import altair as alt
import warnings
import os
import sys
import pytest
import subprocess

# -----------------------------
# Import the functions in scripts/abstract_eda.py to test below
# -----------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.abstract_eda import (increment_filename, 
                                  add_suffix_to_filename,
                                  read_clean_data,
                                  viz_tabular_stats,
                                  viz_mean_temp_years,
                                  viz_linear_regression,
                                  viz_seasonal_lines,
                                  viz_density_dists)

# -----------------------------
# Create test data for test functions below
# -----------------------------
def create_test_data() -> tuple[str, pd.DataFrame, str, pd.DataFrame, pd.DataFrame]:
    """
    Create reproducible test data for use in Pytest compatible functions below.

    Parameters
    ----------
    None

    Returns
    -------
    tuple[toy_path: str, toy_train_df: pd.DataFrame, empty_path: str, empty_df: pd.DataFrame]
        A tuple to unpack of the filepath and DataFrame test data objects to test.

    Typical Cases to test:
            toy_path: str  -- check expected output from valid input
            toy_train_df: pd.DataFrame()  -- check expected output from valid input

    
    Edge Cases to test:
            empty_path: str  -- default to images directory if none is provided
            empty_df: pd.DataFrame()  -- raise error if data is empty
            
    Examples
    --------
       toy_path, toy_train_df, empty_path, empty_df = create_test_data()
    >>> tuple[toy_path: str, toy_train_df: pd.DataFrame, empty_path: str, empty_df: pd.DataFrame, toy_train_df_big: pd.DataFrame]

    """

    toy_path = 'tests/eda_images/some_name.png'

    # Put at least two entries so std value shows in df.describe()
    toy_train_df = pd.DataFrame(
        {'Year': [2000, 2001], 
        'Month': [1, 2], 
        'Day': [1,2], 
        'Day of Year': [1, 33],
        'Anomaly': [-0.5, -1],
        'Temperature': [8.09, 7.59], 
        'Month_Name': ['January', 'February']}
    )

    empty_path = ''

    empty_df = pd.DataFrame()

    # Make sure the tests/eda_test_data folder exists for creating test data.
    # If folder does not exist in the repo for some reason run os.mkdir()
    if not os.path.exists('tests/eda_test_data'):
        os.mkdir('tests/eda_test_data')

    # Create the oy_train_df_big.csv if it does not exist, otherwise read the data
    if not os.path.exists('tests/eda_test_data/toy_train_df_big.csv'):
        # If the training data is not in the data folder run the preprocessing script
        if not os.path.exists('data/global_temp_anomaly_cleaned_train.csv'):
            # Run the preprocessing script if training data does not exist
            subprocess.run(['python', 
                            'scripts/data_preprocessing.py',
                            '--read_path=data/global_temp_anomaly_raw.csv',
                            '--write_path=data/global_temp_anomaly_cleaned',
                            '--plots_path=images',
                            '--logs_path=logs'])
            # Read the training data but sample only 20% of it with random state
            train_df_20pc = pd.read_csv('data/global_temp_anomaly_cleaned_train.csv'
                                        ).sample(frac=0.2, random_state=123)
            train_df_20pc.to_csv('tests/eda_test_data/toy_train_df_big.csv')
        
        # Otherwise read the training data but sample only 20% of it with random state
        else:
            train_df_20pc = pd.read_csv('data/global_temp_anomaly_cleaned_train.csv'
                                        ).sample(frac=0.2, random_state=123)
            train_df_20pc.to_csv('tests/eda_test_data/toy_train_df_big.csv')
        
        toy_train_df_big = pd.read_csv('tests/eda_test_data/toy_train_df_big.csv')
    else:
        toy_train_df_big = pd.read_csv('tests/eda_test_data/toy_train_df_big.csv')

    # Run the abstract_eda.py script to write the data to the tests/eda_test_data folder
    subprocess.run(['python', 
                    'scripts/abstract_eda.py',
                    'data/global_temp_anomaly_cleaned_train.csv',
                    'tests/eda_test_data/eda.png'])

    return toy_path, toy_train_df, empty_path, empty_df, toy_train_df_big

# Note that this writes the training data to the data folder if it does not exist for below
toy_path, toy_train_df, empty_path, empty_df, toy_train_df_big = create_test_data()

# ----------------------------- 
# FUNCTION TO GRADE FOR TESTING IN MILESTONE 4:
# ----------------------------- 
def test_viz_mean_temp_years():
    """
    Test viz_mean_temp_years from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_mean_temp_years(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), 'tests/eda_test_data/eda.png') , alt.LayerChart)
    # Typical example, check side effect functions properly generating png image
    assert os.path.exists('tests/eda_test_data/eda_mean_per_year_plot.png')

# ----------------------------- 
# OTHER FUNCTIONS WITH SIMPLE TESTS FOR QUICK CHECKS
# ----------------------------- 

def test_increment_filename():
    """
    Test increment_filename from abstract_eda.py script

    """
    
    # Return type check
    assert isinstance(increment_filename('images/eda_1.png'), str)
    # Typical example, check output
    assert increment_filename('images/eda_1.png') == 'images/eda_2.png'
    # Atypical example, check output
    assert increment_filename('images/eda_1_1.png') == 'images/eda_1_2.png'
    # Edge case example, check output
    assert increment_filename('')=='_1.png'


def test_add_suffix_to_filename():
    """
    Test add_prefix_to_increment from abstract_eda.py script

    """
     
    # Return type check
    assert isinstance(add_suffix_to_filename('images/eda_1.png', 'plot'), str)
    # Typical example, check output
    assert add_suffix_to_filename('images/eda.png','plot') == 'images/eda_plot.png'
    # Atypical example, check output
    assert add_suffix_to_filename('images/train_df.csv', 'table') == 'images/train_df_table.csv'

def test_read_clean_data():
    """
    Test read_clean_data from abstract_eda.py script

    """
    
    # Return Type Check
    assert isinstance(read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), pd.DataFrame)
    # Typical example, check all columns exist
    assert {'Year', 'Month', 'Day', 'Anomaly', 'Day of Year', 'Temperature', 'Month_Name'}.issubset(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv').columns)
    # Typical example, check that more rows are in training data rather than test data
    assert len(read_clean_data(
        'data/global_temp_anomaly_cleaned_test.csv')) < len(read_clean_data(
            'data/global_temp_anomaly_cleaned_train.csv'))

def test_viz_tabular_stats():
    """
    Test viz_tabular_stats from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert viz_tabular_stats(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), 'tests/eda_test_data/eda.png') is None
    # Typical example, check side effect functions properly generating csv tables
    assert os.path.exists('images/eda_training_data_info_table.csv')
    assert os.path.exists('images/eda_training_data_stats_table.csv')
    assert {'Column', 'Contains NA Values', 'Data Type'}.issubset(
        pd.read_csv('images/eda_training_data_info_table.csv'))
    assert len(pd.read_csv('images/eda_training_data_info_table.csv')) == 7
    assert {'Statistic', 'Year', 'Month', 'Day', 
            'Anomaly', 'Day of Year', 'Temperature'}.issubset(
        pd.read_csv('images/eda_training_data_stats_table.csv'))
    assert len(pd.read_csv('images/eda_training_data_stats_table.csv')) == 8

def test_viz_linear_regression():
    """
    Test viz_linear_regression from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_linear_regression(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'),  'tests/eda_test_data/eda.png') , alt.LayerChart)
    # Typical example, check side effect functions properly generating png image
    assert os.path.exists('tests/eda_test_data/eda_linear_fit_plot.png.png')

def test_viz_seasonal_lines():
    """
    Test viz_seasonal_lines from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_seasonal_lines(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), 'tests/eda_test_data/eda.png') , alt.LayerChart)
    # Typical example,  check side effect functions properly generating png images
    assert os.path.exists('tests/eda_test_data/eda_facet_by_month_plot.png.png')

def test_viz_density_dists():
    """
    Test viz_density_dists from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_density_dists(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), 'tests/eda_test_data/eda.png') , alt.LayerChart)
    # Typical example,  check side effect functions properly generating png images
    assert os.path.exists('tests/eda_test_data/eda_density_distributions_plot.png')