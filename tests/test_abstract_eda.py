import sys
import os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.abstract_eda import (increment_filename, 
                                  add_prefix_to_increment,
                                  read_clean_data,
                                  viz_tabular_stats,
                                  viz_mean_temp_years,
                                  viz_linear_regression,
                                  viz_seasonal_lines,
                                  viz_density_dists)

"""
Test increment_filename from abstract_eda.py script
"""
def test_increment_filename():
    # Return type check
    assert isinstance(increment_filename('images/eda_1.png'), str)
    # Typical example check
    assert increment_filename('images/eda_1.png') == 'images/eda_2.png'
    # Atypical example check
    assert increment_filename('images/eda_1_1.png') == 'images/eda_1_2.png'

"""
Test add_prefix_to_increment from abstract_eda.py script
"""
def test_add_prefix_to_increment():
    # Return type check
    assert isinstance(add_prefix_to_increment('images/eda_1.png', 'plot'), str)
    # Typical example check
    assert add_prefix_to_increment('images/eda_1.png','plot') == 'images/eda_plot_1.png'
    # Atypical example check
    assert add_prefix_to_increment('images/train_df_1.csv', 'table') == 'images/train_df_table_1.csv'


"""
Test read_clean_data from abstract_eda.py script
"""
def test_read_clean_data():
    # Return Type Check
    assert isinstance(read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), pd.DataFrame)
    # Typical example check all columns exist
    assert {'Year', 'Month', 'Day', 'Anomaly', 'Day of Year', 'Temperature', 'Month_Name'}.issubset(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv').columns)
    # Typical example check that more rows are in training data rather than test data
    assert len(read_clean_data(
        'data/global_temp_anomaly_cleaned_test.csv')) < len(read_clean_data(
            'data/global_temp_anomaly_cleaned_train.csv'))

"""
Test viz_tabular_stats from abstract_eda.py script
"""
def test_viz_tabular_stats():
    # Return Type Check
    assert viz_tabular_stats(
        read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), 'images/eda.png') is None
    # Typical example check side effect functions properly generating tables
    viz_tabular_stats(read_clean_data('data/global_temp_anomaly_cleaned_train.csv'), 'images/eda.png')
    assert os.path.exists('images/eda_table_1.csv')
    assert os.path.exists('images/eda_table_2.csv')
    # assert 
    # Atypical example check


"""
Test viz_mean_temp_years from abstract_eda.py script
"""



"""
Test viz_linear_regression from abstract_eda.py script
"""



"""
Test viz_seasonal_lines from abstract_eda.py script
"""



"""
Test viz_density_dists from abstract_eda.py script
"""



