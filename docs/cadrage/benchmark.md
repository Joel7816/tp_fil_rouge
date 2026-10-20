# TP 6 - Opportunité & concurrence

## Objectif : Situer NutriScope sur son marché et formuler sa proposition de valeur

### 1. Benchmark des applications existantes

| Application | Fonctionnalités | Modèle économique | Points faibles |
|---|---|---|---|
| **Yuka** | Scan alimentaire<br>Note /100 (nutrition 60 %, additifs 30 %, bio 10 %)<br>Suggestions d'alternatives<br>Programme nutrition payant | Gratuit<br>~50 % programme payant (59 €)<br>~50 % dons<br>Vente produits dérivés | Pondération additifs/bio contestée (Pr Hercberg)<br>Effet culpabilisant sans alternative accessible |
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
| Accompagnement nutrition (recettes, plan) | ✓ | | | | |
| Co-création avec les marques | | | | ✓ | |
| Intégration sites marchands | | | ✓ | | |
| Suivi de prix | | ✓ | | | |

**Cases vides les plus significatives :**
- **Reconnaissance visuelle du produit (photo)** : vide chez les 4 concurrents. Tous reposent sur le scan de code-barres, aucun ne propose d'identification par image (utile pour un produit sans code-barres lisible, en vrac, ou fait maison).
- **Assistant conversationnel** : vide chez les 4. Aucun ne permet à l'utilisateur de poser une question libre ("qu'est-ce que je peux manger si je veux réduire le sucre ?") plutôt que de simplement scanner.
- **Score + alternative + personnalisation réunis dans une seule appli** : chaque concurrent couvre une partie de la grille (myLabel a la personnalisation mais pas la suggestion auto ; Yuka a la suggestion mais pas la personnalisation ni l'environnement) ; aucun ne cumule les trois.

### 3. Analyse rapide type SWOT de NutriScope

| | Positif | Négatif |
|---|---|---|
| **Interne** | **Forces**<br>- Ajoute reconnaissance d'image et chatbot conversationnel — absents des 4 concurrents — par-dessus une base score + suggestion d'alternative déjà validée par le marché via Yuka<br>- S'appuie sur Open Food Facts (base ouverte, gratuite, déjà fiabilisée en partie) plutôt que de repartir de zéro<br>- Conformité (RGPD, AI Act, biais) pensée dès la conception, pas ajoutée après coup<br>- Scope resserré et assumé dès le départ (refus explicite du conseil médical), ce qui évite la dilution des concurrents généralistes | **Faiblesses**<br>- Aucune notoriété ni base utilisateurs (vs Yuka, référence installée)<br>- Pas de modèle économique validé à ce stade<br>- Produit non testé auprès d'utilisateurs réels — pas encore de retour terrain pour valider les hypothèses<br>- Équipe data réduite, budget MVP plafonné à 120 000 € — peu de marge pour itérer largement |
| **Externe** | **Opportunités**<br>- Cases vides identifiées dans la matrice (reco image, chatbot, personnalisation + suggestion réunies) → différenciation claire<br>- Ancrage local (Lille / Hauts-de-France) mobilisable pour un premier marché ou des partenariats<br>- Appétence grand public déjà créée par Yuka : le marché est éduqué, pas à convaincre de l'intérêt du scan<br>- Positionnement inoccupé entre trois familles d'acteurs : apps de scan jugées trop simplistes (Yuka), sites nutritionnels jugés trop techniques, assistants conversationnels généralistes jugés peu fiables — NutriScope vise l'entre-deux | **Menaces**<br>- Open Food Facts étant une donnée ouverte, un concurrent peut répliquer la même différenciation sur la même base<br>- Yuka en position dominante avec effet de marque fort (1,8M+ d'utilisateurs rien qu'en Belgique)<br>- Dépendance à la qualité/couverture des données Open Food Facts (catégories mal renseignées, comme vu plus tôt)<br>- Risque réputationnel majeur en cas de recommandation inadaptée à une personne allergique ou diabétique (identifié par la direction comme la priorité n°1 à éviter) |

### 4. Proposition de valeur

**Phrase testable :**

Pour les familles pressées qui font leurs courses sur smartphone et trouvent les scores nutritionnels illisibles sans y passer du temps, NutriScope traduit la qualité d'un produit en une explication courte et compréhensible, sans jargon ni diagnostic médical, avec une alternative immédiate — hypothèse validée si au moins 70 % des utilisateurs test comprennent la recommandation sans aide et déclarent qu'elle a influencé leur choix en rayon.

**Paragraphe :**

Pour les familles pressées, qui veulent une réponse simple en quelques secondes plutôt qu'un chiffre à interpréter, NutriScope se positionne entre les applications de scan jugées trop simplistes, les sites nutritionnels jugés trop techniques, et les assistants conversationnels généralistes jugés peu fiables sur le sujet. NutriScope explique la qualité d'un produit en langage clair, propose une alternative directement exploitable, et s'arrête volontairement là où commence le conseil médical — pas de diagnostic, pas de prescription, une transparence assumée sur les sources et les limites des données (Open Food Facts).

### 5. Pitch (3 minutes) — script de présentation

*Notes pour l'oral devant le groupe ; le vote consultatif se fait en direct en séance, rien à committer pour ce point.*

**0:00 – 0:30 — Le problème et la vision**
"Qui ici a déjà scanné un produit avec Yuka, vu un score, et n'a toujours pas su s'il devait l'acheter ou reposer le paquet ? La direction de NutriScope résume bien l'ambition : devenir le réflexe simple et fiable qui aide chacun à faire un meilleur choix alimentaire en quelques secondes, sans avoir besoin de comprendre une étiquette compliquée."

**0:30 – 1:15 — Le benchmark en une phrase**
"On a comparé Yuka, Open Food Facts, myLabel et ScanUp. Chacun fait bien une chose : Yuka score et suggère, Open Food Facts est transparent et gratuit, myLabel personnalise, ScanUp évalue la transformation. Mais aucun ne réunit score, personnalisation, suggestion et reconnaissance visuelle du produit dans une seule appli — et aucun ne répond en langage courant à une vraie question posée librement."

**1:15 – 2:00 — Le positionnement et la proposition de valeur**
"NutriScope se place volontairement entre trois familles d'acteurs : les apps de scan, trop simplistes ; les sites nutritionnels, trop techniques ; les assistants conversationnels généralistes, pas assez fiables sur le sujet. Concrètement, ça veut dire : une explication simple — bon ou pas bon, et pourquoi — avec une alternative immédiate, sans jamais franchir la ligne du conseil médical. Pas un chiffre à interpréter : une réponse, pour une famille pressée qui fait ses courses sur son téléphone."

**2:00 – 2:40 — Pourquoi maintenant, pourquoi nous**
"Le marché est déjà éduqué par Yuka — les gens savent déjà scanner, on n'a pas à les convaincre de l'usage. Notre différenciation s'appuie sur des cases vides réelles du marché, pas une hypothèse en l'air. Et on pense conformité RGPD, biais et refus du conseil médical dès le départ, pas après coup — c'est ce qui nous protège du risque numéro un identifié par la direction : une recommandation dangereuse pour une personne allergique ou diabétique."

**2:40 – 3:00 — Conclusion**
"Notre pari : une famille presse un bouton, obtient une réponse en une phrase, et une alternative sous la main — sans jamais qu'on prétende être un médecin. Simple à dire, mais personne ne le fait encore complètement, entre le scan brut et le site trop technique. C'est notre créneau."