import pickle
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import make_scorer, f1_score
from scipy.stats import loguniform

def perform_random_search(wine_pipe, X_train, y_train, seed, output_path):
    """
    Performs a randomized search for hyperparameter optimization on a given pipeline,
    saves the trained model to a specified

    Args:
        wine_pipe: The pipeline object to optimize.
        X_train: Training features.
        y_train: Training labels.
        seed: Random seed for reproducibility.
        output_path: Path to save the trained RandomizedSearchCV object (default is './results/models/wine_random_search.pickle').

    Returns:
        The fitted RandomizedSearchCV object.
    """
    # Define parameter grid
    param_grid = {
        "logisticregression__C": loguniform(1e-1, 10)
    }

    # Set up RandomizedSearchCV
    random_search = RandomizedSearchCV(
        wine_pipe,
        param_grid,
        n_iter=10,
        n_jobs=-1,
        random_state=seed,
        return_train_score=True,
        scoring=make_scorer(f1_score, pos_label="red")
    )

    # Fit RandomizedSearchCV
    random_search.fit(X_train, y_train)

    print(random_search.best_score_)

    # Save the model
    with open(output_path, "wb") as file:
        pickle.dump(random_search, file)

    return random_search, random_search.best_estimator_
