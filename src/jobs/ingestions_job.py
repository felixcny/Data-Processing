from dagster import define_asset_job, AssetSelection

#on définit le job qui charge toutes nos données ici
chargement_tables_job = define_asset_job(
    name="chargement_tables_job",
    selection=AssetSelection.all()
)
