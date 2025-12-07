# Predicting Daily Land Average Earth Temperature

Authors: Molly Kessler, Daisy Zhou, Ojasv Issar, Jacob Cann

## Summary

This project applies a regression algorithm to a data set of daily average land temperature of the Earth from January 1800 through July 2022 to predict the daily average land temperature of the Earth in the near future.

This project has four code components. First, we read in the data from the online source and applied appropriate formatting to get the data into a table (i.e. removed the extensive metadata header). Second, we preprocessed the data, including setting data for the years 2013-2022 aside to be our test dataset. Third, we performed exploratory data analysis on the training data. We observed a clear increasing trend in the mean daily land temperature from 1880 to 2012, suggesting that a linear model could generalize to future unseen years. To ensure that the trend was not seasonal or isolated to specific months (i.e. only the summers were increasing, while winters were staying the same), we created faceted plots by month which confirmed that the increasing pattern persisted across all months. Lastly, the density plots at selected time points (1880, 1960, 2012) show a clear shift towards a higher mean daily land temperatures over time, with very little overlap between the daily mean land temperatures of 1880 and those of 2012.

Lastly, using our training data (1880 - 2012), we further preprocessed our data and trained our model. As part of our model preprocessing, we converted daily temperature anomalies into yearly averages to capture long-term trends and remove noise from short-term and seasonal fluctuations. First, we compared Linear Regression, Random Forest, and Support Vector Regressor (SVR) models on the following metrics: RMSE, MAE and R². The SVR model performed the best out of the three, so we proceeded with SVR with default hyperparameters. Lastly, we used our model to forecast the global land-average temperature in 2030, which our model predicted will be about **10.56 °C.**, 2 °C warmer than average of the baseline period (1951 and 1980) and a clear continuation of the observed warming trend.

## Data

The data set for this project was published by Berkeley Earth under a Creative Commons BY-NC 4.0 International license, free for non-commercial use, and accessed by our team compliant with the conditions in this license on November 18, 2025. The raw data can be found at <https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt>.

The data set contains 5 columns with time series information, and one column representing the temperature difference relative to the average temperature between January 1951 and December 1980, which they calculated as 8.59 +/- 0.05. For our analysis, we preprocessed the data to get the raw temperature readings back by adding 8.59 to each entry in the Anomaly column. All temperatures are in Celcius.

## Dependencies

All software dependencies for this project are managed using Docker. You can build and run the project directly inside the [Docker](https://www.docker.com/) container. This ensures a consistent and reproducible environmenyt across all systems. To install the relevant dependencies, follow the instructions in the Setup Environment section below.

## Running the Analysis

Follow the instructions to run the analysis or modify the project in an editor.

### Setup Environment

1. Ensure Docker and Docker Compose are installed on your machine.

2. Clone the GitHub repository to your machine.

3. Open a command line interface (e.g. Terminal) on your machine and navigate to the root of this repository. Enter the following command to start and run your multi-container application based on the configuration provided in the docker-compose.yml file.

`docker compose up`

4. After the docker image is created and the container is started, look for an url similar to 'http://127.0.0.1:8888/lab?token=f41ef3f99692f72a4e1efb828a738f38d2da4c648c62d21c' following the line 'Or copy and paste one of these URLs'.

5. Copy and paste the url to browser to launch the jupyter notebook. 

If the page asks for a password or token, it is likely that the port 8888 is already being used on your computer. In this case, you can either remove the existing docker instance on port 8888, or launch this new docker instance on a new port. 

To launch this docker instance on a new port:
a. Remove the current instance by running `docker compose rm` command. 
b. Open the docker-compose.yml file and change the port number in curly braces {} below to an available port (e.g. If 8888 is unavailable, try 8887 or 8889).
    ports:
      - "{8888}:8888"
c. After changing the port number, run `docker compose up` again and look for the url again. Remember to replace the port number in the curly braces {} below with the number you changed to in step b.
'http://127.0.0.1:{8888}/lab?token=f41ef3f99692f72a4e1efb828a738f38d2da4c648c62d21c' 

6. Once you launch the Docker instance successfully, you will be in a local JupyterLab instance in your browser. Now you can navigate to the global_daily_land_temperature_prediction.ipynb document and explore the interactive analysis.

### Running the scripts

1. Run `pwd` to make sure you are located in the project root, otherwise, make sure you naviagte to the root of the project before proceeding to the following steps. 

2. Download the [Berkeley Earth Temperature Data](https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt) with `read_data.py` script by running this command:

 `python scripts/read_data.py "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt" "data/global_temp_anomaly_raw.csv"`

 The script takes two arguments:
 - the path to the input file (a URL or a relative local path, such as data/file.csv)
 - a path/filename where to write the file to and what to call it (e.g., data/cleaned_data.csv)

3. Reads the data from the first script and performs and data cleaning, preprocessing and validation with `data_preprocessing.py` script by runnning this command:

 `python scripts/data_preprocessing.py --read_path="data/global_temp_anomaly_raw.csv" --write_path="data/global_temp_anomaly_cleaned" --plots_path="images" --logs_path="logs"`

The script takes four arguments:
- a path/filename pointing to the data to be read in
- a path/filename pointing to where the cleaned/processed/transformed/partitioned data should live.
- A path pointing to where the plots will be saved
- A path pointing to where the log file will be saved

4. Perform EDA (Exploratory Data Analysis) on the training data with `abstract_eda.py` script by running this command:

`python scripts/abstract_eda.py data/global_temp_anomaly_cleaned_train.csv images/eda.png`

The script takes two arguments:
- a path/filename pointing to the cleaned training data to be analyzed
- a path/filename pointing to where the png images and csv tables will be saved

5. Build machine learning model with `ml_modelling.py` script by running this command:

`python scripts/ml_modelling.py --input_path data/global_temp_anomaly_cleaned_full.csv --output_dir results --cutoff_year 2012`

The script takes three arguments:
- a path/filename pointing to the cleaned full data to be analyzed
- a path/filename pointing to where the analysis result will be saved
- a numeric parameter to take as the cutoff_year for train and test data

## Developer notes

### Developer dependencies
- `conda` (version 25.9.1)
- `conda-lock` (version 3.0.4)

### Adding a new dependency

1. Create and switch to a new GitHub branch by typing `git checkout -b new-branch-name` in the terminal

2. Open the `environment.yml`file and add the new dependencies

3. To update the `conda-linux-64.lock` file, run `conda-lock -k explicit --file environment.yml -p linux-64` in the terminal

4. Remember to rebuild the Docker image locally and make sure it runs locally with `docker compose up`.

5. To make sure the Docker image builds properly, check GitHub Actions on GitHub.com. Ensure the latest Docker image published sucessfully with a green check icon (note: it will take up to 10 minutes for the Docker image to build). 

6. Run `git add modified_file_name` (Remember to add all files with edits i.e. `git add environment.yml`)
       `git commit -m 'add new dependencies'`
       `git push -u origin new-branch-name` to push the local changes to the GitHub repo.

7. Create a new pull request in GitHub and merge the changes to the `main` branch after review.

## License

The Predicting Daily Land Average Earth Temperature report contained herein are licensed under the Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License. See the license file for more information. If re-using/re-mixing please provide attribution and link to this webpage. The software code contained within this repository is licensed under the MIT license. See the license file for more information.
