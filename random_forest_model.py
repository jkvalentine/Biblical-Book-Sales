from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd


def train_random_forest(X_train, y_train, n_estimators=100):
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
        random_state=42)
    random_forest.fit(X_train, y_train)
    return random_forest


def make_ranfom_forest_prediction(random_forest, X_val, y_val):
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
    Return different socring metrics based on
    prediction vs. actual values
    INPUT:
        prediction: predicted values of book
            sales data
        y_val: real values of book sales
    '''
    mse = mean_squared_error(prediction, y_val)
    return mse


if __name__ == '__main__':

    X_train = pd.read_csv(
        'book_sales_train_features.csv')
    y_train = pd.read_csv(
        'book_sales_train_targets.csv').values

    X_val = pd.read_csv('book_sales_val_features.csv')
    y_val = pd.read_csv('book_sales_val_targets.csv').values

#    Drop unwanted features from training model
    X_train.drop(['first_published', 'approximate_sales',
                 'text_file', 'book'], axis=1, inplace=True)

    X_val.drop(['first_published', 'approximate_sales',
                'text_file', 'book'], axis=1, inplace=True)

    random_forest = train_random_forest(
        X_train, y_train.ravel(), n_estimators=100)
    prediction, r_squared = make_ranfom_forest_prediction(
        random_forest,
        X_val,
        y_val)
    mse = score_prediction(prediction, y_val)
    print "mse: {}".format(mse)
    print "r-squared: {}".format(r_squared)
