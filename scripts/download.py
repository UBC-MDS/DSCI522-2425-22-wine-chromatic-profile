# download.py
# Authors: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-05

import click
import os
import pandas as pd
import sys
from ucimlrepo import fetch_ucirepo

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@click.command()
@click.option('--id', type=int, help="ID of the UCI repository dataset to be fetched")
@click.option('--save_to', type=str, help="Path to save the fetched dataset as a CSV file")

def main(id, save_to):
    """
    Fetches a dataset from the UCI repository by ID and saves it as a CSV file.
    """
    try:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        full_path = os.path.join(root_dir, save_to)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        dataset = fetch_ucirepo(id=id)
        data = pd.DataFrame(dataset.data.original)
    
        data.to_csv(full_path, index=False)
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)

if __name__ == '__main__':
    main()


