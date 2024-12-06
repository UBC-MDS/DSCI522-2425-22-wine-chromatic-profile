# preprocessing.py
# author: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-05

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
@click.option('--pipe-to', type=str, help="Path to directory where the pipeline object will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(pipe_to, seed):
    '''This script makes the preprocessor and model pipeline'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    ordinal_features = ["quality"]
    numerical_features = [
        'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides', 
        'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol'
    ]

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
    pipe_path = os.path.join(pipe_to, "wine_pipeline.pickle")
    os.makedirs(os.path.dirname(pipe_path), exist_ok=True)
    pickle.dump(wine_pipe, open(pipe_path, "wb"))

if __name__ == '__main__':
    main()