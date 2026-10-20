"""
Builds the clean, scoped extract used to load the NutriScope database (TP4).

Input:  data/produits_france.parquet (all France products, TP1 Annexe A output)
Output: data/produits_perimetre_clean.parquet (scoped + cleaned, ready for SQL loading)

This script only applies decisions already validated in the TP2 profiling notebook and
the team's périmètre discussion (see docs/perimetre.md) — it does not make new choices.

Documented, deliberate simplifications:
- Impossible nutrient values are set to NaN (treated as missing), not corrected. A known
  correctable case exists ("Capers": salt/sodium off by a factor of ~1000), but automatic
  magnitude-correction is out of scope here — safer to discard a suspicious reading than
  to silently "fix" it with a guessed rule.
- Barcode duplicates are dropped entirely (all rows sharing a duplicated code), not
  deduplicated by keeping one — there is no reliable way to know which row is correct
  when two products share the same code (see the TP2 "MNMS" vs "medaillon végétal" case).
"""

from pathlib import Path

import pandas as pd

# Paths built from this script's own location, not from the current working directory —
# so the script behaves the same whether it's run as `python build_clean_extract.py` from
# inside src/, or as `python src/build_clean_extract.py` from the project root.
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SOURCE_FILE = DATA_DIR / "produits_france.parquet"
OUTPUT_FILE = DATA_DIR / "produits_perimetre_clean.parquet"

# Plausibility bounds per nutrient (min, max), validated in the TP2 notebook (Section 1)
PLAUSIBILITY_BOUNDS = {
    "energy_kcal_100g": (0, 900),
    "sugars_100g": (0, 100),
    "saturated_fat_100g": (0, 100),
    "salt_100g": (0, 100),
    "sodium_100g": (0, 100),
    "fiber_100g": (0, 100),
    "proteins_100g": (0, 100),
    "fruits_vegetables_nuts_100g": (0, 100),
}

# The 7 official Nutri-Score nutrients used for the completeness threshold.
# salt_100g is used rather than sodium_100g: the two measure the same thing (one is
# derived from the other), counting both would inflate the completeness score.
KEY_NUTRIENTS = [
    "energy_kcal_100g", "sugars_100g", "saturated_fat_100g", "salt_100g",
    "fiber_100g", "proteins_100g", "fruits_vegetables_nuts_100g",
]
MIN_KEY_NUTRIENTS_PRESENT = 4

# The 5 rayons retained by the team (see docs/perimetre.md, Section 1)
SELECTED_RAYON_GROUPS = {
    "dairy": ["en:dairies", "en:fermented-milk-products", "en:cheeses"],
    "meats_and_fish": ["en:meats-and-their-products", "en:meats", "en:prepared-meats",
                        "en:seafood", "en:poultries"],
    "sweet_snacks": ["en:sweet-snacks", "en:biscuits-and-cakes", "en:desserts",
                      "en:confectioneries", "en:sweet-spreads"],
    "prepared_frozen": ["en:meals", "en:frozen-foods"],
    "savory_grocery": ["en:condiments", "en:sauces", "en:cereals-and-potatoes",
                        "en:cereals-and-their-products"],
}

FINAL_COLUMNS = [
    "code", "product_name_main", "brands", "nutriscore_score", "nutriscore_grade",
    "categories_tags",
] + list(PLAUSIBILITY_BOUNDS.keys())


def extract_nutrients(nutrients_list, names_to_find):
    """
    Extracts specific nutrients from the nested "nutriments" list of a single
    product (a list of dicts, each with a "name" and a "100g" value).
    """
    result = {column_name: None for column_name in names_to_find.values()}
    if nutrients_list is None:
        return result
    for item in nutrients_list:
        name = item.get("name")
        if name in names_to_find:
            result[names_to_find[name]] = item.get("100g")
    return result


def extract_main_name(names_list):
    """Extracts a single readable product name from the nested "product_name" list."""
    if names_list is None or len(names_list) == 0:
        return None
    for item in names_list:
        if item.get("lang") == "main":
            return item.get("text")
    return names_list[0].get("text")


