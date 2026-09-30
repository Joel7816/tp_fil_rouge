"""Chargement du jeu de données Open Food Facts (France)."""

import random
from collections.abc import Sequence
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from nutriscope_data.config import DATA_DIR

FRANCE_PARQUET = DATA_DIR / "france" / "food_france.parquet"


def _ensure_file_exists(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {path}")


def list_available_columns(path: Path = FRANCE_PARQUET) -> list[str]:
    """Liste les colonnes du parquet en lisant uniquement son schéma."""
    _ensure_file_exists(path)
    return pq.read_schema(path).names


def _check_columns(columns: Sequence[str], path: Path) -> list[str]:
    """Vérifie que les colonnes demandées existent et retourne une liste."""
    missing = set(columns) - set(list_available_columns(path))
    if missing:
        raise ValueError(f"Colonnes absentes du fichier : {sorted(missing)}")
    return list(columns)


def load_products(
    columns: Sequence[str],
    path: Path = FRANCE_PARQUET,
) -> pd.DataFrame:
    """Charge le parquet complet (toutes les lignes) pour les colonnes demandées.

    Les colonnes sont obligatoires : le fichier fait ~2,2 Go et 145 colonnes,
    charger tout en mémoire serait risqué.

    Raises:
        FileNotFoundError: si le fichier n'existe pas.
        ValueError: si des colonnes demandées n'existent pas dans le fichier.
    """
    _ensure_file_exists(path)
    return pd.read_parquet(path, columns=_check_columns(columns, path))


def load_sample(
    columns: Sequence[str],
    n_row_groups: int = 3,
    seed: int = 42,
    path: Path = FRANCE_PARQUET,
) -> pd.DataFrame:
    """Charge un échantillon reproductible : quelques row groups tirés au hasard.

    Utile pour explorer et mettre au point des fonctions. À ne pas utiliser pour
    les chiffres finaux (doublons, cardinalités), qui exigent tout le fichier.
    """
    _ensure_file_exists(path)
    checked = _check_columns(columns, path)

    parquet_file = pq.ParquetFile(path)
    count = min(n_row_groups, parquet_file.num_row_groups)
    chosen = sorted(
        random.Random(seed).sample(range(parquet_file.num_row_groups), count)
    )
    return parquet_file.read_row_groups(chosen, columns=checked).to_pandas()


def summarize(df: pd.DataFrame) -> dict[str, object]:
    """Retourne un résumé : lignes, colonnes, mémoire (Mo) et colonnes par dtype."""
    return {
        "rows": len(df),
        "columns": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 1),
        "dtypes": df.dtypes.astype(str).value_counts().to_dict(),
    }