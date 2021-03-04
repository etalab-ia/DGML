import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
from sklearn.preprocessing import StandardScaler
import IPython
import markdown


#task 2: classification
#target variable: Marque

emissions_2013 = "https://www.data.gouv.fr/fr/datasets/r/6ff09b59-84ca-4346-a8d1-3587ed94da15"
data_2013=pd.read_csv(emissions_2013,encoding='latin-1',compression='zip',error_bad_lines=False,sep=";")

#Pandas profiling
profiling = data_2013.profile_report()
profiling.to_file("emissions_vehicules_2013.html")

data_2013 = data_2013.drop(columns = ['Date de mise à jour','Désignation commerciale', 'CNIT','Type Variante Version (TVV)','Modèle UTAC','Modèle dossier','Champ V9'])

categorical_features = ['Carburant', 'Marque','Hybride','Boîte de vitesse','Carrosserie', 'gamme']

for c in categorical_features:
    data_2013[c] = data_2013[c].astype('category').cat.codes


#automl
y_class = data_2013['Marque'].values
X_class = data_2013.drop(columns=['Marque'])
X_class = StandardScaler().fit_transform(X_class)

X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(X_class, y_class, test_size=0.25, random_state=42)


automl_class = AutoML(total_time_limit=5*60,mode='Explain',random_state=42,ml_task='multiclass_classification')
automl_class.fit(X_train_class,y_train_class)

predictions_class = automl_class.predict(X_test_class)

#generate html report
automl.report()