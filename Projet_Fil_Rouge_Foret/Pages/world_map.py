
import streamlit as st
from Controls.data_loader import load_data
from Views.advanced_visualizations import plot_world_map

st.title("Carte mondiale de la couverture forestière")

df = load_data()

fig = plot_world_map(df)

st.plotly_chart(fig, use_container_width=True)