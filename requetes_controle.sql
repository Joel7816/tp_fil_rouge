-- requetes_controle.sql — Base NutriScope (TP4)
--
-- 5 requêtes de contrôle, à exécuter après chaque `python load_db.py`, pour vérifier que le
-- chargement s'est déroulé comme attendu. Versionnées ici plutôt que tapées ad hoc dans
-- Adminer, pour pouvoir les rejouer identiquement à chaque rechargement.

-- ------------------------------------------------------------------------------------------
-- 1. Volumétrie par table
-- ------------------------------------------------------------------------------------------
SELECT 'produits' AS table_name, COUNT(*) AS nb_lignes FROM produits
UNION ALL SELECT 'marques', COUNT(*) FROM marques
UNION ALL SELECT 'categories', COUNT(*) FROM categories
UNION ALL SELECT 'nutriments', COUNT(*) FROM nutriments
UNION ALL SELECT 'produits_marques', COUNT(*) FROM produits_marques
UNION ALL SELECT 'produits_categories', COUNT(*) FROM produits_categories
ORDER BY table_name;

-- ------------------------------------------------------------------------------------------
-- 2. Produits sans catégorie
-- Devrait toujours renvoyer 0 ligne : le périmètre (docs/perimetre.md) exige qu'un produit
-- corresponde à au moins un des 5 rayons retenus pour entrer dans l'extrait.
-- ------------------------------------------------------------------------------------------
SELECT p.code, p.product_name_main
FROM produits p
LEFT JOIN produits_categories pc ON pc.code_produit = p.code
WHERE pc.code_produit IS NULL;

-- ------------------------------------------------------------------------------------------
-- 3. Top 20 des marques (par nombre de produits)
-- ------------------------------------------------------------------------------------------
SELECT m.name, COUNT(*) AS nb_produits
FROM produits_marques pm
JOIN marques m ON m.id = pm.marque_id
GROUP BY m.name
ORDER BY nb_produits DESC
LIMIT 20;

-- ------------------------------------------------------------------------------------------
-- 4. Complétude du Nutri-Score par rayon
-- nutriscore_score est NOT NULL en base (obligatoire dès le périmètre), donc ce contrôle
-- vaut surtout comme filet de sécurité si ce filtre amont venait à changer. Un produit peut
-- apparaître dans plusieurs rayons (categories_tags multi-valué) : il est compté dans chacun
-- des rayons dont il porte au moins un tag.
-- Le mapping tag -> rayon reprend SELECTED_RAYON_GROUPS de build_clean_extract.py (source de
-- vérité — à garder synchronisé si la liste des rayons/tags change là-bas).
-- ------------------------------------------------------------------------------------------
WITH tag_rayon AS (
    SELECT * FROM (VALUES
        ('en:dairies', 'dairy'),
        ('en:fermented-milk-products', 'dairy'),
        ('en:cheeses', 'dairy'),
        ('en:meats-and-their-products', 'meats_and_fish'),
        ('en:meats', 'meats_and_fish'),
        ('en:prepared-meats', 'meats_and_fish'),
        ('en:seafood', 'meats_and_fish'),
        ('en:poultries', 'meats_and_fish'),
        ('en:sweet-snacks', 'sweet_snacks'),
        ('en:biscuits-and-cakes', 'sweet_snacks'),
        ('en:desserts', 'sweet_snacks'),
        ('en:confectioneries', 'sweet_snacks'),
        ('en:sweet-spreads', 'sweet_snacks'),
        ('en:meals', 'prepared_frozen'),
        ('en:frozen-foods', 'prepared_frozen'),
        ('en:condiments', 'savory_grocery'),
        ('en:sauces', 'savory_grocery'),
        ('en:cereals-and-potatoes', 'savory_grocery'),
        ('en:cereals-and-their-products', 'savory_grocery')
    ) AS t(tag, rayon)
),
produits_rayon AS (
    SELECT DISTINCT pc.code_produit, tr.rayon
    FROM produits_categories pc
    JOIN categories c ON c.id = pc.category_id
    JOIN tag_rayon tr ON tr.tag = c.tag
)
SELECT
    pr.rayon,
    COUNT(*) AS nb_produits,
    COUNT(p.nutriscore_score) AS nb_avec_nutriscore,
    ROUND(100.0 * COUNT(p.nutriscore_score) / COUNT(*), 1) AS pct_complet
FROM produits_rayon pr
JOIN produits p ON p.code = pr.code_produit
GROUP BY pr.rayon
ORDER BY pr.rayon;

-- ------------------------------------------------------------------------------------------
-- 5. Doublons de codes-barres restants
-- Devrait toujours renvoyer 0 ligne : produits.code est en PRIMARY KEY (point 3 des
-- consignes). Sert de filet de sécurité si cette contrainte était un jour retirée par erreur.
-- ------------------------------------------------------------------------------------------
SELECT code, COUNT(*) AS nb_occurrences
FROM produits
GROUP BY code
HAVING COUNT(*) > 1;
