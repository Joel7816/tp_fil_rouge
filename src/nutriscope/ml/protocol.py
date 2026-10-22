"""Protocole d'évaluation unique : mêmes plis, mêmes métriques pour tous les modèles."""

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42
CROSS_VALIDATION = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=RANDOM_STATE,
)
SCORING = [
    'f1_macro',
    'accuracy',
    'balanced_accuracy',
]

def evaluate_cross_validation(
    pipeline: Pipeline,
    X,
    y,
    nom: str,
) -> dict[str, float | str]:
    """Évalue un pipeline en validation croisée (moyenne et écart-type par métrique)."""
    scores = cross_validate(
        pipeline,
        X,
        y,
        cv=CROSS_VALIDATION,
        scoring=SCORING,
        n_jobs=-1,
    )

    resume: dict[str, float | str] = {'modele': nom}

    for metric in SCORING:
        values = scores[f'test_{metric}']
        resume[f'{metric}_moy'] = values.mean()
        resume[f'{metric}_std'] = values.std()

    resume['fit_time_moy'] = scores['fit_time'].mean()
    resume['score_time_moy'] = scores['score_time'].mean()
    return resume
