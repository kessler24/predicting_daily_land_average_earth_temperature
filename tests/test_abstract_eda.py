"""

FUNCTION TO GRADE FOR TESTING: test_viz_mean_temp_years() -- other functions skipped by default for grading.

Please use the command for testing this function:

$ pytest tests/test_abstract_eda.py::test_viz_mean_temp_years -v  (verbose output, from repo root)  

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

Side Effects  
------------
Temperature scatter plot with mean temperature per year line .png generated, for example:
images/
    eda_mean_per_year_plot.png
tests_eda_test_data/
    toy_big_mean_per_year_plot.png

Examples
--------
If test and image data is already present or not you should run the entire test script:
-----------------------------
    
    $ pytest -v    (default output when script is ran skipping previously created tests not to be graded)
    >>> collected 8 items                                                             

        tests/test_abstract_eda.py::test_viz_mean_temp_years PASSED             [ 12%]
        tests/test_abstract_eda.py::test_increment_filename SKIPPED ()          [ 25%]
        tests/test_abstract_eda.py::test_add_suffix_to_filename SKIPPED ()      [ 37%]
        tests/test_abstract_eda.py::test_read_clean_data SKIPPED ()             [ 50%]
        tests/test_abstract_eda.py::test_viz_tabular_stats SKIPPED ()           [ 62%]
        tests/test_abstract_eda.py::test_viz_linear_regression SKIPPED ()       [ 75%]
        tests/test_abstract_eda.py::test_viz_seasonal_lines SKIPPED ()          [ 87%]
        tests/test_abstract_eda.py::test_viz_density_dists SKIPPED ()           [100%]

        ======================== 1 passed, 7 skipped in 12.39s ========================
    
    $ pytest    (for concise output if all tests are enabled, ran from repo root)
    >>> collected 8 items

        tests/test_abstract_eda.py ........
                                                                                                                                                                                                                                                                           
        ======================= 8 passed in 4.80s =======================

    $ pytest -v     (for verbose output if all tests are enabled, ran from repo root)
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

If test and image data is present you can test just the function directly to grade:
-----------------------------
    $ pytest tests/test_abstract_eda.py::test_viz_mean_temp_years -v  (verbose output, from repo root) 
        >>> collected 1 item 
                                                                       
            tests/test_abstract_eda.py::test_viz_mean_temp_years PASSED          [100%]

            ============================ 1 passed in 8.19s =============================
        
"""

# -----------------------------
# import libraries/packages
# -----------------------------
import pandas as pd
import altair as alt
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

    Typical cases for input to test:
            toy_path: str   
            check expected output from valid input

            toy_train_df: pd.DataFrame 
            check expected output from valid input
            
            toy_train_df_big: pd.DataFrame   
            check expected output from valid input

    Edge Cases fro input to test:
            empty_path: str     
            default to images directory if none is provided
            
            empty_df: pd.DataFrame    
            raise error if data is empty

    Parameters
    ----------
    None

    Returns
    -------
    tuple[toy_path: str, toy_train_df: pd.DataFrame, empty_path: str, empty_df: pd.DataFrame]
        A tuple to unpack of the filepath and DataFrame test data objects to test.
            
    Examples
    --------
       toy_path, toy_train_df, empty_path, empty_df = create_test_data()
    >>> tuple[toy_path: str, toy_train_df: pd.DataFrame, empty_path: str,
                 empty_df: pd.DataFrame, toy_train_df_big: pd.DataFrame]

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
            train_df_20pc.to_csv('tests/eda_test_data/toy_train_df_big.csv', index=False)
        
        # Otherwise read the training data but sample only 20% of it with random state
        else:
            train_df_20pc = pd.read_csv('data/global_temp_anomaly_cleaned_train.csv'
                                        ).sample(frac=0.2, random_state=123)
            train_df_20pc.to_csv('tests/eda_test_data/toy_train_df_big.csv', index=False)
        
        toy_train_df_big = pd.read_csv('tests/eda_test_data/toy_train_df_big.csv')
    else:
        toy_train_df_big = pd.read_csv('tests/eda_test_data/toy_train_df_big.csv')

    # Run the abstract_eda.py script to write the data to the tests/eda_test_data folder
    subprocess.run(['python', 
                    'scripts/abstract_eda.py',
                    'data/global_temp_anomaly_cleaned_train.csv',
                    'tests/eda_test_data/eda.png'])

    return toy_path, toy_train_df, empty_path, empty_df, toy_train_df_big

# Note that this writes the training data to the data folder if it does not exist for tests below
toy_path, toy_train_df, empty_path, empty_df, toy_train_df_big = create_test_data()

