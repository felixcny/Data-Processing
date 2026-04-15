from dagster import Definitions, load_assets_from_package_module, AssetSelection
from src import assets  #on importe le dossier asset

# on charge tous les assets qui sont dans notre dossier src/assets/
tous_les_assets = load_assets_from_package_module(assets)

#on fait pareil pour le job
chargement_tables_job = define_asset_job(
    name="chargement_tables_job",
    selection=AssetSelection.all() #on prend tous nos assets
)

defs = Definitions(
    assets=tous_les_assets,
    jobs=[chargement_tables_job]
)

