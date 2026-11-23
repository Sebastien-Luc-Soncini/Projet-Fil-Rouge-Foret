import streamlit as st
from Controls.data_loader import load_data
from Models.analysis import analyse_statistique
from Views.visualizations import plot_top_10_forest, plot_bottom_10_forest

st.title("Analyse statistique")

df = load_data()

st.subheader("Statistiques descriptives")

resultats = analyse_statistique(df)

statistiques = resultats["statistiques_foret"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Moyenne", f"{statistiques['mean']:.2f} %")
col2.metric("Médiane", f"{statistiques['50%']:.2f} %")
col3.metric("Écart-type", f"{statistiques['std']:.2f}")
col4.metric("Maximum", f"{statistiques['max']:.2f} %")

st.subheader("Les 10 pays ayant la plus forte couverture forestière")

st.write(resultats["top_10_foret"])

fig = plot_top_10_forest(df)
st.pyplot(fig)

st.subheader("Les 10 pays ayant la plus faible couverture forestière")

st.write(resultats["bottom_10_foret"])

fig = plot_bottom_10_forest(df)
st.pyplot(fig)