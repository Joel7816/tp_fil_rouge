"""Tests unitaires des règles de nettoyage (``nutriscope_data.cleaning``).

Lancer depuis la racine du projet, .venv activé :
    pytest -v
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nutriscope_data.cleaning import (
    add_missing_flag,
    bound_energy,
    bound_nutrients,
    clean,
    deduplicate_barcodes,
    drop_seen_barcodes,
    impute_energy,
    impute_median_by_category,
    impute_salt_sodium,
    merge_reports,
    normalize_empty_categories,
    normalize_grade,
)

@pytest.fixture
def raw_df() -> pd.DataFrame:
    """Petit jeu brut qui déclenche chaque règle exactement une fois (ou presque)."""
    return pd.DataFrame(
        {
            "code": ["001", "001", "002", "003"],
            "product_name": ["a", "a bis", "b", "c"],
            "pnns_groups_1": ["Fruits", "Fruits", "unknown", "Beverages"],
            "pnns_groups_2": ["Fruits", "Fruits", "", "Soda"],
            "nutriscore_grade": ["a", "a", "unknown", "c"],
            "brands": ["X", "X", None, "Y"],
            "energy-kcal_100g": [100.0, 100.0, np.nan, 2000.0],
            "energy_100g": [418.4, 418.4, 800.0, 8000.0],
            "fat_100g": [1.0, 1.0, 150.0, 5.0],
            "carbohydrates_100g": [10.0, 10.0, 20.0, 5.0],
            "sugars_100g": [5.0, 5.0, 2.0, 1.0],
            "fiber_100g": [1.0, 1.0, np.nan, np.nan],
            "proteins_100g": [2.0, 2.0, 3.0, 1.0],
            "salt_100g": [0.5, 0.5, np.nan, 0.2],
            "sodium_100g": [np.nan, np.nan, 0.1, 0.08],
        }
    )


# --- bound_nutrients ----------------------------------------------------------

def test_bound_nutrients_sets_out_of_range_values_to_na() -> None:
    """Les valeurs hors de [0, 100] deviennent NA, les bornes elles-mêmes sont valides."""
    df = pd.DataFrame({"fat_100g": [150.0, -5.0, 20.0], "sugars_100g": [10.0, 0.0, 100.0]})

    result, count = bound_nutrients(df)

    assert count == 2
    assert result["fat_100g"].isna().tolist() == [True, True, False]
    assert result["sugars_100g"].tolist() == [10.0, 0.0, 100.0]


def test_bound_nutrients_does_not_modify_input() -> None:
    df = pd.DataFrame({"fat_100g": [150.0, 20.0]})
    original = df.copy()

    bound_nutrients(df)

    pd.testing.assert_frame_equal(df, original)


def test_bound_nutrients_ignores_missing_columns_and_existing_na() -> None:
    """Une colonne absente est ignorée, un NA existant n'est pas compté."""
    df = pd.DataFrame({"fat_100g": [np.nan, 5.0]})

    result, count = bound_nutrients(df)

    assert count == 0
    assert result["fat_100g"].isna().tolist() == [True, False]


# --- bound_energy -------------------------------------------------------------

def test_bound_energy_sets_implausible_values_to_na() -> None:
    df = pd.DataFrame(
        {
            "energy-kcal_100g": [950.0, 250.0, np.nan],
            "energy_100g": [1000.0, 4000.0, 500.0],
        }
    )

    result, count = bound_energy(df)

    assert count == 2  # 950 kcal et 4000 kJ
    assert result["energy-kcal_100g"].isna().tolist() == [True, False, True]
    assert result["energy_100g"].isna().tolist() == [False, True, False]


# --- deduplicate_barcodes -----------------------------------------------------

def test_deduplicate_barcodes_keeps_most_complete_row() -> None:
    df = pd.DataFrame(
        {
            "code": ["0001", "0001", " 0002 ", "0002", None, None],
            "product_name": [None, "Pâtes", "A", "A", "x", "y"],
            "brands": [None, "B", None, "C", None, None],
        }
    )

    result, count = deduplicate_barcodes(df)

    kept = result.dropna(subset=["code"]).set_index("code")
    assert count == 2
    assert len(result) == 4
    assert kept.loc["0001", "product_name"] == "Pâtes"  # la plus complète, zéros conservés
    assert kept.loc["0002", "brands"] == "C"  # après strip des espaces
    assert result["code"].isna().sum() == 2  # les lignes sans code ne sont jamais fusionnées


