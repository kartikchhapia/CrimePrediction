import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import ensemble
from sklearn import model_selection
from sklearn import preprocessing
import math
from sklearn.utils import shuffle

#%%
df = pd.read_csv('../../data/TestDataSet/crime_landmarks_census.csv', index_col=0)
dataset=df.values

#%% Deleting nan columns
dataset = np.delete(dataset,[5,32],1)
label = dataset[:,2:5]
y = map(lambda x: x[0]+x[1]+x[2],label)
X = dataset[:,5:]
X = np.delete(X,[17],1)

#%%
scaler = preprocessing.StandardScaler(copy=True, with_mean=True, with_std=True)
scaler.fit(X)
X = scaler.transform(X)
X,y = shuffle(X,y,random_state=0)
X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.3,random_state=0)

#%% Labels array
colNames = df.columns
colNames = np.delete(colNames,[5,32])
colNames = colNames[5:]
colNames = np.delete(colNames,[17])
#%%
reg = ensemble.RandomForestRegressor(n_estimators=200,random_state=0)
param_grid = {'max_depth':[1,4,8,12,16,20],'max_features':[5,10,20,40,80]}
gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None, 
                             refit=True, cv=3, verbose=2,
                             return_train_score=True)
gscv.fit(X_train,y_train)
print ('best hyper params:' + str(gscv.best_params_['max_depth']) +','+
       str(gscv.best_params_['max_features']))
#%%
reg = gscv.best_estimator_

#%%
#reg = linear_model.Ridge(alpha=0.0)
reg.fit(X_train,y_train)
featureImp = reg.feature_importances_
y_pred = reg.predict(X_test)
MSE = sum(np.abs(y_pred-y_test))/float(len(y_pred))

#%%
predCompare = np.vstack([y_test,y_pred,(y_pred-y_test)])
predCompare = np.transpose(predCompare)

#%%