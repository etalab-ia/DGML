import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
from sklearn.impute import SimpleImputer
import IPython
import markdown

#dataset:DVF
#task: regression
#target variable: Valeur fonciere

url_2020 = "https://www.data.gouv.fr/fr/datasets/r/90a98de0-f562-4328-aa16-fe0dd1dca60f"
data_2020 = pd.read_csv(url_2020, sep='|')  #dataframe des demandes de valeurs foncières du premier trimestre de 2020

#Pandas profiling
profiling = data_2020.profile_report()
profiling.to_file("90a98de0-f562-4328-aa16-fe0dd1dca60f.html")

#drop columns with >90% missing values & columns identified as unsupported by Pandas profiling
data_2020 = data_2020.drop(columns=[col for col in data_2020.columns if data_2020[col].isna().sum()/len(data_2020)>0.9])
data_2020 = data_2020.drop(columns=['1er lot','Code departement'])

#set proper target variable type
data_2020['Valeur fonciere'] = data_2020['Valeur fonciere'].str.replace(',', '.', regex=True)
data_2020['Valeur fonciere'] = data_2020['Valeur fonciere'].astype(float)

#handle target variable missing values
data_2020 = data_2020[data_2020['Valeur fonciere'].isna()==False]

#categorical variables
categorical_features = ['Nature culture', 'Type local','Code type local', 'Nature mutation']

for c in categorical_features:
    data_2020[c] = data_2020[c].astype('category').cat.codes

#missing values imputation(scikit-learn sipleimputer with most_frequent strategy)

imp = SimpleImputer(strategy="most_frequent")
data_2020[['Type de voie', 'Type local', 'Surface reelle bati', 'Nombre pieces principales', 'Nature culture',
             'Surface terrain']]=imp.fit_transform(data_2020[['Type de voie','Type local','Surface reelle bati','Nombre pieces principales','Nature culture','Surface terrain']])

#automl
y = data_2020['Valeur fonciere'].values
X = data_2020.drop(columns=['Valeur fonciere'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

automl = AutoML(total_time_limit=6*60,mode='Explain',random_state=42)
automl.fit(X_train,y_train)

predictions = automl.predict(X_test)

#generate html report
automl.report()

