import os
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn import set_config

def clean_n_split(raw_data_path, test_size=0.3, random_state=123):
    """
    Cleans raw data and splits it into test and train sets, 
    which are put into data/proc/ directory

    This function reads the raw wine data from a CSV file, removes any duplicate rows, 
    and splits the data into training and testing sets. The proportions of the training 
    and testing sets are controlled by the `test_size` parameter. The resulting datasets 
    are then saved as CSV files in a specified directory.

    Parameters:
        raw_data_path (str): The file path to the raw data CSV file that needs to be processed.
        test_size (float, optional): The proportion of the data to be used for the test set. 
                                      Defaults to 0.3 (30% test set, 70% train set).
        random_state (int, optional): A seed for the random number generator to ensure reproducibility. 
                                      Defaults to 123.

    Returns:
        None: The function does not return any values. It saves the processed datasets as CSV files.
    
    Example:
        clean_n_split("data/raw/wine_data.csv")
    """
    set_config(transform_output="pandas")
    
    wine = pd.read_csv(raw_data_path).drop_duplicates()
    
    train_df, test_df = train_test_split(
        wine, 
        test_size=test_size, 
        shuffle=True, 
        random_state=random_state
    )
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), "data/proc")

    train_df.to_csv(output_dir + "/wine_train.csv", index=False)
    test_df.to_csv(output_dir + "/wine_test.csv", index=False)
    

