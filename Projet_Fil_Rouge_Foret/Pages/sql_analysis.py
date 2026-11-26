
import streamlit as st
from Controls.data_loader import load_data
from Controls.sql import (
    create_database,
    get_high_density_countries,
    get_forest_by_agriculture
)

# ==========================================
# CHARGEMENT DES DONNEES ET CREATION SQL
# ==========================================

df = load_data()

connexion = create_database(df)

# on écrit un titre et paragraphe...

st.title("Analyse SQL")

st.markdown("""
Cette section permet de mettre en pratique SQL à travers quelques requêtes réalisées directement sur notre base de données. 
""")

# ==========================================
# REQUETE SQL : PAYS A FORTE DENSITE
# ==========================================

st.header("Pays à forte densité de population")

st.code("""
SELECT Country, "Density (people/km²)"
FROM forest
WHERE "Density (people/km²)" > 200
ORDER BY "Density (people/km²)" DESC;
""", language="sql")

df_density = get_high_density_countries(connexion)

st.dataframe(df_density, use_container_width=True)

# ==========================================
# REQUETE SQL : FORET PAR CATEGORIE AGRICOLE
# ==========================================

st.header("Surface forestière selon la part de terres agricoles")

st.code("""
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
""", language="sql")

df_agriculture = get_forest_by_agriculture(connexion)

st.dataframe(df_agriculture, use_container_width=True)