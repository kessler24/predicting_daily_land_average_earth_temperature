# Predicting Daily Land Average Earth Temperature

Authors: Molly Kessler, Daisy Zhou, Ojasv Issar, Jacob Cann

## Summary

This project applies a regression algorithm to a data set of daily average land temperature of the Earth from January 1800 through July 2022 to predict the daily average land temperature of the Earth in the near future.

This project has four code components. First, we read in the data from the online source and applied appropriate formatting to get the data into a table (i.e. removed the extensive metadata header). Second, we preprocessed the data, including setting data for the years 2013-2022 aside to be our test dataset. Third, we performed exploratory data analysis on the training data. We observed a clear increasing trend in the mean daily land temperature from 1880 to 2012, suggesting that a linear model could generalize to future unseen years. To ensure that the trend was not seasonal or isolated to specific months (i.e. only the summers were increasing, while winters were staying the same), we created faceted plots by month which confirmed that the increasing pattern persisted across all months. Lastly, the density plots at selected time points (1880, 1960, 2012) show a clear shift towards a higher mean daily land temperatures over time, with very little overlap between the daily mean land temperatures of 1880 and those of 2012.

Lastly, using our training data (1880 - 2012), we further preprocessed our data and trained our model. As part of our model preprocessing, we converted daily temperature anomalies into yearly averages to capture long-term trends and remove noise from short-term and seasonal fluctuations. First, we compared Linear Regression, Random Forest, and Support Vector Regressor (SVR) models on the following metrics: RMSE, MAE and R². The SVR model performed the best out of the three, so we proceeded with SVR with default hyperparameters. Lastly, we used our model to forecast the global land-average temperature in 2030, which our model predicted will be about **10.56 °C.**, 2 °C warmer than average of the baseline period (1951 and 1980) and a clear continuation of the observed warming trend.

## Data

The data set for this project was published by Berkeley Earth under a Creative Commons BY-NC 4.0 International license, free for non-commercial use, and accessed by our team compliant with the conditions in this license on November 18, 2025. The raw data can be found [here](https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt).

The data set contains 5 columns with time series information, and one column representing the temperature difference relative to the average temperature between January 1951 and December 1980, which they calculated as 8.59 +/- 0.05. For our analysis, we preprocessed the data to get the raw temperature readings back by adding 8.59 to each entry in the Anomaly column. All temperatures are in Celcius.

## Dependencies

