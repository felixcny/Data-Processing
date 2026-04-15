from dagster import Definitions, load_assets_from_package_module
from src import assets  #on importe le dossier asset

# on charge tous les assets qui sont dans notre dossier src/assets/
tous_les_assets = load_assets_from_package_module(assets)

defs = Definitions(
    assets=tous_les_assets,
)
