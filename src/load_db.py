"""
load_db.py — Charge la base NutriScope (TP4) depuis l'extrait nettoyé du périmètre.

Rejouable et idempotent : exécute intégralement schema.sql (qui commence par des
DROP TABLE IF EXISTS ... CASCADE) avant de recharger les données. Donc :

    python load_db.py

suffit, à tout moment, à détruire et recharger toute la base en une seule commande.

Entrée : data/produits_perimetre_clean.parquet (produit par build_clean_extract.py)

La logique de nettoyage des marques (normalize_brand_key) est reprise telle quelle depuis
check_data.ipynb, sans modification — c'est elle qui a servi à valider les chiffres cités
dans proposition_schema.md (33 738 marques distinctes après normalisation).
"""

import os
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# load_db.py vit dans src/, comme build_clean_extract.py : data/ et schema.sql sont donc des
# dossiers/fichiers frères de src/, à la racine du projet — d'où le .parent (même convention
# que SCRIPT_DIR.parent / "data" dans build_clean_extract.py).
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_FILE = PROJECT_ROOT / "data" / "produits_perimetre_clean.parquet"
SCHEMA_FILE = PROJECT_ROOT / "schema.sql"

NUTRIENT_COLUMNS = [
    "energy_kcal_100g", "sugars_100g", "saturated_fat_100g", "salt_100g",
    "sodium_100g", "fiber_100g", "proteins_100g", "fruits_vegetables_nuts_100g",
]

TO_SQL_KWARGS = {"if_exists": "append", "index": False, "method": "multi", "chunksize": 1000}


# --- Connexion ---------------------------------------------------------------------------

def get_engine():
    load_dotenv()
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    database = os.environ["POSTGRES_DB"]
    port = os.environ.get("POSTGRES_PORT", "5432")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:{port}/{database}")


def reset_schema(engine):
    """Exécute schema.sql en entier : DROP puis CREATE de toutes les tables."""
    with engine.begin() as connexion:
        connexion.execute(text(SCHEMA_FILE.read_text(encoding="utf-8")))


# --- Nettoyage des marques (repris tel quel de check_data.ipynb) -------------------------

def normalize_brand_key(raw_name):
    """
    Builds a comparison key that treats case, spacing, and "&" vs "and" as equivalent.
    Does NOT resolve abbreviations (e.g. "M&S" stays distinct from "Marks & Spencer") —
    that would need a hand-maintained alias table, out of scope for this cleanup.
    """
    name = raw_name.strip().lower()
    name = re.sub(r"\s*&\s*", " & ", name)     # uniformise les espaces autour de "&"
    name = name.replace(" & ", " and ")         # traite "&" et "and" comme équivalents
    name = re.sub(r"\s+", " ", name).strip()    # réduit les espaces multiples restants
    return name


def build_brand_tables(dataframe):
    """
    Éclate `brands` sur la virgule, exclut les chaînes vides, puis regroupe les doublons
    via normalize_brand_key — le nom canonique retenu par groupe est l'orthographe la plus
    fréquente (vote majoritaire), comme validé dans check_data.ipynb.
    """
    exploded = dataframe.loc[dataframe["brands"].notna(), ["code", "brands"]].copy()
    exploded["brands"] = exploded["brands"].str.split(",")
    exploded = exploded.explode("brands")
    exploded["raw_name"] = exploded["brands"].str.strip()
    exploded = exploded[exploded["raw_name"] != ""]
    exploded["normalization_key"] = exploded["raw_name"].apply(normalize_brand_key)

    canonical_names = (
        exploded.groupby("normalization_key")["raw_name"]
        .agg(lambda values: values.value_counts().idxmax())
        .reset_index()
        .rename(columns={"raw_name": "name"})
        .sort_values("normalization_key")
        .reset_index(drop=True)
    )
    canonical_names.insert(0, "id", range(1, len(canonical_names) + 1))

    key_to_id = dict(zip(canonical_names["normalization_key"], canonical_names["id"]))
    exploded["marque_id"] = exploded["normalization_key"].map(key_to_id)

    marques_table = canonical_names[["id", "name"]]
    produits_marques_table = (
        exploded[["code", "marque_id"]]
        .drop_duplicates()
        .rename(columns={"code": "code_produit"})
    )
    return marques_table, produits_marques_table


