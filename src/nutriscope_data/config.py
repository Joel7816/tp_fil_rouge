"""Chemins et constantes partagés par tout le projet."""

from dataclasses import dataclass
from pathlib import Path

# config.py -> nutriscope/ -> src/ -> racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

COLUMNS: list[str] = [
    "code",
    "product_name",
    "brands_tags",
    "categories_tags",
    "labels_tags",
    "countries_tags",
    "image_url",
    "image_small_url",
    "ingredients_text",
    "ingredients_tags",
    "ingredients_analysis_tags",
    "allergens_en",
    "traces_tags",
    "additives_tags",
    "nutriscore_score",
    "nutriscore_grade",
    "nova_group",
    "pnns_groups_1",
    "pnns_groups_2",
    "food_groups",
    "food_groups_tags",
    "food_groups_en",
    "completeness",
    "energy-kj_100g",
    "energy-kcal_100g",
    "energy_100g",
    "fat_100g",
    "saturated-fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
    "sodium_100g",
    "fruits-vegetables-legumes_100g",
]

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