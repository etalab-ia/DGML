import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML

df = pd.read_csv("/home/pavel/Downloads/Agribalyse_Synthese(3).csv")
y = df["DQR - Note de qualité de la donnée (1 excellente ; 5 très faible)"].values
df.pop("DQR - Note de qualité de la donnée (1 excellente ; 5 très faible)")

X = df
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

automl = AutoML(total_time_limit=5*60)
automl.fit(X_train, y_train)