
# Guide au AutoML Leaderboard report

Cette page a pour but de vous aider à mieux comprendre les résultats du AutoML Leaderboard report qui est fourni pour chaque jeu de données.

Cliquez ici pour lire le guide officiel de la librairie `mljar-supervised` à l'aide de laquelle nous avons généré ces rapport : https://supervised.mljar.com/

## Page principale

Dans la page principale du rapport, un tableau récapitule les modèles entraînés sur le jeu de données avec les métriques associées. Un graphique vous permet également de visualiser ces résultats :

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_0a89bb8156a84a6eecc08aa537ce14af.png)

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_2d16a5e2955e2e9ed810819c82d3cd7c.png)


### A quoi correspondent les algorithmes?

1. `Baseline`: correspond au [`DummyClassifier` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html) pour la Classification et au [`DummyRegressor` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html) pour la Régression
2. `DecisionTree`: utilise le [`DecisionTreeClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) pour la Classification et le [`DecisionTreeRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html) pour la Régression
3. `Linear`: [`LogisticRegression` de scikit-learn](https://scikit-learn.org/0.16/modules/generated/sklearn.linear_model.LogisticRegression.html) pour la Classification et  [`LinearRegression` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) pour la Régression
4. `Random Forest` : [`RandomForestClassifier`de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) pour la Classification et [`RandomForestRegressor` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) pour la Régression
5. `Extra Trees`: [`ExtraTreesClassifier` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html) pour la Classification et  [`ExtraTreesRegressor` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html) pour la Régression
6. `Xgboost`: utilise le package [`Xgboost`](https://xgboost.readthedocs.io/en/latest/index.html)
7. `NeuralNetwork`: [`Keras`](https://keras.io) et [`TensorFlow`](https://www.tensorflow.org) sont utilisés. Les hyperparamètres sont identiques pour la Regression et la Classification, il existe un différence entre le type de neurones de sortie et la fonction de perte en fonction de la tâche (plus de détails [ici])(https://supervised.mljar.com/features/algorithms/).
8. `Ensemble`: l'algorithme est construit à partir de [ce papier](http://www.cs.cornell.edu/~alexn/papers/shotgun.icml04.revised.rev2.pdf). Un modèle ensembliste est un ensemble de modèles combinés par moyenne pondérée ou par voting dans le but d'améliorer les prédictions obtenues par chaque modèle individuellement. Ici, la moyenne est utilisée.


### A quoi correspondent les métriques?

Voici une liste (très complète) des métriques : https://scikit-learn.org/stable/modules/model_evaluation.html



*Remarque:* Pour tous les algorithmes, nous avons partagé le jeu de données en base d'apprentissage et de test avec une proportion de 75% / 25%.



## Détail de chaque modèle

Pour chaque modèle, on dispose d'un rapport détaillé :

**Détail des paramètres du modèle, ensemble des métriques :**


![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_f38a93bc7bfb7ab6b04bcaeacb98cdd2.png)

et une matrice de confusion pour la Classification :
 
![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_287b10760cab43d831685a476ed0a421.png)


**Learning curves:**

Montrent l'évolution de la métrique (*logloss* pour la Classification et *rmse* pour la Régression) au fur et à mesure que les itérations de l'algorithme avancent. La ligne verticale qui apparaît dans la majorité des graphiques indique le nombre optimal d'itérations, qui sera ensuite utilisé dans le calcul des prédictions.

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_ec388131c685a744ad919138c9a1b104.png)

*Remarque:* Les informations présentées jusque là sont fournies pour chacun des modèles et pour chaque jeu de données. Les plots décrits dans la suite sont disponibles pour la majorité des jeux de données et des modèles mais pas pour tous.

**Permutation-based importance:**

L'évaluation de l'importance des variables (features) est faite à partir de [`permutation_importance` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.inspection.permutation_importance.html)

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_f765abeebade2054a4a26bd09e04db14.png)


Pour plus de détail sur la `feature-importance`, cliquer ici: https://scikit-learn.org/stable/modules/permutation_importance.html#permutation-importance

**SHAP importance, SHAP dependence plots, SHAP decision plots:**

Pour calculer les SHAP importance, SHAP dependence plots, SHAP decision plots le [package `shap`](https://shap.readthedocs.io/en/latest/) est utilisé.

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_2c0c730957a8750228369de8b61d2272.png)


![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_c2a0f0aa86f56d96ddbaea4ff8b0c6e9.png)


![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_ddd0c0eea10c390863cee45684a3f004.png)


SHAP (SHapley Additive exPlanations) est une approche issue de la théorie des jeux qui nous permet de mieux comprendre les résultats d'un modèle de Machine Learning.
Pour faire cela, les changements de prédiction sont quantifiées (magnitude et direction) lorsqu'une variable est soustraite du modèle.
Les *dependence plot* nous permettent ensuite de visualiser l'impacte de chaque variable sur les prédictions: chaque point représente une ligne du dataset, les valeurs sur l'axe des abscisses représentent les valeurs de la variable en question et celles sur l'axe des ordonnées la valeur SHAP correspondante, qui quantifie l'influence des différentes valeurs sur la prédiction.
Les *decision plots* nous indiquent enfin de quelle manière le modèle "prend des décisions" pour les 10 meilleures prédictions (premier plot) et pour les 10 pires prédictions (2ème plot)
Plus de détails sur SHAP [ici](https://github.com/slundberg/shap/blob/master/README.md).










