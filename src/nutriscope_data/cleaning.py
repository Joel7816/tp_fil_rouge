"""Règles de nettoyage du jeu de données Open Food Facts.

Chaque règle est une fonction pure : elle ne modifie jamais le DataFrame reçu
et renvoie ``(DataFrame nettoyé, nombre d'éléments touchés)``.
Aucun code ne s'exécute à l'import : le chargement des données et les
``print`` vivent dans un script séparé.

Ordre logique du pipeline (voir ``clean``) :
unités -> bornage -> dédoublonnage -> catégories -> imputation -> drapeaux.
"""

from __future__ import annotations

from typing import Any, Final

import pandas as pd

# --- Constantes (à déplacer dans config.py une fois le TP validé) -----------

KJ_PER_KCAL: Final[float] = 4.184
SALT_PER_SODIUM: Final[float] = 2.5
ENERGY_KCAL_MAX: Final[float] = 900.0
ENERGY_KJ_MAX: Final[float] = 3_800.0
NUTRIENT_MIN: Final[float] = 0.0
NUTRIENT_MAX: Final[float] = 100.0

NUTRIENT_COLUMNS_G: Final[tuple[str, ...]] = (
    "fat_100g",
    "saturated-fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
    "sodium_100g",
)
CATEGORY_COLUMNS: Final[tuple[str, ...]] = ("pnns_groups_1", "pnns_groups_2")
EMPTY_VALUES: Final[frozenset[str]] = frozenset({"", "unknown", "nan", "none"})


# --- 1. Normalisation des unités ---------------------------------------------

# TODO: règle en attente. À écrire à partir des cas tordus relevés au TP 2,
# pas d'une hypothèse (l'échange kcal/kJ n'est pas justifié par les données).
#
# def normalize_units(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, int]:
#     """Remet kcal et kJ dans la bonne colonne quand ils sont inversés."""
#     result = dataframe.copy()
#     kcal = result["energy-kcal_100g"]
#     kj = result["energy_100g"]
#     swapped = kcal.notna() & kj.notna() & (kcal > kj)
#
#     result.loc[swapped, ["energy-kcal_100g", "energy_100g"]] = result.loc[
#         swapped, ["energy_100g", "energy-kcal_100g"]
#     ].to_numpy()
#     return result, int(swapped.sum())


# --- 2. Bornage ---------------------------------------------------------------

