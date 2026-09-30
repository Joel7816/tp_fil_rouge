"""Extraction des produits d'un pays depuis les exports Open Food Facts (Parquet et CSV)."""

import contextlib
import gzip
from collections.abc import Callable
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from tqdm import tqdm

from nutriscope_data import config

COUNTRY_COLUMN = "countries_tags"
BATCH_SIZE = 50_000  # Parquet : petit lot, le fichier a beaucoup de colonnes lourdes
CSV_CHUNK_ROWS = 100_000  # CSV : nombre de lignes lues à la fois


def output_path_for(country_tag: str, dataset_name: str = "parquet") -> Path:
    """`en:belgium`, `csv` -> data/belgium/food_belgium.csv.gz"""
    slug = country_tag.split(":", 1)[-1]
    suffix = config.DATASETS[dataset_name].output_suffix
    return config.DATA_DIR / slug / f"food_{slug}{suffix}"


def contains_tag(tags: pa.Array, tag: str) -> pa.Array:
    """Masque booléen : True si la liste de la ligne contient `tag` (False si liste nulle ou vide)."""
    values = pc.list_flatten(tags)  # toutes les valeurs de toutes les listes, à plat
    row_of_value = pc.list_parent_indices(tags)  # pour chaque valeur, la ligne d'où elle vient
    matching_rows = row_of_value.filter(pc.equal(values, tag))
    return pc.is_in(pa.array(range(len(tags)), type=pa.int64()), value_set=matching_rows)


def _partial_path(destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination.with_name(destination.name + ".part")


def _finalize(partial: Path, destination: Path, rows_kept: int, country_tag: str) -> None:
    """Publie le fichier partiel, ou le supprime (et lève une erreur) s'il est vide."""
    if rows_kept == 0:
        # Un fichier vide serait pris pour valide au prochain lancement (garde-fou "existe déjà").
        partial.unlink()
        with contextlib.suppress(OSError):  # ne supprime le dossier que s'il est vide
            destination.parent.rmdir()
        raise ValueError(
            f"Aucun produit pour '{country_tag}'. Le tag doit être de la forme 'en:belgium'."
        )
    partial.replace(destination)  # le fichier final n'apparaît que s'il est complet


def _extract_parquet(source: Path, destination: Path, country_tag: str) -> int:
    parquet_file = pq.ParquetFile(source)
    schema = parquet_file.schema_arrow

    column_type = schema.field(COUNTRY_COLUMN).type
    if not (pa.types.is_list(column_type) or pa.types.is_large_list(column_type)):
        raise TypeError(f"{COUNTRY_COLUMN} devrait être une liste, reçu : {column_type}")

    partial = _partial_path(destination)
    rows_kept = 0

    with (
        pq.ParquetWriter(partial, schema) as writer,
        tqdm(
            total=parquet_file.metadata.num_rows,
            unit="ligne",
            unit_scale=True,
            desc="Lecture Parquet",
        ) as progress,
    ):
        for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
            mask = contains_tag(batch.column(COUNTRY_COLUMN), country_tag)
            country_rows = pa.Table.from_batches([batch]).filter(mask)
            if country_rows.num_rows > 0:
                writer.write_table(country_rows)
                rows_kept += country_rows.num_rows
            progress.update(batch.num_rows)
            progress.set_postfix(kept=f"{rows_kept:,}")

    _finalize(partial, destination, rows_kept, country_tag)
    return rows_kept


def _extract_csv(source: Path, destination: Path, country_tag: str) -> int:
    partial = _partial_path(destination)
    needle = f",{country_tag},"  # les tags sont séparés par des virgules : on encadre pour un match exact
    rows_kept = 0

    with (
        pd.read_csv(
            source,
            sep="\t",
            dtype=str,  # tout en texte : on recopie les lignes telles quelles
            keep_default_na=False,  # "NA" ou "" restent du texte, pas des valeurs manquantes
            chunksize=CSV_CHUNK_ROWS,
            on_bad_lines="warn",
        ) as reader,
        gzip.open(partial, "wt", encoding="utf-8", newline="", compresslevel=6) as output,
        tqdm(unit="ligne", unit_scale=True, desc="Lecture CSV") as progress,
    ):
        for chunk in reader:
            if COUNTRY_COLUMN not in chunk.columns:
                raise KeyError(f"Colonne '{COUNTRY_COLUMN}' absente du CSV.")
            wrapped_tags = "," + chunk[COUNTRY_COLUMN] + ","
            selected = chunk[wrapped_tags.str.contains(needle, regex=False)]
            if not selected.empty:
                selected.to_csv(
                    output,
                    sep="\t",
                    index=False,
                    header=(rows_kept == 0),  # l'en-tête n'est écrit qu'une fois
                    lineterminator="\n",
                )
                rows_kept += len(selected)
            progress.update(len(chunk))
            progress.set_postfix(kept=f"{rows_kept:,}")

    _finalize(partial, destination, rows_kept, country_tag)
    return rows_kept


_EXTRACTORS: dict[str, Callable[[Path, Path, str], int]] = {
    "parquet": _extract_parquet,
    "csv": _extract_csv,
}


def extract_country(dataset_name: str, country_tag: str) -> Path:
    """Extrait les produits de `country_tag` de l'export `dataset_name`. Retourne le fichier de sortie.

    Ne refait rien si le fichier de sortie existe déjà.
    """
    source = config.dataset_path(dataset_name)
    if not source.exists():
        raise FileNotFoundError(
            f"{source.name} introuvable : lance d'abord "
            f"`python -m nutriscope download --only {dataset_name}`."
        )

    destination = output_path_for(country_tag, dataset_name)
    if destination.exists():
        print(f"{destination.name} existe déjà, extraction ignorée.")
        return destination

    rows_kept = _EXTRACTORS[dataset_name](source, destination, country_tag)
    size_mb = destination.stat().st_size / 1e6
    print(f"OK [{dataset_name}] : {rows_kept:,} produits ({country_tag}) dans {destination} ({size_mb:.0f} Mo)")
    return destination