
import streamlit as st

st.set_page_config(
    page_title="Projet Fil Rouge - Forêt",
    layout="wide"
)

home_page = st.Page(
    "Pages/home.py",
    title="Accueil",
    icon=":material/home:",
    default=True
)

data_cleaning_page = st.Page(
    "Pages/data_cleaning.py",
    title="Nettoyage des données",
    icon=":material/database:"
)

statistical_page = st.Page(
    "Pages/statistical_analysis.py",
    title="Analyse statistique",
    icon=":material/analytics:"
)

exploration_page = st.Page(
    "Pages/exploration.py",
    title="Analyse exploratoire",
    icon=":material/travel_explore:"
)

sql_page = st.Page(
    "Pages/sql_analysis.py",
    title="Analyse SQL",
    icon=":material/query_stats:"
)

world_map_page = st.Page(
    "Pages/world_map.py",
    title="Carte mondiale",
    icon=":material/public:"
)

navigation = st.navigation([
    home_page,
    data_cleaning_page,
    statistical_page,
    exploration_page,
    sql_page,
    world_map_page
])

navigation.run()