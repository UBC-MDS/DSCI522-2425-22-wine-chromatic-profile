import pytest
import os
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_column_names import validate_column_names

# Correct columns
correct_columns = {"column1", "column2", "column3"}

# Test data
correct_df = pd.DataFrame(columns=["column1", "column2", "column3"])
extra_column_df = pd.DataFrame(columns=["column1", "column2", "column3", "extra_column"])
missing_column_df = pd.DataFrame(columns=["column1", "column2"])
wrong_column_df = pd.DataFrame(columns=["wrong_column1", "wrong_column2", "wrong_column3"])

# Test for correct column names
def test_validate_column_names_correct():
    try:
        validate_column_names(correct_df, correct_columns)
    except ValueError:
        pytest.fail("validate_column_names raised ValueError unexpectedly for correct columns.")

# Test for extra column
def test_validate_column_names_extra_column():
    with pytest.raises(ValueError, match="Unexpected columns:"):
        validate_column_names(extra_column_df, correct_columns)

# Test for missing column
def test_validate_column_names_missing_column():
    with pytest.raises(ValueError, match="Missing columns:"):
        validate_column_names(missing_column_df, correct_columns)

# Test for completely wrong columns
def test_validate_column_names_wrong_column():
    with pytest.raises(ValueError, match="Unexpected columns:"):
        validate_column_names(wrong_column_df, correct_columns)

# Test for both extra and missing columns
def test_validate_column_names_extra_and_missing():
    mixed_df = pd.DataFrame(columns=["column1", "extra_column"])
    with pytest.raises(ValueError, match="Unexpected columns:.*missing columns:"):
        validate_column_names(mixed_df, correct_columns)