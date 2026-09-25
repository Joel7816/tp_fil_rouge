from pathlib import Path
import pandas as pd

notebook_directory = Path.cwd()
data_directory = notebook_directory / "data"
csv_file = data_directory / "food.csv"

pnns_apercu = pd.read_csv(csv_file, sep="\t", usecols=['pnns_groups_1', 'pnns_groups_2'], nrows=1000)
print(pnns_apercu['pnns_groups_1'].unique())
print(pnns_apercu['pnns_groups_2'].unique())

# columns_to_load = [
#     "code",
#     "product_name",
#     "countries_tags",
#     "pnns_groups_1",
#     "pnns_groups_2",
#     "nutriscore_grade",
#     "brands",
#     "energy-kcal_100g",
#     "fat_100g",
#     "carbohydrates_100g",
#     "sugars_100g",
#     "salt_100g",
#     "sodium_100g",
# ]

# lecteur = pd.read_csv(
#     csv_file,
#     sep="\t",
#     usecols=columns_to_load,
#     chunksize=50_000,
#     low_memory=False,
# )

# chunks_filtres = []
# rows = 0

# for i, chunk in enumerate(lecteur):
#     est_francais = chunk['countries_tags'].fillna("").str.contains("en:france")
#     chunk_fr = chunk[est_francais]

#     chunks_filtres.append(chunk_fr)
#     rows += len(chunk_fr)

#     print(f"lot {i} lu, {rows} lignes françaises cumulées")

#     if rows >= 10_000:
#         break

# dataframe = pd.concat(chunks_filtres, ignore_index=True).head(10_000)
# print(dataframe.shape)
# print(dataframe[['countries_tags', 'pnns_groups_1']])