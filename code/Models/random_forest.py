from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import Imputer, StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error


def fit_rf():
    df = pd.read_csv('../../data/TestDataSet/crime_landmarks_census.csv', index_col=0)
    df = df.sample(frac=1).reset_index(drop=True)   # Shuffle
    df_census = df[df.columns[18:]]
    df_census = df_census.div(df_census['total_population'], axis=0)
    df_y = df[df.columns[2]] + df[df.columns[3]] + df[df.columns[4]]
    Y = df_y.as_matrix()
    X = df_census.as_matrix()
    imputer = Imputer()
    scaler = StandardScaler()
    X = imputer.fit_transform(X)
    X = scaler.fit_transform(X)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.33, random_state = 1)
    rf = RandomForestRegressor()
    param_grid = {
        'n_estimators': [5, 10 ,20],
        'criterion': ['mae'],
        'max_depth': [None, 2, 5, 10]
    }
    grid = GridSearchCV(rf, param_grid=param_grid, n_jobs=1)
    grid.fit(x_train, y_train)
    y_pred = grid.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    print grid.best_params_
    print [df_census.columns[i[0]] for i in sorted(enumerate(grid.best_estimator_.feature_importances_), key=lambda x:x[1])]
    print mae


if __name__ == '__main__':
    fit_rf()