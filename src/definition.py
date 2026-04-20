from dagster import Definitions, load_assets_from_package_module, in_process_executor
from src import assets  #on importe le dossier assets
from src.jobs.ingestions_job import chargement_tables_job    #on importe le dossier jobs

# on charge tous les assets qui sont dans notre dossier src/assets/
tous_les_assets = load_assets_from_package_module(assets)


defs = Definitions(
    assets=tous_les_assets,
    jobs=[chargement_tables_job],
    executor=in_process_executor #eviter les crash
)

