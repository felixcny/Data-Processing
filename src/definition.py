from dagster import Definitions, asset

@asset
def mon_premier_asset():
    """Un asset de test pour vérifier que tout marche."""
    return "Hello Data!"

defs = Definitions(
    assets=[mon_premier_asset],
)