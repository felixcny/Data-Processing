from dagster import Definitions, load_assets_from_package_module, AssetChecksDefinition, in_process_executor
from src import assets 
from src.jobs.ingestions_job import chargement_tables_job 
from src.schedules.planning_jour import planning_jour

# On charge tout le dossier assets
tous_les_assets = load_assets_from_package_module(assets)

defs = Definitions(
    assets=tous_les_assets, 
    jobs=[chargement_tables_job],
    schedules=[planning_jour],
    executor=in_process_executor
)
