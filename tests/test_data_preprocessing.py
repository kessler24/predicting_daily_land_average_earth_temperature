import pytest
import pandas as pd
import math
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.data_preprocessing import data_cleaning

# run all tests
def main():
    test_returns_dataframe()
    test_empty_returns_empty()
    test_ranges()
    test_columns_not_modified()
    test_returned_types()
    test_drop_date_number_column()
    test_month_names()
    test_add_temperature_column()
    test_set_baseline()
    test_incorrect_types_errors()
    print("All tests passed.")

# create general test data
raw_test_data = pd.DataFrame({
    "Date Number" : [1880.001, 1880.004, 1880.007],
    "Year" : [1880, 1880, 1880],
    "Month" : [1, 1, 1],
    "Day" : [1, 2, 3],
    "Day of Year" : [1, 2, 3],
    "Anomaly" : [-0.692, -0.592, -0.673]
})

# test that passing a non-empty dataframe returns a non-empty dataframe
def test_returns_dataframe():
    cleaned_data = data_cleaning(raw_test_data)
    assert isinstance(cleaned_data, pd.DataFrame)
    assert cleaned_data.loc(0) is not None

# test that passing an empty dataframe returns an empty dataframe
raw_test_data_empty = pd.DataFrame({
    "Date Number" : pd.Series([], dtype="float64"),
    "Year" : pd.Series([], dtype="int64"),
    "Month" : pd.Series([], dtype="int64"),
    "Day" : pd.Series([], dtype="int64"),
    "Day of Year" : pd.Series([], dtype="int64"),
    "Anomaly" : pd.Series([], dtype="float64")
})

def test_empty_returns_empty():
    assert (data_cleaning(raw_test_data_empty)).empty

# test that the numbers for month, day, and day of year are within the expected ranges
raw_test_data_range_limits = pd.DataFrame({
    "Date Number" : [0, 0, 0],
    "Year" : [1880, 2000, 2022],
    "Month" : [1, 5, 12],
    "Day" : [1, 15, 31],
    "Day of Year" : [1, 60, 365],
    "Anomaly" : [-0.692, -0.592, -0.673]
})

def test_ranges():
    cleaned_data_range_limits = data_cleaning(raw_test_data_range_limits)
    assert cleaned_data_range_limits["Month"].between(1, 12).all()
    assert cleaned_data_range_limits["Day"].between(1, 31).all()
    assert cleaned_data_range_limits["Day of Year"].between(1, 365).all()

# test that year, month, day, day of year, and anomaly are not modified in data cleaning
def test_columns_not_modified():
    cleaned_data = data_cleaning(raw_test_data)
    assert (cleaned_data["Year"]).equals(raw_test_data["Year"])
    assert (cleaned_data["Month"]).equals(raw_test_data["Month"])
    assert (cleaned_data["Day"]).equals(raw_test_data["Day"])
    assert (cleaned_data["Day of Year"]).equals(raw_test_data["Day of Year"])

# test that all returned columns are of the expected type
def test_returned_types():
    cleaned_data = data_cleaning(raw_test_data)

    expected_types = {
        "Year": "int64",
        "Month": "int64",
        "Day": "int64",
        "Day of Year": "int64",
        "Anomaly": "float64",
        "Temperature": "float64",
        "Month_Name": pd.CategoricalDtype(categories=['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December'], ordered=True)
    }

    assert cleaned_data.dtypes.to_dict() == expected_types

# test that date column is dropped
def test_drop_date_number_column():
    cleaned_data = data_cleaning(raw_test_data)
    assert "Date Number" not in cleaned_data.columns 

# test that the Month_Name categorical column is properly for every month number
raw_test_data_all_months = pd.DataFrame({
    "Date Number" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Year" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Month" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Day" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Day of Year" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Anomaly" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
})

def test_month_names():
    clean_test_data_all_months = data_cleaning(raw_test_data_all_months)
    cleaned_month_list = [
        'January', 
        'February', 
        'March', 
        'April', 
        'May', 
        'June', 
        'July', 
        'August', 
        'September', 
        'October', 
        'November', 
        'December'
    ]
    
    assert(list(clean_test_data_all_months['Month_Name']) == cleaned_month_list)

# test the calculation for temperature using default baseline
def test_add_temperature_column():
    cleaned_data = data_cleaning(raw_test_data)
    assert "Temperature" in cleaned_data.columns
    assert math.isclose(cleaned_data["Temperature"][0], 7.898, abs_tol = 0.001)

# test the calculation for temperature using another baseline
def test_set_baseline():
    cleaned_data = data_cleaning(raw_test_data, 1.0)
    assert math.isclose(cleaned_data["Temperature"][0], (-0.692 + 1), abs_tol = 0.001)

# test that passing a dataframe with incompatible data types raises a TypeError
raw_test_data_incorrect_year = pd.DataFrame({
    "Date Number" : [1880.001, 1880.004, 1880.007],
    "Year" : ["1880", 1880.6, (2000*3)],
    "Month" : [1, 1, 1],
    "Day" : [1, 2, 3],
    "Day of Year" : [1, 2, 3],
    "Anomaly" : [-0.692, -0.592, -0.673]
})

raw_test_data_incorrect_day = pd.DataFrame({
    "Date Number" : [1880.001, 1880.004, 1880.007],
    "Year" : [1880, 1880, 1880],
    "Month" : [1, 1, 1],
    "Day" : [1.1, (4/3), "2"],
    "Day of Year" : [1, 2, 3],
    "Anomaly" : [-0.692, -0.592, -0.673]
})

raw_test_data_multi_incorrect = pd.DataFrame({
    "Date Number" : [1880.001, 1880.004, 1880.007],
    "Year" : ["1880", 1880.6, (2000*3)],
    "Month" : [1, 1, 1],
    "Day" : [1.1, (4/3), "2"],
    "Day of Year" : [1, 2, 3],
    "Anomaly" : [-0.692, -0.592, -0.673]
})

def test_incorrect_types_errors():
  with pytest.raises(TypeError):
    data_cleaning(raw_test_data_incorrect_year)
    data_cleaning(raw_test_data_incorrect_day)
    data_cleaning(raw_test_data_multi_incorrect)

# test when values in anomaly are very large
# test when values in year are very large or negative
# test when column names are misspelled
# test when some columns missing

if __name__ == "__main__":
    main()
