# DGML (Data Gouv for Machine Learning)

DGML is a **data repository for Machine Learning** using open data from **data.gouv.fr**.


:link: [datascience.etalab.studio/dgml/](https://datascience.etalab.studio/dgml/)

Open Data, such as the data on data.gouv.fr, is sometimes neglected in Machine Learning applications, since it can be hard to identify, among thousands of datasets, those that would be adequate for Machine Learning.
In DGML, you can **quickly choose a dataset from data.gouv.fr for Machine Learning** and **check all the informations you might need to do a Machine Learning application**.

 ### In DGML you find:
 
 - 60 datasets for Machine Learning (click [here]() for more info about the choice of datasets), that you can filter according to a ML task, size of the dataset etc.

 
 For each of these datasets you find:
 - A statistical profile, quickly showing you some statistics about the dataset, the distribution of its variables, of its missing values and correlations
 - The results of the automatic training and testing of a set of ML algorithms on a target variable of the dataset (click [here]() to better understand these results)
 - Simple examples of code and existing applications on data.gouv.fr

![](https://storage.gra.cloud.ovh.net/v1/AUTH_0f20d409cb2a4c9786c769e2edec0e06/imagespadincubateurnet/uploads/upload_3f6f170c0eab8a384f823d997235e6e8.png)

### How to use this repo locally
 
 1. Clone/Fork the repo (more information [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository))
 2. Install requirements from `requirements.txt`:
     - Using pip: `pip install -r requirements.txt`
     - Using conda:`conda env create --name envname --file=environment.yml`

To launch the app from your command line, from root:

`cd openml_app`

`python main.py`

### Libraries 
 
 - [pandas profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/) for the statistical profiling
 - [mljar-supervised](https://supervised.mljar.com/) for the automatic training and testing of algorithms
 
 ### Ressources
 
 - [Machine Learning on open datasets](https://zenodo.org/record/4739309#.YJO3DCaxXK4)
 - [Catalogue de jeux de données pour le Machine Learning sur data.gouv.fr]()

