"""Registre des modèles du TP 14, avec la préparation unique."""
from lightgbm import LGBMClassifier
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from nutriscope.ml.preparation import preparation

def boosting_models() -> dict:
    return {
        'hist_gradient_boosting': HistGradientBoostingClassifier(random_state=42),
        'xgboost': XGBClassifier(
            n_estimators=300,
            learning_rate=0.1,
            max_depth=6,
            random_state=42,
            n_jobs=1,
        ),
        'lightgbm': LGBMClassifier(
            n_estimators=300,
            learning_rate=0.1,
            random_state=42,
            n_jobs=1,
            verbose=-1,
        ),
    }

def build_pipeline(
    classifier,
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> Pipeline:
    return Pipeline(steps=[
        ('preprocessor', preparation(numeric_columns, categorical_columns)),
        ('classifier', classifier),
    ])

def tp14_models() -> dict:
    return {
        'dummy_most_frequent': DummyClassifier(strategy='most_frequent'),
        'dummy_stratified': DummyClassifier(strategy='stratified', random_state=42),
        'tree_depth_3': DecisionTreeClassifier(max_depth=3, random_state=42),
        'tree_depth_8': DecisionTreeClassifier(max_depth=8, random_state=42),
        'logreg': LogisticRegression(max_iter=1000, random_state=42),
        'random_forest': RandomForestClassifier(n_estimators=200, random_state=42),
        'random_forest_balanced': RandomForestClassifier(
            n_estimators=200,
            class_weight='balanced',
            random_state=42,
        ),
    }
