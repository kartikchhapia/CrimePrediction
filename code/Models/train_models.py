from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.preprocessing import Imputer, StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.feature_selection import SelectKBest, chi2
from store import get_census_train_test_data




def fit_linreg():
    X, Y, cols = get_census_train_test_data()
    linreg = LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)
    linreg.fit(x_train, y_train)
    y_pred = linreg.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    print 'Linear Regression MAE = ', mae


def fit_rf():
    X, Y, cols = get_census_train_test_data()
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.33, random_state = 1)
    rf = RandomForestRegressor()
    rf.fit(x_train, y_train)
    y_pred = rf.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    print [cols[i[0]] for i in sorted(enumerate(rf.feature_importances_), key=lambda x:x[1])]
    print 'Random Forest MAE = ', mae

def fit_svr():
    best_k = 0
    best_mae = 9999999
    for k in range(1, 75):
        X, Y, cols = get_census_train_test_data()
        feat_sel = SelectKBest(chi2, k)
        X = feat_sel.fit_transform(X+10, Y)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)
        svrreg = SVR()
        param_grid = {
            'C': [ 100, 1000, 9000],
            'gamma':[2**-7, 2**-6, 2**-5, 2**-3, 2**2]
        }
        grid = GridSearchCV(svrreg, param_grid=param_grid, cv=10, scoring='neg_mean_absolute_error', n_jobs=2)
        grid.fit(x_train, y_train)
        y_pred = grid.predict(x_test)
        mae = mean_absolute_error(y_test, y_pred)
        if mae < best_mae:
            best_mae = mae
            best_k = k
        print grid.best_params_
        print 'For k = {} SVR MAE = {}'.format(k, mae)
    print 'Best features for k = {}'.format(best_k)

if __name__ == '__main__':
    # fit_linreg()
    # fit_rf()
    fit_svr()