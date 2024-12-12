import pytest
import os
import pickle
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.random_search import perform_random_search

@pytest.fixture
def setup_data(request):
    """
    Pytest fixture to set up train, test data, and the pipeline for testing.

    Args:
        request: Pytest's request object to retrieve command-line options for test data paths.

    Returns:
        tuple: A tuple containing:
            - wine_pipe: The loaded pipeline object.
            - X_train: Training features as a DataFrame.
            - y_train: Training labels as a Series.
            - X_test: Testing features as a DataFrame.
            - y_test: Testing labels as a Series.
    """
    # Retrieve paths to data and pipeline from pytest command-line options
    train_data = request.config.getoption("--train_data")
    test_data = request.config.getoption("--test_data")
    pipeline_path = request.config.getoption("--pipeline_path")

    # Load train and test datasets
    wine_train = pd.read_csv(train_data)
    wine_test = pd.read_csv(test_data)

    # Load the pre-built pipeline
    with open(pipeline_path, 'rb') as f:
        wine_pipe = pickle.load(f)

    # Split datasets into features (X) and labels (y)
    X_train = wine_train.drop(columns=["color"])
    y_train = wine_train["color"]
    X_test = wine_test.drop(columns=["color"])
    y_test = wine_test["color"]

    return wine_pipe, X_train, y_train, X_test, y_test


def test_perform_random_search(setup_data, tmp_path):
    """
    Test the `perform_random_search` function for proper execution and output.

    This test ensures that:
        - RandomizedSearchCV object is returned successfully.
        - Best estimator is returned.
        - Best score is a valid float within the range [0, 1].

    Args:
        setup_data: The Pytest fixture providing data and pipeline.
        tmp_path: Pytest's built-in fixture for creating a temporary directory.

    Asserts:
        - The returned object is a RandomizedSearchCV instance.
        - The best estimator is not None.
        - The best score is a float and within a valid range.
    """
    # Extract the setup data
    wine_pipe, X_train, y_train, X_test, y_test = setup_data

    # Define the path for saving the model
    output_path = tmp_path / "wine_random_search.pickle"

    # Call the function under test
    random_s, best_estimator = perform_random_search(
        wine_pipe, X_train, y_train, seed=42, output_path=output_path
    )

    # Assertions to validate the outputs
    assert isinstance(random_s, RandomizedSearchCV), "RandomizedSearchCV object was not returned."
    assert best_estimator is not None, "Best estimator was not returned."
    assert isinstance(random_s.best_score_, float), "Best score is not a float."
    assert 0 <= random_s.best_score_ <= 1, "Best score is not within valid range."


def test_model_saving(setup_data, tmp_path):
    """
    Test that the `perform_random_search` function saves the trained model correctly.

    This test ensures that the output model is saved to the specified path.

    Args:
        setup_data: The Pytest fixture providing data and pipeline.
        tmp_path: Pytest's built-in fixture for creating a temporary directory.

    Asserts:
        - The output file exists at the specified path.
    """
    # Extract the setup data
    wine_pipe, X_train, y_train, _, _ = setup_data

    # Define the path for saving the model
    output_path = tmp_path / "wine_random_search.pickle"

    # Call the function under test
    _, _ = perform_random_search(
        wine_pipe, X_train, y_train, seed=42, output_path=output_path
    )

    # Assert that the model file was saved
    assert os.path.exists(output_path), f"Model file not saved at {output_path}."
