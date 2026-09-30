"""Chemins et constantes partagés par tout le projet."""

from dataclasses import dataclass
from pathlib import Path

# config.py -> nutriscope/ -> src/ -> racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

COMPLETENESS_NUTRIENTS: list[str] = [
    "energy-kcal_100g", "fat_100g", "saturated-fat_100g", "sugars_100g",
    "fiber_100g", "proteins_100g", "salt_100g",
]
CONTROL_NUTRIENTS: list[str] = [
    "energy-kj_100g", "energy_100g", "carbohydrates_100g",
    "sodium_100g", "fruits-vegetables-legumes_100g",
]
NUTRIENTS: list[str] = COMPLETENESS_NUTRIENTS + CONTROL_NUTRIENTS

INFORMATIONS: list[str] = [
    'code',
    'product_name',
    'brands',
    'categories',
    'categories_tags',
    'labels',
    'countries',
    'countries_tags',
    'allergens',
    'nutriscore_score',
    'nutriscore_grade',
    'pnns_groups_1',
    'pnns_groups_2',
    'food_groups',
    'food_groups_tags',
    'completeness',
]

COLUMNS = NUTRIENTS + INFORMATIONS

MAX_PER_100G = 100  # un nutriment ne peut pas dépasser 100 g pour 100 g de produit
KJ_KCAL_RATIO_RANGE = (3.8, 4.6)  # ratio théorique 4,184, élargi pour les arrondis
KJ_MAX = 3700
KCAL_MAX = 900  # ≈ graisse pure
MACRO_SUM_MAX = 105  # graisses + glucides + protéines + sel, marge d'arrondi
LABEL_ROUNDING_TOL = 0.5  # g/100g, arrondis d'étiquette
SALT_PER_SODIUM = 2.5
SALT_SODIUM_ABS_TOL = 0.05  # g/100g
SALT_SODIUM_REL_TOL = 0.10

NUTRISCORE_GRADES = "abcde"  # les notes valides, hors "unknown" et "not-applicable"
MIN_NUTRIENTS = 6

@dataclass(frozen=True)
class Dataset:
    url: str
    filename: str
    output_suffix: str  # extension des fichiers extraits par pays


DATASETS: dict[str, Dataset] = {
    "parquet": Dataset(
        url=(
            "https://huggingface.co/datasets/openfoodfacts/product-database"
            "/resolve/main/food.parquet"
        ),
        filename="food.parquet",
        output_suffix=".parquet",
    ),
    "csv": Dataset(
        url="https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz",
        filename="food.csv.gz",
        output_suffix=".csv.gz",
    ),
}

DEFAULT_COUNTRY = "en:france"


def dataset_path(name: str) -> Path:
    """Chemin local de l'export complet (`parquet` ou `csv`)."""
    return DATA_DIR / DATASETS[name].filename