# test_evaluation.py
# author: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-12

import os
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay, PrecisionRecallDisplay, 
    recall_score, precision_score, f1_score, accuracy_score
)

def test_evaluation(model, X_test, y_test, pos_label, plot_to, table_to):
    """
    This function performs evaluation on the test dataset including evaluating test score on 
    recall, precision, f-1, and accuracy metrics,
    plotting the confusion matrix and precision-recall curve,
    then save the results to the designated directories.

    Parameter:
        model (scikit-learn object): The model that the train data is fit on and to be evaluated.
        X_test (pd.DataFrame): The dataframe that contains the features of the test data.
        y_test (pd.Series): The series that contains the targets of the test data.
        pos_label (str): The positive label of the classification problem.
        plot_to (str): The relative path to save the plots to.
        table_to (str): The relative path to save the tables to.

    Returns:
        None
    
    Examples:
        test_evalutation(random_search, X_test, y_test, 'red', 'results/tables', 'results/plots')
    """
    # Compute accuracy on test data
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, pos_label=pos_label)
    recall = recall_score(y_test, predictions, pos_label=pos_label)
    f1 = f1_score(y_test, predictions, pos_label=pos_label)

    test_scores = pd.DataFrame({
        'accuracy': [accuracy],
        'precision': [precision],
        'recall': [recall],
        'F1 score': [f1]
    })

    if not os.path.exists(table_to):
        os.mkdir(table_to)
    test_scores.to_csv(os.path.join(table_to, "test_scores.csv"), index=False)

    # Confusion matrix 
    confusion_matrix = ConfusionMatrixDisplay.from_estimator(
        model,
        X_test,
        y_test,
        values_format="d"
    )

    if not os.path.exists(plot_to):
        os.mkdir(plot_to)
    confusion_matrix.figure_.savefig(os.path.join(plot_to, "confusion_matrix.png"))

    # Precision-recall Curve
    pr_curve = PrecisionRecallDisplay.from_estimator(
        model,
        X_test,
        y_test,
        pos_label=pos_label,
        name='wine_quality'
        )
    pr_curve.figure_.savefig(os.path.join(plot_to, "pr_curve.png"))
