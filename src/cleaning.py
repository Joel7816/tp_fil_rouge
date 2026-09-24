'''

TP 9 — Nettoyage industrialisé · jeu 24/09 (C. Ringot, ½ j après 3.2)
Objectif : transformer les recettes de nettoyage du matin en module testé et rejouable.
1. Créer src/cleaning.py : chaque règle de nettoyage devient une fonction pure documentée — normalisation des
unités, bornage des nutriments (0–100 g/100 g, énergies plausibles), déduplication des codes-barres, traitement
des catégories vides.
2. Stratégie de valeurs manquantes par colonne et par usage (supprimer, imputer, garder avec drapeau) — décision
écrite, pas implicite.
3. Tests pytest sur chaque règle, y compris les cas tordus relevés au TP 2.
4. Rapport avant/après généré par script : lignes touchées par règle, volumétrie finale.
5. Brancher le nettoyage sur le chargement de la base du TP 4 (la base ne reçoit plus que du propre).
À committer : src/cleaning.py + tests verts + docs/data/rapport_nettoyage.md .

Définitions : 

- MCAR => Manque qui ne dépend de rien
- MAR => Manque qui dépend d'une autre colonne
- MNAR => La valeur est manquante parce qu'elle est nulle, gênante ou sans objet

Ce qu'on fait sur : 
- MCAR => Supprimer les lignes ou imputer sans biais
- MAR => Imputer conditionnellement (par rayon, par complétude)
- MNAR => Garder NA + drapeau (ne jamais prendre la médiane)

'''
from pathlib import Path
import pandas as pd

notebook_directory = Path.cwd()
data_directory = notebook_directory / "data"
csv_file = data_directory / "food.csv"

useful_columns = [
    "code",
    "product_name",
    "countries_tags",
    "pnns_groups_1",
    "pnns_groups_2",
    "nutriscore_grade",
    "brands",
    "energy-kcal_100g",
    "fat_100g",
    "carbohydrates_100g",
    "energy_100g",
    "fiber_100g",
    "sugars_100g",
    "proteins_100g",
    "salt_100g",
    "sodium_100g",
    "stores"
]

reader = pd.read_csv(
    csv_file,
    sep='\t',
    usecols=useful_columns,
    chunksize=50_000,
    low_memory=False,
)

filtered_batches = []
total_rows = 0

for i, batch in enumerate(reader):
    is_french = batch['countries_tags'].fillna("").str.contains('en:france')
    batch_fr = batch[is_french]

    filtered_batches.append(batch_fr)
    total_rows += len(batch_fr)

    print(f"batch {i} read, {total_rows} french rows cumulated")

    if total_rows >= 5_000:
        break

dataframe = pd.concat(filtered_batches, ignore_index=True).head(5_000)
print(dataframe.shape)

'''
Normalisation des grades
'''
def normaliser_grade(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    '''1. Cible : « unknown » devient NA ; on ne remplit jamais'''
    result = dataframe.copy()
    sentinelle = result['nutriscore_grade'].astype('string').str.lower().eq('unknown')
    result['nutriscore_grade'] = result["nutriscore_grade"].mask(sentinelle, pd.NA)

    return result, int(sentinelle.sum())

'''
Imputation métier pour l'énergie
'''
def imputer_energie_metier(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """2. Énergie : d'abord les kJ, ensuite 4/4/9, jamais une moyenne."""
    result = dataframe.copy()
    kcal = result["energy-kcal_100g"]
    depuis_kj = kcal.isna() & result["energy_100g"].notna()
    kcal = kcal.mask(depuis_kj, (result["energy_100g"] / 4.184).round(1))
    calc = 4 * result["carbohydrates_100g"] + 4 * result["proteins_100g"] + 9 * result["fat_100g"]
    depuis_macros = kcal.isna() & calc.notna() & (calc <= 900)
    kcal = kcal.mask(depuis_macros, calc.round(1))
    result["energy-kcal_100g"] = kcal
    return result, {"depuis_kj": int(depuis_kj.sum()), "depuis_macros": int(depuis_macros.sum()), "restant": int(kcal.isna().sum())}

def imputer_sel_sodium(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """3. Sel et sodium : relation exacte dans les deux sens."""
    res = dataframe.copy()
    sel, sodium = res["salt_100g"], res["sodium_100g"]
    sel_ok = sel.isna() & sodium.notna()
    sodium_ok = sodium.isna() & sel.notna()
    res["salt_100g"] = sel.mask(sel_ok, sodium * 2.5)
    res["sodium_100g"] = sodium.mask(sodium_ok, sel / 2.5)
    return res, {"sel_depuis_sodium": int(sel_ok.sum()), "sodium_depuis_sel": int(sodium_ok.sum()), "restant": int(res["salt_100g"].isna().sum())}


def drapeau(dataframe: pd.DataFrame, colonne: str) -> tuple[pd.DataFrame, int]:
    """4. et 5. Fibres, marques : la valeur reste manquante, le modèle saura qu'elle manque."""
    res = dataframe.copy()
    res[f"{colonne}_manquant"] = res[colonne].isna().astype("boolean")
    return res, int(res[f"{colonne}_manquant"].sum())


def mediane_par_rayon_apres_split(train: pd.DataFrame, test: pd.DataFrame, colonne: str) -> tuple[pd.Series, pd.Series]:
    """L'imputation statistique se calcule sur le train et s'applique au test : jamais l'inverse."""
    medianes = train.groupby("pnns_groups_1")[colonne].median()
    repli = train[colonne].median()
    remplir = lambda d: d[colonne].fillna(d["pnns_groups_1"].map(medianes)).fillna(repli)  # noqa: E731
    return remplir(train), remplir(test)

dataframe, n = normaliser_grade(dataframe)
print(f'nutriscore_grade : {n} « unknown » → NA ; manquants réels : {dataframe['nutriscore_grade'].isna().mean() * 100:.1f} % (jamais imputés)')
dataframe, bilan = imputer_energie_metier(dataframe)
print("energy-kcal_100g :", bilan, f"-> {dataframe['energy-kcal_100g'].isna().mean() * 100:.1f} % manquants")
dataframe, bilan = imputer_sel_sodium(dataframe)
print("salt_100g / sodium_100g :", bilan)
dataframe, n = drapeau(dataframe, "fiber_100g")
print(f"fiber_100g : {n} drapeaux posés, valeur laissée NA ({dataframe} %)")
dataframe, n = drapeau(dataframe, "brands")
print(f"brands : {n} drapeaux posés")
dataframe = dataframe.drop(columns=["stores"])
print("stores : colonne supprimée ->", dataframe.shape[1], "colonnes")