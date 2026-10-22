"""Garde-fou contre la fuite de la cible."""

FORBIDDEN_FEATURES = frozenset({'nutriscore_score', 'nutriscore_grade'})

def assert_no_target_leak(input_columns) -> None:
    leaked = FORBIDDEN_FEATURES & set(input_columns)
    assert not leaked, f'Fuite de la cible : {sorted(leaked)} ne doit pas être une feature'
