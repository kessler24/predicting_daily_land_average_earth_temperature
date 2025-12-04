# documentation comments
"""

Add docstrings to each function


"""

# import libraries/packages
#--------------------

import pandas as pd
import altair as alt
import click

# code for other functions
#--------------------

# def read_clean_data(args[1]: str): 
#     """
    
#     """
#     train_df = pd.read_csv('data/cleaned.csv')

# Configure Plot Sizes
# NOTE: may be able to remove this?
# Configure Plot Sizes Globally
plot_size = {'width': 450, 'height': 300}
facet_plot_size = {'width': 250, 'height': 200}

def viz_tabular_stats(train_df_csv_path, base_plot_png_name):
    ...

def viz_linear_regression():
    ...

def viz_mean_temp_years():
    ...

def viz_seasonal_lines():
    ...

def viz_density_dists():
    ...


# define main function with click commands
#--------------------
@click.command()
@click.argument('train_df_csv_path', type=click.Path(exists=True))
@click.argument('base_plot_png_name')
def main(train_df_csv_path, base_plot_png_name):
    # code for "guts" of script goes here
    viz_density_dists()
    print(f'\n{train_df_csv_path}\n')
    print(f'\n{base_plot_png_name}\n') 
    
# call main function
#--------------------

if __name__ == "__main__":
    
    
    main() # pass any command line args to main here