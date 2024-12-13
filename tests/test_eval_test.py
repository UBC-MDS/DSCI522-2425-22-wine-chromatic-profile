import pytest
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.test_evaluation import test_evaluation

# Create data to test
X_test_data = {
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
    'quality': [5, 5, 5]
}
X_test = pd.DataFrame(X_test_data)
y_test = pd.Series(['red', 'red', 'white'])

# Create a fitted model
model = LogisticRegression(seed=123, max_iter=1000, class_weight="balanced")
model.fit(X_test, y_test)

# temporaray plot_to, table_to paths
plot_to = "../temp/plots"
table_to = "../temp/tables"


def test_saving():
    """
    This tests that the function test_evaluation saves the plots and tables in the right place
    """
    test_evaluation(model, X_test, y_test, plot_to, table_to)

    table_path = '../temp/tables/test_scores.csv'
    con_plot_path = '../temp/plots/confusion_matrix.png'
    pr_plot_path = '../temp/plots/pr_curve.png'

    assert os.path.exists(table_path), f"Test scores results does not exist in the directory '{table_path}'"
    assert os.path.exists(con_plot_path), f"Confusion matrix does not exist in the directory '{con_plot_path}'"
    assert os.path.exists(pr_plot_path), f"PR curve does not exist in the directory '{pr_plot_path}'"


def test_table():
    """
    This tests the table output saved in the table path.
    """

    table_path = '../temp/tables/test_scores.csv'
    test_scores = pd.read_csv(table_path)

    # test if the output test scores dataframe has only one row
    assert test_scores.shape[0] == 1, "The test scores dataframe does not contain one row."
    # test if the output test scores dataframe has 4 columns
    assert test_scores.shape[1] == 4, "The test scores dataframe does not contain four columns."
    # test the output test scores column names
    assert list(test_scores.columns) == ["accuracy", "precision", "recall", "F1 score"], "The test scores dataframe does not contain the correct columns names."
    # test the scores are floats
    assert isinstance(test_scores.iloc[0, 0], float), "Accuracy score is not a float."
    assert isinstance(test_scores.iloc[0, 1], float), "Precision score is not a float."
    assert isinstance(test_scores.iloc[0, 2], float), "Recall score is not a float."
    assert isinstance(test_scores.iloc[0, 3], float), "F1 score is not a float."
    # check the range of the scores
    assert 0 <= test_scores.iloc[0, 0] <= 1, "Accuracy is not within valid range."
    assert 0 <= test_scores.iloc[0, 1] <= 1, "Precision is not within valid range."
    assert 0 <= test_scores.iloc[0, 2] <= 1, "Recall is not within valid range."
    assert 0 <= test_scores.iloc[0, 3] <= 1, "F1 is not within valid range."