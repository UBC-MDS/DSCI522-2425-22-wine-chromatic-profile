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
def create_sample_data():
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
    return sample_df

def test_split_size_no_duplicates(create_sample_data):
    """
    Test the correctness of data splitting and ensure no duplicates exist in the raw or split data.

    This test function:
    - Ensures that the input data contains no duplicate rows.
    - Verifies that the dataset is split into training and testing sets with the correct proportions (70% training, 30% testing).

    Args:
        create_sample_data (pd.DataFrame): The sample DataFrame provided by the fixture.
    Asserts:
        - raw data does not contain duplicates
        - data is split into correct sizes
    """
    sample_df = create_sample_data

    assert sample_df.duplicated().sum() == 0, "Duplicates found in the raw data"

    train_df, test_df = clean_n_split(sample_df)
    total_rows = len(sample_df)
    train_rows = len(train_df)
    test_rows = len(test_df)

    assert train_rows + test_rows == total_rows, "The split sizes do not match the total rows"
    assert test_rows == int(total_rows * 0.3), "Test split size is incorrect"
    assert train_rows == total_rows - test_rows, "Train split size is incorrect"
