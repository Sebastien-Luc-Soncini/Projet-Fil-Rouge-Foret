# script testé et validé !

import pandas as pd


# --------------------------------------------------
# 1. ANALYSES STATISTIQUES
# --------------------------------------------------

def analyse_statistique(df):

    # Statistiques générales de toutes les colonnes
    statistiques_generales = df.describe()

    # Statistiques spécifiques à la surface forestière
    statistiques_foret = df["Forested Area (%)"].describe()

    # Les 10 pays avec le plus de surface forestière
    top_10_foret = df.loc[
        df["Forested Area (%)"].nlargest(10).index,
        ["Country", "Forested Area (%)"]
    ]

    # Les 10 pays avec le moins de surface forestière
    bottom_10_foret = df.loc[
        df["Forested Area (%)"].nsmallest(10).index,
        ["Country", "Forested Area (%)"]
    ]

    return {
        "statistiques_generales": statistiques_generales,
        "statistiques_foret": statistiques_foret,
        "top_10_foret": top_10_foret,
        "bottom_10_foret": bottom_10_foret
    }


# --------------------------------------------------
# 2. ANALYSES DES CORRELATIONS
# --------------------------------------------------

def analyse_correlations(df):

    # Corrélations entre la surface forestière
    # et les autres variables numériques
    correlations_foret = (
        df.corr(numeric_only=True)["Forested Area (%)"]
        .sort_values(ascending=False)
    )

    return correlations_foret


# --------------------------------------------------
# 3. ANALYSE DES TERRES AGRICOLES
# --------------------------------------------------

def analyse_agriculture(df):

    # Création de catégories selon la part
    # des terres agricoles
    df["Agriculture_categorie"] = pd.cut(
        df["Agricultural Land (%)"],
        bins=[0, 20, 40, 60, 80, float("inf")],
        labels=["0-20", "20-40", "40-60", "60-80", ">80"]
    )

    # Nombre de pays dans chaque catégorie
    nombre_pays = (
        df["Agriculture_categorie"]
        .value_counts()
        .sort_index()
    )

    # Médiane de la surface forestière
    # pour chaque catégorie agricole
    medianes_foret = (
        df.groupby("Agriculture_categorie", observed=True)
        ["Forested Area (%)"]
        .median()
    )

    # Aperçu de la nouvelle colonne
    apercu_categories = df[
        ["Country", "Agricultural Land (%)", "Agriculture_categorie"]
    ].head(10)

    return {
        "nombre_pays": nombre_pays,
        "medianes_foret": medianes_foret,
        "apercu_categories": apercu_categories
    }


# --------------------------------------------------
# 4. ANALYSE DE LA DENSITE DE POPULATION
# --------------------------------------------------

def analyse_densite(df):

    # Corrélation entre densité de population
    # et surface forestière
    correlation_densite = df["Density (people/km²)"].corr(
        df["Forested Area (%)"]
    )

    # On conserve uniquement les pays dont la densité
    # est inférieure ou égale à 200 habitants/km²
    df_densite_filtre = df[
        df["Density (people/km²)"] <= 200
    ]

    # Corrélation après filtrage
    correlation_densite_filtre = (
        df_densite_filtre["Density (people/km²)"]
        .corr(df_densite_filtre["Forested Area (%)"])
    )

    # Création des catégories de densité
    df["Densite_categorie"] = pd.cut(
        df["Density (people/km²)"],
        bins=[0, 20, 50, 100, 200, float("inf")],
        labels=["0-20", "20-50", "50-100", "100-200", ">200"]
    )

    # Aperçu des catégories
    apercu_categories = df[
        ["Country", "Density (people/km²)", "Densite_categorie"]
    ].head(10)

    # Nombre de pays dans chaque catégorie
    nombre_pays = (
        df["Densite_categorie"]
        .value_counts()
        .sort_index()
    )

    # Médiane de la surface forestière
    # pour chaque catégorie de densité
    medianes_foret = (
        df.groupby("Densite_categorie", observed=True)
        ["Forested Area (%)"]
        .median()
    )

    return {
        "correlation_densite": correlation_densite,
        "correlation_densite_filtre": correlation_densite_filtre,
        "df_densite_filtre": df_densite_filtre,
        "apercu_categories": apercu_categories,
        "nombre_pays": nombre_pays,
        "medianes_foret": medianes_foret
    }
