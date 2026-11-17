import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. TOP 10 DES PAYS LES PLUS FORESTIERS
# --------------------------------------------------

def plot_top_10_forest(df):

    # Sélection des 10 pays avec la plus grande surface forestière
    top_10_foret = df.nlargest(10, "Forested Area (%)")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(
        top_10_foret["Country"],
        top_10_foret["Forested Area (%)"],
        color="forestgreen",
        edgecolor="darkgreen",
        linewidth=1.2,
        label="Surface forestière"
    )

    # Le pays le plus forestier apparaît en haut
    ax.invert_yaxis()

    ax.set_title(
        "Les 10 pays les plus forestiers",
        fontsize=16,
        fontweight="bold"
    )
    ax.set_xlabel("Surface forestière (%)", fontsize=12)
    ax.set_ylabel("Pays", fontsize=12)

    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.legend()

    fig.tight_layout()

    return fig


# --------------------------------------------------
# 2. TERRES AGRICOLES ET COUVERTURE FORESTIERE
# --------------------------------------------------

def plot_agriculture_forest(df):

    # Sélection des deux variables
    donnees = df[
        ["Agricultural Land (%)", "Forested Area (%)"]
    ].dropna()

    # Définition de x et y
    x = donnees["Agricultural Land (%)"]
    y = donnees["Forested Area (%)"]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Calcul de la droite de régression
    pente, ordonnee_origine = np.polyfit(x, y, 1)

    # Création de 100 points pour tracer la droite
    x_droite = np.linspace(x.min(), x.max(), 100)
    y_droite = pente * x_droite + ordonnee_origine

    # Nuage de points
    ax.scatter(
        x,
        y,
        color="seagreen",
        marker="o",
        s=60,
        alpha=0.7,
        edgecolors="black",
        linewidths=0.5,
        label="Pays"
    )

    # Droite de tendance
    ax.plot(
        x_droite,
        y_droite,
        color="darkred",
        linestyle="--",
        linewidth=2,
        label="Droite de tendance"
    )

    ax.set_title(
        "Terres agricoles et couverture forestière",
        fontsize=15,
        fontweight="bold"
    )
    ax.set_xlabel("Terres agricoles (%)", fontsize=12)
    ax.set_ylabel("Surface forestière (%)", fontsize=12)

    ax.grid(linestyle="--", alpha=0.3)
    ax.legend()

    fig.tight_layout()

    return fig


# --------------------------------------------------
# 3. BOXPLOT : COUVERTURE FORESTIERE PAR CATEGORIE
# --------------------------------------------------

def plot_forest_boxplot(df):

    categories = ["0-20", "20-40", "40-60", "60-80", ">80"]

    # Sélection des données pour chaque catégorie
    donnees_boxplot = [
        df.loc[
            df["Agriculture_categorie"] == categorie,
            "Forested Area (%)"
        ].dropna()
        for categorie in categories
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    boites = ax.boxplot(
        donnees_boxplot,
        tick_labels=categories,
        patch_artist=True
    )

    # Personnalisation des boîtes
    for boite in boites["boxes"]:
        boite.set_facecolor("seagreen")
        boite.set_edgecolor("black")
        boite.set_linewidth(1.2)

    ax.set_title(
        "Couverture forestière selon la proportion de terres agricoles",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Terres agricoles (%)", fontsize=12)
    ax.set_ylabel("Surface forestière (%)", fontsize=12)

    ax.grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()

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

    fig, ax = plt.subplots(figsize=(11, 8))

    image = ax.imshow(
        correlations,
        cmap="RdYlGn",
        vmin=-1,
        vmax=1
    )

    # Noms des variables sur les axes
    ax.set_xticks(range(len(variables)))
    ax.set_xticklabels(
        variables,
        rotation=45,
        ha="right"
    )

    ax.set_yticks(range(len(variables)))
    ax.set_yticklabels(variables)

    # Valeurs des corrélations dans chaque case
    for i in range(len(variables)):
        for j in range(len(variables)):

            valeur = correlations.iloc[i, j]

            ax.text(
                j,
                i,
                f"{valeur:.2f}",
                ha="center",
                va="center",
                color="black",
                fontsize=10
            )

    # Barre de couleurs
    fig.colorbar(
        image,
        ax=ax,
        label="Coefficient de corrélation"
    )

    ax.set_title(
        "Matrice de corrélation des variables",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    fig.tight_layout()

    return fig