def bound_nutrients(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Met à NA les nutriments hors de [0, 100] g/100 g.

    On ne ``clip`` pas : ramener 5000 à 100 serait inventer une donnée.
    Retourne le DataFrame corrigé et le nombre de **valeurs** mises à NA.
    """
    result = dataframe.copy()
    columns = [c for c in NUTRIENT_COLUMNS_G if c in result.columns]
    values = result[columns]
    out_of_bounds = values.lt(NUTRIENT_MIN) | values.gt(NUTRIENT_MAX)

    result[columns] = values.mask(out_of_bounds)
    return result, int(out_of_bounds.sum().sum())


def bound_energy(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Met à NA les énergies implausibles (kcal hors [0, 900], kJ hors [0, 3800])."""
    result = dataframe.copy()
    kcal, kj = result["energy-kcal_100g"], result["energy_100g"]
    kcal_invalid = kcal.notna() & ~kcal.between(0, ENERGY_KCAL_MAX)
    kj_invalid = kj.notna() & ~kj.between(0, ENERGY_KJ_MAX)

    result["energy-kcal_100g"] = kcal.mask(kcal_invalid)
    result["energy_100g"] = kj.mask(kj_invalid)
    return result, int(kcal_invalid.sum() + kj_invalid.sum())


# --- 3. Déduplication des codes-barres ---------------------------------------

def deduplicate_barcodes(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Garde une seule ligne par code-barres : la plus complète.

    Le code est converti en ``string`` (pas ``int``) pour ne pas perdre les
    zéros initiaux. Les lignes sans code ne sont jamais considérées comme
    doublons entre elles. Retourne le DataFrame et le nombre de lignes retirées.
    """
    result = dataframe.copy()
    result["code"] = result["code"].astype("string").str.strip()

    # On trie par complétude décroissante pour que "keep=first" garde la meilleure ligne
    completeness = result.notna().sum(axis=1)
    order = completeness.sort_values(ascending=False, kind="stable").index
    result = result.loc[order]

    is_duplicate = result["code"].duplicated(keep="first") & result["code"].notna()
    return result[~is_duplicate].sort_index(), int(is_duplicate.sum())


def drop_seen_barcodes(dataframe: pd.DataFrame, seen_codes: set[str]) -> tuple[pd.DataFrame, int]:
    """Retire les lignes dont le code a déjà été vu dans un lot précédent.

    Sert au traitement par lots, où l'on ne peut pas comparer toutes les lignes
    entre elles : on garde la première occurrence rencontrée.

    Attention : cette fonction n'est pas pure, elle **ajoute** les codes du lot
    à ``seen_codes`` (c'est ce qui permet de se souvenir d'un lot à l'autre).
    """
    codes = dataframe["code"]
    already_seen = codes.isin(seen_codes) & codes.notna()
    seen_codes.update(codes.dropna().tolist())
    return dataframe[~already_seen], int(already_seen.sum())


# --- 4. Catégories vides -------------------------------------------------------

def normalize_empty_categories(
    dataframe: pd.DataFrame,
    columns: tuple[str, ...] = CATEGORY_COLUMNS,
) -> tuple[pd.DataFrame, int]:
    """Ramène "", espaces, "unknown", "nan"... à un vrai NA dans les catégories.

    Retourne le DataFrame et le nombre de cellules converties en NA.
    """
    result = dataframe.copy()
    total = 0
    for column in columns:
        if column not in result.columns:
            continue
        text = result[column].astype("string").str.strip()
        is_empty = text.str.lower().isin(EMPTY_VALUES)
        result[column] = text.mask(is_empty, pd.NA)
        total += int(is_empty.sum())
    return result, total


def normalize_grade(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Convertit la sentinelle « unknown » de ``nutriscore_grade`` en NA (jamais imputé)."""
    result = dataframe.copy()
    is_sentinel = result["nutriscore_grade"].astype("string").str.lower().eq("unknown")
    result["nutriscore_grade"] = result["nutriscore_grade"].mask(is_sentinel, pd.NA)
    return result, int(is_sentinel.sum())


# --- Valeurs manquantes (décisions par colonne) --------------------------------

def impute_energy(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Impute l'énergie en kcal : d'abord depuis les kJ, ensuite par 4/4/9, jamais une moyenne."""
    result = dataframe.copy()
    kcal = result["energy-kcal_100g"]

    from_kj = kcal.isna() & result["energy_100g"].notna()
    kcal = kcal.mask(from_kj, (result["energy_100g"] / KJ_PER_KCAL).round(1))

    from_macros_value = (
        4 * result["carbohydrates_100g"]
        + 4 * result["proteins_100g"]
        + 9 * result["fat_100g"]
    )
    from_macros = kcal.isna() & from_macros_value.notna() & (from_macros_value <= ENERGY_KCAL_MAX)
    kcal = kcal.mask(from_macros, from_macros_value.round(1))

    result["energy-kcal_100g"] = kcal
    report = {
        "from_kj": int(from_kj.sum()),
        "from_macros": int(from_macros.sum()),
        "remaining": int(kcal.isna().sum()),
    }
    return result, report


def impute_salt_sodium(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Complète sel et sodium l'un depuis l'autre (sel = 2,5 x sodium)."""
    result = dataframe.copy()
    salt, sodium = result["salt_100g"], result["sodium_100g"]
    salt_from_sodium = salt.isna() & sodium.notna()
    sodium_from_salt = sodium.isna() & salt.notna()

    result["salt_100g"] = salt.mask(salt_from_sodium, sodium * SALT_PER_SODIUM)
    result["sodium_100g"] = sodium.mask(sodium_from_salt, salt / SALT_PER_SODIUM)
    report = {
        "salt_from_sodium": int(salt_from_sodium.sum()),
        "sodium_from_salt": int(sodium_from_salt.sum()),
        "remaining": int(result["salt_100g"].isna().sum()),
    }
    return result, report


def add_missing_flag(dataframe: pd.DataFrame, column: str) -> tuple[pd.DataFrame, int]:
    """Ajoute ``<column>_missing`` (MNAR) : la valeur reste NA, le modèle sait qu'elle manque."""
    result = dataframe.copy()
    flag_name = f"{column}_missing"
    result[flag_name] = result[column].isna().astype("boolean")
    return result, int(result[flag_name].sum())


def impute_median_by_category(
    train: pd.DataFrame, test: pd.DataFrame, column: str
) -> tuple[pd.Series, pd.Series]:
    """Impute par la médiane du rayon, calculée sur le train et appliquée au test."""
    medians = train.groupby("pnns_groups_1")[column].median()
    fallback = train[column].median()

    def fill(data: pd.DataFrame) -> pd.Series:
        return data[column].fillna(data["pnns_groups_1"].map(medians)).fillna(fallback)

    return fill(train), fill(test)


# --- Pipeline et rapport -------------------------------------------------------

def merge_reports(total: dict[str, Any], part: dict[str, Any]) -> dict[str, Any]:
    """Additionne deux rapports, y compris les sous-dictionnaires, sans modifier ``total``.

    Sert à cumuler les rapports de chaque lot en un rapport global.
    """
    merged = dict(total)
    for key, value in part.items():
        if isinstance(value, dict):
            merged[key] = merge_reports(merged.get(key, {}), value)
        else:
            merged[key] = merged.get(key, 0) + value
    return merged


def clean(
    dataframe: pd.DataFrame,
    seen_codes: set[str] | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Applique toutes les règles dans l'ordre et renvoie (DataFrame propre, rapport).

    Le rapport contient, pour chaque règle, le nombre d'éléments touchés,
    ainsi que la volumétrie avant/après.

    Traitement par lots : passer le même ``seen_codes`` (un ``set`` vide au départ)
    à chaque appel. Dans un lot on garde la ligne la plus complète ; entre lots,
    la première rencontrée (voir ``drop_seen_barcodes``, qui modifie ce set).
    """
    report: dict[str, Any] = {"rows_before": len(dataframe)}

    # df, report["units_swapped"] = normalize_units(dataframe)  # en attente (voir TODO)
    df, report["nutrients_out_of_bounds"] = bound_nutrients(dataframe)
    df, report["energies_out_of_bounds"] = bound_energy(df)
    df, report["duplicates_removed"] = deduplicate_barcodes(df)
    if seen_codes is not None:
        df, removed_across_batches = drop_seen_barcodes(df, seen_codes)
        report["duplicates_removed"] += removed_across_batches
    df, report["empty_categories"] = normalize_empty_categories(df)
    df, report["unknown_grades"] = normalize_grade(df)
    df, report["energy_imputed"] = impute_energy(df)
    df, report["salt_sodium_imputed"] = impute_salt_sodium(df)
    df, report["fiber_flagged"] = add_missing_flag(df, "fiber_100g")
    df, report["brands_flagged"] = add_missing_flag(df, "brands")

    report["rows_after"] = len(df)
    return df, report