import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown

#dataset:concentration_pollution
#task: classification
#target variable: nom_pollu

url = 'https://www.data.gouv.fr/fr/datasets/r/ce203343-6ed9-4fd3-b310-e553ae437f6d'
data_conc_pollu = pd.read_csv(url,sep=';')

#Pandas profiling
profiling = data_conc_pollu.profile_report()
profiling.to_file("concentration_pollution.html")

#drop rows if "statut_valid" = 0 (i.e. data are not exploitable)

data_conc_pollu = data_conc_pollu[data_conc_pollu['statut_valid']==1]

#create latitude and logitude columns

data_conc_pollu['lat'] = data_conc_pollu['geo_point_2d'].str.split(',').str[0].astype(float)
data_conc_pollu['long'] = data_conc_pollu['geo_point_2d'].str.split(',').str[1].astype(float)

#drop unsupported columns, one useless column and two redundant columns


#handling categorical variables
categorical_var = ['nom_com','insee_com','nom_station','code_station','typologie','influence','nom_poll','id_poll_ue']
for c in categorical_var:
    data_conc_pollu[c] = data_conc_pollu[c].astype('category').cat.codes

#handling datatime variables
data_conc_pollu['date_debut'] = pd.to_datetime(data_conc_pollu['date_debut'],format='%Y-%m-%dT%H:%M:%S', utc=True)
data_conc_pollu['date_fin'] = pd.to_datetime(data_conc_pollu['date_fin'],format='%Y-%m-%dT%H:%M:%S', utc=True)

data_conc_pollu['jour_semaine_debut'] = data_conc_pollu['date_debut'].dt.weekday
data_conc_pollu['jour_semaine_fin'] = data_conc_pollu['date_fin'].dt.weekday
data_conc_pollu['jour_debut'] = data_conc_pollu['date_debut'].dt.day
data_conc_pollu['jour_fin'] = data_conc_pollu['date_fin'].dt.day
data_conc_pollu['heure_debut'] = data_conc_pollu['date_debut'].dt.hour
data_conc_pollu['heure_fin'] = data_conc_pollu['date_fin'].dt.hour
data_conc_pollu['minute_debut'] = data_conc_pollu['date_debut'].dt.minute
data_conc_pollu['minute_fin'] = data_conc_pollu['date_fin'].dt.minute

#drop cols

data_conc_pollu = data_conc_pollu.drop(columns=['nom_dept','metrique','unite','code_epci','statut_valid','geo_shape','geo_point_2d','date_debut','date_fin'])


#automl

y = data_conc_pollu['nom_poll'].values
X = data_conc_pollu.drop(columns=['nom_poll','id_poll_ue'])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

automl = AutoML(total_time_limit=5*60,mode='Explain',random_state=42)
automl.fit(X_train,y_train)

predictions = automl.predict(X_test)

#generate report
automl.report()

