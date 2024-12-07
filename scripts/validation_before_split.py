# validation_before_split.py
# author: Adrian Leung, Daria Khon, Farhan Bin Faisal, Zhiwei Zhang
# date: 2024-12-05

import os
import click
import pandas as pd
import pandera as pa

# Define schemas for validation
def define_schemas():
    # Checking for missingness
    base_checks = [pa.Check(lambda s: s.isna().mean() <= 0.05, element_wise=False, error="Too many null values.")]
    
    general_schema = pa.DataFrameSchema({
        "fixed_acidity": pa.Column(float, base_checks, nullable=True),
        "volatile_acidity": pa.Column(float, base_checks, nullable=True),
        "citric_acid": pa.Column(float, base_checks, nullable=True),
        "residual_sugar": pa.Column(float, base_checks, nullable=True),
        "chlorides": pa.Column(float, base_checks, nullable=True),
        "free_sulfur_dioxide": pa.Column(float, base_checks, nullable=True),
        "total_sulfur_dioxide": pa.Column(float, base_checks, nullable=True),
        "density": pa.Column(float, base_checks, nullable=True),
        "pH": pa.Column(float, base_checks, nullable=True),
        "sulphates": pa.Column(float, base_checks, nullable=True),
        "alcohol": pa.Column(float, base_checks, nullable=True),
        "quality": pa.Column(int, base_checks, nullable=True),
        "color": pa.Column(str, base_checks, nullable=True)
    })

    outlier_schema = pa.DataFrameSchema({
        "fixed_acidity": pa.Column(float, pa.Check.between(3.5, 16)),
        "volatile_acidity": pa.Column(float, pa.Check.between(0.08, 1.6)),
        "citric_acid": pa.Column(float, pa.Check.between(0.0, 1)),
        "residual_sugar": pa.Column(float, pa.Check.between(0.5, 66)),
        "chlorides": pa.Column(float, pa.Check.between(0.01, 0.7)),
        "free_sulfur_dioxide": pa.Column(float, pa.Check.between(0, 200)),
        "total_sulfur_dioxide": pa.Column(float, pa.Check.between(0, 400)),
        "density": pa.Column(float, pa.Check.between(0.985, 1.04)),
        "pH": pa.Column(float, pa.Check.between(2.5, 4.0)),
        "sulphates": pa.Column(float, pa.Check.between(0.2, 1.8)),
        "alcohol": pa.Column(float, pa.Check.between(8.0, 15.0)),
        "quality": pa.Column(int, pa.Check.between(3, 9))
    })

    category_schema = pa.DataFrameSchema({
        "color": pa.Column(str, pa.Check.isin(["red", "white"]))
    })

    duplicate_check = pa.DataFrameSchema(checks=[
        pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found.")
    ])

    empty_row_check = pa.DataFrameSchema(
            checks=[
                pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
    ])

    return general_schema, outlier_schema, category_schema, duplicate_check, empty_row_check


# Validate column names
def validate_column_names(wine, correct_columns):
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

@click.command()
@click.option("--file_name", required=True, help="Name of the input CSV file.")
@click.option("--data_path", required=True, help="Path to the directory containing the file.")
# Main function for script execution
def main(file_name, data_path):
    path = os.path.join(data_path, file_name)
    
    # 1. Validate file existence and format
    if not os.path.exists(path):
        raise FileNotFoundError(f"{file_name} does not exist inside the {data_path} directory")
    if not path.endswith('.csv'):
        raise ValueError("File extension is not in .csv format")
    print("File existence and format test passed!")

    # Read data
    wine = pd.read_csv(path)
    
    # Define correct columns
    correct_columns = {
        'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
        'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates',
        'alcohol', 'quality', 'color'
    }
    
    # 2. Validate column names
    validate_column_names(wine, correct_columns)
    
    # Load schemas
    general_schema, outlier_schema, category_schema, duplicate_check, empty_row_check = define_schemas()

    # 3, 4 General validation #Missingness check
    # General validation (Colum type check & Missingness check)
    try:
        general_schema.validate(wine, lazy=True)
        print("General validation passed!")
    except pa.errors.SchemaErrors as e:
        print("General validation failed:", e)

    # 5.Category validation # Checking correct column types
    # Empty row validation
    try:
        empty_row_check.validate(wine, lazy=True)
        print("Empty row check passed!")
    except pa.errors.SchemaErrors as e:
        print("Empty row check failed:")
        print(pd.DataFrame(e.failure_cases).to_string())

    # Outlier validation
    try:
        outlier_schema.validate(wine, lazy=True)
        print("Outlier validation passed!")
    except pa.errors.SchemaErrors as e:
        print("Outlier validation failed:")
        print(pd.DataFrame(e.failure_cases).to_string())

    # Category validation
    try:
        category_schema.validate(wine, lazy=True)
        print("Category validation passed!")
    except pa.errors.SchemaErrors as e:
        print("Category validation failed:", e)

    # 6. Duplicate row validation
    try:
        duplicate_check.validate(wine, lazy=True)
        print("Duplicate check passed!")
    except pa.errors.SchemaErrors as e:
        print("Duplicate check failed:")
        print(pd.DataFrame(e.failure_cases).to_string())

    # 7. Outlier validation
    try:
        outlier_schema.validate(wine, lazy=True)
        print("Outlier validation passed!")
    except pa.errors.SchemaErrors as e:
        print("Outlier validation failed:")
        print(pd.DataFrame(e.failure_cases).to_string())

if __name__ == "__main__":
    main()