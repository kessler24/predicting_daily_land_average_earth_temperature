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
    assert increment_filename('images/eda_1') == 'images/eda_2'


"""
Test add_prefix_to_increment from abstract_eda.py script
"""



"""
Test read_clean_data from abstract_eda.py script
"""



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



