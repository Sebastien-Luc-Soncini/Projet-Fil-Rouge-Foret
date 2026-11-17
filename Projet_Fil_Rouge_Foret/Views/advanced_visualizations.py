
import matplotlib.pyplot as plt
import plotly.express as px

from Models.advanced_analysis import (
    calculer_pib_par_habitant,
    calculer_residus_agriculture_foret,
    calculer_distribution_foret
)


def plot_density_scatter(df):
    """
    Affiche la relation entre densité de population
    et couverture forestière pour tous les pays.
    """

    donnees = df.dropna(
        subset=["Density (people/km²)", "Forested Area (%)"]
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        donnees["Density (people/km²)"],
        donnees["Forested Area (%)"]
    )

    ax.set_title("Densité de population et couverture forestière")
    ax.set_xlabel("Densité (habitants/km²)")
    ax.set_ylabel("Surface forestière (%)")
    ax.grid(linestyle="--", alpha=0.3)

    fig.tight_layout()

    return fig


def plot_density_scatter_filtered(df):
    """
    Affiche la relation entre densité de population
    et couverture forestière en excluant les pays
    dont la densité dépasse 200 habitants/km².
    """

    donnees = df[
        df["Density (people/km²)"] <= 200
    ].dropna(
        subset=["Density (people/km²)", "Forested Area (%)"]
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        donnees["Density (people/km²)"],
        donnees["Forested Area (%)"]
    )

    ax.set_title(
        "Densité de population et couverture forestière "
        "(densité inférieure ou égale à 200)"
    )

    ax.set_xlabel("Densité (habitants/km²)")
    ax.set_ylabel("Surface forestière (%)")
    ax.grid(linestyle="--", alpha=0.3)

    fig.tight_layout()

    return fig


def plot_gdp_forest(df):
    """
    Affiche la relation entre PIB par habitant
    et couverture forestière.
    """

    donnees_pib_foret, correlation = calculer_pib_par_habitant(df)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        donnees_pib_foret["GDP_per_capita (USD)"],
        donnees_pib_foret["Forested Area (%)"],
        color="seagreen",
        s=60,
        alpha=0.7,
        edgecolors="black",
        linewidths=0.5
    )

    ax.set_title("PIB par habitant et couverture forestière")
    ax.set_xlabel("PIB par habitant ($)")
    ax.set_ylabel("Surface forestière (%)")

    ax.set_xscale("log")

    ax.grid(linestyle="--", alpha=0.3)
    fig.tight_layout()

    return fig


def plot_residuals(df):
    """
    Affiche les 10 pays ayant les résidus les plus positifs
    et les 10 pays ayant les résidus les plus négatifs.
    """

    _, pays_atypiques = calculer_residus_agriculture_foret(df)

    couleurs = [
        "forestgreen" if residu > 0 else "firebrick"
        for residu in pays_atypiques["Residus"]
    ]

    fig, ax = plt.subplots(figsize=(11, 8))

    ax.barh(
        pays_atypiques["Country"],
        pays_atypiques["Residus"],
        color=couleurs,
        edgecolor="black",
        linewidth=0.5
    )

    ax.axvline(0, color="black", linewidth=1)

    ax.set_title(
        "Pays les plus éloignés de la tendance agriculture-forêt"
    )

    ax.set_xlabel("Résidu (points de pourcentage)")
    ax.set_ylabel("Pays")

    ax.grid(axis="x", linestyle="--", alpha=0.3)
    fig.tight_layout()

    return fig


def plot_forest_distribution(df):
    """
    Affiche la distribution de la couverture forestière
    des pays avec une ligne indiquant la moyenne.
    """

    donnees_foret, moyenne_foret, _ = calculer_distribution_foret(df)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        donnees_foret,
        bins=10,
        color="forestgreen",
        edgecolor="black",
        alpha=0.8,
        label="Nombre de pays"
    )

    ax.axvline(
        moyenne_foret,
        color="darkorange",
        linestyle="--",
        linewidth=2.5,
        label=f"Moyenne : {moyenne_foret:.1f} %"
    )

    ax.set_title("Distribution de la couverture forestière des pays")
    ax.set_xlabel("Surface forestière (%)")
    ax.set_ylabel("Nombre de pays")

    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend()

    fig.tight_layout()

    return fig


def plot_world_map(df):
    """
    Crée une carte interactive de la couverture forestière
    par pays avec Plotly.
    """

    carte_foret = df.dropna(
        subset=["Country", "Forested Area (%)"]
    )

    fig = px.choropleth(
        carte_foret,
        locations="Country",
        locationmode="country names",
        color="Forested Area (%)",
        color_continuous_scale="Greens",
        range_color=(0, 100),
        hover_name="Country",
        hover_data={
            "Forested Area (%)": ":.1f"
        },
        title="Couverture forestière mondiale par pays"
    )

    fig.update_layout(
        title={
            "text": "Couverture forestière mondiale par pays (%)",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22}
        },
        width=1200,
        height=700,
        margin={"l": 20, "r": 80, "t": 80, "b": 20},
        geo={
            "projection_type": "natural earth",
            "showframe": False,
            "showcoastlines": True,
            "landcolor": "lightgray"
        },
        coloraxis_colorbar={
            "title": "Surface forestière (%)",
            "thickness": 18,
            "len": 0.75
        }
    )

    return fig
