import requests
import pandas as pd
import json  
from dagster import asset, Output

@asset()
def paniers_json():
    """On extrait les données de la table paniers depuis l'API DummyJSON"""
    
    #l'api retourne 50 paniers. on va en récupérer 45
    #on fait une première requête pour connaître le 'total'
    requete = requests.get("https://dummyjson.com/carts?limit=1")
    total_des_paniers = requete.json().get('total')
    total_des_paniers = total_des_paniers - 5
    reponse = requests.get(f"https://dummyjson.com/carts?limit={total_des_paniers}")
    
    data = reponse.json()['carts']
    
    #on écrit dans le fichier créé
    with open("data/raw/carts.json", "w") as f:
        json.dump(data, f, indent=4)
    
    #on transforme en dataframe pour faire nos manipulations
    df = pd.DataFrame(data)

    #on regarde le résultat en sortie 
    return Output(
        value=df,
        metadata={
            "nombre_de_lignes": len(df),
            "nom_du_fichier": "data/raw/carts.json",
            "preview": df.head().to_html()
        }
    )
