
import streamlit as st
from Controls.data_loader import load_data

# ==========================================
# PAGE D'ACCUEIL
# ==========================================

st.title("Projet Fil Rouge - Forêt")

st.subheader("Analyse de la couverture forestière mondiale")

st.write(
    """
    Bienvenue dans notre application dédiée à l'exploration des données sur la couverture forestière mondiale.

    Ce projet s'appuie sur un dataset regroupant différents indicateurs économiques, 
    sociaux et environnementaux pour plusieurs pays.

    Il comprend une première étape de nettoyage et de préparation des données, 
    suivie d'une analyse statistique et de visualisations interactives 
    afin d'explorer les facteurs liés à la couverture forestière.
    """
)

# ==========================================
# ILLUSTRATIONS
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.image("Assets/foret.jpg", use_container_width=True)

with col2:
    st.image("Assets/statistiques.png", use_container_width=True)

with col3:
    st.image("Assets/carte.jpg", use_container_width=True)
