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


def get_cleaned_data():
    df = pd.read_csv('../../data/TestDataSet/crime_landmarks_census.csv', index_col=0)
    df = df[df.total_population != 0]
    df = df[df.hous_units != 0]
    dataset = df.values

    # Delete Nan columns
    col_names = np.array(df.columns).astype(str)
    col_names = np.delete(col_names, [5, 23, 32])
    col_names = col_names[5:]

    # Delete Nan columns
    dataset = np.delete(dataset, [5, 23, 32], 1)
    label = dataset[:, 2:5]
    y = map(lambda x: x[0]+x[1]+x[2], label)     # Add all three types of crime
    x = dataset[:, 5:]

    # Scale and shuffle
    x, y = shuffle(x, y, random_state=0)
    scaler = preprocessing.StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(x)
    x = scaler.transform(x)

    # Add features
    x, col_names = add_features(x, col_names)
    return x, y, col_names


# %%
def lasso_fs(x_train, y_train, x_test, y_test, col_names):
    reg = linear_model.Lasso(alpha=1.0, fit_intercept=True, normalize=False, 
                       precompute=False, copy_X=True, max_iter=1000, 
                       random_state=0)
    param_grid = {'alpha' : range(10)}
    gscv = model_selection.GridSearchCV(reg, param_grid, scoring=None,fit_params=None,
                                 refit=True, cv=3, verbose=2,
                                 return_train_score=True)
    gscv.fit(x_train, y_train)
    reg = gscv.best_estimator_
    bad_features = np.where(np.abs(reg.coef_)<0.1)
    x_train = np.delete(x_train, bad_features, axis=1)
    x_test = np.delete(x_test, bad_features, axis=1)
    col_names = np.delete(col_names, bad_features)
    print(str(len(col_names)) + ' features preserved')
    return x_train, x_test, col_names
    
#%%

                                            
#%% Helpers
def add_features(x, col_names):
    
    new_cols = [
        '%houses vacant',
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
        'F/M 60+'
    ]
    col_names = np.append(col_names, new_cols)
    # Normalize the column values. For example, replace the number of vacant
    # houses with percentage vacant houses. Do that by dividing vacant houses
    # by the number of total houses.
    new_features = np.zeros([x.shape[0], 26])
    new_features[:,0]  = x[:, 22] / x[:, 21]
    new_features[:,1]  = x[:, 20] / x[:, 21]
    new_features[:,2]  = x[:, 83] / x[:, 82]
    new_features[:,3]  = x[:, 13] / x[:, 82]
    new_features[:,4]  = x[:, 14] / x[:, 82]
    new_features[:,5]  = x[:, 13] / x[:, 14]
    new_features[:,6]  = x[:, 16] / x[:, 82]
    new_features[:,7]  = x[:, 16] / x[:, 21]
    new_features[:,8]  = x[:, 21] / x[:, 82]
    new_features[:,9]  = x[:, 26] / x[:, 21]
    new_features[:,10] = x[:, 27] / x[:, 21]
    new_features[:,11] = x[:, 14] / x[:, 82]
    new_features[:,12] = (x[:, 17] + x[:, 19]) / x[:, 21]
    new_features[:,13] = x[:, 30] / x[:, 82]
    new_features[:,14] = x[:, 34] / x[:, 82]
    new_features[:,15] = x[:, 28] / x[:, 82]
    new_features[:,16] = x[:, 32] / x[:, 82]
    new_features[:,17] = np.sum(x[:, 36:58], axis=1) / x[:, 82]
    new_features[:,18] = np.sum(x[:, 50:82], axis=1) / x[:, 82]
    new_features[:,19] = new_features[:,18]/new_features[:,17]
    new_features[:,20] = (x[:, 49] + x[:, 58]) / (x[:, 72] + x[:, 81])
    new_features[:,21] = np.sum(x[:, 36:38], axis=1) / np.sum(x[:, 59:61], axis=1)
    new_features[:,22] = np.sum(x[:, 38:42], axis=1) / np.sum(x[:, 61:65], axis=1)
    new_features[:,23] = np.sum(x[:, 42:44], axis=1) / np.sum(x[:, 65:67], axis=1)
    new_features[:,24] = np.sum(x[:, 44:49], axis=1) / np.sum(x[:, 67:72], axis=1)
    new_features[:,25] = np.sum(x[:, 50:58], axis=1) / np.sum(x[:, 73:81], axis=1)
    
    x = np.hstack([x, new_features])
    scaler = preprocessing.StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(x)
    x = scaler.transform(x)
    return x, col_names

#%%

if __name__ == '__main__':
    x, y, col_names = get_cleaned_data()
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state=0)
    x_train, x_test, col_names = lasso_fs(x_train, y_train, x_test, y_test, col_names)