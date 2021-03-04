import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown

#dataset: Données carroyées
#task: Regression
#target variable: Log_soc


path_metr = '/home/giulia/Desktop/backup/data/Filosofi2015_carreaux_niveau_naturel_metropole.csv'
carreaux_metr = pd.read_csv(path_metr)

#Pandas profiling
profiling = carreaux_metr.profile_report()
profiling.to_file("donnes_carroyees.html")


carreaux_metr = carreaux_metr.drop(columns=['Ind_inc','Log_inc'])  #drop columns contaning the 'missing values' of the dataset


y = carreaux_metr['Log_soc'].values
X = carreaux_metr.drop(columns=['Log_soc'])

#automl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

automl = AutoML(total_time_limit=5*60, mode='Explain',random_state=42)
automl.fit(X_train,y_train)
predictions = automl.predict(X_test)

#generate report
automl.report()