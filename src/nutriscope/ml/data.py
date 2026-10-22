"""Chargement du jeu ML et découpage figé (colonne `split`, jamais recalculée).

Données : © Open Food Facts contributors — ODbL
"""

from pathlib import Path

import pandas as pd

from nutriscope.config import ML_SAMPLE

TARGET = 'nutriscore_grade'
LABELS = [
    'a',
    'b',
    'c',
    'd',
    'e',
]
FEATURES = [
    'energy-kcal_100g',
    'fat_100g',
    'saturated-fat_100g',
    'carbohydrates_100g',
    'sugars_100g',
    'proteins_100g',
    'salt_100g',
    'fiber_100g',
    'fruits-vegetables-legumes_100g',
    'nova_group',
    'additives_n',
    'pnns_groups_1',
    'pnns_groups_2',
]


def load_dataset(path: Path = ML_SAMPLE) -> pd.DataFrame:
    return pd.read_parquet(path)


def split_xy(dataframe: pd.DataFrame):
    """Retourne X_train, X_test, y_train, y_test d'après la colonne `split`."""
    assert set(dataframe['split'].unique()) == {'train', 'test'}, 'valeurs de `split` inattendues'
    is_train = dataframe['split'] == 'train'
    X, y = dataframe[FEATURES].copy(), dataframe[TARGET].copy()

    return X[is_train], X[~is_train], y[is_train], y[~is_train]


def column_types(dataframe: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Colonnes numériques et catégorielles (même règle que le notebook TP 14)."""
    numeric = dataframe.select_dtypes(
        include=[
            'int64',
            'float64',
        ],
    ).columns.to_list()
    categorical = dataframe.select_dtypes(
        include=[
            'object',
            'str',
        ],
    ).columns.to_list()

    return numeric, categorical
