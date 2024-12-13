# clean_data.py
# Authors: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-12

import click
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.split_data import clean_n_split

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")

def main(raw_data):
    '''This script drops duplicates from the data, 
    as well as splits the raw data into train and test sets
    '''
    clean_n_split(raw_data)

if __name__ == '__main__':
    main()

