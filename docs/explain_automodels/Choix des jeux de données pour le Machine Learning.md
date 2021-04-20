# Choix des jeux de données pour le Machine Learning

Parmi le grand nombre de jeux de données disponibles sur data.gouv.fr, nous avons séléctionné les jeux de données ayant les caractéristiques suivantes:

1. Une **taille adéquate** pour pouvoir entraîner et tester les algorithmes: nombre de lignes allant de l'ordre de 10^{3} à 10^{6} et nombre de colonnes de l'ordre de 10^{1} ou 10^{2}. Le ratio entre la taille des lignes et des colonnes a également été pris en compte.
2. Un bon **équilibre** entre le nombre de **variables catégorielles** et de le nombre de variables **numériques** (on écarte par exemple les jeux de données avec 0 variables numériques).
3. Pour les variables catégorielles, nous avons privilégié les variables ayant un nombre faible de classes et avec des **classes** assez **équilibrées** 

Nous avons également partiellement pris en compte:
1. La proportion et distribution des valeurs manquantes.
2. L'éventuelle présence de prolèmes de haute cardinalité (variables catégorielles avec un très grand nombre de classes).
3. La compléxité du pre-traitement nécessaire pour pouvoir utiliser le jeu de données dans les algorithmes et la complexité lié au regroupement de plusieurs jeux de données différents (par exemple les jeux de données [Données hospitalières liées à l'épidémie de COVID-19](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/)).


*Références:*

Randal S.Olson, William La Cava, Patryk Orzechowski, Ryan J.Urbanowicz, and Ryan H. Moore. Pmlb: a large benchmark suite for machine learning evaluation and com-
parison. *Bio Data Mining*, 2017.


 Macià, Núria, and Ester Bernadó-Mansilla. Towards UCI+: A Mindful Repository Design. *Information sciences 261* (2014): 237–262. Web.


