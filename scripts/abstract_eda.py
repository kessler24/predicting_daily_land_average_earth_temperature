# documentation comments
"""




"""

# import libraries/packages
#--------------------

import pandas as pd
import altair as alt

# parse/define command line arguments here
#--------------------

args: list[str] = [path, base_filename]

# code for other functions
#--------------------

def read_clean_data(args[1]: str): # commandline args[1] -- get rel path from user
    ...
def viz_tabular_stats(train_df, args[1]): # commandline args[2] -- get basefilename from user to increment
    ...

def viz_linear_regression():
    ...

def viz_mean_temp_years():
    ...

def viz_seasonal_lines():
    ...

def viz_density_dists():
    ...

# define main function
#--------------------

def main():
    # code for "guts" of script goes here

    
# call main function
#--------------------

if __name__ == "__main__":
    main() # pass any command line args to main here