import requests
import pandas as pd
import json
import duckdb  
from dagster import asset, Output

@asset()
def utilisateurs_json():
    """On extrait les données de la table des users depuis l'API DummyJSON"""
    
    reponse = requests.get("https://dummyjson.com/users?limit=150")

    data = reponse.json()['users']

    with open("data/raw/users.json", "w") as f:
        json.dump(data, f, indent=4)
    
    #on transforme en dataframe pour faire nos manipulations
    df = pd.DataFrame(data)

    #on regarde le résultat en sortie 
    return Output(
        value=df,
        metadata={
            "nombre_de_lignes": len(df),
            "nom_du_fichier": "data/raw/users.json",
            "preview": df.head().to_html()
        }
    )

@asset(
    deps=["users_json"] 
)
def table_utilisateurs():
   
    #on se connecte au fichier de base de données
    con = duckdb.connect("data/local_database.duckdb")
    
    query = """
    CREATE OR REPLACE TABLE users AS (
        SELECT
	    id AS id_user,
	    firstName,
	    lastName,
	    gender,
	    birthDate,
	    address,
	    role 
        FROM read_json_auto('data/raw/users.json')
    );
    """
    
    con.execute(query)
    con.close()
