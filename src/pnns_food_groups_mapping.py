"""Correspondances entre les colonnes pnns_groups_* et food_groups_tags (Open Food Facts).

Mappings établis en comparant le CSV et le Parquet, jointure sur `code`.
"""

from typing import Final

# pnns_groups_1 -> tag de niveau 1 de food_groups_tags.
# "unknown" et les valeurs vides n'ont volontairement pas de tag.
# Concordance mesurée : ~98,5 % des produits classés.
PNNS1_TO_FOOD_GROUP_TAG: Final[dict[str, str]] = {
    "Alcoholic beverages": "en:alcoholic-beverages",
    "Baby foods": "en:baby-foods-and-milks",
    "Beverages": "en:beverages",
    "Cereals and potatoes": "en:cereals-and-potatoes",
    "Composite foods": "en:composite-foods",
    "Fat and sauces": "en:fats-and-sauces",
    "Fish Meat Eggs": "en:fish-meat-eggs",
    "Fruits and vegetables": "en:fruits-and-vegetables",
    "Milk and dairy products": "en:milk-and-dairy-products",
    "Salty snacks": "en:salty-snacks",
    "Sugary snacks": "en:sugary-snacks",
}

# pnns_groups_2 -> ensemble de tags acceptables dans food_groups_tags.
# Le tag peut être à n'importe quelle profondeur de la liste (ex. "Alcoholic
# beverages" est au niveau 1), donc on teste l'appartenance, pas une position.
PNNS2_TO_FOOD_GROUP_TAGS: Final[dict[str, frozenset[str]]] = {
    "Alcoholic beverages": frozenset({"en:alcoholic-beverages"}),
    "Appetizers": frozenset({"en:appetizers"}),
    "Baby foods": frozenset({"en:baby-foods"}),
    "Baby milks": frozenset({"en:baby-milks"}),
    "Biscuits and cakes": frozenset({"en:biscuits-and-cakes"}),
    "Bread": frozenset({"en:bread"}),
    "Breakfast cereals": frozenset({"en:breakfast-cereals"}),
    "Cereals": frozenset({"en:cereals"}),
    "Cheese": frozenset({"en:cheese"}),
    "Chocolate products": frozenset({"en:chocolate-products"}),
    "Dairy desserts": frozenset({"en:dairy-desserts"}),
    "Dressings and sauces": frozenset({"en:dressings-and-sauces"}),
    "Dried fruits": frozenset({"en:dried-fruits"}),
    "Eggs": frozenset({"en:eggs"}),
    "Fats": frozenset({"en:fats"}),
    "Fish and seafood": frozenset({"en:fish-and-seafood"}),
    "Fruits": frozenset({"en:fruits"}),
    "Ice cream": frozenset({"en:ice-cream"}),
    "Legumes": frozenset({"en:legumes"}),
    "Meat": frozenset({"en:meat"}),
    "Milk and yogurt": frozenset({"en:milk-and-yogurt"}),
    "Nuts": frozenset({"en:nuts"}),
    "Offals": frozenset({"en:offals"}),
    "One-dish meals": frozenset({"en:one-dish-meals"}),
    "Pastries": frozenset({"en:pastries"}),
    "Pizza pies and quiches": frozenset({"en:pizza-pies-and-quiches"}),
    "Plant-based milk substitutes": frozenset({"en:plant-based-milk-substitutes"}),
    "Potatoes": frozenset({"en:potatoes"}),
    "Processed meat": frozenset({"en:processed-meat"}),
    "Salty and fatty products": frozenset({"en:salty-and-fatty-products"}),
    "Sandwiches": frozenset({"en:sandwiches"}),
    "Soups": frozenset({"en:soups"}),
    "Sweetened beverages": frozenset({"en:sweetened-beverages"}),
    "Sweets": frozenset({"en:sweets"}),
    "Unsweetened beverages": frozenset({"en:unsweetened-beverages"}),
    "Vegetables": frozenset({"en:vegetables"}),
    # Boissons : food_groups_tags classe aussi selon la teneur en sucre, donc le
    # tag précis peut être remplacé par un tag frère (sucré / non sucré).
    "Artificially sweetened beverages": frozenset(
        {"en:artificially-sweetened-beverages", "en:sweetened-beverages"}
    ),
    "Fruit juices": frozenset({"en:fruit-juices", "en:unsweetened-beverages"}),
    "Fruit nectars": frozenset({"en:fruit-nectars", "en:unsweetened-beverages"}),
    "Teas and herbal teas and coffees": frozenset(
        {"en:teas-and-herbal-teas-and-coffees", "en:unsweetened-beverages"}
    ),
    "Waters and flavored waters": frozenset(
        {"en:waters-and-flavored-waters", "en:unsweetened-beverages"}
    ),
}