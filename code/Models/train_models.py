from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import Imputer, StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error
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


if __name__ == '__main__':
    fit_linreg()
    fit_rf()