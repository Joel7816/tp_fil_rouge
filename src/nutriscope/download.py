"""Téléchargement de fichiers en streaming."""

from pathlib import Path

import requests
from tqdm import tqdm

CHUNK_SIZE = 1024 * 1024  # 1 Mio par lot
TIMEOUT_SECONDS = 30
HEADERS = {"User-Agent": "NutriScope-TP/0.1 (formation)"}


def download_file(url: str, destination: Path) -> Path:
    """Télécharge `url` vers `destination` en streaming, sans écraser un fichier existant."""
    if destination.exists():
        print(f"{destination.name} existe déjà, téléchargement ignoré.")
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + ".part")

    with requests.get(url, stream=True, timeout=TIMEOUT_SECONDS, headers=HEADERS) as response:
        response.raise_for_status()
        total_bytes = int(response.headers.get("Content-Length", 0))
        print(f"Dernière modification serveur : {response.headers.get('Last-Modified')}")

        with (
            partial.open("wb") as file,
            tqdm(
                total=total_bytes or None,  # None : barre sans pourcentage si la taille est inconnue
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=destination.name,
            ) as progress,
        ):
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)
                progress.update(len(chunk))

    partial.replace(destination)  # le fichier final n'apparaît que s'il est complet
    return destination
