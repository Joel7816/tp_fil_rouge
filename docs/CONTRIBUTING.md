# CONTRIBUTING.md — NutriScope

Conventions d'équipe pour ce dépôt. À ajuster ensemble si un point ne convient pas — l'objectif
est d'avoir une règle simple et suivie, pas une procédure lourde.

## Format des messages de commit

Convention adoptée : commits conventionnels (`type(scope): description`).

Types utilisés :

- `feat` — nouvelle fonctionnalité
- `fix` — correction de bug
- `docs` — documentation uniquement (README, `docs/`, `CONTRIBUTING.md`...)
- `refactor` — changement de code sans changement de comportement
- `test` — ajout ou modification de tests
- `chore` — tâches diverses (dépendances, configuration, nettoyage...)

Exemples, basés sur ce qu'on a déjà fait sur ce projet :

```
feat(profiling): ajoute l'analyse des rayons candidats
fix(nutriments): corrige l'extraction des unités déclarées
docs(perimetre): met à jour le seuil de complétude après révision des rayons
```

Règles :

- Description à l'impératif, en français, concise (idéalement moins de 72 caractères sur la
  première ligne)
- Un commit = un changement logique cohérent — éviter de mélanger plusieurs sujets dans un seul
  commit (ça complique un `git revert` ciblé si besoin plus tard)

## Taille des Pull Requests

- Une PR = une fonctionnalité ou un correctif, pas un mélange de plusieurs sujets
- Cible indicative : rester sous ~400 lignes modifiées quand c'est possible ; au-delà, se
  demander si la PR peut être découpée en plusieurs
- Une PR doit rester relisable en 20-30 minutes par l'autre membre de l'équipe — si ce n'est
  pas le cas, c'est probablement le signe qu'elle est trop grosse
- Ne pas inclure de nettoyage ou de refactor "en passant" sur du code sans rapport avec le sujet
  de la PR — ouvrir une PR séparée (`refactor`/`chore`) si besoin

## Qui relit quoi

Équipe de 2 personnes : chaque Pull Request est relue et approuvée par l'autre membre de
l'équipe avant fusion — cohérent avec la règle de protection GitHub ("Require approvals: 1")
configurée sur `main`. Pas de répartition par zone de responsabilité pour l'instant, la revue
croisée systématique suffit à cette taille d'équipe.

## Flux de travail associé

Rappel du flux de branches (voir aussi `docs/perimetre.md` pour les décisions liées aux données) :

1. Créer une branche `feat/nom-de-la-fonctionnalite` à partir de `dev`
2. Committer en suivant la convention ci-dessus
3. Ouvrir une Pull Request vers `dev`
4. Attendre l'approbation de l'autre membre de l'équipe avant de fusionner
5. `dev` est périodiquement fusionnée vers `main` une fois stable (release)
