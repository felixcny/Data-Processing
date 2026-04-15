import requests
import pandas as pd
import json  
from dagster import asset, Output

@asset()
def users_json():
    """On extrait les données de la table des users depuis l'API DummyJSON"""
    
    response = requests.get("https://dummyjson.com/users?limit=150")

    data = response.json()['users']

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
