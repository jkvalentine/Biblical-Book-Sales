from sklearn.ensemble import RandomForectRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score,\
    f1_score, accuracy_score
import cPickle as pickle


def create_train_test_split(text_data_df):
    '''
    Create training, tesing, and validation set
    from data
    INPUT:
        - texts_df: dataframe containing
            text data
    OUTPUT:
        - X_train, X_test, y_train, y_test:
            dataframes and series
    '''
    with open('book_sales_df.pkl', 'r') as data:
        book_sales_df = pickle.load(data)
    sales = book_sales_df['avg_sales_per_year']
    features = text_data_df.drop('avg_sales_per_year')
    X_train, X_test, y_train, y_test = train_test_split(
        features, sales)
    with open('test_data.pkl') as k:



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
    random_forest = RandomForectRegressor(n_estimators=n_estimators)
    return random_forest.fit(X_train, y_train)

def make_ranfom_forest_prediction(random_forest, X_val, y_val):
    '''
    Make a prediction based on fit random forest model

    INPUT:
        random_forest: fit random forest model
        X_val: feature validation data
        y_val: book sales validation data
    '''
    prediction = random_forest.predict(X_val, y_val)
    return prediction



def score_prediction(prediction, y_val):
    '''
    Return different socring metrics based on
    prediction vs. actual values
    INPUT:
        prediction: predicted values of book
            sales data
        y_val: real values of book sales
    '''
    #Calculate precision, accuracy, recall
    recall = recall_score(y_val, prediction)
    precision = precision_score(y_val, prediction)
    accuracy = accuracy_score(y_val, prediction)
    f_1_score = f1_score(y_val, prediction)

    print "recall is {}".format(recall)
    print "precision is {}".format(precision)
    print "accuracy is {}".format(accuracy)
    print "f1 score is {}".format(f_1_score)



if __name__ == '__main__':
