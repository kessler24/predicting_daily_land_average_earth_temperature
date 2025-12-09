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
from src.download_temperature_data import download_temperature_data

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