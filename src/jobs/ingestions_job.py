from dagster import define_asset_job, AssetSelection


maselection = AssetSelection.keys(

    "commentaires_json",
    "paniers_json",
    "produits_json",
    "publications_json",
    "recettes_json",
    "utilisateurs_json",
    
    "table_commentaires",
    "table_paniers",
    "table_produits",
    "table_publications",
    "table_recettes",
    "table_utilisateurs"
)
#on définit le job qui charge toutes nos données ici
chargement_tables_job = define_asset_job(
    name="chargement_tables_job",
    selection=maselection
)
