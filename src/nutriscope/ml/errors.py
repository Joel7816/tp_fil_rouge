import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score

GRAVITY_NAMES = {
    1: 'un cran',
    2: 'deux crans',
    3: 'trois crans ou plus',
}

def build_results(
    y_true,
    y_predicted,
):
    results = pd.DataFrame(
        {
            'reel': y_true,
            'predit': y_predicted,
        },
        index=y_true.index,
    )

    results['ecart'] = (results['reel'] - results['predit']).abs()

    return results

def confusion_by_row(
    results,
    labels,
):
    matrix = confusion_matrix(
        results['reel'],
        results['predit'],
        normalize='true',
    )

    table = pd.DataFrame(matrix, index=labels, columns=labels)

    return table.rename_axis(index='réel', columns='prédit')

def top_error_pairs(
    results,
    labels,
    top=5,
):
    errors = results[results['reel'] != results['predit']]
    pairs = (
        errors.groupby(['reel', 'predit'])
        .size()
        .sort_values(ascending=False)
        .head(top)
        .rename('effectif')
        .reset_index()
    )

    pairs['réel'] = pairs['reel'].map(lambda index: labels[index])
    pairs['prédit'] = pairs['predit'].map(lambda index: labels[index])
    pairs['part des erreurs'] = (pairs['effectif'] / len(errors)).round(3)

    return pairs[['réel', 'prédit', 'effectif', 'part des erreurs']]


def error_gravity(results):
    errors = results[results['reel'] != results['predit']]

    gravity = (
        errors['ecart']
        .clip(upper=3)
        .map(GRAVITY_NAMES)
        .value_counts()
        .reindex(list(GRAVITY_NAMES.values()))
        .fillna(0)
        .astype(int)
        .to_frame('effectif')
    )

    gravity['part des erreurs'] = (gravity['effectif'] / len(errors)).round(3)

    return gravity


def performance_by_group(
    results,
    groups,
):
    rows = []

    for name, group in results.groupby(groups):
        rows.append({
            'rayon': name,
            'effectif': len(group),
            'accuracy': (group['reel'] == group['predit']).mean(),
            'f1_macro': f1_score(group['reel'], group['predit'], average='macro'),
        })
        
    return pd.DataFrame(rows).set_index('rayon').sort_values('accuracy')