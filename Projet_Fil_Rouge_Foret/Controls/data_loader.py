
from pathlib import Path
import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent.parent / "Data" / "foret_clean.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


# on charge foret_clean.csv parce que nos pages d'analyse ont besoin de données nettoyées