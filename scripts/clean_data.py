# clean data
# Authors: Daria Khon, Farhan Bin Faisel, Adrian Leung, Zhiwei Zhang
# date: 2024-12-05

import click
import os
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn import set_config
import sys

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")

def main(raw_data):
    '''This script drops duplicates from the data, as well as
    splits the raw data into train and test sets'''
    
    set_config(transform_output="pandas")
    colnames = [
        'fixed_acidity', 
        'volatile_acidity', 
        'citric_acid', 
        'residual_sugar', 
        'chlorides', 
        'free_sulfur_dioxide', 
        'total_sulfur_dioxide', 
        'density', 
        'pH', 
        'sulphates', 
        'alcohol', 
        'quality', 
        'color'
    ]

    # clean data
    wine = pd.read_csv(raw_data).drop_duplicates()
    wine.to_csv('../data/wine_debug.csv')
    
    # create the split
    train_df, test_df = train_test_split(
        wine, test_size=0.3, shuffle=True, random_state=123
    )
    path = Path(__file__).parent
 
    train_df.to_csv(path/ "../data/wine_train.csv", index = False)
    test_df.to_csv(path/ "../data/wine_test.csv", index = False)
    
if __name__ == '__main__':
    main()