def test_deduplicate_barcodes_does_not_modify_input() -> None:
    df = pd.DataFrame({"code": ["1", "1"], "brands": [None, "B"]})
    original = df.copy()

    deduplicate_barcodes(df)

    pd.testing.assert_frame_equal(df, original)


# --- drop_seen_barcodes -------------------------------------------------------

def test_drop_seen_barcodes_removes_known_codes_and_updates_set() -> None:
    seen = {"111"}
    df = pd.DataFrame({"code": pd.array(["111", "222", None], dtype="string")})

    result, count = drop_seen_barcodes(df, seen)

    assert count == 1
    assert len(result) == 2  # "222" et la ligne sans code
    assert set(result["code"].dropna()) == {"222"}
    assert seen == {"111", "222"}  # le set a été enrichi


# --- normalize_empty_categories / normalize_grade -----------------------------

def test_normalize_empty_categories_converts_all_empty_forms() -> None:
    df = pd.DataFrame(
        {
            "pnns_groups_1": ["Beverages", "", "  ", "unknown", "Unknown", None],
            "pnns_groups_2": ["Soda", "nan", "None", "Cheese", " Fruits ", None],
        }
    )

    result, count = normalize_empty_categories(df)

    assert count == 6  # 4 dans la colonne 1, 2 dans la colonne 2 (les NA existants ne comptent pas)
    assert result["pnns_groups_1"].isna().sum() == 5
    assert result["pnns_groups_2"].isna().sum() == 3
    assert result["pnns_groups_2"].iloc[4] == "Fruits"  # espaces retirés sur les valeurs valides


def test_normalize_grade_converts_unknown_to_na() -> None:
    df = pd.DataFrame({"nutriscore_grade": ["a", "unknown", "UNKNOWN", None, "e"]})

    result, count = normalize_grade(df)

    assert count == 2
    assert result["nutriscore_grade"].isna().sum() == 3
    assert result["nutriscore_grade"].iloc[0] == "a"


# --- impute_energy ------------------------------------------------------------

def test_impute_energy_prefers_kj_then_macros_and_never_overwrites() -> None:
    df = pd.DataFrame(
        {
            "energy-kcal_100g": [np.nan, np.nan, np.nan, 100.0, np.nan],
            "energy_100g": [418.4, np.nan, np.nan, 999.0, np.nan],
            "carbohydrates_100g": [0.0, 10.0, 100.0, 0.0, np.nan],
            "proteins_100g": [0.0, 5.0, 100.0, 0.0, np.nan],
            "fat_100g": [0.0, 2.0, 100.0, 0.0, np.nan],
        }
    )

    result, report = impute_energy(df)

    kcal = result["energy-kcal_100g"]
    assert kcal.iloc[0] == pytest.approx(100.0)  # 418,4 kJ / 4,184
    assert kcal.iloc[1] == pytest.approx(78.0)  # 4*10 + 4*5 + 9*2
    assert np.isnan(kcal.iloc[2])  # 1700 kcal : implausible, on n'impute pas
    assert kcal.iloc[3] == pytest.approx(100.0)  # valeur existante intacte
    assert np.isnan(kcal.iloc[4])
    assert report == {"from_kj": 1, "from_macros": 1, "remaining": 2}


# --- impute_salt_sodium -------------------------------------------------------

def test_impute_salt_sodium_both_directions() -> None:
    df = pd.DataFrame(
        {
            "salt_100g": [np.nan, 2.5, np.nan, 1.0],
            "sodium_100g": [0.4, np.nan, np.nan, 0.4],
        }
    )

    result, report = impute_salt_sodium(df)

    assert result["salt_100g"].iloc[0] == pytest.approx(1.0)  # 0,4 x 2,5
    assert result["sodium_100g"].iloc[1] == pytest.approx(1.0)  # 2,5 / 2,5
    assert result["salt_100g"].iloc[3] == pytest.approx(1.0)  # valeurs présentes intactes
    assert report == {"salt_from_sodium": 1, "sodium_from_salt": 1, "remaining": 1}


