import pytest

def pytest_addoption(parser):
    parser.addoption("--train_data", action="store", help="Path to train data CSV file")
    parser.addoption("--test_data", action="store", help="Path to test data CSV file")
    parser.addoption("--pipeline_path", action="store", help="Path to pickled pipeline")