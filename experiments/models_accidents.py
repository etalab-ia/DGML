import pandas as pd
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown

#dataset:accidents_routiers
#task: classification
#target variable: grav

#import data and merge in an unique dataset
carac = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/e22ba475-45a3-46ac-a0f7-9ca9ed1e283a',sep=';')
lieux = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/2ad65965-36a1-4452-9c08-61a6c874e3e6',sep=';')
veh = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/780cd335-5048-4bd6-a841-105b44eb2667',sep=';')
usag = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/36b1b7b3-84b4-4901-9163-59ae8a9e3028',sep=';')

a=pd.merge(usag,veh,on='Num_Acc')
b=pd.merge(a,carac,on='Num_Acc')

data=pd.merge(b,lieux,on='Num_Acc')

#Pandas profiling:

profile_accidents_routiers = data.profile_report()
profile_accidents_routiers.to_file("accidents_routiers.html")

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

