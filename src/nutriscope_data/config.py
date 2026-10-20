"""Chemins et constantes partagés par tout le projet."""

from dataclasses import dataclass
from pathlib import Path

# config.py -> nutriscope/ -> src/ -> racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


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