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

#%%

def get_data():
    df = pd.read_csv('../../data/TestDataSet/crime_landmarks_census.csv', index_col=0)
    df = df[df.total_population != 0]
    df = df[df.hous_units != 0]
    dataset=df.values
    #Delete Nan columns
    colNames = np.array(df.columns).astype(str)
    colNames = np.delete(colNames,[5,23,32])
    colNames = colNames[5:]
    #Delete Nan columns
    dataset = np.delete(dataset,[5,23,32],1)
    label = dataset[:,2:5]
    y = map(lambda x: x[0]+x[1]+x[2],label)
    X = dataset[:,5:]
    # scale & shuffle
    X,y = shuffle(X,y,random_state=0)
    scaler = preprocessing.StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(X)
    X = scaler.transform(X)
    #add features
    X,colNames = add_features(X,colNames)
    return (X,y,colNames)

#%%
def lassoFS(X_train,y_train,X_test,y_test,colNames):
    reg = linear_model.Lasso(alpha=1.0, fit_intercept=True, normalize=False, 
                       precompute=False, copy_X=True, max_iter=1000, 
                       random_state=0)
    param_grid = {'alpha' : range(10)}
    gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None, 
                                 refit=True, cv=3, verbose=2,
                                 return_train_score=True)
    gscv.fit(X_train,y_train)
    reg = gscv.best_estimator_
    badFeatures = np.where(np.abs(reg.coef_)<0.1)
    X_train = np.delete(X_train,badFeatures,axis=1)
    X_test  = np.delete(X_test,badFeatures,axis=1)
    colNames = np.delete(colNames,badFeatures)
    print(str(len(colNames)) + ' features preserved')
    return (X_train,X_test,colNames)
    
                                            
#%% Helpers

def add_features(X,colNames):
    
    newCols = ['%houses vacant',
               '%houses occupied',
               '%unemployed',
               '%in labour force',
               '% employed',
               'labor force/ employed',
               'Families per capita',
               'Families per housing unit',
               'Houses per capita',
               ' % owned clear',
               '% owned with mortage',
               '% renter occupied',
               '% non family households',
               '%black',
               '%white',
               '%asian',
               '%other',
               'Total females',
               'Total Males',
               'Sex ratio',
               'F/M below 10',
               'F/M 10-17',
               'F/M 18-24',
               'F/M 25-35',
               'F/M 35-60',
               'F/M 60+']
    colNames = np.append(colNames,newCols)
      
    newFeatures = np.zeros([X.shape[0],26])
    newFeatures[:,0]  = X[:,22]/X[:,21]
    newFeatures[:,1]  = X[:,20]/X[:,21]
    newFeatures[:,2]  = X[:,83]/X[:,82]
    newFeatures[:,3]  = X[:,13]/X[:,82]
    newFeatures[:,4]  = X[:,14]/X[:,82]
    newFeatures[:,5]  = X[:,13]/X[:,14]
    newFeatures[:,6]  = X[:,16]/X[:,82]
    newFeatures[:,7]  = X[:,16]/X[:,21]
    newFeatures[:,8]  = X[:,21]/X[:,82]
    newFeatures[:,9]  = X[:,26]/X[:,21]
    newFeatures[:,10] = X[:,27]/X[:,21]
    newFeatures[:,11] = X[:,14]/X[:,82]
    newFeatures[:,12] = (X[:,17]+X[:,19])/X[:,21]
    newFeatures[:,13] = X[:,30]/X[:,82]
    newFeatures[:,14] = X[:,34]/X[:,82]
    newFeatures[:,15] = X[:,28]/X[:,82]
    newFeatures[:,16] = X[:,32]/X[:,82]
    newFeatures[:,17] = np.sum(X[:,36:58],axis=1)/X[:,82]
    newFeatures[:,18] = np.sum(X[:,50:82],axis=1)/X[:,82]
    newFeatures[:,19] = newFeatures[:,18]/newFeatures[:,17]
    newFeatures[:,20] = (X[:,49]+X[:,58])/(X[:,72]+X[:,81])
    newFeatures[:,21] = np.sum(X[:,36:38],axis=1)/np.sum(X[:,59:61],axis=1)
    newFeatures[:,22] = np.sum(X[:,38:42],axis=1)/np.sum(X[:,61:65],axis=1)
    newFeatures[:,23] = np.sum(X[:,42:44],axis=1)/np.sum(X[:,65:67],axis=1)
    newFeatures[:,24] = np.sum(X[:,44:49],axis=1)/np.sum(X[:,67:72],axis=1)
    newFeatures[:,25] = np.sum(X[:,50:58],axis=1)/np.sum(X[:,73:81],axis=1)
    
    X = np.hstack([X,newFeatures])
    scaler = preprocessing.StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(X)
    X = scaler.transform(X)
    return (X,colNames)

#%%

if __name__ == '__main__':
    X,y,colNames = get_data()
    X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.3,random_state=0)
    X_train,X_test,colNames = lassoFS(X_train,y_train,X_test,y_test,colNames)