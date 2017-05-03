import pickle
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
from prepare_data import get_cleaned_data, get_cleaned_landmarks_data, get_cleaned_census_data, lasso_fs
from sklearn.metrics import mean_squared_error, mean_absolute_error

#%%

def train_nn():
    x, y, col_names = get_cleaned_data()
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state=0)
    x_train, x_test, col_names = lasso_fs(x_train, y_train, x_test, y_test, col_names)

    #%% Neural net + grid serach
    reg = neural_network.MLPRegressor(
        hidden_layer_sizes=(50, ),
        activation='relu', solver='lbfgs',
        alpha=0.0001, batch_size='auto',
        learning_rate='adaptive',
        learning_rate_init=0.001,
        power_t=0.5, max_iter=2000,
        shuffle=True, random_state=0,
        tol=0.0001, verbose=False,
        warm_start=False, momentum=0.9,
        nesterovs_momentum=True
    )


    param_grid = {
        'alpha': [0.001, 0.01],
        'hidden_layer_sizes': [40, 50, 60],
        'activation': ['logistic'],
        'solver': ['lbfgs']
    }
    gscv = model_selection.GridSearchCV(reg, param_grid, scoring='neg_mean_absolute_error',fit_params=None,
                                        refit=True, cv=3, verbose=2,
                                        return_train_score=True)
    #%% Neural net + randomized search
    reg_rn = neural_network.MLPRegressor(
        hidden_layer_sizes=(50, ),
        activation='relu', solver='lbfgs',
        alpha=0.0001, batch_size='auto',
        learning_rate='adaptive',
        learning_rate_init=0.001,
        power_t=0.5, max_iter=2000,
        shuffle=True, random_state=0,
        tol=0.0001, verbose=False,
        warm_start=False, momentum=0.9,
        nesterovs_momentum=True
    )

    param_dist = {"hidden_layer_sizes": range(2, 100),
                 "activation": ['relu', 'logistic'],
                 'alpha':[0.001, 0.01, 0.0001],}

    rscv = model_selection.RandomizedSearchCV(reg_rn, param_dist, n_iter=20,
                                      scoring='neg_mean_absolute_error', fit_params=None, n_jobs=1,
                                      iid=True, refit=True, cv=None, verbose=2,
                                      pre_dispatch='2*n_jobs', random_state=None,
                                      error_score='raise', return_train_score=True)

    print 'Using grid search CV'
    gscv.fit(x_train, y_train)
    reg = gscv.best_estimator_
    print reg

    reg.fit(x_train, y_train)
    y_pred = reg.predict(x_test)
    mae_n = mean_absolute_error(y_pred, y_test)
    rmse_n = np.sqrt(mean_squared_error(y_pred, y_test))
    print 'MAE', mae_n
    print 'RMSE', rmse_n

    print 'Using random search CV'
    rscv.fit(x_train, y_train)
    reg_rn = rscv.best_estimator_
    print reg_rn
    reg_rn.fit(x_train, y_train)
    y_pred = reg_rn.predict(x_test)
    mae = mean_absolute_error(y_pred, y_test)
    rmse = np.sqrt(mean_squared_error(y_pred, y_test))
    print 'MAE', mae
    print 'RMSE', rmse
    nn_res = {
        'rcv_mae': mae_n,
        'rcv_rmse': rmse_n,
        'gcv_mae': mae,
        'gcv_rmse': rmse
    }
    pickle.dump(nn_res, open("results/nn_res.p", "wb"))


def train_svm():
    x, y, col_names = get_cleaned_data()
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state=0)
    x_train, x_test, col_names = lasso_fs(x_train, y_train, x_test, y_test, col_names)
    reg = svm.SVR()
    param_grid = {
        'C': [1000,10000,20000,50000],
        'epsilon': [0.1],
        'gamma': np.exp2(range(-10,-6))
    }

    gscv = model_selection.GridSearchCV(reg, param_grid, scoring='neg_mean_absolute_error',fit_params=None,
                                refit=True, cv=3, verbose=2,
                                return_train_score=True)
    print 'SVM: Using grid search CV'
    gscv.fit(x_train, y_train)
    reg = gscv.best_estimator_
    print reg

    reg.fit(x_train, y_train)
    y_pred = reg.predict(x_test)
    mae = mean_absolute_error(y_pred, y_test)
    rmse = np.sqrt(mean_squared_error(y_pred, y_test))
    print 'MAE', mae
    print 'RMSE', rmse
    svm_res = {
        'mae': mae,
        'rmse': rmse
    }
    pickle.dump(svm_res, open("results/svm_res.p", "wb"))


