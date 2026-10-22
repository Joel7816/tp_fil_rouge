"""Réglage raisonné d'XGBoost avec Optuna : budget explicite, élagage, 3 plis."""

import time

import optuna
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier

from nutriscope.ml.models import build_pipeline

RANDOM_STATE = 42
TUNING_SPLITS = 3
DEFAULT_PARAMS = {
    'n_estimators': 300,
    'learning_rate': 0.1,
    'max_depth': 6,
    'min_child_weight': 1,
    'subsample': 1.0,
    'colsample_bytree': 1.0,
}

def make_tuning_folds(
    X,
    y,
) -> list:
    splitter = StratifiedKFold(
        n_splits=TUNING_SPLITS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    return list(splitter.split(X, y))

def suggest_params(trial) -> dict:
    return {
        'n_estimators': trial.suggest_int('n_estimators', 200, 800, step=100),
        'learning_rate': trial.suggest_float('learning_rate', 0.03, 0.3, log=True),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
    }

def cross_validated_f1(
    params: dict,
    X,
    y,
    numeric_columns: list[str],
    categorical_columns: list[str],
    folds: list,
    trial=None,
) -> float:
    scores = []

    for step, (fit_index, val_index) in enumerate(folds):
        pipeline = build_pipeline(
            XGBClassifier(**params, random_state=RANDOM_STATE, n_jobs=-1),
            numeric_columns,
            categorical_columns,
        )

        pipeline.fit(X.iloc[fit_index], y.iloc[fit_index])

        prediction = pipeline.predict(X.iloc[val_index])

        scores.append(f1_score(y.iloc[val_index], prediction, average='macro'))

        if trial is not None:
            trial.report(sum(scores) / len(scores), step)
            if trial.should_prune():
                raise optuna.TrialPruned()
            
    return sum(scores) / len(scores)


def time_one_trial(
    X,
    y,
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> float:
    """Durée en secondes d'un essai avec les paramètres par défaut (pour annoncer le budget)."""
    folds = make_tuning_folds(X, y)
    start = time.perf_counter()
    cross_validated_f1(DEFAULT_PARAMS, X, y, numeric_columns, categorical_columns, folds)

    return time.perf_counter() - start


def tune(
    X,
    y,
    numeric_columns: list[str],
    categorical_columns: list[str],
    n_trials: int,
) -> optuna.Study:
    """Recherche Optuna avec élagage. `n_trials` est obligatoire : le budget s'annonce avant."""
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    folds = make_tuning_folds(X, y)

    def objective(trial):
        return cross_validated_f1(
            suggest_params(trial),
            X,
            y,
            numeric_columns,
            categorical_columns,
            folds,
            trial,
        )

    study = optuna.create_study(
        direction='maximize',
        sampler=optuna.samplers.TPESampler(seed=RANDOM_STATE),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=5),
    )
    study.optimize(objective, n_trials=n_trials)
    
    return study