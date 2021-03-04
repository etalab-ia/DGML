import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
from sklearn.impute import SimpleImputer
import IPython
import markdown

#dataset: arbres urbains
#task: classification
#target variable: classification_diagnostic

url = 'https://www.data.gouv.fr/fr/datasets/r/96f4164d-956d-4c1c-b161-68724eb0ccdc'
data = pd.read_csv(url)

#Pandas profiling
profiling = df.profile_report()
profiling.to_file("arbres_urbains.html")

#drop useless columns identified by Pandas profiling
data = data.drop(columns=['ID_ARBRE','commune','controle','champignon_collet', 'insecte_collet','champignon_collet', 'insecte_collet','champignon_tronc', 'insecte_tronc',
       'fissure_tronc','ecorce_incluse_houppier','type_delai_1', 'delai_annee_programmation',
       'type_delai_2', 'delai_preconisation_2', 'delai_saison_programmation_2',
       'delai_annee_programmation_2', 'reference_photo'])

#drop columns with more than 80% missing values
data = data.drop(columns=[col for col in data.columns if data[col].isna().sum()/len(data)>0.8])

#imputation of missing values

imp = SimpleImputer(strategy="most_frequent")
data[['cote_voirie', 'prescription_1', 'prescription_2']] = imp.fit_transform(data[['cote_voirie', 'prescription_1', 'prescription_2']])

#automl
y = data['classification_diagnostic'].values
X = data.drop(columns=['classification_diagnostic'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

automl = AutoML(total_time_limit=5*60,mode='Explain',random_state=42)
automl.fit(X_train,y_train)

predictions = automl.predict(X_test)

#generate report
automl.report()
