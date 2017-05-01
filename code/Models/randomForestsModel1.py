from sklearn import neural_network
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import ensemble
from sklearn import model_selection
from sklearn import preprocessing
import math
from sklearn.utils import shuffle
from prepareData import get_data
from prepareData import lassoFS

#%%
X,y,colNames = get_data()
X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.3,random_state=0)
X_train,X_test,colNames = lassoFS(X_train,y_train,X_test,y_test,colNames)

#%%
reg = ensemble.RandomForestRegressor(n_estimators=500,random_state=0)
#param_grid = {'max_depth':[8,9,10,11,12,13,14],'max_features':[5,10,20,40,80,100]}
param_grid = {'max_depth':[12],'max_features':[40]}

gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None, 
                             refit=True, cv=3, verbose=2,
                             return_train_score=True)
gscv.fit(X_train,y_train)
print ('best hyper params:' + str(gscv.best_params_['max_depth']) +','+
       str(gscv.best_params_['max_features']))
#%%
reg = gscv.best_estimator_
print reg
reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
MAE = sum(np.abs(y_pred-y_test))/float(len(y_pred))
RMSE = np.sqrt(sum(np.abs(y_pred-y_test)**2)/float(len(y_pred)))