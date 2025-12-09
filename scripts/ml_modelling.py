"""
Temperature Anomaly Forecasting Pipeline

This script loads yearly-averaged global temperature anomaly data, trains
multiple regression models, evaluates their performance, and forecasts
temperature anomalies for 2030. The outputs include model performance
tables, forecast values, and visualizations.

Pipeline steps:
- Load daily climate data and aggregate to yearly averages
- Train-test split based on a cutoff year
- Train multiple regression models (Linear, Random Forest, SVR)
- Evaluate models on test set using RMSE, MAE, R2
- Select best model (lowest RMSE) and forecast 2030 anomaly
- Visualize historical anomalies, model trends, and 2030 forecast
- Save all outputs to specified directories

Usage
-----
(from repo root)

python scripts/ml_modelling.py \
    --input_path data/global_temp_anomaly_cleaned_full.csv \
    --output_dir results \
    --cutoff_year 2012

Outputs
-------
- model_results.csv: Evaluation metrics for all models on test set
- forecast_2030.txt: Predicted anomaly and temperature for 2030
- forecast_plot.png: Visualization of train/test data, model trends, and forecast

"""

# -----------------------------
# Core Libraries
# -----------------------------
import os                 # File path handling and directory operations
import click              # Command line interface for user input
import pandas as pd       # DataFrames for data manipulation
import numpy as np        # Numerical operations (arrays, metrics)
import matplotlib.pyplot as plt  # Plotting for visualization

# -----------------------------
# Machine Learning Libraries
# -----------------------------
from sklearn.linear_model import LinearRegression           # Simple linear regression
from sklearn.ensemble import RandomForestRegressor          # Ensemble method
from sklearn.svm import SVR                                  # Support Vector Regression
from sklearn.pipeline import Pipeline                        # Create ML pipelines
from sklearn.preprocessing import StandardScaler             # Feature scaling
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# -----------------------------
# Global Constants
# -----------------------------
BASELINE_TEMP = 8.59  # Baseline land-average temperature (°C)
# This is used to convert anomaly values back to absolute temperature

