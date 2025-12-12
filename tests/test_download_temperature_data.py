import pytest
import pandas as pd
from src.download_temperature_data import download_temperature_data

# fixture
@pytest.fixture
def sample_raw_data():
    """return raw data in the format of the Berkeley Earth data"""
    
    return """\
1880.001     1880     1     1        1      -0.692
1880.004     1880     1     2        2      -0.592
1880.007     1880     1     3        3      -0.673
1880.010     1880     1     4        4      -0.615
1880.012     1880     1     5        5      -0.681
1880.015     1880     1     6        6      -0.743
1880.018     1880     1     7        7      -0.646
1880.021     1880     1     8        8      -0.716
1880.023     1880     1     9        9      -0.984
"""

@pytest.fixture
def sample_input_file_path(file_path, sample_raw_data):
    """Generate a temporary file path with the sample raw data"""
    input_file_path = file_path/"raw_sample_data.txt"
    input_file_path.write_text(sample_raw_data)
    return input_file_path

# tests
def test_invalid_input(temp_path):
    """Test when the input file is not in a readable format or cannot be found"""

    # create a bad example out output
    bad_input_file = temp_path/"output_data"
    test_output_file = temp_path/"output_data.csv"

    with pytest.raises(IOError):
        download_temperature_data(str(bad_input_file), str(test_output_file))

def test_invalid_output_path(test_input_file, temp_path):
    """Test when the output is not written as a .csv file"""

    # create a bad example out output
    bad_output_file = temp_path/"output_data.txt"
    
    #run the funtion
    download_temperature_data(str(test_input_file), str(bad_output_file))

    #check if the file is still saved 
    assert not bad_output_file.exists()

def test_dowanload_data(test_input_file, temp_path):
    """Test if a white space delimited file can be read successfully"""
   
    #create an output file path for saved data
    output_file = temp_path/"output_data.csv"
    
    #run the funtion and read the output file as a dataframe
    download_temperature_data(str(test_input_file), str(output_file))
    saved_df = pd.read_csv(output_file)

    #check if the output file exists
    assert output_file.exists()

    #check if the data frame size is as the size of the sample_raw_data
    assert saved_df.shape == (9, 6)

    #check if the column names are as assigned in download_temperature_data()
    assert list(saved_df.columns) == ["Date Number", "Year", "Month", "Day", "Day of Year", "Anomaly"]





    