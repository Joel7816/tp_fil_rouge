## 1. Contexte

Dans la situation actuelle, les gens veulent manger de manière équilibré sans trop se prendre la tête.
C'est particulièrement vrai pour les personnes pressées, les familles et les gens avec des pathologies (allergie, diabète, ...).
Elles ne veulent pas pas passés trop de temps à déchiffrer des étiquettes.
Avec une confiance très friable envers les fabricants, les gens sont plus suceptibles d'utiliser des applications indépendantes comme Yuka.
Nous allons créer notre application de nutriscore, en nous appuyant sur les données de Open Food Facts.


## 2. Besoin

Avoir un outil simple d'usage pour obtenir le nutriscore d'un produit.
On doit pouvoir expliquer en quelques mots le niutriscore affiché et aussi pour les alternatives qu'on propose.
Notre solution ne doit pas donner des conseils médicaux, ou être culpabilisantes.
Elle doit juste données une information clair et simple à lire et à comprendre.


## 3. Parties prenantes

| Parties | Membres |
|:--------|:--------|
| Direction | les formateurs |
| Marketing | Nous |
| Equipe data | Alexandre et Joël |
| utilisateurs finaux | Personnnes faisant les courses |
| Délégués à la protection des données | Nous |
| Fournisseur de données | Open Food facts | 
| Sponsor | les formateurs |


## 4. Périmètres

5 rayons retenus sur les 8 candidats étudiés (détail de l'exploration dans
`notebook_profiling.ipynb`, Section 6) :

- Produits laitiers
- Viandes et poissons
- Sucré/snacking
- Plats préparés et surgelés
- Épicerie salée

Boissons, Petit-déjeuner et Fruits et légumes ne sont pas couverts au lancement (voir Section 3).

 Au moins **4 des 7 nutriments clés** renseignés : seuil sur les features, volontairement pas plus strict pour ne pas biaiser l'entraînement vers les produits/marques les mieux renseignés.

 On laisse certaines informations de côtés pour l'instant car elles n'entrent pas dans le calcul du nutriscore aujourd'hui,
 et on considère qu'elles sont moins d'impact sur les choix des populations françaises aujourd'hui.


 ## 5. KPI / ROI



 ## 6. Riques / plan de mitigation

 | Risques | Impacts | Plan d migigation |
 |:------------ |:------------ | :------------------- |
 | collecte des données personnelles |  Atteinte à la vie privée, fuite de données, non-conformité RGPD, perte de confiance | Demander les informations les plus importantes pour l'appli, et peu de données privés (adresse, ...) |
 |Erreur dans l’algorithme | Score incorrect → perte de confiance, mauvaise information utilisateur | Faire plusieurs tests, et demander un retour utilisateur pour identifier les soucis |
 |Données produit incomplètes ou erronées | Calcul faussé ou impossible | Fiabilisé la donnée d'entrainements le plus possibles |
 | Mauvaise gestion des cas particuliers | Résultats incorrects pour certaines catégories | Indiquer les catégories pour lesquels l'appli ne peut pas donner de résultats fiables |
| Manque de visibilité ou de clarté | Abandon des utilisateurs | réaliser une interface simple et lisible en un coup d'oeil


## 7. Macro-planing

| Jalons | Descriptif | Date |
| :-------- | :-------- | :-------- |
| J3 | pipeline data documenté + rapport EDA + tableaux de bord | 14/10 |
| J4 | modèles ML et DL évalués (notebooks propres + métriques) | 04/11 |
| J5 | assistant RAG démontrable + rapport d'évaluation | 30/11 |
| J6 | application déployée (URL), CI/CD, images Docker | 29/12 |
| J7 | produit final + documentation + soutenance blanche | 14/01 |


## 8. Users stories

**User Story 1 — Calculer le Nutri-Score** 

En tant qu’utilisateur, je veux saisir pouvoir scanner un produit, afin d’obtenir automatiquement son Nutri-Score.

Critères d’acceptation :
* L’utilisateur peut scanner le code barre (Mo).
* L’application vérifie que les données saisies sont valides (S).
* Le Nutri-Score calculé est affiché clairement (Mo).
* Le résultat correspond à la méthode de calcul utilisée par l’application (Mo).


**User Story 2 — Consulter le détail du calcul**

En tant qu’utilisateur, je veux pouvoir consulter le détail du calcul du Nutri-Score, afin de comprendre comment le résultat a été obtenu.

Critères d’acceptation :
* Le score obtenu est affiché (Mo).
* Les principaux éléments ayant contribué au calcul sont présentés (S).
* Les valeurs nutritionnelles utilisées sont visibles (Co).
* Le résultat est compréhensible par un utilisateur non technique (Mo).


**User Story 3 — Protéger mes données personnelles**

En tant qu’utilisateur, je veux que mes données personnelles soient protégées, afin de pouvoir utiliser l’application sans craindre qu’elles soient utilisées ou partagées sans mon accord.

Critères d’acceptation :
* Seules les données nécessaires au fonctionnement de l’application sont collectées (Mo).
* Les données personnelles sont sécurisées(Mo).
* L’utilisateur est informé des données collectées et de leur utilisation (S).
* L’utilisateur peut demander la suppression de ses données lorsque cela est applicable (Co).

**User Story 4 — Gérer les évolutions du Nutri-Score**

En tant qu’administrateur, je veux pouvoir mettre à jour les règles de calcul du Nutri-Score, afin que l’application reste conforme lorsque la méthode officielle évolue.

Critères d’acceptation :
* La version de la méthode de calcul utilisée est identifiable (Mo).
* Les paramètres de calcul peuvent être mis à jour (Co).
* Une modification des règles ne casse pas les calculs existants (S).
* Des tests de non-régression permettent de vérifier les nouvelles règles (S).

**User Story 5 — Utiliser le chat**

En tant qu'utilisateur, je veux pouvoir utiliser le chat pour demander des informations à l'application.

Critères d’acceptation :
* L’utilisateur peut ouvrir le chat depuis l’application (Mo).
* L’utilisateur peut saisir et envoyer un message (Mo).
* Le chat affiche clairement les messages de l’utilisateur et les réponses de l’assistant (Mo).
* L’assistant répond aux questions liées au Nutri-Score et aux informations nutritionnelles (Mo).
* L’assistant indique lorsqu’il ne dispose pas de suffisamment d’informations pour répondre (Mo).
* L’assistant ne présente pas une information incertaine comme une certitude (Mo).
* Le chat gère correctement les messages vides ou invalides (Co).
* Une erreur technique est signalée clairement si le service de chat est indisponible (S).
* Les données personnelles éventuellement présentes dans les conversations sont protégées(Co).


**User Story 6 — Faire des photos pour trouver un produit**

Comme utilisateur, je veux pouvoir trouver un produit à partir d'une photo.

Critères d’acceptation :
* faire une photo depuis l'application (Mo)
* importer une photo depuis la galerie (Co)
* L’application analyse la photo et tente d’identifier le produit (Mo)
* Lorsque le produit est identifié, son nom et ses informations nutritionnelles sont affichés.(Mo)
* Si aucun produit n’est identifié, l’application informe clairement l’utilisateur et lui propose de réessayer (Mo)
