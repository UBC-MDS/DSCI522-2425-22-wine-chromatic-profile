# split_n_preprocess.py
# author: Tiffany Timbers
# date: 2023-11-27

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--pipe-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(raw_data, data_to, preprocessor_to, seed):
    '''This script makes the preprocessor and model pipeline'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    wine = pd.read_csv(raw_data)

    ordinal_features = ["quality"]
    numerical_features = [col for col in wine.columns if col != "color" and col != "quality"]

    preprocessor = make_column_transformer(
        (OrdinalEncoder(dtype=int), ordinal_features),
        (StandardScaler(), numerical_features),
        remainder='passthrough' 
    )
    wine_pipe = make_pipeline(
        preprocessor, 
        LogisticRegression(random_state=seed, max_iter=1000, class_weight="balanced"),
    )
    
    # save pipeline
    pickle.dump(wine_pipe, open(os.path.join(pipe_to, "wine_pipeline.pickle"), "wb"))

if __name__ == '__main__':
    main()