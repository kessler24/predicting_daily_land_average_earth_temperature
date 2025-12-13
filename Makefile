# Makefile

# Adapted from Lecture Book Part 24: Tiffany Timbers, Nov 2018
# 24  Data analysis pipelines with GNU Make
# https://ubc-dsci.github.io/reproducible-and-trustworthy-workflows-for-data-science/lectures/180-pipelines-make.html#gnu-make-as-a-data-analysis-pipeline-tool

# Before running the commands below ensure your environment has
# the required dependencies by running $ docker compose up.

# Example usage:
# $ make all
# $ make clean

# Setup PHONY targets
.PHONY: all downloading preprocessing eda model report clean

# run entire analysis
all: report

# Get the raw data from the url
downloading : scripts/read_data.py
	python scripts/read_data.py \
        "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt" \
        "data/global_temp_anomaly_raw.csv"

# Run the preprocessing and generate the images and data
preprocessing : scripts/data_preprocessing.py downloading
	python scripts/data_preprocessing.py \
	--read_path="data/global_temp_anomaly_raw.csv" \
	--write_path="data/global_temp_anomaly_cleaned" \
	--plots_path="images" \
	--logs_path="logs"

# Use default values for Makefile consistency
eda : preprocessing scripts/abstract_eda.py
	python scripts/abstract_eda.py

model: scripts/ml_modelling.py preprocessing
	python scripts/ml_modelling.py \
	--input_path data/global_temp_anomaly_cleaned_full.csv \
	--output_dir results \
	--cutoff_year 2012

# write the report
report : reports/global_daily_land_temperature_prediction.qmd preprocessing eda model
	quarto render reports/global_daily_land_temperature_prediction.qmd

clean : 
	rm -f data/global_temp_anomaly_cleaned_full.csv \
		data/global_temp_anomaly_cleaned_test.csv \
		data/global_temp_anomaly_cleaned_train.csv \
		data/global_temp_anomaly_raw.csv \
		images/eda_training_data_info_table.csv \
		images/eda_training_data_stats_table.csv \
		results/forecast_2030.csv \
		results/model_results.csv \
		results/forecast_plot.png \
		images/correlation_heatmap.png \
		images/eda_density_distributions_plot.png \
		images/eda_facet_by_month_plot.png \
		images/eda_linear_fit_plot.png \
		images/eda_mean_per_year_plot.png \
		images/month_vs_day_of_year_correlation.png \
		images/temperature_and_anomaly_distributions.png \
		reports/global_daily_land_temperature_prediction.html \
		reports/global_daily_land_temperature_prediction.pdf