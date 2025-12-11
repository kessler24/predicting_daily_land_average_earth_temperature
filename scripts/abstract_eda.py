"""
The following script modularizes the Exploratory Data Analysis (EDA) notebook.
Click commands take user input for the input training data filepath and
the png file output path and filename.

Parameters
----------
train_df_csv_path: str, default data/global_temp_anomaly_cleaned_train.csv
    The current relative filepath of the clean training data to be analyzed.

plots_path: str, default 'images/eda.png'
    The target relative filepath of the png images and csv tables to be generated 
    and a preferred file prefix. The default prefix is 'eda'. Use '_' as a separator
    if need be for proper handling of filenames. 

Returns
-------
None
    Generates training data png files of the plots and summary csv tables in the target folder.

Examples
--------
    $ python scripts/abstract_eda.py data/global_temp_anomaly_cleaned_train.csv images/eda.png  --  (from repo root)
    >>> None
    
    $ python scripts/abstract_eda.py  --  using defaults for train_df_csv_path and plots_path (from repo root)
    >>> None
    
    Side Effects:
    -------------
        images/
            train_df_eda_table_1.csv
            train_df_eda_table_2.csv
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
# Define main function with click command arguments and default values
# -----------------------------
@click.command()
@click.argument('train_df_csv_path', 
                    type=click.Path(exists=True), 
                    default='data/global_temp_anomaly_cleaned_train.csv')
@click.argument('plots_path', 
                    type=click.Path(), 
                    default='images/eda.png')
def main(train_df_csv_path:str, plots_path: str) -> None:

    dirname, prefixed_name  = os.path.split(plots_path)

    # Split above filename into the base name and the extension
    prefixed_name, ext = os.path.splitext(prefixed_name)

    # Handle empty path or bad file extension, default to .png
    if not ext == '.png':
        ext = '.png'

    plots_path = os.path.join(dirname, prefixed_name + ext)


    # Read the training data csv into a dataframe to use for tables and plots
    train_df = read_clean_data(train_df_csv_path)

    # Save the dataframe as a .csv for high level for stats and null presence 
    viz_tabular_stats(train_df, plots_path)

    # Create the temperature scatter plot with mean temperature per year line
    viz_mean_temp_years(train_df, plots_path)
    
    # Create the scatter plot with a simple linear regression fit
    viz_linear_regression(train_df, plots_path)

    # Create the mean temperature per year line plots for each month
    viz_seasonal_lines(train_df, plots_path)
    
    # Create the density plot with for three years separated by ~60 years
    viz_density_dists(train_df, plots_path)

# -----------------------------
# Increment any filename by one with *_\d*.ext suffix
# -----------------------------
def increment_filename(filepath: str) -> str:

    # Split the input filepath into the directory path and the file
    dirname, filename  = os.path.split(filepath)

    # Split above filename into the base name and the extension
    filename, ext = os.path.splitext(filename)
    
    # Handle empty path or no file ext, default to .png
    if ext == '':
        ext = '.png'

    # If the filename has a *_.ext as a numeric suffix increment it by one
    if filename.split('_').pop(-1).isnumeric():
       inc = int(filename.split('_')[-1])
       inc += 1
       new_filename = '_'.join(filename.split('_')[:-1]) + '_' + str(inc)
       
    # Otherwise add the *_.ext numeric suffix starting at 1
    else:
        new_filename = filename + '_1'

    # Join the input directory with the modified filename and return the new path
    return os.path.join(dirname, new_filename + ext)

# -----------------------------
# Add an underscore prefix to an incremented filename
# -----------------------------
def add_suffix_to_filename(filename: str, 
                                suffix: str) -> str:
    
    # Split the input filepath into the directory path and the file
    dirname, prefixed_name  = os.path.split(filename)

    # Split above filename into the base name and the extension
    prefixed_name, ext = os.path.splitext(prefixed_name)

    # Handle empty path or no file ext, default to .png
    if ext == '':
        ext = '.png'

    # Split by *_* for inserting, requires an incremented file
    prefixed_name = prefixed_name.split('_')

    # Insert _suffix_ before *_\d*
    if suffix not in prefixed_name:
        prefixed_name.append(suffix)

    # Join list[str] together for new filename
    prefixed_name = '_'.join(prefixed_name)

    # Construct the new path
    prefixed_name = os.path.join(dirname, prefixed_name + ext)

    # Return incremented filename with the provided prefix
    return prefixed_name

# -----------------------------
# Read the training data csv into a dataframe from the user provided path
# -----------------------------
def read_clean_data(train_df_csv_path: str) -> pd.DataFrame:

    # Create the training dataframe for tables and plots
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

    # Show the data types of the features
    contains_na_df['Data Type'] = train_df.dtypes.values

    # Strip the .png extension
    filename, ext = os.path.splitext(plots_path)

    if plots_path.split('_').pop(-1).isnumeric():
        # Increment the plots_path if end is numeric and make .csv extension
        table_name = increment_filename(f"{filename}.csv")
    else:
        # Otherwise use plots_path for filename
        table_name = f"{filename}.csv"

    # Export contains_na_df to csv at plots_path directory
    contains_na_df.to_csv(add_suffix_to_filename(table_name, 'training_data_info_table'),
                            index=False)

    if plots_path.split('_').pop(-1).isnumeric():
        # Increment the plots_path if end is numeric and make .csv extension
        table_name = increment_filename(f"{filename}.csv")
    else:
        # Otherwise use plots_path for filename
        table_name = f"{filename}.csv"

    # Export train_df.describe() to csv at plots_path directory with rounded numbers
    train_desc = train_df.describe().round(2)
    # Rename the index column
    train_desc.index.name = 'Statistic'
    train_desc.to_csv(add_suffix_to_filename(table_name, 'training_data_stats_table'),
                                    index=True)

# -----------------------------
# FUNCTION TO GRADE FOR TESTING IN MILESTONE 4:
# Create the temperature scatter plot with mean temperature per year line
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_mean_temp_years(train_df: pd.DataFrame, 
                            plots_path: str,
                            plot_size: dict = {'width': 450, 'height': 300}) -> alt.LayerChart:
    
    """
    
    
    
    """

    # -----------------------------
    # Defensive programming checks
    # -----------------------------
    # Check the input type
    if not isinstance(train_df, pd.DataFrame):
        raise TypeError('The "train_df" parameter must be a valid pd.DataFrame object for plotting.')
    # Check the number of input data rows
    if not len(train_df) > 1:
        raise ValueError('The "train_df" parameter must have at least two rows for plotting.')
    # Check plotting path is a valid string
    if not isinstance(plots_path, str):
        raise TypeError('The plotting output path object must be of type str()')
    # Check the target output path exists
    # Split the input filepath into the directory path and the file
    dirname, prefixed_name  = os.path.split(plots_path)
    if not os.path.exists(dirname):
        warnings.warn('The desired output folder does not exist, creating the folder...')
        os.mkdir(dirname)

    # Simplify Working with Large Datasets 
    alt.data_transformers.enable('vegafusion')

    # Suppress altair plot warnings for cleaner output
    warnings.filterwarnings('ignore', module='altair')

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

    if plots_path.split('_').pop(-1).isnumeric():
        # Increment the file name in the png path if ending in numeric
        plot_name = increment_filename(plots_path)
    else:
        # Otherwise use plots_path for filename
        plot_name = plots_path

    # Add _plot_ prefix to incremented file name
    plot_name  = add_suffix_to_filename(plot_name, 'mean_per_year_plot')

    plot_layered = temp_points+temp_line_mean

    # save the plot as a png file
    plot_layered.save(plot_name, ppi=300)

    # Return the incremented plot filepath
    return plot_layered

# -----------------------------
# Create the scatter plot with a simple linear regression fit
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_linear_regression(train_df: pd.DataFrame, 
                            plots_path: str,
                            plot_size: dict = {'width': 450, 'height': 300}) -> alt.LayerChart:
    
    # Simplify Working with Large Datasets 
    alt.data_transformers.enable('vegafusion')

    # Suppress altair plot warnings for cleaner output
    warnings.filterwarnings('ignore', module='altair')

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
    plot_layered = temp_points_avg+temp_points_avg.mark_line(
        size=2, color='red').transform_regression(
        'Year',
        'Temperature'
    ).properties(**plot_size)
    
    if plots_path.split('_').pop(-1).isnumeric():
        # Increment the file name in the png path if ending in numeric
        plot_name = increment_filename(plots_path)
    else:
        # Otherwise use plots_path for filename
        plot_name = plots_path

    # Add _plot_ prefix to incremented file name
    plot_name  = add_suffix_to_filename(plot_name, 'linear_fit_plot')

    # save the plot as a png file
    plot_layered.save(plot_name, ppi=300)

    # Return the incremented plot filepath
    return plot_layered

# -----------------------------
# Create the mean temperature per year line plots for each month
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_seasonal_lines(train_df: pd.DataFrame, 
                        plots_path: str,
                        facet_plot_size: dict = {'width': 450, 'height': 300}) -> alt.LayerChart:
    
    # Simplify Working with Large Datasets 
    alt.data_transformers.enable('vegafusion')

    # Suppress altair plot warnings for cleaner output
    warnings.filterwarnings('ignore', module='altair')

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
    plot_layered = alt.hconcat(temp_plot).properties(
        title='Seasonality of Annual Means of Global Daily Average Land Temperature')
    
    if plots_path.split('_').pop(-1).isnumeric():
        # Increment the file name in the png path if ending in numeric
        plot_name = increment_filename(plots_path)
    else:
        # Otherwise use plots_path for filename
        plot_name = plots_path

    # Add _plot_ prefix to incremented file name
    plot_name  = add_suffix_to_filename(plot_name, 'facet_by_month_plot')

    # save the plot as a png file
    plot_layered.save(plot_name, ppi=300)

    # Return the incremented plot filepath
    return plot_layered

# -----------------------------
# Create the density plot with for three years separated by ~60 years
# Save the plot as a png file to the image folder with provided filename
# -----------------------------
def viz_density_dists(train_df: pd.DataFrame, 
                        plots_path: str,
                        plot_size: dict = {'width': 450, 'height': 300}) -> alt.LayerChart:
    
    # Simplify Working with Large Datasets 
    alt.data_transformers.enable('vegafusion')

    # Suppress altair plot warnings for cleaner output
    warnings.filterwarnings('ignore', module='altair')

    # Years to be analyzed separated by ~60 years
    years_selection = [1880, 1960, 2012]

    # Select necessary data only
    data_subset = train_df[train_df['Year'].isin(years_selection)]

    # Create density plot for each selected year and add opacity to view overlap
    plot_layered = alt.Chart(data_subset
        ).transform_density(
        'Temperature',
        groupby=['Year'],
        as_=['Temperature', 'density']
    ).mark_area(opacity=0.6).encode(
        x=alt.X('Temperature',title='Temperature [°C]'),
        y=alt.Y('density:Q',title='Density').stack(False),
        color = 'Year:N'
    ).properties(**plot_size, title = 'Distributions of Global Daily Average Land Temperature')

    if plots_path.split('_').pop(-1).isnumeric():
        # Increment the file name in the png path if ending in numeric
        plot_name = increment_filename(plots_path)
    else:
        # Otherwise use plots_path for filename
        plot_name = plots_path
    
    # Add _plot_ prefix to incremented file name
    plot_name  = add_suffix_to_filename(plot_name, 'density_distributions_plot')

    # save the plot as a png file
    plot_layered.save(plot_name, ppi=300)

    # Return the incremented plot filepath
    return plot_layered

# -----------------------------    
# Call main() with name guard
# -----------------------------
if __name__ == "__main__":
    main()