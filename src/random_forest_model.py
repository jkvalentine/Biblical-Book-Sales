from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


def train_random_forest(X_train, y_train, n_estimators=10000):
    '''
    Train random forest regressor on
    training data

    INPUT:
        - X_train: df of features for prediction
        - y_train: pandas series of book sales info
    OUTPUT:
        - fit randon forest regressor model
    '''
    random_forest = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=42,
        oob_score=True)
    random_forest.fit(X_train, y_train)
    return random_forest


def make_random_forest_prediction(random_forest, X_val, y_val):
    '''
    Make a prediction based on fit random forest model

    INPUT:
        - random_forest: fit random forest model
        - X_val: feature validation data
    OUTPUT:
        - prediction: random forest regression
            results
        - r_squared: r-squared score of prediction
    '''
    prediction = random_forest.predict(X_val)
    r_squared = random_forest.score(X_val, y_val)
    return prediction, r_squared


def score_prediction(prediction, y_val):
    '''
    Return different rmse
    INPUT:
        prediction: predicted values of book
            sales data
        y_val: real values of book sales
    '''
    rmse = np.sqrt(mean_squared_error(prediction, y_val))
    return rmse


if __name__ == '__main__':

    X_train = pd.read_csv(
        'book_sales_train_features.csv')
    y_train = pd.read_csv(
        'book_sales_train_targets.csv').values

    X_test = pd.read_csv('book_sales_test_features.csv')
    y_test = pd.read_csv('book_sales_test_targets.csv').values

# Drop unwanted features from training model
    X_train.drop(['first_published', 'approximate_sales',
                 'text_file', 'book'], axis=1, inplace=True)

    X_test.drop(['first_published', 'approximate_sales',
                'text_file', 'book'], axis=1, inplace=True)

# Fit random forest to training data
    random_forest = train_random_forest(
        X_train, y_train.ravel(), n_estimators=10000)

# Make prediction based on testing data
    prediction_test, r_squared_test = make_random_forest_prediction(
        random_forest,
        X_test,
        y_test)

# Make prediction based on training error
    prediction_train, r_squared_train = make_random_forest_prediction(
        random_forest,
        X_train,
        y_train)

    train_rmse = score_prediction(prediction_train, y_train)
    test_rmse = score_prediction(prediction_test, y_test)

    oob = random_forest.oob_score_
    feature_importance = random_forest.feature_importances_
    sales_data = np.vstack((y_test, y_train))
    mean_sales = np.mean(sales_data)

    print "oob error: {}".format(oob)
    print "important features: {}".format(feature_importance)
    print "mean sales: {}".format(mean_sales)

    print '*#*#*#*#*#*#*#*#*#*#*#*'

    print "train rmse: {}".format(train_rmse)
    print "train r-squared: {}".format(r_squared_train)

    print '*#*#*#*#*#*#*#*#*#*#*#*'
    print "test rmse: {}".format(test_rmse)
    print "test r-squared: {}".format(r_squared_test)
    