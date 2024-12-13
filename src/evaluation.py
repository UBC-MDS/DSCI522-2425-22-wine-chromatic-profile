# evaluation.py
# author: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-12

import os
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay, PrecisionRecallDisplay, 
    recall_score, precision_score, f1_score, accuracy_score
)

def evaluation(model, X_test, y_test, pos_label, table_to, plot_to):
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
        table_to (str): The relative path to save the tables to.
        plot_to (str): The relative path to save the plots to.

    Returns:
        None: This function is not returning anything as it only does side-effects
    
    Examples:
        evalutation(random_search, X_test, y_test, 'red', 'results/tables', 'results/plots')
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
    test_scores.to_csv(os.path.join(table_to, "test_scores.csv"), index=False)

    # Confusion matrix 
    confusion_matrix = ConfusionMatrixDisplay.from_estimator(
        model,
        X_test,
        y_test,
        values_format="d"
    )
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
