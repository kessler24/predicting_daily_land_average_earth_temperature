"""

The following script modularizes the Exploratory Data Analysis notebook.
Click commands take user input for the input training data filepath and
the png file output path and filename.

Parameters
----------
train_df_csv_path: str
    The current relative filepath of the clean training data to be analyzed.

plots_path: str
    The target relative filepath of the png images to be generated. 

Returns
-------
None
    Generates png image files of the plots in the target folder.

Examples
    --------
    >>> python scripts/abstract_eda.py data/train_df.csv images/eda.png (from repo root )
    None
        images/
            eda_table_1.html
            eda_table_2.html
            eda_plot_1.png
            eda_plot_2.png
            eda_plot_3.png
            eda_plot_4.png

"""

# -----------------------------
# import libraries/packages
# -----------------------------

import pandas as pd
import altair as alt
import click
import warnings
import os

# -----------------------------
# Define main function with click command arguments
# -----------------------------
@click.command()
@click.argument('train_df_csv_path', type=click.Path(exists=True))
@click.argument('plots_path', type=click.Path())
def main(train_df_csv_path:str, plots_path: str) -> None:

    # Read the training data csv into a dataframe from first command line argument
    train_df = read_clean_data(train_df_csv_path)

    # Simplify Working with Large Datasets 
    alt.data_transformers.enable('vegafusion')

    # Suppress altair plot warnings for cleaner output
    warnings.filterwarnings('ignore', module='altair')

    # View training dataframe at a high level for stats and null presence
    # Save the dataframe views as html files
    viz_tabular_stats(train_df, plots_path)

    # Create the temperature scatter plot with mean temperature per year line
    # Pass the command line argument plots_path to plot function for image output 
    # Pass the plots_path with the filename incremented by one to next plot
    inc_name = viz_mean_temp_years(train_df, plots_path)
    
    # Create the scatter plot with a simple linear regression fit
    # Pass the plots_path with the filename incremented by one to next plot
    inc_name = viz_linear_regression(train_df, plots_path=inc_name)

    # Create the mean temperature per year line plots for each month
    # Pass the plots_path with the filename incremented by one to next plot
    inc_name = viz_seasonal_lines(train_df, plots_path=inc_name)
    
    # Create the density plot with for three years separated by ~60 years
    # Pass the plots_path with the filename incremented by one to next plot
    inc_name = viz_density_dists(train_df, plots_path=inc_name)

# -----------------------------
# Increment any filename by one with *_\d*.ext suffix
# -----------------------------
def increment_filename(filepath: str) -> str:

    # Split the input filepath into the directory path and the file
    dirname, filename  = os.path.split(filepath)

    # Split above filename into the base name and the extension
    filename, ext = os.path.splitext(filename)
    
    # If the filename has a *_.ext as a numeric suffix increment it by one
    if filename.split('_')[-1].isnumeric():
       inc = int(filename.split('_')[-1])
       inc+=1
       new_filename = filename.split('_')[0]+'_'+str(inc)+ext
    
    # Otherwise add the *_.ext numeric suffix starting at 1
    else:
        new_filename = filename+'_'+str(1)+ext

    # Join the input directory with the modified filename and return the new path
    return os.path.join(dirname, new_filename)

# -----------------------------
# Add an underscore prefix to an incremented filename
# -----------------------------
def add_prefix_to_increment(inc_filename: str, 
                                    prefix: str) -> str:
    
    # Split the input filepath into the directory path and the file
    dirname, prefixed_name  = os.path.split(inc_filename)

    # Split above filename into the base name and the extension
    prefixed_name, ext = os.path.splitext(prefixed_name)

    # Split by *_* for inserting, requires an incremented file
    prefixed_name = prefixed_name.split('_')

    # Insert _suffix_ before *_\d*
    prefixed_name.insert(-1, '_'+prefix+'_')

    # Join list[str] together for new filename
    prefixed_name = ''.join(prefixed_name)

    # Construct the new path
    prefixed_name = os.path.join(dirname, prefixed_name+ext)

    # Return incremented filename with the provided prefix
    return prefixed_name

# -----------------------------
# Read the training data csv into a dataframe from the user provided path
# -----------------------------
def read_clean_data(train_df_csv_path: str) -> pd.DataFrame:
    train_df = pd.read_csv(train_df_csv_path)
    return train_df