def train_gbt():
    data_config = {
        'landmarks': get_cleaned_landmarks_data,
        'census': get_cleaned_census_data,
        'both': get_cleaned_data
    }
    for data_subset, data_method in data_config.items():
        x, y, col_names = data_method()
        x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state=0)
        x_train, x_test, col_names = lasso_fs(x_train, y_train, x_test, y_test, col_names)
        reg = ensemble.GradientBoostingRegressor(n_estimators=100)
        if data_subset == 'landmarks':
            param_grid = {
                'max_depth':[2, 4, 6, 8, 10, 12, 14, 16, 18],
                'max_features':[5, 8, 10]
            }
        else:
            param_grid = {
                'max_depth': [2, 4, 6, 8, 10, 12, 14, 16, 18],
                'max_features': [5, 10, 15, 20, 25, 30, 35, 40]
            }
        gscv = model_selection.GridSearchCV(reg, param_grid, scoring='neg_mean_absolute_error',fit_params=None,
                                    refit=True, cv=3, verbose=0,
                                    return_train_score=True)
        print 'GBT: Using grid search CV {}'.format(data_subset)
        gscv.fit(x_train, y_train)
        reg = gscv.best_estimator_
        print reg
        if data_subset == 'both':
            pickle.dump(gscv.cv_results_, open("hpopt/gbt_cvresults.p", "wb"))
            pickle.dump(reg.feature_importances_, open("featimp/gbt_featimps.p", "wb"))
        reg.fit(x_train, y_train)
        y_pred = reg.predict(x_test)
        mae = mean_absolute_error(y_pred, y_test)
        rmse = np.sqrt(mean_squared_error(y_pred, y_test))
        print 'MAE', mae
        print 'RMSE', rmse
        gbtres = {
            'mae': mae,
            'rmse': rmse
        }
        pickle.dump(gbtres, open("results/gbt_res_{}.p".format(data_subset), "wb"))


def train_linreg():
    fs = True
    data_config = {
        'landmarks': get_cleaned_landmarks_data,
        'census': get_cleaned_census_data,
        'both': get_cleaned_data
    }
    for data_subset, data_method in data_config.items():
        x, y, col_names = data_method()
        x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state=0)
        if fs:
            x_train, x_test, col_names = lasso_fs(x_train, y_train, x_test, y_test, col_names)

        reg = linear_model.LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)
        print 'Linear Regression {}'.format(data_subset)

        reg.fit(x_train, y_train)
        y_pred = reg.predict(x_test)
        featimp = np.abs(reg.coef_) / np.sum(np.abs(reg.coef_))
        pickle.dump(featimp, open("featimp/lr_featimps.p", "wb"))
        mae = mean_absolute_error(y_pred, y_test)
        rmse = np.sqrt(mean_squared_error(y_pred, y_test))
        print 'MAE', mae
        print 'RMSE', rmse
        lrres = {
            'mae': mae,
            'rmse': rmse
        }
        fs_str = '' if fs else 'wo_fs'
        pickle.dump(lrres, open("results/lr_res_{}_{}.p".format(data_subset, fs_str), "wb"))


def train_rf():
    fs = False
    data_config = {
        # 'landmarks': get_cleaned_landmarks_data,
        # 'census': get_cleaned_census_data,
        'both': get_cleaned_data
    }
    for data_subset, data_method in data_config.items():
        x, y, col_names = data_method()
        x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3, random_state=0)
        if fs:
            x_train, x_test, col_names = lasso_fs(x_train, y_train, x_test, y_test, col_names)

        reg = ensemble.RandomForestRegressor(n_estimators=100, random_state=0)  # changeable
        if data_subset == 'landmarks':
            param_grid = {
                'max_depth':[2, 4, 6, 8, 10, 12, 14, 16, 18],
                'max_features':[5, 8, 10]
            }
        else:
            param_grid = {
                'max_depth': [2, 4, 6, 8, 10, 12, 14, 16, 18],
                'max_features': [5, 10, 15, 20, 25, 30, 35, 40]
            }
        gscv = model_selection.GridSearchCV(reg, param_grid, scoring='neg_mean_absolute_error', fit_params=None,
                                            refit=True, cv=3, verbose=0,
                                            return_train_score=True)
        print 'Random forest: Using grid search CV {}'.format(data_subset)
        gscv.fit(x_train, y_train)
        reg = gscv.best_estimator_
        if data_subset == 'both' and fs:
            pickle.dump(gscv.cv_results_, open("hpopt/rf_cvresults.p", "wb"))
            pickle.dump(reg.feature_importances_, open("featimp/rf_featimps.p", "wb"))
        print reg

        reg.fit(x_train, y_train)
        y_pred = reg.predict(x_test)
        mae = mean_absolute_error(y_pred, y_test)
        rmse = np.sqrt(mean_squared_error(y_pred, y_test))
        print 'MAE', mae
        print 'RMSE', rmse
        rfres = {
            'mae': mae,
            'rmse': rmse
        }
        fs_str = '' if fs else 'wo_fs'
        pickle.dump(rfres, open("results/rf_res_{}_{}.p".format(data_subset, fs_str), "wb"))


if __name__ == '__main__':
    pass
    # train_nn()
    # train_svm()
    # train_gbt()
    train_linreg()
    # train_rf()
