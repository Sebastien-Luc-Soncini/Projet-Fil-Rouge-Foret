
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

    fig = px.scatter(
        donnees,
        x="Density (people/km²)",
        y="Forested Area (%)",
        hover_name="Country",
        labels={
            "Density (people/km²)": "Densité (habitants/km²)",
            "Forested Area (%)": "Surface forestière (%)"
        },
        title="Densité de population et couverture forestière",
        color_discrete_sequence=["#228B22"]
    )

    fig.update_layout(
        template="plotly_white"
    )

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

    fig = px.scatter(
        donnees,
        x="Density (people/km²)",
        y="Forested Area (%)",
        hover_name="Country",
        labels={
            "Density (people/km²)": "Densité (habitants/km²)",
            "Forested Area (%)": "Surface forestière (%)"
        },
        title=(
            "Densité de population et couverture forestière "
            "(densité inférieure ou égale à 200)"
        ),
        color_discrete_sequence=["#228B22"]
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def plot_gdp_forest(df):
    """
    Affiche la relation entre PIB par habitant
    et couverture forestière.
    """

    donnees_pib_foret, correlation = calculer_pib_par_habitant(df)

    fig = px.scatter(
        donnees_pib_foret,
        x="GDP_per_capita (USD)",
        y="Forested Area (%)",
        hover_name="Country",
        labels={
            "GDP_per_capita (USD)": "PIB par habitant ($)",
            "Forested Area (%)": "Surface forestière (%)"
        },
        title="PIB par habitant et couverture forestière",
        color_discrete_sequence=["#228B22"]
    )

    fig.update_xaxes(type="log")

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def plot_residuals(df):
    """
    Affiche les 10 pays ayant les résidus les plus positifs
    et les 10 pays ayant les résidus les plus négatifs.
    """

    _, pays_atypiques = calculer_residus_agriculture_foret(df)

    pays_atypiques["Couleur"] = [
        "Positif" if residu > 0 else "Négatif"
        for residu in pays_atypiques["Residus"]
    ]

    fig = px.bar(
        pays_atypiques,
        x="Residus",
        y="Country",
        orientation="h",
        color="Couleur",
        hover_data={"Residus": True, "Couleur": False},
        labels={
            "Residus": "Résidu (points de pourcentage)",
            "Country": "Pays",
            "Couleur": "Type de résidu"
        },
        title="Pays les plus éloignés de la tendance agriculture-forêt",
        color_discrete_map={
            "Positif": "forestgreen",
            "Négatif": "firebrick"
        }
    )

    fig.add_vline(x=0, line_color="black", line_width=1)

    fig.update_layout(
        template="plotly_white"
    )

    return fig


def plot_forest_distribution(df):
    """
    Affiche la distribution de la couverture forestière
    des pays avec une ligne indiquant la moyenne.
    """

    donnees_foret, moyenne_foret, _ = calculer_distribution_foret(df)

    fig = px.histogram(
        x=donnees_foret,
        nbins=10,
        labels={
            "x": "Surface forestière (%)",
            "count": "Nombre de pays"
        },
        title="Distribution de la couverture forestière des pays",
        color_discrete_sequence=["forestgreen"],
        opacity=0.8,
    )

    fig.update_traces(
    marker_line_color="black",
    marker_line_width=1
)

    fig.add_vline(
        x=moyenne_foret,
        line_color="darkorange",
        line_dash="dash",
        line_width=2.5,
        annotation_text=f"Moyenne : {moyenne_foret:.1f} %",
        annotation_position="top"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Surface forestière (%)",
        yaxis_title="Nombre de pays"
    )

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