# -----------------------------
# View descriptive statistics and null presence in training data
# -----------------------------
def viz_tabular_stats(train_df: pd.DataFrame,
                        plots_path: str) -> None:
    
    # Check if any NA values are in any of the columns in the training dataset
    contains_na_df = train_df.isna().any().reset_index(
        ).rename(columns={'index': 'Column', 0: 'Contains NA Values'})

    # Increment the plots_path filename and strip the .png extension, add .html
    table_name = increment_filename(plots_path.removesuffix('.png')+'.html')

    # Export contains_na_df to html at plot_paths directory
    contains_na_df.to_html(add_prefix_to_increment(table_name, 'table'))

    # Increment the table html filename above
    table_name = increment_filename(table_name)

    # Export train_df.describe() to html at plots_path directory with rounded numbers
    train_df.describe().round(2).to_html(add_prefix_to_increment(table_name, 'table'))

# -----------------------------
# Create the temperature scatter plot with mean temperature per year line
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_mean_temp_years(train_df: pd.DataFrame, 
                            plots_path: str,
                            plot_size: dict = {'width': 450, 'height': 300}) -> str:

    # Create scatter of raw data with some opacity to reduce plot noise
    temp_points = alt.Chart(train_df,
            title=alt.Title(
            text='Global Daily Average Land Temperature',
            subtitle='Mean Temperature Indicated by Red Line')
            ).mark_point(opacity=0.6, size=1).encode(
        x = 'Year:T',
        y = 'Temperature:Q')

    # Create line plot of the mean of all the measurements in a given year 
    temp_line_mean = temp_points.mark_line(size=2, color='red').encode(
        x = alt.X('Year:T', title='Year'),
        y = alt.Y('mean(Temperature):Q', title='Temperature [°C]'
                ).scale(zero=False) 
    ).properties(**plot_size)

    # Increment the file name in the png path
    plot_name = increment_filename(plots_path)

    # Add _plot_ prefix to incremented file name
    plot_name  = add_prefix_to_increment(plot_name, 'plot')

    # save the plot as a png file
    (temp_points+temp_line_mean).save(plot_name)

    # Return the incremented plot filepath
    return plot_name

# -----------------------------
# Create the scatter plot with a simple linear regression fit
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_linear_regression(train_df: pd.DataFrame, 
                            plots_path: str,
                            plot_size: dict = {'width': 450, 'height': 300}) -> str:
    
    # PLot a scatter plot of the mean temperatures for each year
    temp_points_avg = alt.Chart(train_df,
            title=alt.Title(
            text='Annual Means of Global Daily Average Land Temperature',
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
    
    # Increment the file name in the png path
    plot_name = increment_filename(plots_path)

    # Add _plot_ prefix to incremented file name
    plot_name  = add_prefix_to_increment(plot_name, 'plot')

    # save the plot as a png file
    reg.save(plot_name)

    # Return the incremented plot filepath
    return plot_name

# -----------------------------
# Create the mean temperature per year line plots for each month
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_seasonal_lines(train_df: pd.DataFrame, 
                        plots_path: str,
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
    
    # Increment the file name in the png path
    plot_name = increment_filename(plots_path)

    # Add _plot_ prefix to incremented file name
    plot_name  = add_prefix_to_increment(plot_name, 'plot')

    # save the plot as a png file
    final_figure.save(plot_name)

    # Return the incremented plot filepath
    return plot_name

# -----------------------------
# Create the density plot with for three years separated by ~60 years
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_density_dists(train_df: pd.DataFrame, 
                        plots_path: str,
                        plot_size: dict = {'width': 450, 'height': 300}) -> str:
    
    # Years to be analyzed separated by ~60 years
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

    # Increment the file name in the png path
    plot_name = increment_filename(plots_path)
    
    # Add _plot_ prefix to incremented file name
    plot_name  = add_prefix_to_increment(plot_name, 'plot')

    # save the plot as a png file
    temp_density.save(plot_name)

    # Return the incremented plot filepath
    return plot_name

# -----------------------------    
# Call main() with name guard
# -----------------------------
if __name__ == "__main__":
    main()