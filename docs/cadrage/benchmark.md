# TP 6 - Opportunité & concurrence

## Objectif : Situer NutriScope sur son marché et formuler sa proposition de valeur

1. Benchmark de l'existant : Yuka, l'application Open Food Facts, myLabel, ScanUp… <br> 
Pour chacun : fonctionnalités, modèle économique, points faibles visibles.
2. Matrice comparative (fonctionnalités × acteurs) : où sont les cases vides ?
3. Analyse rapide type SWOT de NutriScope au regard du benchmark.
4. Formulation de la proposition de valeur en une phrase testable, puis en un paragraphe : qu'est-ce qu'on fait mieux
ou différemment, pour qui.
5. Pitch de 3 minutes par équipe devant le groupe ; vote consultatif sur la proposition la plus convaincante.


### 1. Benchmark des applications existantes

| Application | Fonctionnalités | Modèle économique | Points faibles |
|---|---|---|---|
| **Yuka** | Scan (alimentaire + cosmétique)<br>Note /100 (nutrition 60 %, additifs 30 %, bio 10 %)<br>Suggestions d'alternatives<br>Programme nutrition payant | Gratuit<br>~50 % programme payant (59 €)<br>~50 % dons <br> Vente produits dérivés| Pondération additifs/bio contestée (Pr Hercberg)<br>Analyse cosmétique fragile (ignore concentration/fréquence)<br>Effet culpabilisant sans alternative accessible |
| **Open Food Facts** | Scan<br>Nutri-Score<br>Eco-Score<br>Alertes allergènes<br>Préférences personnalisées<br>Extensions (beauté, animalier, prix) | Association à but non lucratif<br>Dons<br>Pas de pub ni payant<br>Contributeurs bénévoles | Interface peu intuitive<br>Pas de suivi/plan alimentaire perso<br>Pas de recettes/menus |
| **myLabel** | Scan multi-critères (santé/environnement/social)<br>Nutri Perso (score personnalisé selon profil/portions)<br>Intégration sites d'achat en ligne | Entreprise à mission (ESUS)<br>Vente d'études anonymisées aux marques<br>Pas de pub | Score personnalisé moins comparable qu'un score universel<br>Base produits plus restreinte |
| **ScanUp** | Scan<br>Degré de transformation produit (Siga)<br>Nutri-Score, allergènes, labels<br>Co-création (votes consommateurs → marques) | Financée par les marques partenaires<br>Paiement à la question<br>B2B | Conflit d'intérêt potentiel (financée par les marques évaluées)<br>Vote orienté développement produit, pas notation objective |

### 2. Matrice comparative (fonctionnalités × acteurs)

*Légende : ✓ = fonctionnalité confirmée / mise en avant ; case vide = non identifiée dans nos sources (n'exclut pas une présence mineure ou non documentée).*

| Fonctionnalité | Yuka | Open Food Facts | myLabel | ScanUp | NutriScope (visé) |
|---|:---:|:---:|:---:|:---:|:---:|
| Scan code-barres | ✓ | ✓ | ✓ | ✓ | ✓ |
| Score nutritionnel unique | ✓ | ✓ | ✓ | ✓ | ✓ |
| Score environnemental | | ✓ | ✓ | | |
| Score social / éthique | | | ✓ | | |
| Personnalisation du score (profil/portions) | | | ✓ | | |
| Alertes allergènes | | ✓ | | ✓ | |
| Suggestion automatique d'alternatives | ✓ | | | | ✓ |
| Reconnaissance visuelle du produit (photo) | | | | | ✓ |
| Assistant conversationnel (chatbot) | | | | | ✓ |
| Segmentation / typologie du catalogue | | | | | ✓ |
| Accompagnement nutrition (recettes, plan) | ✓ | | | | |
| Co-création avec les marques | | | | ✓ | |
| Intégration sites marchands | | | ✓ | | |
| Extensions hors alimentaire (cosmétique, animalier) | ✓ | ✓ | | | |
| Suivi de prix | | ✓ | | | |

**Cases vides les plus significatives :**
- **Reconnaissance visuelle du produit (photo)** : vide chez les 4 concurrents. Tous reposent sur le scan de code-barres, aucun ne semble proposer une identification par image (utile par exemple pour un produit sans code-barres lisible, en vrac, ou fait maison).
- **Assistant conversationnel** : vide chez les 4. Aucun ne permet à l'utilisateur de poser une question libre ("qu'est-ce que je peux manger si je veux réduire le sucre ?") plutôt que de simplement scanner.
- **Score + alternative + personnalisation réunis dans une seule appli** : chaque concurrent couvre une partie de la grille (myLabel a la personnalisation mais pas la suggestion auto ; Yuka a la suggestion mais pas la personnalisation ni l'environnement), aucun ne cumule les trois.

### 3. Analyse rapide type SWOT de NutriScope

| | Positif | Négatif |
|---|---|---|
| **Interne** | **Forces**<br>- Combine des briques qu'aucun concurrent ne réunit : score + moteur de substitution + reconnaissance d'image + chatbot RAG<br>- S'appuie sur Open Food Facts (base ouverte, gratuite, déjà fiabilisée en partie) plutôt que de repartir de zéro<br>- Conformité (RGPD, AI Act, biais) pensée dès la conception, pas ajoutée après coup | **Faiblesses**<br>- Aucune notoriété ni base utilisateurs (vs Yuka, référence installée)<br>- Pas de modèle économique validé à ce stade<br>- Produit non testé auprès d'utilisateurs réels — pas encore de retour terrain pour valider les hypothèses|
| **Externe** | **Opportunités**<br>- Cases vides identifiées dans la matrice (reco image, chatbot, personnalisation + suggestion réunies) → différenciation claire<br>- Ancrage local (Lille / Hauts-de-France) mobilisable pour un premier marché ou des partenariats<br>- Appétence grand public déjà créée par Yuka : le marché est éduqué, pas à convaincre de l'intérêt du scan | **Menaces**<br>- Open Food Facts étant une donnée ouverte, un concurrent peut répliquer la même différenciation sur la même base<br>- Yuka en position dominante avec effet de marque fort (1,8M+ d'utilisateurs rien qu'en Belgique)<br>- Dépendance à la qualité/couverture des données Open Food Facts (catégories mal renseignées, comme vu plus tôt) |

### 4. Proposition de valeur

Pour les familles pressées, qui ont besoin d'une explication simple et claire plutôt qu'un chiffre "brut", ou d'une interface trop technique pour être manipulée simplement et rapidement, NutriScope est une application qui propose d'aller à l'essentielle : une petite explication qui résume si le produit est bon ou pas, et les alternatives associées.
Contrairement aux applications concurrentes, nous résumons le score ou nutriscore sous forme d'un texte claire, concis et rapidement compréhensible pour savoir si le produit vaut la peine d'être acheté ou non, pour sa bande de mioches