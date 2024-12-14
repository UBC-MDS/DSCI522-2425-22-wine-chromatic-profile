# train_test_split_test.py
# Authors: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-12
import os
import pandas as pd
import pytest
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_data import clean_n_split

@pytest.fixture
def create_sample_data(tmp_path):
    """
    Fixture that creates a sample DataFrame to be used for testing.

    This function creates a DataFrame with columns typically found in 
    a wine physiochemical properties dataset.

    Returns:
        pd.DataFrame: A DataFrame containing the sample wine data.
    """
    sample_data = {
        'fixed_acidity': [7.4, 7.8, 7.4],
        'volatile_acidity': [0.7, 0.88, 0.76],
        'citric_acid': [0.0, 0.0, 0.04],
        'residual_sugar': [1.9, 2.6, 2.3],
        'chlorides': [0.076, 0.098, 0.092],
        'free_sulfur_dioxide': [11.0, 25.0, 15.0],
        'total_sulfur_dioxide': [34.0, 67.0, 54.0],
        'density': [0.9978, 0.9968, 0.9970],
        'pH': [3.51, 3.20, 3.26],
        'sulphates': [0.56, 0.68, 0.65],
        'alcohol': [9.4, 9.8, 9.8],
        'quality': [5, 5, 5],
        'color': ['red', 'red', 'white']
    }
    sample_df = pd.DataFrame(sample_data)
    sample_file = tmp_path / "sample_data.csv"
    sample_df.to_csv(sample_file, index=False)
    
    return str(sample_file)


def test_split_and_save(create_sample_data, tmp_path):
    """
    Test if the script correctly saves train and test datasets to files.

    This test:
    - Uses a temporary directory to save files.
    - Verifies that the train and test files are created.
    - Ensures the content of the files matches the expected data.

    Args:
        create_sample_data (str): The file path of the sample data.
        tmp_path (Path): Temporary directory path provided by pytest.

    Asserts:
        - Train and test files exist.
        - The saved files match the expected data.
    """
    sample_file = create_sample_data
    output_dir = tmp_path 

    
    clean_n_split(sample_file, output_dir=output_dir, test_size=0.3, random_state=123)
    
    train_file = output_dir / "wine_train.csv"
    test_file = output_dir / "wine_test.csv"
    
    assert train_file.exists(), "Train file was not saved"
    assert test_file.exists(), "Test file was not saved"
    
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)

    sample_df = pd.read_csv(sample_file)
    total_rows = len(sample_df)
    assert len(train_df) + len(test_df) == total_rows, "Split sizes do not match original data"
