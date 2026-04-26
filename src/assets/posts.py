import requests
import pandas as pd
import json
import duckdb  
from dagster import asset, Output

@asset()
def publications_json():
    """On extrait les données du fichier json des publications depuis l'API DummyJSON"""
    
    reponse = requests.get("https://dummyjson.com/posts")

    data = reponse.json()['posts']

    with open("/opt/dagster/app/data/raw/posts.json", "w") as f:
        json.dump(data, f, indent=4)
    
    #on transforme en dataframe pour faire nos manipulations
    df = pd.DataFrame(data)

    #on regarde le résultat en sortie 
    return Output(
        value=df,
        metadata={
            "nombre_de_lignes": len(df),
            "nom_du_fichier": "data/raw/posts.json",
            "preview": df.head().to_html()
        }
    )

@asset(
    deps=["publications_json"] 
)
def table_publications():
   
    #on se connecte au fichier de base de données
    con = duckdb.connect("/opt/dagster/app/data/local_database.duckdb")
    
    query = """
    CREATE OR REPLACE TABLE posts AS (
        SELECT
	    id AS id_post,
	    userId AS id_user,
	    title,
	    body,
	    reactions
        FROM read_json_auto('data/raw/posts.json')
    );
    """
    
    con.execute(query)
    con.close()
