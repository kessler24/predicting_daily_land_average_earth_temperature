"""

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
    $ pytest for concise output (from repo root)
    or
    $ pytest -v for verbose output (from repo root) 
    >>> 
        tests/test_abstract_eda.py::test_increment_filename PASSED
        tests/test_abstract_eda.py::test_add_prefix_to_increment PASSED
        tests/test_abstract_eda.py::test_read_clean_data PASSED
        tests/test_abstract_eda.py::test_viz_tabular_stats PASSED
        tests/test_abstract_eda.py::test_viz_mean_temp_years PASSED
        tests/test_abstract_eda.py::test_viz_linear_regression PASSED
        tests/test_abstract_eda.py::test_viz_seasonal_lines PASSED
        tests/test_abstract_eda.py::test_viz_density_dists PASSED

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

# -----------------------------
# Import the functions in scripts/abstract_eda.py to test below
# -----------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.abstract_eda import (increment_filename, 
                                  add_prefix_to_increment,
                                  read_clean_data,
                                  viz_tabular_stats,
                                  viz_mean_temp_years,
                                  viz_linear_regression,
                                  viz_seasonal_lines,
                                  viz_density_dists)

def create_test_data() -> tuple[str, pd.DataFrame, str, pd.DataFrame]:
    """
    Create reproducible test data for use in Pytest compatible functions below.

    Parameters
    ----------
    None

    Returns
    -------
    tuple[str, pd.DataFrame, str, pd.DataFrame]
        Typical Cases:
            toy_path: str
            toy_train_df: pd.DataFrame()

        Edge Cases:
            empty_path: str
            empty_df: pd.DataFrame()

    Examples
    --------
        toy_path, toy_train_df, empty_path, empty_df = create_test_data()

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

    return toy_path, toy_train_df, empty_path, empty_df

toy_path, toy_train_df, empty_path, empty_df = create_test_data()

"""
Test increment_filename from abstract_eda.py script
"""
def test_increment_filename():
    # Return type check
    assert isinstance(increment_filename('images/eda_1.png'), str)
    # Typical example, check output
    assert increment_filename('images/eda_1.png') == 'images/eda_2.png'
    # Atypical example, check output
    assert increment_filename('images/eda_1_1.png') == 'images/eda_1_2.png'

"""
Test add_prefix_to_increment from abstract_eda.py script
"""
def test_add_prefix_to_increment():
    # Return type check
    assert isinstance(add_prefix_to_increment('images/eda_1.png', 'plot'), str)
    # Typical example, check output
    assert add_prefix_to_increment('images/eda_1.png','plot') == 'images/eda_plot_1.png'
    # Atypical example, check output
    assert add_prefix_to_increment('images/train_df_1.csv', 'table') == 'images/train_df_table_1.csv'


"""
Test read_clean_data from abstract_eda.py script
"""
def test_read_clean_data():
    # Return Type Check
    assert isinstance(read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), pd.DataFrame)
    # Typical example, check all columns exist
    assert {'Year', 'Month', 'Day', 'Anomaly', 'Day of Year', 'Temperature', 'Month_Name'}.issubset(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv').columns)
    # Typical example, check that more rows are in training data rather than test data
    assert len(read_clean_data(
        'data/global_temp_anomaly_cleaned_test.csv')) < len(read_clean_data(
            'data/global_temp_anomaly_cleaned_train.csv'))

"""
Test viz_tabular_stats from abstract_eda.py script
"""
def test_viz_tabular_stats():
    # Return Type Check, Data exists in folder after this check
    assert viz_tabular_stats(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), 'images/eda.png') is None
    # Typical example, check side effect functions properly generating csv tables
    assert os.path.exists('images/eda_table_1.csv')
    assert os.path.exists('images/eda_table_2.csv')
    assert {'Column', 'Contains NA Values', 'Data Type'}.issubset(
        pd.read_csv('images/eda_table_1.csv'))
    assert len(pd.read_csv('images/eda_table_1.csv')) == 7
    assert {'Statistic', 'Year', 'Month', 'Day', 'Anomaly', 'Day of Year', 'Temperature'}.issubset(
        pd.read_csv('images/eda_table_2.csv'))
    assert len(pd.read_csv('images/eda_table_2.csv')) == 8

"""
Test viz_mean_temp_years from abstract_eda.py script
"""
def test_viz_mean_temp_years():
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_mean_temp_years(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), increment_filename('images/eda.png')) , str)
    # Typical example, check side effect functions properly generating png image
    assert os.path.exists('images/eda_plot_1.png')

"""
Test viz_linear_regression from abstract_eda.py script
"""
def test_viz_linear_regression():
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_linear_regression(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), increment_filename('images/eda.png')) , str)
    # Typical example, check side effect functions properly generating png image
    assert os.path.exists('images/eda_plot_2.png')


"""
Test viz_seasonal_lines from abstract_eda.py script
"""
def test_viz_seasonal_lines():
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_seasonal_lines(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), increment_filename('images/eda.png')) , str)
    # Typical example,  check side effect functions properly generating png images
    assert os.path.exists('images/eda_plot_3.png')


"""
Test viz_density_dists from abstract_eda.py script
"""
def test_viz_density_dists():
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_density_dists(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), increment_filename('images/eda.png')) , str)
    # Typical example,  check side effect functions properly generating png images
    assert os.path.exists('images/eda_plot_4.png')