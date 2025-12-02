import argparse
import pandas as pd

def main():
    # define a parser
    parser = argparse.ArgumentParser(
        description="Read data from a URL or local path and save it as a CSV file."
    )

    # define the input file path
    parser.add_argument("input_path", help="Please give an URL or local file path (e.g. data/input.txt)")

    # define the output file path
    parser.add_argument("output_path", help="Output file path (e.g. data/raw.csv)")

    # set up and get the separate arguments
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path

    # make sure the input_path (first atrgument is a propoer url before downloading)
    if input_path.startswith("http://") or input_path.startswith("https://"):
        print(f"Downloading data from an URL: {input_path} ")
    else:
        print(f"Reading local file from {input_path}")

    # read the data with pandas to a csv 
    df = pd.read_csv(input_path, sep=r"\s+", comment="%", header=None)
    column_names = ["Date Number", "Year", "Month", "Day" , "Day of Year", "Anomaly"]
    df.columns = column_names

    if output_path.endswith(".csv"):
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    else:
        print("Please aware that your data is not write into a csv file.")

if __name__ == "__main__":
    main()