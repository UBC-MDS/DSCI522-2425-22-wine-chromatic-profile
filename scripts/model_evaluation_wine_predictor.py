# model_evaluation_wine_predictor.py
# author: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-05

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.metrics import (
    ConfusionMatrixDisplay, PrecisionRecallDisplay, 
    make_scorer, recall_score, precision_score, f1_score, 
    accuracy_score
)

from sklearn.model_selection import cross_validate
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import PredictionDrift

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.random_search import perform_random_search
from src.evaluation import evaluation


@click.command()
@click.option('--train-data', type=str, help="Path to train data")
@click.option('--test-data', type=str, help="Path to test data")
@click.option('--pipeline-path', type=str, help="Path to directory where the pipeline object lives")
@click.option('--table-to', type=str, help="Path to directory where the tables will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plots will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)

def main(train_data, test_data, pipeline_path, table_to, plot_to, seed):
    '''Optimize the wine chromatic profile classifier
    and evaluates the wine chromatic profile classifier on the test data 
    and saves the optimization and evaluation results.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")

    # Create paths to save tables and plots if they do not exist
    if not os.path.exists(table_to):
        os.mkdir(table_to)
    if not os.path.exists(plot_to):
        os.mkdir(plot_to)

    # Read in data & wine_pipe (pipeline object)
    wine_train = pd.read_csv(train_data)
    wine_test = pd.read_csv(test_data)
    with open(pipeline_path, 'rb') as f:
        wine_pipe = pickle.load(f)

    # Split train and test data into X and y
    X_train = wine_train.drop(columns = ["color"])
    y_train = wine_train["color"]
    X_test = wine_test.drop(columns = ["color"])
    y_test = wine_test["color"]

    # Running cross validation on default model
    scoring = {
        "accuracy": 'accuracy',
        'precision': make_scorer(precision_score, pos_label = 'red'),
        'recall': make_scorer(recall_score, pos_label = 'red'),
        'f1': make_scorer(f1_score, pos_label = 'red')
    }

    # Hyperparameter Optimization with RandomizedSearchCV via F1 scoring
    random_search, best_estimator = perform_random_search(wine_pipe, X_train, y_train, seed, 
        './results/models/wine_random_search.pickle'
    )
    
    random_search_df = pd.DataFrame(random_search.cv_results_)[
        [
            "mean_train_score",
            "mean_test_score",
            "param_logisticregression__C",
            "mean_fit_time",
            "rank_test_score"
        ]
    ].set_index("rank_test_score").sort_index().T
    random_search_df.to_csv(os.path.join(table_to, "random_search.csv"))

    cv_df = pd.DataFrame(
        cross_validate(best_estimator, X_train, y_train, cv = 5, scoring = scoring)
    ).agg(['mean']).round(3).T.reset_index()

    cv_df = cv_df[~cv_df['index'].isin(["fit_time", "score_time"])]
    cv_df = cv_df.set_index('index').T
    cv_df.to_csv(os.path.join(table_to, "cross_validation.csv"), index=False)

    # Results
    # call test_evalutaion function to evaluate test scores, plot confusion matrix and PR-curve
    evaluation(random_search, X_test, y_test, "red", plot_to, table_to)

    # Prediction drift check
    wine_train_ds = Dataset(wine_train, label="color", cat_features=[])
    wine_test_ds = Dataset(wine_test, label="color", cat_features=[])
    target_drift_check = PredictionDrift()

    expected_distribution = {"red": 0.25, "white": 0.75} 
    actual_distribution = wine_train['color'].value_counts(normalize=True).to_dict()

    for cat, prob in expected_distribution.items():
        if abs(actual_distribution.get(cat) - prob) > 0.1:
            print(f"Class '{cat}' deviates significantly from the expected distribution {prob}.")

    target_dist_result = target_drift_check.run(
        wine_train_ds, 
        wine_test_ds, 
        model = random_search.best_estimator_
    )
    drift_df =  pd.DataFrame([target_dist_result.reduce_output()])
    drift_df.to_csv(os.path.join(table_to, "drift_score.csv"))

if __name__ == '__main__':
    main()