# -------------------------------------------- 
# FUNCTION TO GRADE FOR TESTING IN MILESTONE 4
# --------------------------------------------
def test_viz_mean_temp_years() -> None:
    """
    Test viz_mean_temp_years() function from abstract_eda.py script.

    This test checks the output of typical expected inputs, as well as 
    erroneous inputs to the function. Also check the expected errors are 
    raised by the function when tested with erroneous input.

    Parameters
    ----------
    None
        This script takes no arguments, test data is generated from within the script by the 
        create_test_data() function below.

    Returns
    -------
    None
        Prints the passed/failed tests in the terminal when using the $ pytest command.

    Side Effects  
    ------------
    Temperature scatter plot with mean temperature per year line .png generated, for example:
        images/
            eda_mean_per_year_plot.png
        tests_eda_test_data/
            toy_big_mean_per_year_plot.png

    Examples
    --------
    If test and image data is present you can test just the function directly to grade:
        $ pytest tests/test_abstract_eda.py::test_viz_mean_temp_years -v  (verbose output, from repo root) 
        >>> collected 1 item 
                                                                       
            tests/test_abstract_eda.py::test_viz_mean_temp_years PASSED          [100%]

            ============================ 1 passed in 8.19s =============================
    """
    
    # ---------------------------------------------
    # Checks on different expected input data
    # ---------------------------------------------

    # Get the training dataframe for some of the tests
    train_df = read_clean_data('data/global_temp_anomaly_cleaned_train.csv')

    # Return Type Check, data exists at plots_path once viz_mean_temp_years() is called
    assert isinstance(viz_mean_temp_years(train_df, 'tests/eda_test_data/eda.png') , alt.LayerChart)
    
    # Typical example, check side effect functions properly generating png image
    assert os.path.exists('tests/eda_test_data/eda_mean_per_year_plot.png')
    
    # Run checks on atypical toy_train_df
    assert isinstance(viz_mean_temp_years(toy_train_df, 'tests/eda_test_data/toy.png') , alt.LayerChart)
    
    # Typical example, check side effect functions properly generating png image
    assert os.path.exists('tests/eda_test_data/toy_mean_per_year_plot.png')
    
    # Edge case example empty filepath, use default plots_path value
    assert isinstance(viz_mean_temp_years(train_df, empty_path), alt.LayerChart)
    
    # Check that the image was still generated with the default filepath
    assert os.path.exists('images/eda_mean_per_year_plot.png')
    
    # ---------------------------------------------
    # Checks on different unexpected input data 
    # ---------------------------------------------

    # Check error raised when non-existent but non-empty directory passed in plots_path
    with pytest.raises(ValueError):
        viz_mean_temp_years(toy_train_df, 'fake_dir/eda.png')

    # Check invalid string for plots_path
    with pytest.raises(TypeError):
        viz_mean_temp_years(toy_train_df, 1)
    
    # Check erroneous input from integer
    with pytest.raises(TypeError):
        viz_mean_temp_years(1, 'tests/eda_test_data/eda.png')
    
    # Check erroneous input from empty dataframe
    with pytest.raises(ValueError):
        viz_mean_temp_years(empty_df, 'tests/eda_test_data/eda.png')

    # ---------------------------------------------
    # Checks on a preprocessed, validated dataFrame generated by create_test_data()
    # ---------------------------------------------
    
    # Validate toy_train_df_big from eda_test_data folder
    assert len(toy_train_df_big) > 1
    assert {'Year', 'Month', 'Day', 'Anomaly', 'Day of Year', 'Temperature'}.issubset(toy_train_df_big)
    assert len(toy_train_df_big.columns) == 7

    # Generated Layered Plot
    plot_layered = viz_mean_temp_years(toy_train_df_big, 'tests/eda_test_data/toy_big.png')

    # Check return type and image generated for toy_train_df_big exists in eda_test_data folder
    assert isinstance(plot_layered, alt.LayerChart)
    assert os.path.exists('tests/eda_test_data/toy_big_mean_per_year_plot.png')

    # ---------------------------------------------
    # Check the attributes of the chart are correct according to viz_mean_temp_years()
    # ---------------------------------------------

    # Check both layers exist and data exists in chart object
    assert len(plot_layered.layer) == 2
    assert len(plot_layered.data) > 1
    
    # Check axis titles, overall title and subtitles
    assert plot_layered.layer[1].encoding.x['title'] == 'Year'
    assert plot_layered.layer[1].encoding.y['title'] == 'Temperature [°C]'
    assert plot_layered.layer[1].title['text'] == 'Global Daily Average Land Temperature'
    assert plot_layered.layer[1].title['subtitle'] == 'Mean Temperature Indicated by Red Line'    

    # Check columns are encoded properly and are the right type (T, Q)
    assert plot_layered.layer[0].encoding.x['shorthand'] == 'Year:T'
    assert plot_layered.layer[1].encoding.x['shorthand'] == 'Year:T'
    assert plot_layered.layer[0].encoding.y['shorthand'] == 'Temperature:Q'
    assert plot_layered.layer[1].encoding.y['shorthand'] == 'mean(Temperature):Q'

    # Check layer mark types
    assert plot_layered.layer[0].mark['type'] == 'point'
    assert plot_layered.layer[1].mark['type'] == 'line'


test_viz_mean_temp_years()

