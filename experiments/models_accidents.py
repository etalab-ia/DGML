import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown

#dataset:accidents_routiers
#task: classification
#target variable: grav

#import data from community resources
data = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/6af37c98-0933-4ae4-8380-5f63212fb52a',index_col=0)

#Pandas profiling:

#profile_accidents_routiers = data.profile_report()
#profile_accidents_routiers.to_file("accidents_routiers.html")

#modify lat and long columns
data['lat'] = data['lat'].str.replace(',', '.', regex=True)
data['lat'] = data['lat'].astype(float)
data['long'] = data['long'].str.replace(',', '.', regex=True)
data['long'] = data['long'].astype(float)

#generate two new columns for the time of the accident

def hour(n):
    n=str(n)
    if len(n)<4:
        n='0'+n
    return int(n[:2])

data['heure']=data['hrmn'].apply(hour)
data['mom_acc']=pd.to_datetime(pd.DataFrame({'year': data['an'],'month': data['mois'],'day': data['jour'],'hour':data['heure']}))

#new variable for the day of the week
data['jour_semaine']=data['mom_acc'].dt.dayofweek

#select features

features = ['place','catu','sexe','trajet','secu1','secu2','secu3','locp',
            'catv','an_nais','mois',
            'occutc','obs','obsm','choc','manv',
            'lum','agg','int','atm','col',
            'catr','circ','vosp','prof','plan',
            'surf','infra','situ','lat','long','heure','mom_acc','jour_semaine']

#fit model
y = data['grav'].values
X = data[features]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

automl = AutoML(algorithms=['Random Forest', 'Xgboost', 'Decision Tree', 'Baseline', 'Linear'],mode='Explain',random_state=42,explain_level=0)
automl.fit(X_train,y_train)

predictions = automl.predict(X_test)

#generate html report
automl.report()

