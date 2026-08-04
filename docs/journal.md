# 29/07/2026

1. on choisit le format .parquet car on veut travailler avec la BDD DuckDB pour la découvrir
    taille: 7.18 Go
    date téléchargement 29/07 10:38

    Fait: télécharger le fichier, commencer la lecture des datas
        Réponses aux questions:
            1- 1.247.346 produits vendus en France
            2- 37,18% de ces produits ont un nutriscore renseignés
            3- Le top 10 des marques sont (si on exclue les valeurs non renseignées):
                brands      
                                54688
                Carrefour       12052
                U               11974
                Auchan           6291
                Leader Price     5427
                Casino           5119
                Cora             3960
                Le Gaulois       3548
                Picard           3501
                Monoprix         3399
                Nestlé           3341
            4- Le taux de manquant en energie, en sucre et en sel est : 30.22% ,  38.00% , 42.45%
            5- Parmi les données ci-dessus, les plus sales sont celles qui manquent de sel
    Décidé : utiliser le format parquet
    Bloqué: chargement des produits français