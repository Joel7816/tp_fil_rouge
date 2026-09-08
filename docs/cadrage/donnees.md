### Choisissez, pour la base OFF, les trois dimensions de qualité qui menacent le plus votre cas d'usage, et la requête qui les mesurera

Les dimensions de qualité qui menacent le plus notre cas d'usage sont : 
* La fraicheur - Les données OFF sont mises à jour quotidiennement mais cela implique de les télécharger à chaque fois
* La complétude - Beaucoup de produits ont des valeurs manquantes
* La cohérence - Nous avons parfois des valeurs aberrantes dans le données

#### Requêtes SQL pour mesurer les dimensions de qualités :
##### Pour mesurer la complétude des nutriments 
SELECT
    COUNT(*) AS total_fiches,
    ROUND(100.0 * COUNT(*) FILTER (WHERE energy_kcal_100g IS NULL) / COUNT(*), 1) AS pct_energie_nulle,
    ROUND(100.0 * COUNT(*) FILTER (WHERE sugars_100g IS NULL) / COUNT(*), 1) AS pct_sucres_nuls,
    ROUND(100.0 * COUNT(*) FILTER (WHERE saturated_fat_100g IS NULL) / COUNT(*), 1) AS pct_graisses_sat_nulles,
    ROUND(100.0 * COUNT(*) FILTER (WHERE salt_100g IS NULL) / COUNT(*), 1) AS pct_sel_nul,
    ROUND(100.0 * COUNT(*) FILTER (WHERE fiber_100g IS NULL) / COUNT(*), 1) AS pct_fibres_nulles,
    ROUND(100.0 * COUNT(*) FILTER (WHERE proteins_100g IS NULL) / COUNT(*), 1) AS pct_proteines_nulles,
    ROUND(100.0 * COUNT(*) FILTER (WHERE fruits_vegetables_nuts_100g IS NULL) / COUNT(*), 1) AS pct_fruits_legumes_nuls
FROM nutriments;

Explication : 
Complétude au niveau des champs — la présence d'une ligne dans nutriments ne garantit pas que ses colonnes soient renseignées. Chaque COUNT(*) FILTER (WHERE colonne IS NULL) mesure, indépendamment des autres, le taux de valeurs manquantes sur un nutriment donné (énergie, sucres, graisses saturées, sel, fibres, protéines, fruits/légumes/noix), rapporté au nombre total de fiches.

##### Pour mesurer la cohérence des données
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE
        COALESCE(sugars_100g,0) + COALESCE(saturated_fat_100g,0)
        + COALESCE(proteins_100g,0) + COALESCE(fiber_100g,0) > 100
    ) AS somme_macros_superieure_100g,
    COUNT(*) FILTER (WHERE
        salt_100g IS NOT NULL AND sodium_100g IS NOT NULL
        AND ABS(salt_100g - sodium_100g * 2.5) > 0.5
    ) AS sel_sodium_incoherents
FROM nutriments;

Explication : 
Cohérence — logique inter-champs que le CHECK ne couvre pas. Le CHECK valide chaque colonne isolément, mais pas leur relation. Deux vraies incohérences possibles : la somme des macronutriments qui dépasse 100g, et le ratio sel/sodium (sel ≈ sodium × 2,5)