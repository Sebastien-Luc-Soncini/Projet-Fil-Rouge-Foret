
import streamlit as st
import pandas as pd
from pathlib import Path
from Models.cleaning import clean_data

st.title("Nettoyage des données")
st.subheader("Exploration des données brutes")

DATA_PATH = Path(__file__).parent.parent / "Data" / "foret.csv"
df = pd.read_csv(DATA_PATH)

st.write("Aperçu des données brutes avant nettoyage :")

st.dataframe(df.head(10))

if st.button("Lancer le nettoyage"):
    df_clean = clean_data(df)

    colonnes_supprimees = list(set(df.columns) - set(df_clean.columns))

    nb_lignes_supprimees = len(df) - len(df_clean)
    pourcentage_supprime = (nb_lignes_supprimees / len(df)) * 100

    DATA_CLEAN_PATH = Path(__file__).parent.parent / "Data" / "foret_clean.csv"
    df_clean.to_csv(DATA_CLEAN_PATH, index=False)

    st.success("Nettoyage des données terminé !")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Lignes avant", len(df))
    col2.metric("Lignes après", len(df_clean))
    col3.metric("Taux de lignes supprimées", f"{pourcentage_supprime:.2f}%")
    col4.metric("Colonnes avant", len(df.columns))
    col5.metric("Colonnes après", len(df_clean.columns))

    st.subheader("Aperçu des données nettoyées")
    st.dataframe(df_clean.head(10))