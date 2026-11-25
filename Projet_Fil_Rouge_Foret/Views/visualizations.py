import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# 1. TOP 10 DES PAYS LES PLUS FORESTIERS
# --------------------------------------------------

def plot_top_10_forest(df):

    # Sélection des 10 pays avec la plus grande surface forestière
    top_10_foret = df.nlargest(10, "Forested Area (%)").copy()

    # Graphique interactif
    fig = px.bar(
        top_10_foret,
        x="Forested Area (%)",
        y="Country",
        orientation="h",
        title="Les 10 pays les plus forestiers",
        labels={
            "Forested Area (%)": "Surface forestière (%)",
            "Country": "Pays"
        },
        hover_data={"Forested Area (%)": ":.2f"},
        color_discrete_sequence=["#228B22"]
    )

    # Le pays le plus forestier apparaît en haut
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        template="plotly_white"
    )

    return fig


# --------------------------------------------------
# 2. TERRES AGRICOLES ET COUVERTURE FORESTIERE
# --------------------------------------------------

def plot_agriculture_forest(df):

    # Sélection des deux variables
    donnees = df[
        ["Country", "Agricultural Land (%)", "Forested Area (%)"]
    ].dropna()

    # Calcul de la droite de régression
    x = donnees["Agricultural Land (%)"]
    y = donnees["Forested Area (%)"]

    pente, ordonnee_origine = np.polyfit(x, y, 1)

    # Création des points pour la droite
    x_droite = np.linspace(x.min(), x.max(), 100)
    y_droite = pente * x_droite + ordonnee_origine

    # Nuage de points interactif
    fig = px.scatter(
        donnees,
        x="Agricultural Land (%)",
        y="Forested Area (%)",
        hover_name="Country",
        labels={
            "Agricultural Land (%)": "Terres agricoles (%)",
            "Forested Area (%)": "Surface forestière (%)"
        },
        title="Terres agricoles et couverture forestière",
        color_discrete_sequence=["#228B22"]
    )

    # Ajout de la droite de tendance
    fig.add_scatter(
        x=x_droite,
        y=y_droite,
        mode="lines",
        name="Droite de tendance",
        line=dict(color="darkred", dash="dash", width=2)
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# --------------------------------------------------
# 3. BOXPLOT : COUVERTURE FORESTIERE PAR CATEGORIE
# --------------------------------------------------

def plot_forest_boxplot(df):

    categories = ["0-20", "20-40", "40-60", "60-80", ">80"]

    donnees_boxplot = [
        df.loc[
            df["Agriculture_categorie"] == categorie,
            "Forested Area (%)"
        ].dropna()
        for categorie in categories
    ]

    fig = go.Figure()

    for categorie, donnees in zip(categories, donnees_boxplot):

        mediane = donnees.median()

        # Boxplot avec position X explicite
        fig.add_trace(
            go.Box(
                x=[categorie] * len(donnees),
                y=donnees,
                name=f"{categorie} (n={len(donnees)})",
                boxpoints="outliers",
                marker_color="seagreen",
                line_color="seagreen",
                fillcolor="rgba(46, 139, 87, 0.5)"
            )
        )

        # Ligne de médiane noire
        fig.add_shape(
            type="line",
            x0=categorie,
            x1=categorie,
            y0=mediane,
            y1=mediane,
            xref="x",
            yref="y",
            line=dict(
                color="black",
                width=4
            )
        )

        # Valeur de la médiane en noir
        fig.add_annotation(
            x=categorie,
            y=mediane,
            text=f"{mediane:.0f}",
            showarrow=False,
            font=dict(
                color="black",
                size=14
            ),
            yshift=12
        )

    fig.update_layout(
        title="Couverture forestière selon la proportion de terres agricoles",
        xaxis_title="Terres agricoles (%)",
        yaxis_title="Surface forestière (%)",
        template="plotly_white",
        legend=dict(
            title="Valeurs en noir : médianes"
        ),
        xaxis=dict(
            categoryorder="array",
            categoryarray=categories
        )
    )

    return fig


# --------------------------------------------------
# 4. MATRICE DE CORRELATION
# --------------------------------------------------

def plot_correlation_matrix(df):

    variables = [
        "Forested Area (%)",
        "Agricultural Land (%)",
        "Density (people/km²)",
        "Land Area (km²)",
        "Population (people)",
        "GDP (USD)"
    ]

    # Calcul des corrélations
    correlations = df[variables].corr()

    fig = px.imshow(
        correlations,
        text_auto=".2f",
        color_continuous_scale="RdYlGn",
        zmin=-1,
        zmax=1,
        labels={
            "x": "Variables",
            "y": "Variables",
            "color": "Coefficient de corrélation"
        },
        title="Matrice de corrélation des variables"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig

# les dix pays avec le moins de forêt

def plot_bottom_10_forest(df):

    # Sélection des 10 pays avec la plus faible surface forestière
    bottom_10_foret = df.nsmallest(10, "Forested Area (%)").copy()

    # Graphique interactif
    fig = px.bar(
        bottom_10_foret,
        x="Forested Area (%)",
        y="Country",
        orientation="h",
        title="Les 10 pays ayant la plus faible couverture forestière",
        labels={
            "Forested Area (%)": "Surface forestière (%)",
            "Country": "Pays"
        },
        hover_data={"Forested Area (%)": ":.2f"},
        color_discrete_sequence=["#D2A679"]
    )

    # Le pays avec la plus faible couverture apparaît en haut
    fig.update_layout(
        yaxis={"categoryorder": "total descending"},
        template="plotly_white"
    )

    return fig