# --- add_missing_flag ---------------------------------------------------------

def test_add_missing_flag_keeps_value_na_and_adds_flag() -> None:
    df = pd.DataFrame({"fiber_100g": [1.0, np.nan]})

    result, count = add_missing_flag(df, "fiber_100g")

    assert count == 1
    assert result["fiber_100g_missing"].tolist() == [False, True]
    assert str(result["fiber_100g_missing"].dtype) == "boolean"
    assert result["fiber_100g"].isna().tolist() == [False, True]  # jamais imputé


# --- impute_median_by_category -----------------------------------------------

def test_impute_median_by_category_uses_train_statistics_only() -> None:
    train = pd.DataFrame({"pnns_groups_1": ["A", "A", "B", "B"], "x": [1.0, 3.0, 10.0, np.nan]})
    test = pd.DataFrame({"pnns_groups_1": ["A", "B", "C"], "x": [np.nan, np.nan, np.nan]})

    train_filled, test_filled = impute_median_by_category(train, test, "x")

    assert train_filled.tolist() == [1.0, 3.0, 10.0, 10.0]  # médiane de B
    assert test_filled.tolist() == [2.0, 10.0, 3.0]  # médiane A, médiane B, repli global (C inconnu)


def test_impute_median_by_category_ignores_test_values() -> None:
    """Pas de fuite : changer le contenu du test ne change pas ce qui est appris sur le train."""
    train = pd.DataFrame({"pnns_groups_1": ["A", "A"], "x": [1.0, 3.0]})
    test_a = pd.DataFrame({"pnns_groups_1": ["A"], "x": [np.nan]})
    test_b = pd.DataFrame({"pnns_groups_1": ["A", "A"], "x": [np.nan, 1_000_000.0]})

    _, filled_a = impute_median_by_category(train, test_a, "x")
    _, filled_b = impute_median_by_category(train, test_b, "x")

    assert filled_a.iloc[0] == filled_b.iloc[0] == 2.0


# --- merge_reports ------------------------------------------------------------

def test_merge_reports_adds_nested_values_without_modifying_inputs() -> None:
    first = {"rows_before": 10, "energy_imputed": {"from_kj": 1, "remaining": 2}}
    second = {
        "rows_before": 5,
        "energy_imputed": {"from_kj": 3, "remaining": 1},
        "duplicates_removed": 2,
    }

    merged = merge_reports(first, second)

    assert merged == {
        "rows_before": 15,
        "energy_imputed": {"from_kj": 4, "remaining": 3},
        "duplicates_removed": 2,
    }
    assert first == {"rows_before": 10, "energy_imputed": {"from_kj": 1, "remaining": 2}}


# --- clean (pipeline complet) -------------------------------------------------

def test_clean_applies_every_rule_and_reports_counts(raw_df: pd.DataFrame) -> None:
    original = raw_df.copy()

    result, report = clean(raw_df)

    assert report["rows_before"] == 4
    assert report["rows_after"] == 3 == len(result)
    assert report["nutrients_out_of_bounds"] == 1  # fat = 150
    assert report["energies_out_of_bounds"] == 2  # 2000 kcal et 8000 kJ
    assert report["duplicates_removed"] == 1
    assert report["empty_categories"] == 2
    assert report["unknown_grades"] == 1
    assert report["energy_imputed"] == {"from_kj": 1, "from_macros": 1, "remaining": 0}
    assert report["salt_sodium_imputed"]["remaining"] == 0
    assert not result["code"].duplicated().any()
    assert {"fiber_100g_missing", "brands_missing"} <= set(result.columns)
    pd.testing.assert_frame_equal(raw_df, original)  # l'entrée n'a pas bougé


def test_clean_removes_codes_already_seen_in_previous_batches(raw_df: pd.DataFrame) -> None:
    seen: set[str] = set()

    first_result, _ = clean(raw_df, seen)
    second_result, second_report = clean(raw_df, seen)

    assert len(first_result) == 3
    assert second_result.empty
    assert second_report["duplicates_removed"] == 4  # 1 dans le lot + 3 déjà vus