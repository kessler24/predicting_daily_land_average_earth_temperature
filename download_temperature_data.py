import pandas as pd

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
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    else:
        print("Error: Please be aware that your data has not been written as the output_path is not to a .csv file.")