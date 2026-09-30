"""Fonctions de profiling du jeu de données Open Food Facts."""

from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from nutriscope_data.loading import FRANCE_PARQUET

# Colonnes nutritionnelles en g/100 g dont la valeur ne peut pas dépasser 100
GRAMS_PER_100G_COLUMNS: tuple[str, ...] = (
    "fat_100g",
    "saturated-fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
)


# --- Profiling sur un DataFrame déjà chargé (colonnes ciblées ou échantillon) ---


def find_duplicate_codes(df: pd.DataFrame, code_col: str = "code") -> pd.DataFrame:
    """Retourne toutes les lignes dont le code-barres apparaît plusieurs fois."""
    mask = df[code_col].duplicated(keep=False) & df[code_col].notna()
    return df.loc[mask].sort_values(code_col)


def duplicate_stats(df: pd.DataFrame, code_col: str = "code") -> dict[str, int]:
    """Résume les doublons : codes manquants, codes uniques, codes dupliqués, lignes en trop."""
    codes = df[code_col]
    return {
        "missing_codes": int(codes.isna().sum()),
        "unique_codes": int(codes.nunique()),
        "duplicated_codes": int((codes.value_counts() > 1).sum()),
        "extra_rows": int(codes.duplicated().sum()),
    }


def _blank_mask(series: pd.Series) -> pd.Series:
    """Masque des chaînes vides ou composées uniquement d'espaces."""
    if series.dtype == object or pd.api.types.is_string_dtype(series):
        return series.map(lambda value: isinstance(value, str) and not value.strip())
    return pd.Series(False, index=series.index)


def completeness(df: pd.DataFrame) -> pd.DataFrame:
    """Taux de complétude par colonne (en %) d'un DataFrame, du plus rempli au moins rempli.

    Les valeurs nulles et les chaînes vides comptent comme manquantes.
    """
    rates = {
        col: round((~(df[col].isna() | _blank_mask(df[col]))).mean() * 100, 1)
        for col in df.columns
    }
    return (
        pd.Series(rates, name="completeness_pct")
        .sort_values(ascending=False)
        .to_frame()
    )


def impossible_values(
    df: pd.DataFrame,
    columns: tuple[str, ...] = GRAMS_PER_100G_COLUMNS,
) -> pd.DataFrame:
    """Compte, pour chaque colonne, les valeurs négatives ou supérieures à 100."""
    rows = []
    for col in columns:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce")
        rows.append(
            {
                "column": col,
                "negative": int((series < 0).sum()),
                "over_100": int((series > 100).sum()),
            }
        )
    return pd.DataFrame(rows).set_index("column")


def cardinalities(df: pd.DataFrame) -> pd.DataFrame:
    """Nombre de valeurs distinctes par colonne (colonnes non hashables : None)."""
    result = {}
    for col in df.columns:
        try:
            result[col] = df[col].nunique()
        except TypeError:
            result[col] = None
    return pd.Series(result, name="n_unique").sort_values().to_frame()


# --- Profiling exact sur le fichier, colonne par colonne (économe en mémoire) ---


def _empty_count(col: pa.ChunkedArray) -> int:
    """Compte les valeurs vides non nulles : chaînes vides/blanches et listes vides."""
    if pa.types.is_string(col.type) or pa.types.is_large_string(col.type):
        trimmed = pc.utf8_trim_whitespace(col)
        return pc.sum(pc.equal(trimmed, "")).as_py() or 0
    if pa.types.is_list(col.type) or pa.types.is_large_list(col.type):
        return pc.sum(pc.equal(pc.list_value_length(col), 0)).as_py() or 0
    return 0


def column_completeness(path: Path = FRANCE_PARQUET) -> pd.DataFrame:
    """Complétude exacte de toutes les colonnes du fichier, lues une par une.

    Peut prendre plusieurs dizaines de secondes : sauvegarde le résultat.
    """
    rows = []
    for name in pq.read_schema(path).names:
        col = pq.read_table(path, columns=[name]).column(0)
        missing = col.null_count + _empty_count(col)
        rows.append(
            {
                "column": name,
                "dtype": str(col.type),
                "missing_pct": round(missing / len(col) * 100, 1),
            }
        )
    return pd.DataFrame(rows).set_index("column").sort_values("missing_pct")