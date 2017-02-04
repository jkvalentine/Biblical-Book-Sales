from sklearn.model_selection import train_test_split
import pandas as pd

def create_train_test_split(sales_data_csv):
    '''
    Create training, tesing, and validation set
    from data; create separate data frame
    for bible for ease of comparison
    INPUT:
        - texts_df: dataframe containing
            text data
    OUTPUT:
        - train, test, validation data
            frames as csv files
    '''
    #Load book sales csv
    book_sales_df = pd.read_csv(sales_data_csv)

    #Split data frame into features, targets, and Bible df
    bible_df = book_sales_df[book_sales_df['book']=='The_Bible']
    book_sales_df = book_sales_df.drop(
        book_sales_df['book'] == 'The_Bible', axis=0)
    sales = book_sales_df['avg_sales_per_year']
    features = book_sales_df.drop('avg_sales_per_year', axis=1)

    #Create test set
    X_train1, X_test, y_train1, y_test = train_test_split(
        features, sales)

    #Create train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X_train1, y_train1)

    bible_df.to_csv('bible_sales_data.csv')

    X_test.to_csv('book_sales_test_features.csv')
    y_test.to_csv('book_sales_test_targets.csv')

    X_train.to_csv('book_sales_train_features.csv')
    y_train.to_csv('book_sales_train_targets.csv')

    X_val.to_csv('book_sales_val_features.csv')
    y_val.to_csv('book_sales_va_targets.csv')


if __name__ == '__main__':

    create_train_test_split('book_sales_df.csv')
