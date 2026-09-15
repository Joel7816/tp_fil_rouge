# Note d'hypothèses — KPI, coûts & ROI NutriScope (v2)

TP 7 · accompagne `kpi_roi_v2.xlsx` · chiffres repris du Module 2.4 (cours)

## 1. La décision demandée

Valider **71 770 €** de budget pour une v1 NutriScope, avec un modèle économique combinant abonnement premium et contrats B2B, sur les 12 premiers mois.

## 2. Payback et ROI du scénario central, en une phrase

Sur les hypothèses centrales (50 000 utilisateurs actifs, 3 % de conversion premium, 2 clients B2B), le projet est **tout juste rentable dès l'année 1** (ROI de **+ 8,4 %**).

## 3. Les trois scénarios (12 mois)

| Scénario | Hypothèses | Coûts | Revenus | ROI |
|---|---|---|---|---|
| Pessimiste | 20 000 actifs · 2 % premium · 0 B2B | 71 770 € | 14 352 € | − 80,0 % |
| Central | 50 000 actifs · 3 % premium · 2 B2B | 71 770 € | 77 820 € | + 8,4 % |
| Optimiste | 120 000 actifs · 4 % premium · 4 B2B | 71 770 € | 220 224 € | + 206,8 % |

## 4. Les hypothèses qui font tout, et comment on le saura

Valeurs reprises du cours (non recalculées sur notre propre total de coûts — cf. §6) :

- **Taux de conversion premium** (3 % central) — à ± 50 %, ROI de − 45 % à + 50 %. Vérifiable via un pilote sur 2 000 utilisateurs, 8 semaines.
- **Clients B2B signés** (2 central) — à ± 50 %, ROI de − 13 % à + 19 %. Vérifiable via trois rendez-vous distributeurs avant le jalon J4.
- **Utilisateurs actifs** (50 000 central) — à ± 50 %, ROI de − 50 % à + 55 %. Vérifiable via la courbe d'acquisition des 3 premiers mois.
- **Coût par conversation LLM** (0,012 € central) — à ± 50 %, ROI de + 6 % à 0 %. Effet secondaire, vérifiable dès la phase 5 sur mesure réelle.

Les deux premières hypothèses (conversion, B2B) pèsent le plus lourd — ce sont elles qui font basculer le scénario central de la perte au profit.

## 5. Critère d'arrêt

Si, après les 8 premières semaines de pilote, le taux de conversion premium mesuré est **inférieur à 1,5 %** (moitié de l'hypothèse centrale) **et** qu'aucun client B2B n'a signé avant le jalon J4, le scénario central n'est plus crédible : le projet repasse en arbitrage devant le sponsor avant d'engager les dépenses de run de l'année 2.

---

## 6. Détail et origine des hypothèses

### Modèle économique
Freemium **+ B2B**, repris tel quel de l'exemple travaillé du Module 2.4 (cours) — contrairement à une première version de ce dossier qui avait écarté le B2B par choix d'équipe. Cette v2 sert de référence alignée sur le cours ; le modèle définitif reste à trancher en équipe.

### Coûts (TCO année 1 = 71 770 €)
Repris des ordres de grandeur du cours, sans les ajustements qu'on avait testés dans une v1 (pas de réduction de temps de dev via l'IA, pas de tarifs fournisseurs réels recherchés — Claude/OpenAI, Scaleway/OVHcloud). Détail du coût LLM : 30 000 conversations/mois × 4 échanges × 1 500 tokens × 2 €/million de tokens × 12 mois = 4 320 €/an.

**Écart avec le cours** : le cours affiche un total arrondi de ≈ 76 000 € pour ce même détail de postes, mais la somme exacte des lignes qu'il donne (avec le calcul précis du coût LLM à 4 320 € plutôt que 4 300 € arrondis) donne 71 770 €. On a gardé la somme exacte plutôt que l'arrondi du cours, pour que le tableur reste cohérent en interne — d'où un écart de ROI avec les chiffres du cours (+ 8,4 % ici contre + 3 % dans le cours pour le scénario central).

### Revenus
Utilisateurs actifs × taux de conversion premium × 2,99 €/mois × 12 mois, **plus** clients B2B × 12 000 €/an — modèle à deux sources de revenus, repris du cours.

### KPI produit
Cibles non fixées à ce stade pour "scans par jour" et "taux d'activation", faute de mesure de baseline — à compléter avant le TP 8. Les autres KPI (rétention, substitution acceptée, coût LLM) sont indépendants du choix de scénario ci-dessus.

### Ce qui manque dans cette v2
Contrairement à une itération précédente, cette version ne comprend pas de projection à 3 ans ni de tarifs fournisseurs vérifiés (LLM, hébergement) — l'objectif ici était de reproduire fidèlement l'exemple du cours comme référence, pas de le personnaliser. Ces éléments peuvent être réintégrés dans une itération suivante si besoin.

---

*Hypothèses non vérifiées (sauf mention contraire), à confronter aux mesures réelles dès le pilote (cf. §4-5). Détail chiffré et formules dans `kpi_roi_v2.xlsx`.*
