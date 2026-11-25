
import streamlit as st
import pandas as pd
from Controls.data_loader import load_data
from Models.analysis import analyse_correlations
from Models.analysis import analyse_agriculture
from Models.analysis import analyse_densite
from Models.advanced_analysis import calculer_residus_agriculture_foret
from Views.visualizations import plot_agriculture_forest
from Views.visualizations import plot_forest_boxplot
from Views.advanced_visualizations import plot_density_scatter, plot_density_scatter_filtered
from Views.advanced_visualizations import plot_residuals

st.title("Exploration des données")

df = load_data()

st.subheader("Corrélations avec la couverture forestière")

correlations = analyse_correlations(df)

st.dataframe(correlations)

st.markdown("""
### Interprétation

La corrélation la plus élevée en valeur absolue est celle entre la proportion de terres agricoles et la couverture forestière (**-0,4346**). Elle révèle une association négative modérée : les pays ayant une proportion plus importante de terres agricoles tendent à présenter une couverture forestière plus faible.

Cette observation nous conduit à approfondir la relation entre terres agricoles et couverture forestière dans la suite de notre analyse exploratoire.
""")

st.subheader("Agriculture et couverture forestière")

agriculture = analyse_agriculture(df)

st.write("Nombre de pays par catégorie de terres agricoles :")
st.dataframe(agriculture["nombre_pays"])

fig = plot_agriculture_forest(df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Interprétation

On observe une **tendance négative** : les pays ayant une proportion importante de terres agricoles ont généralement une couverture forestière plus faible.

Cette observation est cohérente avec le coefficient de corrélation de Pearson, égal à environ **-0,435**, qui indique une corrélation négative modérée.

Toutefois, les points restent dispersés autour de la droite. Certains pays possèdent une couverture forestière élevée malgré une proportion non négligeable de terres agricoles. D'autres facteurs, comme le climat, la géographie ou les politiques d'aménagement du territoire, peuvent également intervenir.
""")

fig = plot_forest_boxplot(df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Interprétation

Ce diagramme en boîtes (*boxplot*) compare la distribution de la couverture forestière entre cinq groupes de pays, définis selon la proportion de terres agricoles dans leur territoire.

On observe une **diminution progressive de la médiane de couverture forestière** lorsque la proportion de terres agricoles augmente. Elle passe d'environ 50 % pour les pays dont les terres agricoles représentent entre 0 et 20 % du territoire, à 41 %, puis 31 % et 13 %. Pour les pays dépassant 80 % de terres agricoles, elle atteint seulement 1 %.

La dispersion des valeurs est également importante dans les premières catégories. Certains pays ont une couverture forestière très élevée, tandis que d'autres en ont très peu. À l'inverse, les pays ayant une forte proportion de terres agricoles présentent généralement une couverture forestière plus faible.

Les points isolés correspondent à des valeurs atypiques, ils représentent des situations géographiques particulières.

**Limite de l'analyse :** la dernière catégorie ne contient que 3 pays. Sa médiane doit donc être interprétée avec prudence.

En conclusion, cette visualisation renforce le constat précédent : dans notre dataset, une proportion élevée de terres agricoles est associée à une couverture forestière généralement plus faible.
""")

st.subheader("Densité de population et couverture forestière")

densite = analyse_densite(df)

fig = plot_density_scatter(df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Interprétation

La densité de population ne semble pas, à elle seule, expliquer beaucoup les différences de couverture forestière entre les pays.

Mais il y a une subtilité : la densité peut être très élevée dans de petits pays et très faible dans de grands pays.

De plus, on observe une sorte de triangle :
- énormément de pays sont concentrés dans les faibles densités ;
- quand la densité augmente, les valeurs de couverture forestière semblent davantage se concentrer vers le bas ;
- quelques pays très denses étirent énormément l'axe horizontal.

Ainsi, la densité ne présente pas de corrélation linéaire forte avec la couverture forestière.

**Piste d'approfondissement :** zoomer sur les pays dont la densité est inférieure ou égale à 200 habitants/km² afin de mieux observer cette tendance.
""")

fig = plot_density_scatter_filtered(df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Corrélation après filtrage

En excluant les pays dont la densité dépasse 200 habitants/km², la relation négative entre densité de population et couverture forestière devient un peu plus visible.

Cependant, cette relation reste faible. Le filtrage améliore la lisibilité du nuage de points et permet de mieux observer la distribution des pays, mais il ne révèle pas une relation linéaire forte.
""")

st.markdown("### Médiane de couverture forestière selon la densité")

df["Densite_categorie"] = pd.cut(
    df["Density (people/km²)"],
    bins=[0, 20, 50, 100, 200, float("inf")],
    labels=["0-20", "20-50", "50-100", "100-200", ">200"]
)

mediane_foret = df.groupby(
    "Densite_categorie", observed=True
)["Forested Area (%)"].median()

st.dataframe(mediane_foret)

st.markdown("""
### Interprétation des médianes

Il y a bien une baisse globale de la médiane quand on passe des densités intermédiaires vers les densités élevées :

**51,3 % → 34,15 % → 25,5 %**

Mais il y a une grosse particularité : la catégorie **0–20** n'a qu'une médiane de **17,6 %**, alors que la catégorie **20–50** monte à **51,3 %**.

Donc ce n'est clairement pas une relation simplement « plus la densité augmente, moins il y a de forêt ».

Il y a probablement plusieurs phénomènes mélangés : les pays très peu denses comprennent notamment des pays désertiques, tandis que certains pays peu ou moyennement denses sont extrêmement forestiers.
""")

st.markdown("### Nombre de pays par catégorie de densité")

nombre_pays = df["Densite_categorie"].value_counts().sort_index()

st.dataframe(nombre_pays)

st.markdown("""
### Interprétation des effectifs

Les catégories sont assez bien représentées, donc aucune des médianes ne repose sur un tout petit échantillon.
""")

st.subheader("Résidus : agriculture et couverture forestière")

residus = calculer_residus_agriculture_foret(df)

fig = plot_residuals(df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Interprétation

Ce graphique met en évidence les pays dont la couverture forestière s'écarte le plus de la tendance générale observée entre la proportion de terres agricoles et la couverture forestière.

Les **résidus négatifs** correspondent aux pays dont la couverture forestière est inférieure à celle prédite par la tendance linéaire, compte tenu de leur proportion de terres agricoles. À l'inverse, les **résidus positifs** désignent les pays dont la couverture forestière est supérieure à la valeur prédite.

Certains pays présentent des écarts particulièrement importants. Parmi les résidus négatifs, on retrouve notamment plusieurs pays arides, comme l'Égypte, le Qatar ou le Koweït. À l'opposé, certains pays affichent une couverture forestière bien supérieure à celle que la tendance linéaire laisserait attendre, comme les Îles Marshall, le Suriname ou Palau.

Ces écarts suggèrent que la proportion de terres agricoles ne suffit pas à expliquer à elle seule les différences de couverture forestière entre les pays. Des facteurs géographiques, climatiques ou liés à l'aménagement du territoire peuvent également jouer un rôle.
""")