import sys
import os
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
    assert read_clean_data('')


"""
Test viz_tabular_stats from abstract_eda.py script
"""



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



