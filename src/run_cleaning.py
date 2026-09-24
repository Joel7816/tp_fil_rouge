"""Nettoie un gros fichier CSV par lots et produit clean_data.csv + rapport_nettoyage.md.

Usage (depuis la racine du projet, .venv activé) :
    python scripts/run_cleaning.py
    python scripts/run_cleaning.py --input data/autre_fichier.csv --chunk-size 200000

Le fichier est lu par lots : la mémoire utilisée ne dépend pas de la taille du fichier,
à l'exception de l'ensemble des codes-barres déjà vus (de l'ordre de 100 à 150 Mo par million de codes distincts).
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any
import sys

import pandas as pd

from nutriscope_data import config
from nutriscope_data.cleaning import clean, merge_reports

DEFAULT_INPUT = config.DATA_DIR / "echantillon_france.csv"
DEFAULT_OUTPUT_CSV = config.DATA_DIR / "clean_data.csv"
DEFAULT_REPORT = config.PROJECT_ROOT / "docs" / "data" / "rapport_nettoyage.md"
DEFAULT_CHUNK_SIZE = 100_000

INPUT_SEP = ","
OUTPUT_SEP = ","

TEXT_COLUMNS = [
    "code",
    "product_name",
    "pnns_groups_1",
    "pnns_groups_2",
    "nutriscore_grade",
    "brands",
]
NUMERIC_COLUMNS = [
    "energy-kcal_100g",
    "energy_100g",
    "fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
    "sodium_100g",
]
USED_COLUMNS = TEXT_COLUMNS + NUMERIC_COLUMNS
# Types imposés pour les colonnes texte : évite les types mixtes d'un lot à l'autre
# et conserve les zéros initiaux des codes-barres.
DTYPES = {column: "string" for column in TEXT_COLUMNS}

RULE_LABELS = {
    "nutrients_out_of_bounds": "Nutriments hors de [0, 100] g/100 g mis à NA (valeurs)",
    "energies_out_of_bounds": "Énergies implausibles mises à NA (valeurs)",
    "duplicates_removed": "Doublons de code-barres retirés (lignes)",
    "empty_categories": "Catégories vides ramenées à NA (cellules)",
    "unknown_grades": "Nutri-Score « unknown » ramené à NA (lignes)",
    "energy_imputed": "Énergie kcal imputée (lignes)",
    "salt_sodium_imputed": "Sel / sodium imputés l'un depuis l'autre (lignes)",
    "fiber_flagged": "Drapeau fiber_100g_missing posé (lignes)",
    "brands_flagged": "Drapeau brands_missing posé (lignes)",
}

MISSING_VALUES_DECISIONS = [
    ("energy-kcal_100g", "Substitution", "kJ / 4,184, sinon 4/4/9 ; le reste est traité plus tard (médiane par rayon, après split)"),
    ("salt_100g / sodium_100g", "Substitution", "relation exacte sel = 2,5 x sodium, dans les deux sens"),
    ("fiber_100g, brands", "Garder NA + drapeau", "manque informatif (MNAR) : jamais de médiane"),
    ("nutriscore_grade", "Garder NA", "« unknown » devient NA, jamais imputé"),
]


def build_markdown_report(report: dict[str, Any], input_file: Path, chunk_size: int) -> str:
    """Construit le texte Markdown du rapport avant/après."""
    rows_before = report["rows_before"]
    rows_after = report["rows_after"]
    removed = rows_before - rows_after
    removed_pct = (removed / rows_before * 100) if rows_before else 0.0

    lines = [
        "# Rapport de nettoyage",
        "",
        f"- Généré le : {datetime.now():%Y-%m-%d %H:%M}",
        f"- Fichier source : `{input_file.name}`",
        f"- Taille des lots : {chunk_size:,}".replace(",", " "),
        "",
        "## Volumétrie",
        "",
        "| | Lignes |",
        "|---|---:|",
        f"| Avant | {rows_before:,} |".replace(",", " "),
        f"| Après | {rows_after:,} |".replace(",", " "),
        f"| Retirées | {removed:,} ({removed_pct:.2f} %) |".replace(",", " "),
        "",
        "## Lignes touchées par règle",
        "",
        "| Règle | Nombre |",
        "|---|---:|",
    ]
    for key, label in RULE_LABELS.items():
        value = report.get(key, 0)
        if isinstance(value, dict):
            lines.append(f"| {label} | |")
            for sub_key, sub_value in value.items():
                lines.append(f"| &nbsp;&nbsp;↳ `{sub_key}` | {sub_value:,} |".replace(",", " "))
        else:
            lines.append(f"| {label} | {value:,} |".replace(",", " "))

    lines += [
        "",
        "## Stratégie de valeurs manquantes",
        "",
        "| Colonne | Décision | Détail |",
        "|---|---|---|",
    ]
    lines += [f"| {column} | {decision} | {detail} |" for column, decision, detail in MISSING_VALUES_DECISIONS]
    lines += [
        "",
        "## Limites connues",
        "",
        "- Doublons : la ligne la plus complète est gardée à l'intérieur d'un lot, "
        "la première rencontrée entre deux lots.",
        "- Règle de normalisation des unités : en attente (voir TODO dans `cleaning.py`).",
        "",
    ]
    return "\n".join(lines)


def run(input_file: Path, output_csv: Path, report_file: Path, chunk_size: int) -> None:
    """Lit le fichier par lots, nettoie, écrit le CSV propre puis le rapport."""
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    report_file.parent.mkdir(parents=True, exist_ok=True)

    # On écrit dans un fichier temporaire, renommé seulement si tout s'est bien passé
    temp_csv = output_csv.with_suffix(output_csv.suffix + ".tmp")
    temp_csv.unlink(missing_ok=True)

    reader = pd.read_csv(
        input_file,
        sep=INPUT_SEP,
        usecols=USED_COLUMNS,
        dtype=DTYPES,
        chunksize=chunk_size,
        low_memory=False,
    )

    seen_codes: set[str] = set()
    total_report: dict[str, Any] = {}

    for index, batch in enumerate(reader):
        cleaned, report = clean(batch, seen_codes)
        cleaned.to_csv(
            temp_csv,
            sep=OUTPUT_SEP,
            mode="w" if index == 0 else "a",
            header=index == 0,
            index=False,
        )
        total_report = merge_reports(total_report, report)
        print(f"lot {index} : {report['rows_before']} -> {report['rows_after']} lignes")

    if not total_report:
        raise SystemExit(f"Aucune ligne lue dans {input_file}")

    temp_csv.replace(output_csv)
    report_file.write_text(build_markdown_report(total_report, input_file, chunk_size), encoding="utf-8")
    print(f"CSV propre : {output_csv}")
    print(f"Rapport    : {report_file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.input, args.output, args.report, args.chunk_size)