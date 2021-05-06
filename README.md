# DGML (Data Gouv pour le Machine Learning)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/etalab-ia/DGML/README.en.md)

Le projet DGML vise à la construction d'un **catalogue de jeux de données de data.gouv.fr pour le Machine Learning.**

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_a2a6cac87d197051d9e09107e78460d1.png =12x12) [datascience.etalab.studio/dgml/](https://datascience.etalab.studio/dgml/)

### Objectifs

Parmi le grand nombre de données ouvertes disponibles sur data.gouv.fr, il peut s'avérer difficile de trouver rapidement des jeux de données réutilisables par des algorithmes de ML et de déterminer si elles seraient adaptées à cette tâche. 
Dans DGML, vous pouvez rapidement **séléctionner un jeu de données de data.gouv.fr pour le Machine Learning** et **avoir un aperçu rapide des informations utiles pour faire du Machine Learning sur ce jeu de données**.
 
 
 ### Ce que vous trouvez dans DGML
 
 - 60 *jeux de données* réutilisables par des algorithmes de ML (cliquez [ici](https://github.com/etalab-ia/open_ML/blob/main/docs/explain_automodels/Choix%20des%20jeux%20de%20donn%C3%A9es%20pour%20le%20Machine%20Learning.md) pour avoir plus d'informations sur le choix des datasets), que vous pouvez trier par tâche (régression ou classification), par taille etc.

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_c6347dbee1bcb73aa66aa35718169f36.png =500x)


Pour chaque jeux de données vous trouvez:
 - Un *profiling statistique* , qui vous donne des infos sur les statistiques du jeu de données, la distribution de ses variables et des valeurs manquantes et les corrélations

 - Les résultats de l'*entraînement et de la validation automatique d'algorithmes de ML* sur ces datasets (cliquez [ici](https://github.com/etalab-ia/open_ML/blob/main/docs/explain_automodels/Guide%20au%20AutoML%20Leaderboard%20report.md) pour mieux comprendre ces résultats)
 - Des *exemples* simples de code et les réutilisations faites sur data.gouv.fr

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_3f6f170c0eab8a384f823d997235e6e8.png)

 
 ### Libraries utilisées
 
 - [pandas profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/) pour le profiling statistique
 - [mljar-supervised](https://supervised.mljar.com/) pour l'entraînement et test automatique des algortihmes de Machine Learning
 
 ### Ressources
 
 - [Machine Learning on open datasets](https://zenodo.org/record/4739309#.YJO3DCaxXK4)
 - [Catalogue de jeux de données pour le Machine Learning sur data.gouv.fr]()
