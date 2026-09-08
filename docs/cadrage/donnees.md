## les trois dimensions de qualité qui menacent le plus votre cas d'usage, et la requête qui les mesurera

Les 3 dimensions qui menacent le plus notre cas d'usage sont:
* **la fraîcheur**: même si la base OFF est mis à jour quotidiennement, nous ne la récupérons pas tous les jours.
 De plus, on n'a pas de date d'insertion ou de mise à jour dans notre base.
* **la complétude**: bien qu'ayant des contrôles pour prendre les données les plus compètent possibles, on constate que pour certains produits il nous manque des éléments.

select count(*) as nb_produits,  
sum(case when energy_kcal_100g is null then 0 else 1 end) as energy_kcal_100g ,  
sum(case when sugars_100g is null then 0 else 1 end) as sugars_100g ,  
sum(case when saturated_fat_100g is null then 0 else 1 end) as saturated_fat_100g ,  
sum(case when salt_100g is null then 0 else 1 end) as salt_100g,  
sum(case when sodium_100g is null then 0 else 1 end) as sodium_100g ,  
sum(case when fiber_100g is null then 0 else 1 end) as fiber_100g ,  
sum(case when proteins_100g is null then 0 else 1 end) as proteins_100g ,  
sum(case when fruits_vegetables_nuts_100g is null then 0 else 1 end) as fruits_vegetables_nuts_100g  
from nutriments

* **l'exatitude**: tant qu'on a pas un mvp, il sera difficile de comparer la réalité avec ce qu'on a en base
