"""Préparation unique des variables du modèle Nutri-Score (TP 14 et suivants).

Données : © Open Food Facts contributors — ODbL
"""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

DERIVED_NAMES = [
    'sugars_ratio',
    'sat_fat_ratio',
    'energy_gap',
]

def add_derived_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Ajoute deux ratios et l'écart entre énergie déclarée et énergie recalculée."""
    dataframe = dataframe.astype('float64')  # Int64 nullable -> float, pd.NA -> NaN
    output = dataframe.copy()

    # where(>0) : un dénominateur nul ou absent donne NaN, jamais inf
    output['sugars_ratio'] = dataframe['sugars_100g'] / dataframe['carbohydrates_100g'].where(dataframe['carbohydrates_100g'] > 0)
    output['sat_fat_ratio'] = dataframe['saturated-fat_100g'] / dataframe['fat_100g'].where(dataframe['fat_100g'] > 0)

    # Facteurs d'Atwater : 4 kcal/g (protéines, glucides), 9 (lipides), ~2 (fibres)
    energy_computed = (
        4 * dataframe['proteins_100g'] + 4 * dataframe['carbohydrates_100g']
        + 9 * dataframe['fat_100g'] + 2 * dataframe['fiber_100g']
    )
    output['energy_gap'] = dataframe['energy-kcal_100g'] - energy_computed
    return output


def derived_feature_names(
    transformer,
    input_features,
):
    return [
        *input_features,
        *DERIVED_NAMES,
    ]


def preparation(
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> ColumnTransformer:
    """Le seul préparateur du projet : à appeler partout, jamais à recopier."""
    numeric = Pipeline(steps=[
        ('derive', FunctionTransformer(add_derived_features, feature_names_out=derived_feature_names)),
        ('imputer', SimpleImputer(strategy='median', add_indicator=True)),
        ('scaler', StandardScaler()),
    ])

    categorical = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', min_frequency=0.01, sparse_output=False)),
    ])

    return ColumnTransformer(transformers=[
        ('num', numeric, numeric_columns),
        ('cat', categorical, categorical_columns),
    ])
