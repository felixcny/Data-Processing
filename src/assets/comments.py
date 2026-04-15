import requests
import pandas as pd
import json
import duckdb  
from dagster import asset, Output

@asset()
def commentaires_json():
    """On extrait les données du fichier des commentaires depuis l'API DummyJSON"""
    
    reponse = requests.get("https://dummyjson.com/comments")

    data = reponse.json()['comments']

    with open("data/raw/comments.json", "w") as f:
        json.dump(data, f, indent=4)
    
    #on transforme en dataframe pour faire nos manipulations
    df = pd.DataFrame(data)

    #on regarde le résultat en sortie 
    return Output(
        value=df,
        metadata={
            "nombre_de_lignes": len(df),
            "nom_du_fichier": "data/raw/comments.json",
            "preview": df.head().to_html()
        }
    )
