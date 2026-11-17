# script testé et validé !


import sqlite3
import pandas as pd
from pathlib import Path


# ==================================================
# CHEMIN DE LA BASE DE DONNEES
# ==================================================

# On remonte de Controls vers le dossier principal
dossier_projet = Path(__file__).resolve().parent.parent

# La base SQLite sera stockée dans Data
chemin_db = dossier_projet / "Data" / "foret.db"


# ==================================================
# 1. CREATION DE LA BASE DE DONNEES
# ==================================================

def create_database(df):

    connexion = sqlite3.connect(chemin_db)

    # Transfert du DataFrame Pandas vers une table SQL
    df.to_sql("forest", connexion, if_exists="replace", index=False)

    return connexion


# ==================================================
# 2. EXECUTION DES REQUETES SQL
# ==================================================

def execute_query(connexion, requete):

    # Execution de la requete SQL
    resultat = pd.read_sql_query(requete, connexion)

    return resultat


# ==================================================
# 3. REQUETE 1 : LES 10 PAYS LES PLUS FORESTIERS
# ==================================================

def get_top_forest_countries(connexion):

    requete = """
    SELECT Country, "Forested Area (%)"
    FROM forest
    ORDER BY "Forested Area (%)" DESC
    LIMIT 10;
    """

    return execute_query(connexion, requete)


# ==================================================
# 4. REQUETE 2 : PAYS AVEC UNE FORTE DENSITE
# ==================================================

def get_high_density_countries(connexion):

    requete = """
    SELECT Country, "Density (people/km²)"
    FROM forest
    WHERE "Density (people/km²)" > 200
    ORDER BY "Density (people/km²)" DESC;
    """

    return execute_query(connexion, requete)


# ==================================================
# 5. REQUETE 3 : MOYENNE DE SURFACE FORESTIERE
# ==================================================

def get_average_forest_area(connexion):

    requete = """
    SELECT AVG("Forested Area (%)") AS moyenne_foret
    FROM forest;
    """

    return execute_query(connexion, requete)


# ==================================================
# 6. REQUETE 4 : SURFACE FORESTIERE PAR CATEGORIE
# ==================================================

def get_forest_by_agriculture(connexion):

    requete = """
    SELECT
        CASE
            WHEN "Agricultural Land (%)" <= 20 THEN '0-20'
            WHEN "Agricultural Land (%)" <= 40 THEN '20-40'
            WHEN "Agricultural Land (%)" <= 60 THEN '40-60'
            WHEN "Agricultural Land (%)" <= 80 THEN '60-80'
            ELSE '>80'
        END AS categorie_agriculture,

        COUNT(*) AS nombre_pays,

        ROUND(AVG("Forested Area (%)"), 2) AS moyenne_foret

    FROM forest

    GROUP BY categorie_agriculture
    ORDER BY categorie_agriculture;
    """

    return execute_query(connexion, requete)
