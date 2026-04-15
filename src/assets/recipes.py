import requests
import pandas as pd
import json  
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
    with open("data/raw/recipes.json", "w") as f:
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

