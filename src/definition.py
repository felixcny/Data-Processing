import os
from dagster import Definitions, load_assets_from_package_module, define_asset_job, AssetSelection, in_process_executor
from dagster_dbt import DbtCliResource, dbt_assets


DBT_PROJECT_DIR = "/opt/dagster/app/dbt_project"
MANIFEST_PATH = os.path.join(DBT_PROJECT_DIR, "target/manifest.json")


from src import assets 
from src.jobs.ingestions_job import chargement_tables_job 
from src.schedules.planning_jour import planning_jour

# chargements assets dbt
@dbt_assets(manifest=MANIFEST_PATH)
def mes_assets_dbt(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

    for event in dbt_run.stream():
        # ajout de logs détaillés
        if "error" in str(event):
            context.log.error(f"Erreur détectée dans dbt : {event}")
        yield event

dbt_job = define_asset_job(
    name="dbt_job",
    selection=AssetSelection.assets(mes_assets_dbt)
)

dbt_test_job = define_asset_job(
    name="dbt_test_job",
    selection=AssetSelection.all_asset_checks()
)

job_complet_quotidien = define_asset_job(
    name="job_complet_quotidien",
    selection=AssetSelection.all()
)

defs = Definitions(
    assets=[*load_assets_from_package_module(assets), mes_assets_dbt], 
    jobs=[chargement_tables_job, dbt_job, dbt_test_job, job_complet_quotidien],
    schedules=[planning_jour],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR)
    },
    executor=in_process_executor
)
