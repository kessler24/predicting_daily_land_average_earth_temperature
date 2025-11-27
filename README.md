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

All software dependencies for this project are managed using Docker. You can build and run the project directly inside the Docker container. This ensures a consistent and reproducible environmenyt across all systems. To install the relevant dependencies, follow the instructions in the Setup Environment section below.

## Running the Analysis

Follow the instructions to run the analysis or modify the project in an editor.

### Setup Environment

1. Ensure Docker and Docker Compose are installed on your machine.

2. Clone the GitHub repository to your machine.

3. Open a command line interface (e.g. Terminal) on your machine and navigate to the root of this repository. Enter the following command to start and run your multi-container application based on the configuration provided in the docker-compose.yml file.

`docker compose up`

4. After the docker image is created and the container is started, look for an url similar to 'http://127.0.0.1:8888/lab?token=f41ef3f99692f72a4e1efb828a738f38d2da4c648c62d21c' following the line 'Or copy and paste one of these URLs'.

5. Copy and paste the url to browser to launch the jupyter notebook. 

If the launch fails and lead to a page asking for password or token, you might want to open the docker-compose.yml file and change the port number in square bracke {} below
    ports:
      - "{8888}:8888"

After changing the port number, remember to replace the port number when you copy and paste the link to browser.

6. In jupyter notebook code, navigate to the global_daily_land_temperature_prediction.ipynb document and explore the interactive analysis.

## License

The Predicting Daily Land Average Earth Temperature report contained herein are licensed under the Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License. See the license file for more information. If re-using/re-mixing please provide attribution and link to this webpage. The software code contained within this repository is licensed under the MIT license. See the license file for more information.
