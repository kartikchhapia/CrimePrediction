from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import Imputer, StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error
import config


def get_census_train_test_data():
    df = pd.read_csv('../../data/TestDataSet/crime_landmarks_census.csv', index_col=0)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle
    df_census = df[df.columns[18:]]
    # df_census = df_census.drop('median_income', 1)
    df_census = df_census.div(df_census['total_population'], axis=0)
    df_census[config.NON_NORMALIZABLE_COLS] = df_census[config.NON_NORMALIZABLE_COLS].mul(df_census['total_population'], axis=0)
    df_y = df[df.columns[2]] + df[df.columns[3]] + df[df.columns[4]]
    Y = df_y.as_matrix()
    X = df_census.as_matrix()
    imputer = Imputer()
    scaler = StandardScaler()
    X = imputer.fit_transform(X)
    X = scaler.fit_transform(X)
    return X, Y, df_census.columns