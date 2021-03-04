import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import io
import requests
import IPython
import markdown

#task: classification
#target variable: Synthese_eval_sanit
url_cont_san = "https://www.data.gouv.fr/fr/datasets/r/fff0cc27-977b-40d5-9c11-f7e4e79a0b72" #données brutes en csv
r = requests.get(url_cont_san,allow_redirects=True)
df=pd.read_csv(io.StringIO(r.content.decode('utf-8')), sep=';')

#Pandas Profiling

profiling = df.profile_report()
profiling.to_file("fff0cc27-977b-40d5-9c11-f7e4e79a0b72.html.html")

#filtre variable: selecting only one filtre when more than one is given

df['filtre'] = df['filtre'].str.split('\|').str[0]

#handle latitude and longitude
df['latitude'] = df['geores'].str.split(',').str[0].astype(float)
df['longitude'] = df['geores'].str.split(',').str[1].astype(float)

#handle target variable
df['Synthese_eval_sanit'] = df['Synthese_eval_sanit'].astype('category').cat.codes


#feature engineering (code partially taken from here: https://colab.research.google.com/drive/1OgqIFNCkEi4YL9Xr7R0yegWbhZGG0HiV#scrollTo=YkR83PK6V_Nr)

df['has_agrement'] = pd.notnull(df['Agrement']).astype(int)


df['dept'] = [int(r[:2]) for r in df['Code_postal']]

df['Date_inspection'] = pd.to_datetime(df['Date_inspection'], format='%Y-%m-%dT%H:%M:%S', utc=True)

df['year'] = df['Date_inspection'].dt.year
df['month'] = df['Date_inspection'].dt.month
df['weekday'] = df['Date_inspection'].dt.weekday

df['count_controls_dept'] = df.groupby('dept')['Synthese_eval_sanit'].transform(lambda x: x.count())
df['score_controls_dept'] = df.groupby('dept')['Synthese_eval_sanit'].transform(lambda x: x.mean())

df['filtre'] = df['filtre'].fillna('NA')
df['count_controls_filtre'] = df.groupby('filtre')['Synthese_eval_sanit'].transform(lambda x: x.count())
df['score_controls_filtre'] = df.groupby('filtre')['Synthese_eval_sanit'].transform(lambda x: x.mean())
df['ods_type_activite'] = df['ods_type_activite'].fillna('NA')
df['count_controls_activite'] = df.groupby('ods_type_activite')['Synthese_eval_sanit'].transform(lambda x: x.count())
df['score_controls_activite'] = df.groupby('ods_type_activite')['Synthese_eval_sanit'].transform(lambda x: x.mean())

df['count_controls_wday'] = df.groupby('weekday')['Synthese_eval_sanit'].transform(lambda x: x.count())
df['score_controls_wday'] = df.groupby('weekday')['Synthese_eval_sanit'].transform(lambda x: x.mean())

#drop useless variables

drop_cols = ['APP_Libelle_etablissement', 'Code_postal', 'SIRET', 'Libelle_commune',
             'APP_Libelle_activite_etablissement', 'Numero_inspection', 'Date_inspection',
             'Agrement', 'geores', 'ods_type_activite','Adresse_2_UA']
df = df.drop(drop_cols, axis=1)


#handle other categorical features
categorical_features = ['dept', 'filtre', 'month', 'weekday']

for c in categorical_features:
    df[c] = df[c].astype('category').cat.codes


#fit model

y = df['Synthese_eval_sanit'].values
X = df.drop(columns = ['Synthese_eval_sanit'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

automl = AutoML(total_time_limit=5*60,mode='Explain',random_state=42)
automl.fit(X_train,y_train)

predictions = automl.predict(X_test)
#generate report
automl.report()