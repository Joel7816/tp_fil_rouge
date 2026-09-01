-- schema.sql — Base NutriScope (TP4)
--
-- DDL rejouable : commence par des DROP TABLE IF EXISTS ... CASCADE, donc peut être exécuté
-- autant de fois que nécessaire sans erreur (c'est ce qui rend load_db.py idempotent — voir
-- ce fichier pour le "détruire et recharger en une commande").
--
-- Basé sur proposition_schema.md. Trois points y sont documentés comme encore à valider avec
-- le formateur ; pour ne pas bloquer le jalon J1, ce DDL retient l'option par défaut de chacun,
-- signalée ci-dessous — à ajuster une fois validés :
--   1. `nutriscore_grade` est conservé à côté de `nutriscore_score` (dénormalisation assumée,
--      Option A de la section "Normalisation" du document — techniquement une dépendance
--      transitive au sens de la 3FN, acceptée pour éviter de recalculer la lettre à la lecture).
--   2. Les CHECK de plausibilité sur les nutriments sont conservés en base (défense en
--      profondeur), en plus du filtrage déjà fait par build_clean_extract.py.
--   3. `energy_kj_100g` n'est pas stocké : absent de produits_perimetre_clean.parquet (voir
--      FINAL_COLUMNS dans build_clean_extract.py), donc rien à modéliser pour l'instant.

DROP TABLE IF EXISTS produits_categories CASCADE;
DROP TABLE IF EXISTS produits_marques CASCADE;
DROP TABLE IF EXISTS nutriments CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS marques CASCADE;
DROP TABLE IF EXISTS produits CASCADE;

-- ---------------------------------------------------------------------------------------
-- Tables de référence
-- ---------------------------------------------------------------------------------------

CREATE TABLE marques (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE categories (
    id  SERIAL PRIMARY KEY,
    tag TEXT NOT NULL UNIQUE  -- valeur brute categories_tags, ex. "en:dairies"
);

-- ---------------------------------------------------------------------------------------
-- Produits
-- ---------------------------------------------------------------------------------------

CREATE TABLE produits (
    code               TEXT PRIMARY KEY,  -- code-barres : unicité garantie par la PK (point 3)
    product_name_main  TEXT,
    nutriscore_score    NUMERIC NOT NULL,  -- obligatoire par construction (voir docs/perimetre.md)
    nutriscore_grade   CHAR(1) CHECK (nutriscore_grade IN ('A', 'B', 'C', 'D', 'E'))
);

CREATE TABLE nutriments (
    code_produit                 TEXT PRIMARY KEY REFERENCES produits(code) ON DELETE CASCADE,
    energy_kcal_100g             NUMERIC CHECK (energy_kcal_100g BETWEEN 0 AND 900),
    sugars_100g                  NUMERIC CHECK (sugars_100g BETWEEN 0 AND 100),
    saturated_fat_100g           NUMERIC CHECK (saturated_fat_100g BETWEEN 0 AND 100),
    salt_100g                    NUMERIC CHECK (salt_100g BETWEEN 0 AND 100),
    sodium_100g                  NUMERIC CHECK (sodium_100g BETWEEN 0 AND 100),
    fiber_100g                   NUMERIC CHECK (fiber_100g BETWEEN 0 AND 100),
    proteins_100g                NUMERIC CHECK (proteins_100g BETWEEN 0 AND 100),
    fruits_vegetables_nuts_100g  NUMERIC CHECK (fruits_vegetables_nuts_100g BETWEEN 0 AND 100)
);

-- ---------------------------------------------------------------------------------------
-- Tables de liaison (plusieurs-à-plusieurs) — 1FN : brands/categories_tags sont multi-valués
-- dans la donnée source, ces tables les éclatent en une ligne par association.
-- ---------------------------------------------------------------------------------------

CREATE TABLE produits_marques (
    code_produit TEXT    NOT NULL REFERENCES produits(code) ON DELETE CASCADE,
    marque_id    INTEGER NOT NULL REFERENCES marques(id) ON DELETE CASCADE,
    PRIMARY KEY (code_produit, marque_id)
);

CREATE TABLE produits_categories (
    code_produit TEXT    NOT NULL REFERENCES produits(code) ON DELETE CASCADE,
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (code_produit, category_id)
);

-- Index sur le sens "inverse" des tables de liaison (la PK composite couvre déjà
-- code_produit -> marque_id/category_id efficacement, mais pas l'inverse, utile pour les
-- requêtes de contrôle du type "top marques" / "produits par catégorie").
CREATE INDEX idx_produits_marques_marque ON produits_marques(marque_id);
CREATE INDEX idx_produits_categories_category ON produits_categories(category_id);