# ----------------------------- 
# OTHER FUNCTIONS WITH SIMPLE TESTS FOR QUICK SANITY CHECKS
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

    # ---------------------------------------------
    # Skip pytest on this function, comment out line below or milestone 4 grading purposes. 
    # Comment line below if data is present and you want to run $ pytest on all test functions
    # ---------------------------------------------
    pytest.skip('\nTest viz_mean_temp_years only')


def test_add_suffix_to_filename():
    """
    Test add_prefix_to_increment from abstract_eda.py script

    """
     
    # Return type check
    assert isinstance(add_suffix_to_filename('images/eda_1.png', 'plot'), str)
    # Typical example, check output
    assert add_suffix_to_filename('images/eda.png','plot') == 'images/eda_plot.png'
    # Typical example, check output
    assert add_suffix_to_filename('images/train_df.csv', 'table') == 'images/train_df_table.csv'

    # ---------------------------------------------
    # Skip pytest on this function, comment out line below or milestone 4 grading purposes. 
    # Comment line below if data is present and you want to run $ pytest on all test functions
    # ---------------------------------------------
    pytest.skip('\nTest viz_mean_temp_years only')

def test_read_clean_data():
    """
    Test read_clean_data from abstract_eda.py script

    """
    
    # Return Type Check
    assert isinstance(read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), pd.DataFrame)
    # Typical example, check all columns exist
    assert {'Year', 'Month', 'Day', 'Anomaly', 'Day of Year', 'Temperature', 'Month_Name'}.issubset(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv').columns)
    # Check that dataframe has at least one row
    assert len(read_clean_data('data/global_temp_anomaly_cleaned_train.csv')) > 0

    # ---------------------------------------------
    # Skip pytest on this function, comment out line below or milestone 4 grading purposes. 
    # Comment line below if data is present and you want to run $ pytest on all test functions
    # ---------------------------------------------
    pytest.skip('\nTest viz_mean_temp_years only')

def test_viz_tabular_stats():
    """
    Test viz_tabular_stats from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert viz_tabular_stats(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), 'tests/eda_test_data/eda.png') is None
    # Typical example, check side effect functions properly generating csv tables
    assert os.path.exists('tests/eda_test_data/eda_training_data_info_table.csv')
    assert os.path.exists('tests/eda_test_data/eda_training_data_stats_table.csv')
    assert {'Column', 'Contains NA Values', 'Data Type'}.issubset(
        pd.read_csv('tests/eda_test_data/eda_training_data_info_table.csv'))
    assert len(pd.read_csv('tests/eda_test_data/eda_training_data_info_table.csv')) == 7
    assert {'Statistic', 'Year', 'Month', 'Day', 
            'Anomaly', 'Day of Year', 'Temperature'}.issubset(
        pd.read_csv('tests/eda_test_data/eda_training_data_stats_table.csv'))
    assert len(pd.read_csv('tests/eda_test_data/eda_training_data_stats_table.csv')) == 8

    # ---------------------------------------------
    # Skip pytest on this function, comment out line below or milestone 4 grading purposes. 
    # Comment line below if data is present and you want to run $ pytest on all test functions
    # ---------------------------------------------
    pytest.skip('\nTest viz_mean_temp_years only')

def test_viz_linear_regression():
    """
    Test viz_linear_regression from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_linear_regression(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'),  'tests/eda_test_data/eda.png') , alt.LayerChart)
    # Typical example, check side effect functions properly generating png image
    assert os.path.exists('tests/eda_test_data/eda_linear_fit_plot.png')

    # ---------------------------------------------
    # Skip pytest on this function, comment out line below or milestone 4 grading purposes. 
    # Comment line below if data is present and you want to run $ pytest on all test functions
    # ---------------------------------------------
    pytest.skip('\nTest viz_mean_temp_years only')

def test_viz_seasonal_lines():
    """
    Test viz_seasonal_lines from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_seasonal_lines(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), 'tests/eda_test_data/eda.png') , alt.HConcatChart)
    # Typical example,  check side effect functions properly generating png images
    assert os.path.exists('tests/eda_test_data/eda_facet_by_month_plot.png')

    # ---------------------------------------------
    # Skip pytest on this function, comment out line below or milestone 4 grading purposes. 
    # Comment line below if data is present and you want to run $ pytest on all test functions
    # ---------------------------------------------
    pytest.skip('\nTest viz_mean_temp_years only')

def test_viz_density_dists():
    """
    Test viz_density_dists from abstract_eda.py script

    """
    
    # Return Type Check, Data exists in folder after this check
    assert isinstance(viz_density_dists(read_clean_data(
        'data/global_temp_anomaly_cleaned_train.csv'), 'tests/eda_test_data/eda.png') , alt.Chart)
    # Typical example,  check side effect functions properly generating png images
    assert os.path.exists('tests/eda_test_data/eda_density_distributions_plot.png')

    # ---------------------------------------------
    # Skip pytest on this function, comment out line below or milestone 4 grading purposes. 
    # Comment line below if data is present and you want to run $ pytest on all test functions
    # ---------------------------------------------
    pytest.skip('\nTest viz_mean_temp_years only')