def validate_column_names(wine, correct_columns):
    """
    This function validates that the column names of the provided DataFrame match the expected column names.

    Parameters:
    ----------
    wine : pandas.DataFrame
        The DataFrame to validate.
    correct_columns : set
        A set of expected column names.

    Raises:
    ------
    ValueError
        If the column names in the DataFrame don't match the expected column names.
        The error will specify:
        - Unexpected columns (columns present in the DataFrame but not in the expected set).
        - Missing columns (columns expected but not present in the DataFrame).

    Returns:
    -------
    None
        If the column names match the expected set, the function will print "Column name test passed!".
    
    Example:
    -------
    >>> import pandas as pd
    >>> wine_df = pd.DataFrame(columns=["feature1", "feature2", "target"])
    >>> expected_columns = {"feature1", "feature2", "target"}
    >>> validate_column_names(wine_df, expected_columns)
    Column name test passed!
    
    >>> incorrect_df = pd.DataFrame(columns=["feature1", "feature3"])
    >>> validate_column_names(incorrect_df, expected_columns)
    ValueError: Unexpected columns: ['feature3'], missing columns: ['feature2', 'target']
    """
    extracted_columns = set(wine.columns)
    if extracted_columns != correct_columns:
        wrong_columns = extracted_columns.difference(correct_columns)
        missing_columns = correct_columns.difference(extracted_columns)
        if wrong_columns and missing_columns:
            raise ValueError(f"Unexpected columns: {list(wrong_columns)}, missing columns: {list(missing_columns)}")
        elif wrong_columns:
            raise ValueError(f"Unexpected columns: {list(wrong_columns)}")
        elif missing_columns:
            raise ValueError(f"Missing columns: {list(missing_columns)}")
    else:
        print("Column name test passed!")