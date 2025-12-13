"""
read_data.py

Script for downloading or reading the Berkeley Earth Global Daily Temperature Anomaly dataset and converting it into a structured CSV file.

This script accepts either:
- A URL pointing to the Berkeley Earth text file, or
- A local path to a raw data file

The script loads the whitespace-delimited text file, assigns meaningful column
names, and saves the result as a CSV file.

Parameters
----------
input_path : str
    URL or local filepath to the raw Berkeley Earth temperature data file.
output_path : str
    Filepath where the processed CSV file should be saved.

Usage
-----
Run this script from the command line:

    python scripts/read_data.py \
        "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt" \
        "data/global_temp_anomaly_raw.csv"

Outputs
-------
- A CSV file containing cleaned, column-labeled temperature anomaly data.
- Console messages indicating whether the input was downloaded from the web
  or read locally.

Notes
-----
The raw Berkeley Earth dataset contains percent-prefixed comment lines and
is whitespace-delimited. These are automatically handled using pandas'
read_csv options.
"""
import click
import pandas as pd
import os

def download_temperature_data(input_path: str, output_path: str):

    """
    Load raw Berkeley Earth daily temperature anomaly data and save as CSV.

    This function determines whether the input path refers to a URL or a local
    file, reads the raw whitespace-delimited dataset, assigns standard column
    names, and writes the formatted dataset to a CSV file.

    Parameters
    ----------
    input_path : str
        URL or local filepath to the raw Berkeley Earth text dataset. Must be a
        whitespace-delimited file where comment lines begin with '%'.
    output_path : str
        Destination filepath for saving the cleaned CSV output. If the provided
        path does not end in ".csv", a warning is printed and the file is
        not written.

    Returns
    -------
    None

    Notes
    -----
    The expected columns in the raw dataset are:

    - Date Number
    - Year
    - Month
    - Day
    - Day of Year
    - Anomaly

    These are applied automatically after reading the file.
    """

    # make sure the input_path (first argument is a proper url before downloading)
    if input_path.startswith("http://") or input_path.startswith("https://"):
        print(f"Downloading data from an URL: {input_path} ")
    else:
        print(f"Reading local file from {input_path}")
    
    # Make sure the file can be read as a csv file format
    try:
        df = pd.read_csv(input_path, sep=r"\s+", comment="%", header=None)
    except Exception as e:
        print(f"Error reading data with the file path: {input_path}: {e}")
        # Re-raise as IOError for proper function testing/robustness
        raise IOError(f"The input file path: {input_path} is not readable/downloadable") from e
    
    # rename data columns 
    column_names = ["Date Number", "Year", "Month", "Day", "Day of Year", "Anomaly"]
    df.columns = column_names
    
    # write and save the data as a csv file
    if output_path.endswith(".csv"):
        dir, _ = os.path.split(output_path)
        if not os.path.exists(dir):
           os.mkdir(dir)
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    else:
        print("Error: Please be aware that your data has not been written as the output_path is not to a .csv file.")

@click.command()
@click.argument("input_path")
@click.argument("output_path")
def main(input_path, output_path):
    """
    Download raw Berkeley Earth daily temperature anomaly data and save as a csv file.
    """
    # calls the processing function and handles exceptions for the function
    try:
        download_temperature_data(input_path, output_path)
    except IOError as e:
        print(f"FATAL ERROR: Processing failed. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()