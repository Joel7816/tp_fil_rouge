"""Ligne de commande : `python -m nutriscope_data <download|filter|prepare>`."""

import argparse
from collections.abc import Sequence

from nutriscope_data import config
from nutriscope_data.download import download_file
from nutriscope_data.filtering import extract_country


def selected_datasets(args: argparse.Namespace) -> list[str]:
    return args.only or list(config.DATASETS)


def cmd_download(args: argparse.Namespace) -> None:
    for name in selected_datasets(args):
        dataset = config.DATASETS[name]
        path = download_file(dataset.url, config.dataset_path(name))
        print(f"OK [{name}] : {path} ({path.stat().st_size / 1e9:.2f} Go)")


def cmd_filter(args: argparse.Namespace) -> None:
    for name in selected_datasets(args):
        extract_country(name, args.country)


def cmd_prepare(args: argparse.Namespace) -> None:
    """Enchaîne les deux étapes. Chacune est idempotente, on peut donc relancer sans risque."""
    cmd_download(args)
    cmd_filter(args)


def add_only_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--only",
        nargs="+",
        choices=list(config.DATASETS),
        help="Formats à traiter (par défaut : tous).",
    )


def add_country_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--country", default=config.DEFAULT_COUNTRY)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nutriscope")
    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser("download", help="Télécharge les exports")
    add_only_argument(download_parser)
    download_parser.set_defaults(func=cmd_download)

    filter_parser = subparsers.add_parser("filter", help="Extrait les produits d'un pays")
    add_only_argument(filter_parser)
    add_country_argument(filter_parser)
    filter_parser.set_defaults(func=cmd_filter)

    prepare_parser = subparsers.add_parser("prepare", help="download, puis filter")
    add_only_argument(prepare_parser)
    add_country_argument(prepare_parser)
    prepare_parser.set_defaults(func=cmd_prepare)

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)