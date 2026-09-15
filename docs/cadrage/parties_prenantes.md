# PARTIES PRENANTES

## 1. Parties prenantes


| Parties | Membres | Pouvoir | Intérêt |
|:--------|:--------|:--------|:--------|
| Direction | les formateurs | fort: ils indiquent ce qu'il faut faire | fort: voir le résultat |
| Marketing | | faible: aucune influence sur la définition ou la réalisation du projet | faible: juste faire leur travail |
| Equipe data | Alexandre et Joël | fort: qualité et choix de la donnée | faible: transmettre ce qui est demandé |
| utilisateurs finaux | Personnnes faisant les courses | faible: n'a pas de pouvoir de décision sur l'évolution du projet  | fort: satisfaire un besoin |
| Délégués à la protection des données | Nous | fort: valide la conformité de l'appli | faible |
| Fournisseur de données | Open Food facts | fort: qualité et mise à disposition de la donnée | faible |
| Sponsor | | fort: gère les finances | faible |

## 2. Trois personas utilisateurs

 * le consommateur lambda qui a l'habitude faire ces courses en grandes surfaces, et qui prendre le produit avec le meilleur nutriscore
 _Amandine, 27 ans qui fait rapidement ces courses chaque semaine_
 * parents pressés qui veulent avoir une bonne alimentation pour sa famille, 
 _Bérangère et Vincent qui souhaitent avoir les produits les plus sains pour nourrir leur famille_
 * personnes faisant attention à leur alimentation pour cause d'allergique, de problème de santé ou autres . 
 _Etienne, 35 ans, qui présente une allergie aux crustacés_

## 3. Trame entretien semi-directif
 
 1. De quoi avez vous besoin ?
 2. Pourquoi voulez vous faire cela ?
 3. A qui destinez vous cette solution ?
 4. Quand est ce que la solution doit être en version final ?
 5. Quelle est votre business plan pour générer de l'argent (la valeur pour l'entreprise)?
 6. Quelles sont les informations indispensables pour vous ?


## 4. Entretien réèl

### 4.1. Interlotrice

Claire Delcourt - 43 ans
**Fonction** | Directrice générale et cofondatrice de NutriScope
**Rôle dans le projet** | Sponsor, porteuse de la vision et décisionnaire finale sur le budget, le calendrier et le périmètre
**Intérêt** | Très élevé
**Disponibilité** | Faible : elle souhaite des échanges courts, orientés décision et
résultats


### 4.2. Contraintes économiques

* Budget maximal envisagé pour le MVP : 120 000 euros, incluant conception,
développement, hébergement et premiers tests utilisateurs
* L’équipe data/IA chargée de la totalité du chantier reste de taille réduite ; elle est
accompagnée par un Product Owner à mi-temps et une UX designer partagée avec
un autre projet
* Impossibilité de recruter avant la démonstration du MVP
* Coût d'utilisation des modèles génératifs et de l'infrastructure à maintenir sous contrôle
* Modèle économique encore incertain : freemium, abonnement ou partenariats


### 4.3. Contraintes de calendrier

* Démonstration au conseil d'administration dans dix semaines
* Version pilote souhaitée dans trois mois
* Lancement public visé dans quatre mois


### 4.4. Contraintes techniques et liées aux données

* Dépendance forte à la couverture et à la qualité des données d'Open Food Facts 
* Nécessité de construire une base produits exploitable, traçable et contrôlée à partir de données externes imparfaites
* Fiches produits parfois incomplètes, anciennes, dupliquées ou contradictoires
* Absence de données fiables sur le prix et la disponibilité locale des produits
* Petite équipe data et absence actuelle de plateforme MLOps complète
* Obligation de tracer les sources et les versions des données utilisées
* Nécessité de surveiller les réponses incorrectes, les dérives et les tentatives de détournement de l'assistant
* Performance souhaitée : réponse standard en moins de trois secondes, sans engagement contractuel à ce stade


### 4.5. Contraintes juridiques et éthiques

* Respect du RGPD : consentement, minimisation, durée de conservation, droit d'accès et suppression
* Vigilance particulière concernant les données de santé ou les informations permettant d'en déduire une pathologie
* Analyse du niveau de risque et des obligations applicables au regard de l'AI Act
* Refus du diagnostic, de la prescription ou du remplacement d'un professionnel de santé
* Transparence sur le recours à l'IA et sur les limites des recommandations
* Accessibilité numérique à intégrer dès la conception
* Prévention des biais envers certains régimes, budgets, cultures alimentaires ou situations de handicap

### 4.6. Contraintes d'image et de réputation

* Une recommandation dangereuse pour une personne allergique ou diabétique serait considérée comme une crise majeure
* La présence de contenus sponsorisés ne doit pas compromettre la confiance
* NutriScope ne doit pas être perçu comme culpabilisant ou moralisateur


### 4.7. Périmètre envisageable
* Recherche d'un produit par nom ou code-barres
* Restitution des informations disponibles dans Open Food Facts
* Première prédiction et explication synthétique du Nutri-Score
* Comparaison de deux produits selon des critères affichés
* Proposition d'alternatives plus saines selon des règles explicites et vérifiables
* Préférences non médicales simples : végétarien, bio, sans alcool ou budget indicatif si la donnée existe
* Affichage des sources, des données manquantes et des limites
* Signalement d'une erreur par l'utilisateur
* Assistant limité aux produits alimentaires avec réponses encadrées
* Collecte de retours utilisateurs et tableau de bord d'usage basique

### 4.8. Briques obligatoires du produit final pouvant être phasées après le premier MVP

* Analyse exploratoire documentée et tableaux de bord destinés aux non-techniciens
* Segmentation du catalogue
* Classifieur d'images
* Chabot RAG fondé sur le catalogue et des sources publiques de référence
* API FastAPI, application de démonstration, conteneurisation, déploiement cloud, CI/CD et supervision

### 4.9. Enjeux contradictoires

La direction n'a pas encore arbitré tous les points suivants.

**Volonté de la direction** | **Tension ou contradiction**
S'adresser à tout le monde | Les besoins du parent pressé, de la personne diabétique et de l'étudiant à petit budget sont très différents
Personnaliser fortement les réponses | La direction affirme parallèlement vouloir collecter lemoins de données possible
Répondre aux besoins des personnes diabétiques | NutriScope refuse de fournir un conseil médical et ne dispose pas d'expertise clinique interne
Donner une réponse très simple | Les recommandations doivent resterexplicables, nuancées et traçables
Fournir « le meilleur choix » | Le meilleur choix peut dépendre de la nutrition, du prix, des allergies, de l'environnement ou des préférences
Proposer des alternatives disponibles | Open Food Facts ne garantit ni le prix ni la disponibilité dans un magasin précis
Afficher une marque indépendante | Les revenus pourraient dépendre de partenariats avec les industriels ou les distributeurs
Construire une technologie propriétaire | Le MVP dépend largement d'une base ouverte et de modèles externes
Récupérer le moins de données possibles | Le marketing souhaite exploiter l'historique des scans pour segmenter les utilisateurs