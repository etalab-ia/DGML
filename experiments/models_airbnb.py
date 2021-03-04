import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown



#dataset: airbnb_bordeaux
#task:regression
#target variable: PrixNuitée

url = "https://www.data.gouv.fr/fr/datasets/r/123e1c18-37e0-4147-ad65-768320387800"
data_airbnb = pd.read_csv(url)
data_airbnb = data_airbnb.drop(columns=['prix_nuitee']) #remove redundant column
data_airbnb = data_airbnb.drop(columns=['Url','Resume','Shampooing']) #remove useless columns

#Pandas profiling
profiling = data_airbnb.profile_report()
profiling.to_file("data_airbnb.html")

#automl

y = data_airbnb['PrixNuitee'].values
X = data_airbnb.drop(columns=['PrixNuitee'])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


automl = AutoML(total_time_limit=5*60, mode='Explain')
automl.fit(X_train,y_train)

predictions = automl.predict(X_test)

#generate html report
automl.report()






