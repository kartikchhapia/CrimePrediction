from sklearn import neural_network
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import ensemble
from sklearn import model_selection
from sklearn import preprocessing
import math
from sklearn.utils import shuffle
from scipy.stats import randint as sp_randint
from sklearn import svm
from prepareData import get_data
from prepareData import lassoFS

#%%

X,y,colNames = get_data()
X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.3,random_state=0)
X_train,X_test,colNames = lassoFS(X_train,y_train,X_test,y_test,colNames)

#%% Neural net + grid serach
#reg = neural_network.MLPRegressor(hidden_layer_sizes=(50, ), 
#                           activation='relu', solver='lbfgs', 
#                           alpha=0.0001, batch_size='auto', 
#                           learning_rate='adaptive', 
#                           learning_rate_init=0.001, 
#                           power_t=0.5, max_iter=2000, 
#                           shuffle=True, random_state=0, 
#                           tol=0.0001, verbose=False, 
#                           warm_start=False, momentum=0.9,
#                           nesterovs_momentum=True)
#
#
#param_grid = {'alpha':[0.001,0.001],'hidden_layer_sizes':[40,50,60],'activation':['logistic'],'solver':['lbfgs']}
#gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None, 
#                             refit=True, cv=3, verbose=2,
#                             return_train_score=True)
#%% Neural net + randomized search
#reg = neural_network.MLPRegressor(hidden_layer_sizes=(50, ), 
#                           activation='relu', solver='lbfgs', 
#                           alpha=0.0001, batch_size='auto', 
#                           learning_rate='adaptive', 
#                           learning_rate_init=0.001, 
#                           power_t=0.5, max_iter=2000, 
#                           shuffle=True, random_state=0, 
#                           tol=0.0001, verbose=False, 
#                           warm_start=False, momentum=0.9,
#                           nesterovs_momentum=True)
#
##hls = []
##for i in range(2,100):
##    for j in range(2,100):
##        hls.append((i,j))
#
#
#param_dist = {"hidden_layer_sizes": range(2,100),
#              "activation": ['relu','logistic'],
#              'alpha':[0.001,0.01,0.0001],}
#
#gscv = model_selection.RandomizedSearchCV(reg, param_dist, n_iter=20, 
#                                   scoring=None, fit_params=None, n_jobs=1, 
#                                   iid=True, refit=True, cv=None, verbose=2, 
#                                   pre_dispatch='2*n_jobs', random_state=None,
#                                   error_score='raise', return_train_score=True)


#%% SVM + grid search
#reg = svm.SVR()
#param_grid = {'C': [1000,10000,20000,50000],
#              'epsilon': [0.1],
#              'gamma': np.exp2(range(-10,-6)),
#                              }
#
#gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None, 
#                             refit=True, cv=3, verbose=2,
#                             return_train_score=True)

#%% GBT
#reg = ensemble.GradientBoostingRegressor(n_estimators=100)
#
#param_grid = {'max_depth':[4],
#              'max_features':[20]
#              }
#
#gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None, 
#                             refit=True, cv=3, verbose=2,
#                             return_train_score=True)
#%% Lasso
#reg = linear_model.LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)
#param_grid = {}
#gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None, 
#                             refit=True, cv=3, verbose=2,
#                             return_train_score=True)

#%%
gscv.fit(X_train,y_train)
reg = gscv.best_estimator_
print reg
#%%

reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
MAE = sum(np.abs(y_pred-y_test))/float(len(y_pred))
RMSE = np.sqrt(sum(np.abs(y_pred-y_test)**2)/float(len(y_pred)))
#%%
