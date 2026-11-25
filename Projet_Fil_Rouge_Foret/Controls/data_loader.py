
from pathlib import Path
import pandas as pd
import streamlit as st

# ==========================================
# CHEMINS DES DONNÉES
# ==========================================

DATA_PATH = Path(__file__).parent.parent / "Data" / "foret_clean.csv"
RAW_DATA_PATH = Path(__file__).parent.parent / "Data" / "foret.csv"


# ==========================================
# CHARGEMENT DES DONNÉES NETTOYÉES
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


# ==========================================
# CHARGEMENT DES DONNÉES BRUTES
# ==========================================

@st.cache_data
def load_raw_data():
    df = pd.read_csv(RAW_DATA_PATH)
    return df


# on charge foret_clean.csv parce que nos pages d'analyse ont besoin de données nettoyées