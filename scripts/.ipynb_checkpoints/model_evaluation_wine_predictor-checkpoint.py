# model_evaluation_wine_predictor.py
# author: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-05

import click
import os
import numpy as np
import pandas as pd
import pickle
from sklearn import set_config
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (
    ConfusionMatrixDisplay, PrecisionRecallDisplay, 
    make_scorer, recall_score, precision_score, f1_score, 
    accuracy_score
)

from sklearn.model_selection import (
    cross_validate,
    RandomizedSearchCV,
)
from scipy.stats import loguniform
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import PredictionDrift

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
    param_grid = {
        "logisticregression__C": loguniform(1e-1, 10)
    }

    random_search = RandomizedSearchCV(
        wine_pipe,
        param_grid,
        n_iter = 10,
        verbose = 1,
        n_jobs = -1,
        random_state = seed,
        return_train_score = True, 
        scoring = make_scorer(f1_score, pos_label = "red")
    )
    random_search.fit(X_train, y_train)
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

    pickle.dump(random_search, open("./results/models/wine_random_search.pickle", "wb"))

    best_estimator = random_search.best_estimator_

    cv_df = pd.DataFrame(
        cross_validate(best_estimator, X_train, y_train, cv = 5, scoring = scoring)
    ).agg(['mean']).round(3).T.reset_index()

    cv_df = cv_df[~cv_df['index'].isin(["fit_time", "score_time"])]
    cv_df = cv_df.set_index('index').T

    if not os.path.exists(table_to):
        os.mkdir(table_to)
    cv_df.to_csv(os.path.join(table_to, "cross_validation.csv"), index=False)

    # Results
    # Compute accuracy on test data
    predictions = best_estimator.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, pos_label="red")
    recall = recall_score(y_test, predictions, pos_label="red")
    f1 = f1_score(y_test, predictions, pos_label="red")

    test_scores = pd.DataFrame({
        'accuracy': [accuracy],
        'precision': [precision],
        'recall': [recall],
        'F1 score': [f1]
    })

    test_scores.to_csv(os.path.join(table_to, "test_scores.csv"), index=False)

    # Confusion matrix 
    confusion_matrix = ConfusionMatrixDisplay.from_estimator(
        random_search,
        X_test,
        y_test,
        values_format="d"
    )

    if not os.path.exists(plot_to):
        os.mkdir(plot_to)
    confusion_matrix.figure_.savefig(os.path.join(plot_to, "confusion_matrix.png"))

    # Precision-recall Curve
    pr_curve = PrecisionRecallDisplay.from_estimator(
        random_search,
        X_test,
        y_test,
        pos_label="red",
        name='wine_quality', 
    )
    pr_curve.figure_.savefig(os.path.join(plot_to, "pr_curve.png"))

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