All software dependencies for this project are managed using Docker. You can build and run the project directly inside the [Docker](https://www.docker.com/) container. This ensures a consistent and reproducible environmenyt across all systems. To install the relevant dependencies, follow the instructions in the Setup Environment section below.


## Running the Analysis

This section describes how to set up the environment, run the full analysis pipeline, execute tests, and render the final report.


## 1. Setup Environment

1. Ensure **Docker** and **Docker Compose** are installed on your machine.

2. Clone this GitHub repository to your local machine.

3. Open a command line interface (e.g., Terminal) and navigate to the **root of this repository**.



## 2. Launch the Docker Environment

Start the multi-container application using Docker Compose:

```bash
docker compose up
````

After the Docker image is built and the container starts, look for a URL in the terminal that looks like:

```
http://127.0.0.1:8888/lab?token=...
```

This appears after the line:

> Or copy and paste one of these URLs

Copy and paste this URL into your browser to launch **JupyterLab**.

---

### Port Conflict Troubleshooting (Optional)

If the page asks for a password or token, port `8888` may already be in use.

To fix this:

1. Stop and remove the current Docker instance:

```bash
docker compose rm
```

2. Open `docker-compose.yml` and change the port to an available one (e.g., 8887 or 8889):

```yaml
ports:
  - "{8888}:8888"
```

3. Restart Docker:

```bash
docker compose up
```

Then open the updated URL:

```
http://127.0.0.1:{8888}/lab?token=...
```

(Replace `{8888}` with the port you selected.)


## 3. Explore the Analysis in JupyterLab

Once Docker launches successfully, you will be in a local **JupyterLab** instance.

Navigate to:

```
global_daily_land_temperature_prediction.qmd
```

to explore the interactive analysis.


## 4. Running the Analysis Pipeline with the Makefile

This project uses a **Makefile** to run the full analysis pipeline and generate all required intermediate files.

To reset the project to a clean state (i.e., remove all generated files), run:

```bash
make clean
```

To run the full analysis from start to finish, run:

```bash
make all
```


## 5. Running Individual Scripts (Optional)

If you prefer to run the analysis step-by-step, ensure you are in the **project root**:

```bash
pwd
```

Then run the scripts in the following order.

### 5.1 Download Raw Data

```bash
python scripts/read_data.py \
  "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt" \
  "data/global_temp_anomaly_raw.csv"
```

Arguments:

* input path (URL or local file)
* output path for the raw data


### 5.2 Data Cleaning and Preprocessing

```bash
python scripts/data_preprocessing.py \
  --read_path="data/global_temp_anomaly_raw.csv" \
  --write_path="data/global_temp_anomaly_cleaned" \
  --plots_path="images" \
  --logs_path="logs"
```

Arguments:

* path to raw data
* output path for cleaned and split data
* directory for plots
* directory for logs


### 5.3 Exploratory Data Analysis (EDA)

```bash
python scripts/abstract_eda.py \
  data/global_temp_anomaly_cleaned_train.csv \
  images/eda.png
```

Arguments:

* cleaned training data
* output path for figures and tables


### 5.4 Model Training and Evaluation

```bash
python scripts/ml_modelling.py \
  --input_path data/global_temp_anomaly_cleaned_full.csv \
  --output_dir results \
  --cutoff_year 2012
```

Arguments:

* cleaned full dataset
* output directory for results
* cutoff year for train/test split


## 6. Testing (Important)

⚠️ **Important:** You must run `make all` **before** running `pytest`.

Some tests depend on files generated during the `make all` step.

### Correct order

```bash
make all
pytest
```

### Common pitfall

Running:

```bash
make clean
pytest
```

will cause tests to fail because required generated files are missing.

After cleaning, always run:

```bash
make all
pytest
```


## 7. Rendering the Final Report

To render the Quarto document as an HTML file, run the following command **from the `reports/` folder**:

```bash
quarto render global_daily_land_temperature_prediction.qmd
```

The rendered file will appear as:

```
global_daily_land_temperature_prediction.html
```

To view the report:

1. Exit Docker
2. Navigate to the local repository
3. Open the HTML file in your preferred browser

> **Note:** Viewing the HTML inside Docker may cause formatting issues.
> To generate a PDF, render to HTML first, open it locally, and save the page as a PDF.


## 8. Shutting Down Docker

When finished:

1. Return to the Terminal running Docker
2. Press `CTRL + C` to stop JupyterLab
3. Remove the Docker instance:

```bash
docker compose rm
```

## Developer notes

### Developer dependencies
- `conda` (version 25.9.1)
- `conda-lock` (version 3.0.4)

### Adding a new dependency

1. Create and switch to a new GitHub branch by running the following command in the terminal

```bash
git checkout -b new-branch-name
```

2. Open the `environment.yml`file and add the new dependencies

3. To update the `conda-linux-64.lock` file, run the following command in the terminal

```bash
conda-lock -k explicit --file environment.yml -p linux-64
```

4. Remember to rebuild the Docker image locally and make sure it runs locally with 

```bash
docker compose up
```

5. To make sure the Docker image builds properly, check GitHub Actions on GitHub.com. Ensure the latest Docker image published sucessfully with a green check icon (note: it will take up to 10 minutes for the Docker image to build).

6. Run 

```bash 
git add modified_file_name
``` 

to add all of the files with edits (e.g. `environment.yml`). Next, run

```bash
git commit -m 'add new dependencies'
```

to commit your changes with a meaningful commit message. Lastly, run

```bash
git push -u origin new-branch-name
```

to push your local changes to the GitHub repo.

7. Create a new pull request in GitHub and merge the changes to the `main` branch after review.

## License

The Predicting Daily Land Average Earth Temperature report contained herein are licensed under the Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License. See the license file for more information. If re-using/re-mixing please provide attribution and link to this webpage. The software code contained within this repository is licensed under the MIT license. See the [license file](https://github.com/kessler24/predicting_daily_land_average_earth_temperature/blob/main/LICENSE.md) for more information.
