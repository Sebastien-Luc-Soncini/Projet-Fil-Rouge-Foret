
import pandas as pd
import numpy as np


def calculer_pib_par_habitant(df):
    """
    Calcule le PIB par habitant et prépare les données
    nécessaires à l'étude de la relation entre richesse
    et couverture forestière.
    """

    donnees = df.copy()

    donnees["GDP_per_capita (USD)"] = (
        donnees["GDP (USD)"] / donnees["Population (people)"]
    )

    donnees_pib_foret = donnees[
        ["Country", "GDP_per_capita (USD)", "Forested Area (%)"]
    ].dropna()

    correlation = donnees_pib_foret[
        "GDP_per_capita (USD)"
    ].corr(
        donnees_pib_foret["Forested Area (%)"]
    )

    return donnees_pib_foret, correlation


def calculer_residus_agriculture_foret(df):
    """
    Calcule les résidus entre la couverture forestière
    observée et celle prédite par une régression linéaire
    basée sur la proportion de terres agricoles.
    """

    donnees_residus = df[
        ["Country", "Agricultural Land (%)", "Forested Area (%)"]
    ].dropna().copy()

    x = donnees_residus["Agricultural Land (%)"]
    y = donnees_residus["Forested Area (%)"]

    pente, ordonnee_origine = np.polyfit(x, y, 1)

    donnees_residus["Foret_predite"] = (
        pente * x + ordonnee_origine
    )

    donnees_residus["Residus"] = (
        y - donnees_residus["Foret_predite"]
    )

    pays_atypiques = pd.concat([
        donnees_residus.nlargest(10, "Residus"),
        donnees_residus.nsmallest(10, "Residus")
    ])

    pays_atypiques = pays_atypiques.sort_values("Residus")

    return donnees_residus, pays_atypiques


def calculer_distribution_foret(df):
    """
    Calcule la moyenne et la médiane de la couverture
    forestière des pays.
    """

    donnees_foret = df["Forested Area (%)"].dropna()

    moyenne_foret = donnees_foret.mean()
    mediane_foret = donnees_foret.median()

    return donnees_foret, moyenne_foret, mediane_foret