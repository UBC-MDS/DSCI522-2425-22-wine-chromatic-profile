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
    """Fixture to set up train, test data, and the pipeline."""
    train_data = request.config.getoption("--train_data")
    test_data = request.config.getoption("--test_data")
    pipeline_path = request.config.getoption("--pipeline_path")

    # Read in train and test datasets
    wine_train = pd.read_csv(train_data)
    wine_test = pd.read_csv(test_data)
    
    # Load the pipeline
    with open(pipeline_path, 'rb') as f:
        wine_pipe = pickle.load(f)

    # Split data into X and y
    X_train = wine_train.drop(columns=["color"])
    y_train = wine_train["color"]
    X_test = wine_test.drop(columns=["color"])
    y_test = wine_test["color"]

    return wine_pipe, X_train, y_train, X_test, y_test

def test_perform_random_search(setup_data, tmp_path):
    """Test the perform_random_search function with wine dataset and pipeline."""
    wine_pipe, X_train, y_train, X_test, y_test = setup_data

    # Temporary path for saving the model
    output_path = tmp_path / "wine_random_search.pickle"

    # Call the function
    random_s, best_estimator = perform_random_search(
        wine_pipe, X_train, y_train, seed=42, output_path=output_path
    )

    # Assertions
    # Ensure RandomizedSearchCV object is returned
    assert isinstance(random_s, RandomizedSearchCV), "RandomizedSearchCV object was not returned."
    # Ensure the best estimator is returned
    assert best_estimator is not None, "Best estimator was not returned."
    # Ensure the best score is a float
    assert isinstance(random_s.best_score_, float), "Best score is not a float."
    # Ensure the best score is within a reasonable range
    assert 0 <= random_s.best_score_ <= 1, "Best score is not within valid range."


def test_model_saving(setup_data, tmp_path):
    """Test that the model is saved correctly."""
    wine_pipe, X_train, y_train, _, _ = setup_data

    output_path = tmp_path / "wine_random_search.pickle"

    _, _ = perform_random_search(
        wine_pipe, X_train, y_train, seed=42, output_path=output_path
    )

    # Check that the file is saved
    assert os.path.exists(output_path), f"Model file not saved at {output_path}."