import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown

#dataset:impacte_aliments
#task: regression
#target variable:DQR - Note de qualité de la donnée (1 excellente ; 5 très faible)

url = 'https://www.data.gouv.fr/fr/datasets/r/c763b24a-a0fe-4e77-9586-3d5453c631cd'
data_agrib = pd.read_csv(url)

#Pandas Profiling

profiling = data_agrib.profile_report()
profiling.to_file("impacte_aliments.html")

#drop id column
data_agrib = data_agrib.drop(columns=['Code AGB','Code CIQUAL'])

#fit model
y = data_agrib["DQR - Note de qualité de la donnée (1 excellente ; 5 très faible)"].values
X = data_agrib.drop(columns=["DQR - Note de qualité de la donnée (1 excellente ; 5 très faible)"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,random_state=42)

automl = AutoML(total_time_limit=5*60,mode='Explain',random_state=42,ml_task='regression')
automl.fit(X_train, y_train)
predictions = automl.predict(X_test)

#generate report
automl.report()