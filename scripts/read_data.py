import click
import pandas as pd

@click.command()
@click.argument("input_path")
@click.argument("output_path")
def main(input_path, output_path):
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