def nullify_impossible_values(dataframe, bounds):
    """
    Sets values outside [min, max] to NaN, column by column, instead of dropping the
    whole row. Prints how many values were neutralized per column.
    """
    for column, (min_value, max_value) in bounds.items():
        out_of_bounds = ~dataframe[column].between(min_value, max_value) & dataframe[column].notna()
        nb_neutralized = out_of_bounds.sum()
        if nb_neutralized > 0:
            print(f"  {column:30s} -> {nb_neutralized:,} valeur(s) impossible(s) neutralisée(s) en NaN")
        dataframe.loc[out_of_bounds, column] = None
    return dataframe


def build_tag_to_rayon(rayon_groups):
    tag_to_rayon = {}
    for rayon_name, tags in rayon_groups.items():
        for tag in tags:
            tag_to_rayon[tag] = rayon_name
    return tag_to_rayon


def matching_rayons(product_tags, tag_to_rayon):
    if product_tags is None:
        return set()
    return {tag_to_rayon[tag] for tag in product_tags if tag in tag_to_rayon}


def main():
    print("=== Construction de l'extrait nettoyé du périmètre ===\n")

    dataframe = pd.read_parquet(SOURCE_FILE)
    print(f"1. Chargement : {len(dataframe):,} produits France")

    # --- Extract nested nutrients and product name -------------------------------
    nutrient_names_to_extract = {
        "energy-kcal": "energy_kcal_100g",
        "sugars": "sugars_100g",
        "saturated-fat": "saturated_fat_100g",
        "salt": "salt_100g",
        "sodium": "sodium_100g",
        "fiber": "fiber_100g",
        "proteins": "proteins_100g",
        "fruits-vegetables-nuts": "fruits_vegetables_nuts_100g",
    }
    extracted_nutrients = pd.DataFrame(
        dataframe["nutriments"].apply(lambda x: extract_nutrients(x, nutrient_names_to_extract)).tolist()
    )
    dataframe = pd.concat(
        [dataframe.reset_index(drop=True), extracted_nutrients.reset_index(drop=True)],
        axis=1,
    )
    dataframe["product_name_main"] = dataframe["product_name"].apply(extract_main_name)
    print("2. Nutriments extraits depuis la colonne imbriquée")

    # --- Neutralize impossible values ---------------------------------------------
    print("3. Neutralisation des valeurs impossibles :")
    dataframe = nullify_impossible_values(dataframe, PLAUSIBILITY_BOUNDS)

    # --- Assign rayon ---------------------------------------------------------------
    tag_to_rayon = build_tag_to_rayon(SELECTED_RAYON_GROUPS)
    dataframe["matched_rayons"] = dataframe["categories_tags"].apply(
        lambda tags: matching_rayons(tags, tag_to_rayon)
    )
    dataframe["nb_matched_rayons"] = dataframe["matched_rayons"].apply(len)

    # --- Apply scope + completeness filters -----------------------------------------
    in_a_rayon = dataframe["nb_matched_rayons"] > 0
    has_nutriscore = dataframe["nutriscore_score"].notna()
    nb_key_nutrients_present = dataframe[KEY_NUTRIENTS].notna().sum(axis=1)
    enough_nutrients = nb_key_nutrients_present >= MIN_KEY_NUTRIENTS_PRESENT

    dataframe = dataframe[in_a_rayon & has_nutriscore & enough_nutrients].copy()
    print(f"4. Après filtre rayon + nutriscore_score + {MIN_KEY_NUTRIENTS_PRESENT}/7 nutriments : "
          f"{len(dataframe):,} produits")

    # --- Drop duplicate barcodes entirely --------------------------------------------
    nb_before = len(dataframe)
    dataframe = dataframe.drop_duplicates(subset="code", keep=False)
    nb_dropped = nb_before - len(dataframe)
    print(f"5. Après suppression des codes-barres en doublon : "
          f"{len(dataframe):,} produits ({nb_dropped:,} lignes retirées)")

    # --- Keep only the columns useful to the database schema -------------------------
    dataframe = dataframe[FINAL_COLUMNS]
    print(f"6. Colonnes conservées : {list(dataframe.columns)}")

    dataframe.to_parquet(OUTPUT_FILE, index=False)
    print(f"\nExtrait sauvegardé : {OUTPUT_FILE} ({len(dataframe):,} produits, "
          f"{len(dataframe.columns)} colonnes)")


if __name__ == "__main__":
    main()
