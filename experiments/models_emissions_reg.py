import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown

#dataset: emissions_vehicules_france 2013
#task 1: regression
#target variable 1: CO2

emissions_2013 = "https://www.data.gouv.fr/fr/datasets/r/6ff09b59-84ca-4346-a8d1-3587ed94da15"
data_2013=pd.read_csv(emissions_2013,encoding='latin-1',compression='zip',error_bad_lines=False,sep=";")

data_2013 = data_2013[data_2013['CO2 (g/km)'].isna()==False] #handle NaN in target variable
data_2013 = data_2013.drop(columns=['Date de mise à jour']) #drop useless column


#automl

y = data_2013['CO2 (g/km)'].values
X = data_2013.drop(columns=['CO2 (g/km)'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

automl = AutoML(total_time_limit=5*60,mode='Explain',random_state=42,ml_task='regression')
automl.fit(X_train,y_train)
predictions = automl.predict(X_test)

#generate report
automl.report()


