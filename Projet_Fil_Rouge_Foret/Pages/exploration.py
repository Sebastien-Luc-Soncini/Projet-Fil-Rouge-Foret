
import streamlit as st
from Controls.data_loader import load_data
from Models.analysis import analyse_correlations
from Models.analysis import analyse_agriculture
from Views.visualizations import plot_agriculture_forest
from Models.analysis import analyse_densite
from Views.advanced_visualizations import plot_density_scatter, plot_density_scatter_filtered
from Views.visualizations import plot_correlation_matrix
from Models.advanced_analysis import calculer_pib_par_habitant
from Views.advanced_visualizations import plot_gdp_forest
from Models.advanced_analysis import calculer_residus_agriculture_foret
from Views.advanced_visualizations import plot_residuals
from Models.advanced_analysis import calculer_distribution_foret
from Views.advanced_visualizations import plot_forest_distribution
from Views.advanced_visualizations import plot_world_map

st.title("Exploration des données")

df = load_data()

st.subheader("Corrélations avec la couverture forestière")

correlations = analyse_correlations(df)

st.dataframe(correlations)

st.subheader("Agriculture et couverture forestière")

agriculture = analyse_agriculture(df)

st.write(agriculture)

fig = plot_agriculture_forest(df)
st.pyplot(fig)

st.subheader("Densité de population et couverture forestière")

densite = analyse_densite(df)

fig = plot_density_scatter(df)
st.pyplot(fig)

fig = plot_density_scatter_filtered(df)
st.pyplot(fig)

fig = plot_correlation_matrix(df)
st.pyplot(fig)

st.subheader("PIB par habitant et couverture forestière")

pib = calculer_pib_par_habitant(df)

fig = plot_gdp_forest(df)
st.pyplot(fig)

st.subheader("Résidus : agriculture et couverture forestière")

residus = calculer_residus_agriculture_foret(df)

fig = plot_residuals(df)
st.pyplot(fig)

st.subheader("Distribution de la couverture forestière")

distribution = calculer_distribution_foret(df)

fig = plot_forest_distribution(df)
st.pyplot(fig)

st.subheader("Carte mondiale de la couverture forestière")

fig = plot_world_map(df)
st.plotly_chart(fig)