
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Import du module de nettoyage
from cleaning import clean_data

# Import des analyses principales
from analysis import (
    analyse_statistique,
    analyse_correlations,
    analyse_agriculture,
    analyse_densite
)

# Import des analyses avancées
from advanced_analysis import (
    calculer_pib_par_habitant,
    calculer_residus_agriculture_foret,
    calculer_distribution_foret
)

# Import des visualisations principales
from visualizations import (
    plot_top_10_forest,
    plot_agriculture_forest,
    plot_forest_boxplot,
    plot_correlation_matrix
)

# Import des visualisations avancées
from advanced_visualizations import (
    plot_density_scatter,
    plot_density_scatter_filtered,
    plot_gdp_forest,
    plot_residuals,
    plot_forest_distribution,
    plot_world_map
)

# Import des fonctions SQL
from sql import (
    create_database,
    get_top_forest_countries,
    get_high_density_countries,
    get_average_forest_area,
    get_forest_by_agriculture
)


def main():

    # Chemin du dossier du projet
    dossier_projet = Path(__file__).resolve().parent

    print("\n====================================")
    print(" PROJET FIL ROUGE - FORET")
    print("====================================\n")


    # --------------------------------
    # 1. CHARGEMENT DES DONNEES
    # --------------------------------

    print("1. Chargement des données...")

    chemin_csv = dossier_projet / "foret.csv"

    df = pd.read_csv(chemin_csv)

    print("Nombre de lignes :", len(df))
    print("Nombre de colonnes :", len(df.columns))


    # --------------------------------
    # 2. NETTOYAGE DES DONNEES
    # --------------------------------

    print("\n2. Nettoyage des données...")

    df = clean_data(df)

    print("Nettoyage terminé.")
    print("Dimensions finales :", df.shape)


    # --------------------------------
    # 3. SAUVEGARDE DU CSV NETTOYE
    # --------------------------------

    print("\n3. Sauvegarde du CSV nettoyé...")

    chemin_csv_nettoye = dossier_projet / "foret_clean.csv"

    df.to_csv(chemin_csv_nettoye, index=False)

    print("Fichier sauvegardé :", chemin_csv_nettoye)


    # --------------------------------
    # 4. ANALYSES STATISTIQUES
    # --------------------------------

    print("\n4. Analyses statistiques...")

    resultats_stats = analyse_statistique(df)

    print("\nStatistiques de la couverture forestière :")
    print(resultats_stats["statistiques_foret"])

    print("\nTop 10 des pays les plus forestiers :")
    print(resultats_stats["top_10_foret"])

    print("\nTop 10 des pays les moins forestiers :")
    print(resultats_stats["bottom_10_foret"])


    # --------------------------------
    # 5. ANALYSES DES CORRELATIONS
    # --------------------------------

    print("\n5. Analyses des corrélations...")

    correlations = analyse_correlations(df)

    print(correlations)


    # --------------------------------
    # 6. ANALYSE AGRICULTURE
    # --------------------------------

    print("\n6. Analyse des terres agricoles...")

    resultats_agriculture = analyse_agriculture(df)

    print("\nNombre de pays par catégorie agricole :")
    print(resultats_agriculture["nombre_pays"])

    print("\nMédiane forestière par catégorie agricole :")
    print(resultats_agriculture["medianes_foret"])


    # --------------------------------
    # 7. ANALYSE DENSITE
    # --------------------------------

    print("\n7. Analyse de la densité de population...")

    resultats_densite = analyse_densite(df)

    print(
        "\nCorrélation densité / forêt :",
        resultats_densite["correlation_densite"]
    )

    print(
        "Corrélation après filtrage :",
        resultats_densite["correlation_densite_filtre"]
    )

    print("\nNombre de pays par catégorie de densité :")
    print(resultats_densite["nombre_pays"])


    # --------------------------------
    # 8. ANALYSES AVANCEES
    # --------------------------------

    print("\n8. Analyses avancées...")

    donnees_pib, correlation_pib = calculer_pib_par_habitant(df)

    print("\nCorrélation PIB par habitant / forêt :")
    print(correlation_pib)

    donnees_residus, pays_atypiques = calculer_residus_agriculture_foret(df)

    print("\nPays les plus atypiques :")
    print(pays_atypiques[["Country", "Residus"]])

    donnees_foret, moyenne_foret, mediane_foret = calculer_distribution_foret(df)

    print("\nDistribution de la couverture forestière :")
    print("Moyenne :", round(moyenne_foret, 2), "%")
    print("Médiane :", round(mediane_foret, 2), "%")


    # --------------------------------
    # 9. GENERATION DES VISUALISATIONS
    # --------------------------------

    print("\n9. Génération des graphiques...")

    graphiques = [
        plot_top_10_forest(df),
        plot_agriculture_forest(df),
        plot_forest_boxplot(df),
        plot_correlation_matrix(df),
        plot_density_scatter(df),
        plot_density_scatter_filtered(df),
        plot_gdp_forest(df),
        plot_residuals(df),
        plot_forest_distribution(df)
    ]

    carte = plot_world_map(df)

    print("Les graphiques ont été générés.")


    # --------------------------------
    # 10. CREATION DE LA BASE SQL
    # --------------------------------

    print("\n10. Création de la base de données SQL...")

    connexion = None

    try:

        connexion = create_database(df)

        print("\nTop 10 SQL des pays les plus forestiers :")
        print(get_top_forest_countries(connexion))

        print("\nPays avec une densité supérieure à 200 :")
        print(get_high_density_countries(connexion))

        print("\nMoyenne de couverture forestière :")
        print(get_average_forest_area(connexion))

        print("\nCouverture forestière par catégorie agricole :")
        print(get_forest_by_agriculture(connexion))

    finally:

        if connexion is not None:
            connexion.close()


    # --------------------------------
    # 11. AFFICHAGE DES GRAPHIQUES
    # --------------------------------

    print("\n11. Affichage des graphiques...")

    plt.show()

    carte.show()

    print("\n====================================")
    print(" ANALYSE TERMINEE AVEC SUCCES")
    print("====================================")


# --------------------------------
# EXECUTION DU PROGRAMME
# --------------------------------

if __name__ == "__main__":
    main()
