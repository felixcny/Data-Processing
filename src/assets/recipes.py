import requests
import pandas as pd
import json
import duckdb  
from dagster import asset, Output

@asset()
def recettes_json():
    """On extrait les données de la table recettes depuis l'API DummyJSON"""
    
    #l'api retourne 100 recettes. on va en récupérer 95
    #on fait une première requête pour connaître le 'total'
    requete = requests.get("https://dummyjson.com/recipes?limit=1")
    total_des_recettes = requete.json().get('total')
    total_des_recettes = total_des_recettes - 5
    reponse = requests.get(f"https://dummyjson.com/recipes?limit={total_des_recettes}")
    
    #mais cela nous renvoie 45 recettes
    data = reponse.json()['recipes']
    
    #on écrit dans le fichier créé
    with open("/opt/dagster/app/data/raw/recipes.json", "w") as f:
        json.dump(data, f, indent=4)
    
    #on transforme en dataframe pour faire nos manipulations
    df = pd.DataFrame(data)

    #on regarde le résultat en sortie 
    return Output(
        value=df,
        metadata={
            "nombre_de_lignes": len(df),
            "nom_du_fichier": "data/raw/recipes.json",
            "preview": df.head().to_html()
        }
    )

@asset(
    deps=["recettes_json"] 
)

def table_recettes():
   
    #on se connecte au fichier de base de données
    con = duckdb.connect("/opt/dagster/app/data/local_database.duckdb")
    
    query = """
    CREATE OR REPLACE TABLE recipes AS (
        SELECT
	    id AS id_recipe,
	    name,
	    ingredients,
	    instructions,
	    difficulty,
	    userID AS id_user,
	    rating
        FROM read_json_auto('data/raw/recipes.json')
    );
    """
    
    con.execute(query)
    con.close()