# -----------------------------
# Command Line Interface
# -----------------------------
@click.command()
@click.option("--input_path", required=True, help="Path to CSV containing daily climate data")
@click.option("--output_dir", required=True, help="Directory to save results")
@click.option("--cutoff_year", default=2012, help="Year to split train/test data")
def main(input_path, output_dir, cutoff_year):
    """
    Main function to execute temperature anomaly forecasting.

    Parameters
    ----------
    input_path : str
        CSV path containing daily temperature anomaly data
    output_dir : str
        Directory where CSV, plot, and forecast outputs will be saved
    cutoff_year : int
        Year used to split training and test data
    """
    
    # -----------------------------------------------------------
    # 1. Load and preprocess data
    # -----------------------------------------------------------
    # Read CSV into pandas DataFrame
    df = pd.read_csv(input_path)

    # Check that all required columns exist in the dataset
    required_cols = {'Year', 'Month', 'Day', 'Anomaly'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Input CSV must contain columns: {required_cols}")

    # Combine Year, Month, Day into a datetime column for resampling
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df.set_index('Date', inplace=True)  # Set Date as index for time-based operations

    # Resample daily anomalies into yearly averages using pandas `resample`
    yearly = df['Anomaly'].resample('A').mean().reset_index()
    yearly['Year'] = yearly['Date'].dt.year  # Extract year as separate column for modeling

    # Features (X) are years, target (y) is anomaly
    X = yearly[['Year']].values  # 2D array for scikit-learn
    y = yearly['Anomaly'].values  # 1D array of anomalies

    # -----------------------------------------------------------
    # 2. Train-test split
    # -----------------------------------------------------------
    # Create boolean masks for train/test split based on cutoff year
    train_mask = yearly['Year'] <= cutoff_year
    test_mask  = yearly['Year'] > cutoff_year

    # Apply masks to split data
    X_train, y_train = X[train_mask], y[train_mask]
    X_test,  y_test  = X[test_mask], y[test_mask]

    # Check that neither training nor test sets are empty
    if X_train.shape[0] == 0 or X_test.shape[0] == 0:
        raise ValueError(
            f"Train or Test split is empty. Check your cutoff year and dataset. "
            f"X_train: {X_train.shape[0]}, X_test: {X_test.shape[0]}"
        )

    # -----------------------------------------------------------
    # 3. Define models
    # -----------------------------------------------------------
    # Dictionary mapping model names to sklearn model instances
    # This allows iterating over multiple models easily
    models = {
        "Linear Regression": LinearRegression(),  # Simple linear trend model
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),  # Ensemble tree-based
        "SVR": Pipeline([  # SVR requires feature scaling for better convergence
            ('scaler', StandardScaler()),  # Standardize years for SVR
            ('svr', SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.01))  # RBF kernel SVR
        ])
    }

    # -----------------------------------------------------------
    # 4. Train, predict, and evaluate
    # -----------------------------------------------------------
    results = {}  # Dictionary to store evaluation metrics

    # Loop over each model, train, predict, and calculate metrics
    for name, model in models.items():
        model.fit(X_train, y_train)         # Fit model on training data
        y_pred = model.predict(X_test)      # Predict anomalies on test data

        # Calculate common regression metrics
        results[name] = {
            "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),  # Root Mean Squared Error
            "MAE": mean_absolute_error(y_test, y_pred),           # Mean Absolute Error
            "R2": r2_score(y_test, y_pred)                        # Coefficient of determination
        }

    # Convert results dict to DataFrame for readability and saving
    results_table = pd.DataFrame(results).T
    print("\nModel Performance on Test Set:\n")
    print(results_table)

    # Rename the index column
    results_table.index.name = 'Model'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Save evaluation table as CSV
    results_table.to_csv(f"{output_dir}/model_results.csv")

    # -----------------------------------------------------------
    # 5. Select best model
    # -----------------------------------------------------------
    # Select model with lowest RMSE as "best"
    best_model_name = results_table["RMSE"].idxmin()
    best_model = models[best_model_name]
    print(f"\nBest model: {best_model_name}")

    # -----------------------------------------------------------
    # 6. Forecast 2030
    # -----------------------------------------------------------
    # Prepare 2030 as input for model prediction
    year_2030 = np.array([[2030]])  # 2D array for sklearn

    # Predict anomaly for 2030 using best model
    forecast_2030_anomaly = best_model.predict(year_2030)[0]
    # Convert anomaly to absolute land-average temperature
    forecast_2030_temp = BASELINE_TEMP + forecast_2030_anomaly

    # Print forecast
    print(f"\nPredicted anomaly for 2030: {forecast_2030_anomaly:.4f} °C")
    print(f"Predicted land-average temperature for 2030: {forecast_2030_temp:.4f} °C")

    # Save forecast to text file
    with open(f"{output_dir}/forecast_2030.txt", "w") as f:
        f.write(f"Predicted anomaly for 2030: {forecast_2030_anomaly:.4f} °C\n")
        f.write(f"Predicted temperature for 2030: {forecast_2030_temp:.4f} °C\n")

    # -----------------------------------------------------------
    # 7. Plot results
    # -----------------------------------------------------------
    plt.figure(figsize=(10,6))  # Set figure size

    # Scatter plot: training anomalies
    plt.scatter(
        yearly['Year'][train_mask], yearly['Anomaly'][train_mask],
        alpha=0.6, color='blue', label='Train Data'
    )

    # Scatter plot: test anomalies
    plt.scatter(
        yearly['Year'][test_mask], yearly['Anomaly'][test_mask],
        alpha=0.8, color='orange', label='Test Data'
    )

    # Plot trend line for best model across all years
    plt.plot(
        yearly['Year'], best_model.predict(X),
        color='black', label=f'{best_model_name} Trend'
    )

    # Highlight 2030 forecast as red dot
    plt.scatter(2030, forecast_2030_anomaly, color='red', s=100, label='2030 Forecast')

    # Vertical line marking train-test split
    plt.axvline(cutoff_year, color='gray', linestyle='--', label='Train/Test Split')

    # Add labels, title, and legend
    plt.xlabel("Year")
    plt.ylabel("Temperature Anomaly (°C)")
    plt.title("Global Temperature Anomaly Forecast")
    plt.legend()
    plt.tight_layout()  # Adjust layout for clarity

    # Save plot to output directory
    plt.savefig(f"{output_dir}/forecast_plot.png", dpi=300)
    plt.show()

    print("\nAll outputs saved successfully!")

# Entry point for CLI
if __name__ == "__main__":
    main()
