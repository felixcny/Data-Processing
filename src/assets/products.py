import requests
import pandas as pd
import json
import duckdb  
from dagster import asset, Output

@asset()
def produits_json():
    """On extrait les données de la table product depuis l'API DummyJSON"""
    
    #l'api retourne 194 produits. on veut récupérer tous les produits
    #on fait une première requête pour connaître le 'total'
    requete = requests.get("https://dummyjson.com/products?limit=1")
    total_des_produits = requete.json().get('total')
    reponse = requests.get(f"https://dummyjson.com/products?limit={total_des_produits}")

    data = reponse.json()['products']
    
    #on écrit dans le fichier créé
    with open("data/raw/products.json", "w") as f:
        json.dump(data, f, indent=4)
    
    #on transforme en dataframe pour faire nos manipulations
    df = pd.DataFrame(data)

    #on regarde le résultat en sortie 
    return Output(
        value=df,
        metadata={
            "nombre_de_lignes": len(df),
            "nom_du_fichier": "data/raw/products.json",
            "preview": df.head().to_html()
        }
    )

@asset(
    deps=["products_json"] 
)
def table_produits():
   
    #on se connecte au fichier de base de données
    con = duckdb.connect("data/local_database.duckdb")
    
    query = """
    CREATE OR REPLACE TABLE products AS (
        SELECT
	    id AS id_product,
	    title,
	    description,
	    category,
	    price,
	    discountPercentage AS discount_percentage,
	    rating,
	    stock,
	    reviews,   -- on juge important
	    availabilityStatus AS availability_status -- on juge important à garder
        FROM read_json_auto('data/raw/products.json')
    );
    """
    
    con.execute(query)
    con.close()
