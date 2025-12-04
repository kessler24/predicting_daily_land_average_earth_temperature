# documentation comments
"""

The following code modularizes the eda code blocks into functions
and adds click commands for input when running the script.

"""

# import libraries/packages
#--------------------

import pandas as pd
import altair as alt
import click
import warnings
import os

# code for other functions
#--------------------

def increment_filename(filepath: str) -> str:

    dirname, filename  = os.path.split(filepath)

    filename, ext = os.path.splitext(filename)
    
    if filename.split('_')[-1].isnumeric():
       inc = int(filename.split('_')[-1])
       inc+=1
       new_filename = filename.split('_')[0]+'_'+str(inc)+ext
    else:
        new_filename = filename+'_'+str(1)+ext
    
    print(new_filename)

    return os.path.join(dirname, new_filename)
    
def read_clean_data(train_df_csv_path: str) -> pd.DataFrame:
    # -- change to clean train_df when ready
    train_df: pd.DataFrame = pd.read_csv(train_df_csv_path)
    return train_df

def viz_tabular_stats(train_df: pd.DataFrame) -> None:
    # --- train_df glance
    print('\n')
    train_df.info()
    print(f'\n{train_df.describe()}\n')

def viz_linear_regression(train_df: pd.DataFrame, base_plot_png_name: str,
        plot_size: dict = {'width': 450, 'height': 300}) -> str:
    
    # PLot a scatter plot of the mean temperatures for each year
    temp_points_avg = alt.Chart(train_df,
            title=alt.Title(
            text='Annual Means of Global Daily Average Land Temperature (Figure 2)',
            subtitle='Linear Regression Indicated by Red Line')
        ).mark_point(size=2).encode(
        x = alt.X('Year:T', title='Year'),
        y = alt.Y('mean(Temperature):Q', 
                title='Temperature [°C]').scale(zero=False) 
    )

    # Add the regression line to the scatter plot and properties
    reg = temp_points_avg+temp_points_avg.mark_line(
        size=2, color='red').transform_regression(
        'Year',
        'Temperature'
    ).properties(**plot_size)
    
    plot_name = increment_filename(base_plot_png_name)

    # save the regression plot
    reg.save(plot_name)

    return plot_name

def viz_mean_temp_years(train_df: pd.DataFrame, base_plot_png_name: str,
        plot_size: dict = {'width': 450, 'height': 300}) -> str:

    # Create scatter of raw data with some opacity to reduce plot noise
    temp_points = alt.Chart(train_df,
            title=alt.Title(
            text='Global Daily Average Land Temperature',
            subtitle='Mean Temperature (Red Line)')
            ).mark_point(opacity=0.6, size=1).encode(
        x = 'Year:T',
        y = 'Temperature:Q')

    # Create line plot of the mean of all the measurements in a given year 
    temp_line_mean = temp_points.mark_line(size=2, color='red').encode(
        x = alt.X('Year:T', title='Year'),
        y = alt.Y('mean(Temperature):Q', title='Temperature [°C]'
                ).scale(zero=False) 
    ).properties(**plot_size)

    plot_name = increment_filename(base_plot_png_name)

    # save png of the raw data distribution along with mean by year
    (temp_points+temp_line_mean).save(plot_name)

    return plot_name

def viz_seasonal_lines(train_df: pd.DataFrame, base_plot_png_name: str,
        facet_plot_size: dict = {'width': 450, 'height': 300}) -> str:
    
    # Average by year for each month in data
    mean_per_month = train_df.groupby(
        ['Year','Month_Name'], observed=True)['Temperature'].mean().reset_index()

    # For empty plotting title
    mean_per_month[' ']=mean_per_month['Month_Name']

    # Create Mean temperature plots and facet by month
    temp_plot = alt.Chart(mean_per_month).mark_line().encode(
        x = 'Year:T',
        y = alt.Y('Temperature:Q', title='Temperature [°C]').scale(zero=False)
    ).properties(**facet_plot_size).facet(' ', columns=2)

    # Show the plot with overall title
    final_figure = alt.hconcat(temp_plot).properties(
        title='Seasonality of Annual Means of Global Daily Average Land Temperature')
    
    plot_name = increment_filename(base_plot_png_name)

    # save the plot
    final_figure.save(plot_name)

    return plot_name

def viz_density_dists(train_df: pd.DataFrame, base_plot_png_name: str,
        plot_size: dict = {'width': 450, 'height': 300}) -> str:
    
    # Years to be analyzed separated by ~60 years make static for now
    years_selection = [1880, 1960, 2012]

    # Select necessary data only
    data_subset = train_df[train_df['Year'].isin(years_selection)]

    # Create density plot for each selected year and add opacity to view overlap
    temp_density  = alt.Chart(data_subset
        ).transform_density(
        'Temperature',
        groupby=['Year'],
        as_=['Temperature', 'density']
    ).mark_area(opacity=0.6).encode(
        x=alt.X('Temperature',title='Temperature [°C]'),
        y=alt.Y('density:Q',title='Density').stack(False),
        color = 'Year:N'
    ).properties(**plot_size, title = 'Distributions of Global Daily Average Land Temperature')

    plot_name = increment_filename(base_plot_png_name)
    
    # save the density plots by select years
    temp_density.save(plot_name)

    return plot_name

# define main function with click commands
#--------------------
@click.command()
@click.argument('train_df_csv_path', type=click.Path(exists=True))
@click.argument('base_plot_png_name')

def main(train_df_csv_path:str , base_plot_png_name: str) -> None:
    # --- code for "guts" of script goes here

    train_df = read_clean_data(train_df_csv_path)

    # Simplify Working with Large Datasets 
    alt.data_transformers.enable('vegafusion')

    warnings.filterwarnings('ignore', module='altair')

    viz_tabular_stats(train_df)

    # Configure Plot Sizes (or use default value in functions?)
    # NOTE: may be able to remove this?
    # Configure Plot Sizes Globally
    plot_size: dict = {'width': 450, 'height': 300}
    facet_plot_size: dict = {'width': 250, 'height': 200}

    inc_name = viz_mean_temp_years(train_df, base_plot_png_name, 
                                    plot_size=plot_size)
    
    inc_name = viz_linear_regression(train_df, base_plot_png_name=inc_name,
                                    plot_size=plot_size)

    inc_name = viz_seasonal_lines(train_df, base_plot_png_name=inc_name, 
                                    facet_plot_size=facet_plot_size)
    
    inc_name = viz_density_dists(train_df, base_plot_png_name=inc_name, 
                                    plot_size=plot_size)

    # --- see output from cli args (debugging)
    print(f'arg 1 : \n{train_df_csv_path}\n')
    print(f'arg 2 : \n{base_plot_png_name}\n')
    print('\nincremented filename\n',
          increment_filename(inc_name))
    
# call main function
#--------------------
if __name__ == "__main__":
    main() # name guard