# 29/07/2026

1. on choisit le format .parquet car on veut travailler avec la BDD DuckDB pour la découvrir
    taille: 7.18 Go
    date téléchargement 29/07 10:38

    ## Fait: télécharger le fichier, commencer la lecture des datas
        Réponses aux questions :
            1- 1 259 443 produits vendus en France

            2- 37,12 % de ces produits ont un Nutri-Score renseigné (grades a/b/c/d/e uniquement ;
            les valeurs "unknown" et "not-applicable" ne sont pas des grades renseignés et sont exclues)

            3- Le top 10 des marques (chaînes vides exclues) :
                U               16 107
                Carrefour       15 126
                Auchan           8 200
                Marque Repère    7 674
                Casino           6 465
                Nestlé           5 944
                Leader Price     5 694
                Lidl             4 676
                Monoprix         4 481
                Cora             4 119

            4- Le taux de manquants en énergie, en sucre et en sel est : 27,54 % , 32,45 % , 37,25 %
            (l'énergie est comptée renseignée si elle apparaît sous n'importe lequel de ses noms
            dans l'export : energy-kcal, energy ou energy-kj)

            5- Parmi les données explorées, deux éléments ressortent comme les plus problématiques :
            - le champ "marques" contient un grand nombre de valeurs vides comptées à tort comme
                une marque à part entière (plus de 55 000 produits dans les données brutes) — un piège
                silencieux, puisque le résultat a l'air correct tant qu'on ne vérifie pas le contenu
                de la première ligne du classement
            - le sel reste le nutriment le moins bien renseigné des trois (37,25 % de manquants),
                suivi du sucre (32,45 %) puis de l'énergie (27,54 %)
    ## Décidé : utiliser le format parquet
    ## Bloqué: chargement des produits français


## 25/08/2026: Profiling et périmètre

   ## Fait
        - analyse des données
        - choix des champs à garder
        - choix des rayons couverts

   ## Décidé
        - choix de 5 rayons avec asssez de produits
        - choix des champs qu'on garde, et taux de remplissage

   ## Bloqué: non


# 27/08/2026 : Git

   ## Fait
        - Création de branches propres dans GIT
        - Exerices sur GIT

   ## Décidé: rien a décider

   ## Bloqué: aucun blocage

## 01/09/2026 : SQL - Construction de la base de données
### Fait : 
* Mise en place de l'infra dockerisée : docker-compose.yml (Postgres 16 + Adminer), .env.example, requirements.txt
* Écriture de schema.sql (DDL des 6 tables : produits, marques, categories, nutriments, produits_marques, produits_categories) avec DROP en tête pour le rendre rejouable
* Écriture de load_db.py : script de chargement idempotent depuis produits_perimetre_clean.parquet
* Écriture de requetes_controle.sql (5 requêtes versionnées : volumétrie par table, produits sans catégorie, top marques, complétude Nutri-Score par rayon, doublons de codes-barres restants)
* Écriture de build_clean_extract.py pour avoir un fichier nettoyé un peu plus que le fichier "france"
* Création du fichier "proposition_schema.md" qui fait état des tables et jointures

### Décidé : 
* remettre au propre / réorganiser le dépôt pour que n'importe qui puisse rejouer les notebooks et autres scripts facilement
* brands et categories_tags, tous deux multi-valués dans la donnée source, sont modélisés via des tables de liaison (produits_marques, produits_categories) plutôt que des colonnes texte, conformément à la consigne
* Les noms de marque sont normalisés à la casse/espaces/& vs and près (fonction normalize_brand_key), avec le nom canonique = orthographe la plus fréquente par groupe
* categories_tags est chargé tel quel en base, y compris les tags non-anglais : pas de filtrage au chargement, un futur usage précis (ex. features du modèle) filtrera à la demande plutôt que de subir un choix pris ici
* nutriscore_grade reste stocké à côté de nutriscore_score (dénormalisation assumée malgré la dépendance transitive au sens de la 3FN), et les CHECK de plausibilité sur les nutriments sont conservés en base en plus du filtrage déjà fait en amont
* produits.code est en TEXT (pas numérique, pour préserver les zéros de tête du code-barres) — pas de perte de performance en PostgreSQL par rapport à VARCHAR(n)
* energy_kj_100g n'est pas stocké (absent de l'extrait nettoyé du périmètre) - On a gardé energy_kcal_100g

### Bloqué : Aucun blocage