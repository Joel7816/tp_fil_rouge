# Proposition de schéma — Base NutriScope (TP4)

Schéma retenu pour la base NutriScope, basé sur l'extrait nettoyé du périmètre
(`produits_perimetre_clean.parquet`, 342 264 lignes) et sur les décisions du TP2/TP3 (voir
`docs/perimetre.md`). DDL correspondant : `schema.sql`.

## Tables

**`marques`** — `id` (PK), `name` (unique). `brands` est multi-valué (~12% des produits ont
plusieurs marques séparées par une virgule) et contient des variantes d'orthographe de la même
marque (casse, espaces, `&`/`and`) : `load_db.py::normalize_brand_key` normalise et fusionne les
doublons, le nom canonique retenu étant l'orthographe la plus fréquente par groupe.

**`categories`** — `id` (PK), `tag` (unique, valeur brute de `categories_tags`, ex.
`en:dairies`). Tout est gardé tel quel, y compris les tags non-anglais présents dans la donnée
source (`ar:`, `bg:`, etc.) — pas de filtrage à ce stade.

**`produits`** — `code` (PK, texte : préserve les zéros de tête du code-barres),
`product_name_main`, `nutriscore_score` (obligatoire), `nutriscore_grade` (A-E, gardé à côté de
`nutriscore_score` malgré la dépendance qu'il introduit — dénormalisation assumée pour éviter un
recalcul à la lecture).

**`nutriments`** — `code_produit` (PK/FK vers `produits`, un-à-un), plus les 7 nutriments du
Nutri-Score et `sodium_100g`, tous numériques.

**`produits_marques`** / **`produits_categories`** — tables de liaison (`code_produit` +
`marque_id`/`category_id`, clé composite), pour les deux relations plusieurs-à-plusieurs.

## Contraintes

- `produits.code` : unicité garantie par la clé primaire
- Toutes les clés étrangères avec `ON DELETE CASCADE`
- `CHECK` sur les nutriments (bornes de plausibilité du TP2) et sur `nutriscore_grade` (A-E)

## Normalisation

Schéma en 1FN (tables de liaison pour `brands`/`categories_tags`, multi-valués), 2FN (les tables
à clé composite ne portent aucune colonne hors clé) et 3FN à une exception assumée près :
`nutriscore_grade` dépend de `nutriscore_score` plutôt que directement de `code` — dénormalisation
volontaire, gardée pour la performance de lecture plutôt que recalculée à la volée.
