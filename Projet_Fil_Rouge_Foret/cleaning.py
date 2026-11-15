# script testé et validé !

import pandas as pd

def clean_data(df):

    # liste des colonnes pas utile selon moi
    colonnes_a_supprimer = [
        "Abbreviation",
        "Calling Code",
        "Capital/Major City",
        "Currency-Code",
        "Largest city",
        "Official language"
    ]

    df = df.drop(columns=colonnes_a_supprimer)

    # on constate dans le fichier excel et le csv d'origine... qu'il y a une ligne "S???" au lieu que ce soit un pays
    # après recherche sur internet, le pays "S???" s'agit très probablement de Sao Tomé-et-Principe, une petite île près de l'Afrique centrale
    # de plus la valeur dans "Land Area (km2) correspond bien"
    # en Anglais, c'est São Tomé and Príncipe, nous allons le mettre dans le data, sans accent
    # il s'agit de la ligne 152 dans le CSV d'origine
    # mais dans pandas on commence à partir de la ligne zéro (au lieu de 1 dans csv ou excel...)
    # et la ligne d'en-tête n'est pas une donnée pour pandas
    # donc c'est la ligne numéro 150 dans pandas

    df.iloc[150, df.columns.get_loc("Country")] = "Sao Tome and Principe"
    
    # on vérifie que la correction s'est bien faite
    print(df.iloc[149:152][["Country", "Density\n(P/Km2)"]])

    # on affiche toutes les valeurs de la ligne 150
    print(df.iloc[150])

    # on complète la latitude et la longitude de Sao Tome and Principe
    df.loc[df["Country"] == "Sao Tome and Principe", "Latitude"] = 0.18636
    df.loc[df["Country"] == "Sao Tome and Principe", "Longitude"] = 6.61308

    # on regarde attentivement la colonne "Forested Area (%)"

    # on liste les colonnes qui ont des valeurs manquantes, avec le nb de valeurs manquantes

    valeurs_manquantes = df.isna().sum()

    print(valeurs_manquantes[valeurs_manquantes > 0])

    # on vérifie qu'il n'y ait pas de pays en double

    doublons = df.duplicated().sum()

    print("Nombre de doublons :", doublons)

    # sauf que dans une colonne, il y a forcément toujours le même type ? Regardons plus précisément...

    # c'est déjà pas seulement de "type object"... affichons les 10 premières valeurs

    print(df["Land Area(Km2)"].head(10).tolist())

    # on convertit toutes les valeurs de land area en nombres entiers ; les virgules à supprimer viennent du format anglais...

    df["Land Area(Km2)"] = (
        df["Land Area(Km2)"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["Land Area(Km2)"] = pd.to_numeric(
        df["Land Area(Km2)"],
        errors="coerce"
    ).astype("Int64")

    # on vérifie que ça a fonctionné

    print(df["Land Area(Km2)"].iloc[0])
    print(type(df["Land Area(Km2)"].iloc[0]))

    # ça a l'air d'avoir fonctionné, on vérifie s'il y'a des valaurs manquantes

    print(df["Land Area(Km2)"].isna().sum())

    # il y a une valeur manquante, identifions la ligne concernée

    print(df[df["Land Area(Km2)"].isna()])

    # il y a des colonnes où les valeurs ont plein de virgules dus au format anglais mais ce sont des entiers... créons une catégorie pour ça

    colonnes_virgules = [
        "Armed Forces size",
        "Co2-Emissions",
        "Population",
        "Urban_population"
    ]

    # on applique alors le nettoyage, la conversion vers des nombres plus propre

    for colonne in colonnes_virgules:
        df[colonne] = pd.to_numeric(
            df[colonne].astype("string").str.replace(",", "", regex=False),
            errors="coerce"
        ).astype("Int64")

    # maintenant on fait pareil avec les colonnes qui contiennent des % ; qui contiennent des nombres décimaux

    colonnes_pourcentage = [
        "Agricultural Land( %)",
        "CPI Change (%)",
        "Forested Area (%)",
        "Gross primary education enrollment (%)",
        "Gross tertiary education enrollment (%)",
        "Out of pocket health expenditure",
        "Population: Labor force participation (%)",
        "Tax revenue (%)",
        "Total tax rate",
        "Unemployment rate"
    ]

    for colonne in colonnes_pourcentage:
        df[colonne] = (
            df[colonne].astype("string")
            .str.replace("%", "", regex=False)
            .astype(float)
        )

    # pareil avec les colonnes avec $ ; qui contiennent des nombres décimaux

    colonnes_dollars = [
        "Gasoline Price",
        "Minimum wage"
    ]

    for colonne in colonnes_dollars:
        df[colonne] = (
            df[colonne].astype("string")
            .str.replace("$", "", regex=False)
            .str.strip()
            .astype(float)
        )

    # maintenant la colonne GDP qui a des virgules et des $ ; les valeurs sont des entiers

    df["GDP"] = (
        df["GDP"].astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype("Int64")
    )

    df["Country"] = df["Country"].astype("string")

    df["Density\n(P/Km2)"] = pd.to_numeric(
        df["Density\n(P/Km2)"]
        .astype("string")
        .str.replace(",", "", regex=False),
        errors="coerce"
    ).astype("Int64")

    df["CPI"] = pd.to_numeric(
    df["CPI"],
    errors="coerce"
    )

    # maintenant on fait un diagnostique avec une belle mise en forme

    manquantes = df.isna().sum()
    pourcentage = (manquantes / len(df)) * 100

    diagnostic = pd.DataFrame({
        "Valeurs manquantes": manquantes,
        "Pourcentage": pourcentage
    })

    print(
        diagnostic[diagnostic["Valeurs manquantes"] > 0]
        .sort_values("Pourcentage", ascending=False)
    )

    # on supprime les colonnes inutiles pour l'analyse de la surface forestière

    df = df.drop(columns=[
        "Minimum wage",
        "Tax revenue (%)",
        "Armed Forces size"
    ], errors="ignore")

    # on supprime la ligne Palestine

    df = df[df["Country"] != "Palestinian National Authority"]

    # on supprime les pays qui n'ont pas de données sur la surface forestière
    df = df.dropna(subset=["Forested Area (%)"])

    # on renomme les colonnes pour ajouter des unités de mesure

    df = df.rename(columns={

        "Country": "Country",
        "Density\n(P/Km2)": "Density (people/km²)",
        "Agricultural Land( %)": "Agricultural Land (%)",
        "Land Area(Km2)": "Land Area (km²)",
        "Birth Rate": "Birth Rate (births/1,000 people/year)",
        "Co2-Emissions": "CO2 Emissions (kt/year)",
        "CPI": "CPI (index)",
        "CPI Change (%)": "CPI Change (%)",
        "Fertility Rate": "Fertility Rate (children/woman)",
        "Forested Area (%)": "Forested Area (%)",
        "Gasoline Price": "Gasoline Price (USD/litre)",
        "GDP": "GDP (USD)",
        "Gross primary education enrollment (%)": "Gross Primary Education Enrollment (%)",
        "Gross tertiary education enrollment (%)": "Gross Tertiary Education Enrollment (%)",
        "Infant mortality": "Infant Mortality (deaths/1,000 live births)",
        "Life expectancy": "Life Expectancy (years)",
        "Maternal mortality ratio": "Maternal Mortality (deaths/100,000 live births)",
        "Out of pocket health expenditure": "Out-of-Pocket Health Expenditure (%)",
        "Physicians per thousand": "Physicians (per 1,000 people)",
        "Population": "Population (people)",
        "Population: Labor force participation (%)": "Labor Force Participation (%)",
        "Total tax rate": "Total Tax Rate (%)",
        "Unemployment rate": "Unemployment Rate (%)",
        "Urban_population": "Urban Population (people)",
        "Latitude": "Latitude (degrees)",
        "Longitude": "Longitude (degrees)"
    })

    # on sélectionne les colonnes numériques contenant des valeurs manquantes
    colonnes_manquantes = df.select_dtypes(include="number").columns[
        df.select_dtypes(include="number").isna().any()
    ]

    # on remplace les valeurs manquantes par la médiane arrondie à 2 décimales
    for colonne in colonnes_manquantes:
        mediane = round(df[colonne].median(), 2)
        df[colonne] = df[colonne].fillna(mediane)

    return df