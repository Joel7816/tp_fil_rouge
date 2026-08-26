# Périmètre de données — NutriScope

## Licence et attribution

Les données proviennent d'[Open Food Facts](https://world.openfoodfacts.org). La structure de la
base est distribuée sous licence **ODbL**, le contenu individuel sous **Database Contents License
(DbCL) 1.0**, et les images sous **CC BY-SA**. Ce document et les jeux de données dérivés
(`produits_france.parquet`) créditent Open Food Facts comme source et sont repartagés sous les
mêmes conditions en cas de diffusion publique.

## 1. Périmètre retenu

### Rayons couverts au lancement

5 rayons retenus sur les 8 candidats étudiés (détail de l'exploration dans
`notebook_profiling.ipynb`, Section 6) :

- Produits laitiers
- Viandes et poissons
- Sucré/snacking
- Plats préparés et surgelés
- Épicerie salée

Boissons, Petit-déjeuner et Fruits et légumes ne sont pas couverts au lancement (voir Section 3).

### Colonnes conservées

| Champ | Usage |
|---|---|
| `code` | Identifiant unique, indispensable pour toute jointure (métadonnées / images / assistant) |
| `product_name` (→ `product_name_main`) | Nom lisible du produit |
| `nutriscore_score` / `nutriscore_grade` | Variable cible de la brique score |
| `energy_kcal_100g`, `sugars_100g`, `saturated_fat_100g`, `salt_100g`, `sodium_100g`, `fiber_100g`, `proteins_100g`, `fruits_vegetables_nuts_100g` | Les 7 nutriments de la formule officielle du Nutri-Score (`sodium_100g` conservé pour vérification croisée, non compté séparément dans le seuil de complétude) |
| `categories_tags` | Détermine le rayon d'un produit et la variante de la formule Nutri-Score applicable |
| `brands`, `countries_tags` | Filtrage et confort d'analyse |

### Seuil de complétude minimal

- `nutriscore_score` renseigné : **obligatoire** (c'est la cible du modèle, aucun entraînement possible sans elle)
- Au moins **4 des 7 nutriments clés** renseignés : seuil sur les features, volontairement pas plus strict pour ne pas biaiser l'entraînement vers les produits/marques les mieux renseignés

### Taille attendue du dataset d'entraînement (brique score)

| Étape | Produits | % du catalogue France |
|---|---|---|
| Catalogue France total | 1 247 336 | 100% |
| Dans un des 5 rayons retenus | 423 344 | 33,9% |
| ...et avec `nutriscore_score` renseigné | 343 651 | 27,6% |
| ...et avec ≥ 4/7 nutriments clés renseignés | 342 277 | 27,4% |

Le pourcentage final (27,4%) peut sembler faible, mais représente un volume tout à fait
suffisant en absolu (~342k produits) pour l'entraînement du modèle.

## 2. Critères de décision

- Alignement avec les usages produit du projet (score, substitution, segmentation, images,
  assistant)
- Priorité au volume absolu plutôt qu'au seul pourcentage de couverture, pour ne pas écarter à
  tort un périmètre pourtant exploitable
- Seuil de complétude volontairement modéré (4/7 plutôt qu'un seuil strict), pour que le modèle
  reste entraîné à gérer des produits partiellement renseignés — c'est précisément là que se
  situe l'intérêt d'un modèle prédictif plutôt qu'un simple calcul de la formule officielle
- Constat empirique tiré du profiling : le vrai goulot d'étranglement du dataset est la présence
  de `nutriscore_score` (-20,2% de perte), pas le seuil sur les nutriments (-0,5% de perte
  seulement une fois le Nutri-Score exigé) — un produit qui a un Nutri-Score a presque toujours
  déjà assez de nutriments renseignés, puisque le score se calcule à partir d'eux

## 3. Ce qu'on écarte, et pourquoi

### Rayons écartés du lancement

| Rayon écarté | Pourquoi |
|---|---|
| Boissons | Le taux de remplissage du `nutriscore_score` le plus faible des 8 candidats étudiés (52,1%, contre 66-90% pour les autres) — la qualité de données la plus fragile du lot |
| Fruits et légumes | Taux de Nutri-Score correct (76,3%), mais produits frais souvent vendus en vrac sans code-barres — peu compatibles avec le principe même d'une app de scan |
| Petit-déjeuner | Choix initial révisé après analyse : à qualité de données comparable à Sucré/snacking (66,2% contre 81,7%), il ne représentait qu'un quart de son volume (33 299 contre 150 060 produits). Remplacé par Sucré/snacking, mieux renseigné et bien plus volumineux |

Ce découpage a été révisé une première fois après avoir comparé le taux de remplissage du
`nutriscore_score` par rayon (voir `notebook_profiling.ipynb`, Section 6) — le premier choix
de rayons (avec Petit-déjeuner à la place de Sucré/snacking) ne se justifiait pas au regard des
données et a été corrigé avant validation finale.

### Colonnes considérées comme du bruit (hors des usages du projet)

| Champ | Pourquoi |
|---|---|
| `creator`, `created_t`/`datetime`, `last_modified_t`/`datetime` | Métadonnées de contribution, pas de valeur produit |
| `url` | Utile pour l'attribution de licence uniquement |
| `emb_codes`, `emb_codes_tags`, `first_packaging_code_geo` | Codes d'agrément d'usine, hors périmètre |
| `cities`, `cities_tags`, `purchase_places`, `manufacturing_places`(`_tags`) | Logistique, hors périmètre du lancement |
| `packaging` | Pas de brique liée à l'emballage/l'éco-score dans le périmètre actuel |
| `stores` | Potentiellement utile plus tard, pas nécessaire pour un MVP |
| `categories_fr`, `labels_fr`, `countries_fr` | Doublons des versions `_tags` normalisées |
| `no_nutriments` | Flag technique interne |
| `ph_100g` | Quasi jamais renseigné |
| `omega-3/6/9-fat_100g` | Taux de remplissage trop faible |
| `carbon-footprint_100g` | Intéressant pour un futur éco-score, mais trop peu renseigné aujourd'hui |
| `nutrition-score-uk_100g` | Variante redondante, hors marché français |
| `origins`, `origins_tags` | Hors périmètre des usages actuels |

### Colonnes pas encore nécessaires (utiles à une autre brique, pas au lancement)

| Champ | Utile pour |
|---|---|
| `image_url`, `image_small_url` | Brique classifieur d'images — nécessite en plus un chantier séparé d'accès au bucket S3 |
| `labels_tags`, `traces_tags` | Brique substitution (filtrer par contrainte) et assistant (répondre "contient-il X ?") |
| `ingredients_text` | Brique assistant (répondre "qu'est-ce qu'il y a dedans ?") |

Contrairement au bruit ci-dessus, ces champs seront réintégrés dès que l'équipe attaquera la
brique correspondante.

### Limite de fiabilité identifiée pendant le profiling

27 codes-barres dupliqués sur 1,2M de produits, dont un cas où le même `code` correspond à deux
produits manifestement différents ("MNMS" vs "medaillon végétal"). Volume négligeable, mais à
garder en tête si `code` sert de clé de jointure entre les bricks (produits ↔ images ↔
assistant) : une jointure sur ce champ peut, dans de rares cas, mélanger deux produits distincts.