# --- Éclatement des catégories ------------------------------------------------------------

def build_category_tables(dataframe):
    """
    Éclate `categories_tags` (liste native, pas une chaîne à séparer) en une ligne par
    association produit/catégorie. Les tags OFF sont déjà des identifiants stables
    (ex. "en:dairies") : pas de normalisation de casse/orthographe nécessaire ici,
    contrairement aux marques.
    """
    exploded = dataframe.loc[dataframe["categories_tags"].notna(), ["code", "categories_tags"]].copy()
    exploded = exploded.explode("categories_tags")
    exploded = exploded[exploded["categories_tags"].notna()]

    tags = sorted(exploded["categories_tags"].unique())
    categories_table = pd.DataFrame({"id": range(1, len(tags) + 1), "tag": tags})

    tag_to_id = dict(zip(categories_table["tag"], categories_table["id"]))
    exploded["category_id"] = exploded["categories_tags"].map(tag_to_id)

    produits_categories_table = (
        exploded[["code", "category_id"]]
        .drop_duplicates()
        .rename(columns={"code": "code_produit"})
    )
    return categories_table, produits_categories_table


# --- Chargement -----------------------------------------------------------------------------

def load_produits(engine, dataframe):
    produits = dataframe[["code", "product_name_main", "nutriscore_score", "nutriscore_grade"]].copy()
    # Open Food Facts fournit nutriscore_grade en minuscules ("a".."e") ; le CHECK de
    # schema.sql attend des majuscules ("A".."E", cohérent avec proposition_schema.md) —
    # on uniformise ici plutôt que de relâcher la contrainte côté base.
    produits["nutriscore_grade"] = produits["nutriscore_grade"].str.upper()
    produits.to_sql("produits", engine, **TO_SQL_KWARGS)


def load_nutriments(engine, dataframe):
    nutriments = (
        dataframe[["code"] + NUTRIENT_COLUMNS]
        .rename(columns={"code": "code_produit"})
    )
    nutriments.to_sql("nutriments", engine, **TO_SQL_KWARGS)


def main():
    engine = get_engine()

    print("1. (Re)création du schéma (DROP puis CREATE, voir schema.sql)...")
    reset_schema(engine)

    print("2. Chargement de l'extrait nettoyé...")
    dataframe = pd.read_parquet(DATA_FILE)
    print(f"   {len(dataframe):,} produits")

    print("3. Chargement de `produits`...")
    load_produits(engine, dataframe)

    print("4. Chargement de `nutriments`...")
    load_nutriments(engine, dataframe)

    print("5. Construction et chargement de `marques` / `produits_marques`...")
    marques_table, produits_marques_table = build_brand_tables(dataframe)
    marques_table.to_sql("marques", engine, **TO_SQL_KWARGS)
    produits_marques_table.to_sql("produits_marques", engine, **TO_SQL_KWARGS)
    print(f"   {len(marques_table):,} marques distinctes, "
          f"{len(produits_marques_table):,} liens produit-marque")

    print("6. Construction et chargement de `categories` / `produits_categories`...")
    categories_table, produits_categories_table = build_category_tables(dataframe)
    categories_table.to_sql("categories", engine, **TO_SQL_KWARGS)
    produits_categories_table.to_sql("produits_categories", engine, **TO_SQL_KWARGS)
    print(f"   {len(categories_table):,} catégories distinctes, "
          f"{len(produits_categories_table):,} liens produit-catégorie")

    print("\nChargement terminé.")


if __name__ == "__main__":
    main()
