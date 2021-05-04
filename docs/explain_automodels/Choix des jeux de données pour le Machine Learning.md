# Choix des jeux de données pour le Machine Learning

Dans OpenML, deux catégories de jeux de données sont proposés: des jeux de données qui ont été séléctionnés à la main (curated datasets) et pour lesquels il y a eu une intervention humaine pour vérifier que les jeux de données sont adaptés aux tâches de Machine Learning et des jeux de données qui ont été extraits automatiquement à partir de data.gouv.fr (automatic datasets) et qui ont été séléctionnés automatiquement en fonction d'un certain nombre de critères statistiques.

Parmi le grand nombre de jeux de données disponibles sur data.gouv.fr, nous avons séléctionné les jeux de données ayant les caractéristiques suivantes:

1. Une **taille adéquate** pour pouvoir entraîner et tester les algorithmes: nombre de lignes allant de l'ordre de 10^{3} à 10^{6} et nombre de colonnes de l'ordre de 10^{1} ou 10^{2}. Le ratio entre la taille des lignes et des colonnes a également été pris en compte.
2. Des **variables catégorielles** et des **variables numériques**
3. Un nombre assez faible de valeur manquantes

Nous avons également pris en compte dans un deuxième temps:
1. L'éventuelle présence de variables catégorielles à **haute cardinalité** 
2. Les variables **fortement corrélées**
3. La compléxité du pre-traitement nécessaire pour pouvoir utiliser le jeu de données dans les algorithmes et la complexité lié au regroupement de plusieurs jeux de données différents (par exemple les jeux de données [Données hospitalières liées à l'épidémie de COVID-19](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/)).
4. Les colonnes inutilisables (ex. des colonnes à valeurs constantes)

*Références:*

Randal S.Olson, William La Cava, Patryk Orzechowski, Ryan J.Urbanowicz, and Ryan H. Moore. Pmlb: a large benchmark suite for machine learning evaluation and com-
parison. *Bio Data Mining*, 2017.


 Macià, Núria, and Ester Bernadó-Mansilla. Towards UCI+: A Mindful Repository Design. *Information sciences 261* (2014): 237–262. Web.


