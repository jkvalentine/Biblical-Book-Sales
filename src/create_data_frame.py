import pandas as pd
from sentiment_analysis import create_list_text_strings,\
    create_blobs_from_texts, get_document_polarity, \
    get_document_subjectivity
from topic_model_1 import calculate_cosine_similarity
import cPickle as pickle


def create_data_frame(book_sales_file_path):
    '''
    Create a data-frame from sales data and
    text-features

    INPUT:
            - book_sales_file_path: string path to
                    book sales csv
    OUTPUT:
            - book_sales_df: data frame with
                    features for random forest
    '''

    book_sales_df = pd.read_csv(book_sales_file_path)
    book_sales_df['years_in_print'] = 2017 - book_sales_df['first_published']
    book_sales_df.drop(['original_language', 'author'], axis=1,
                       inplace=True)
    new_col = (
        book_sales_df['approximate_sales'] / book_sales_df['years_in_print'])
    book_sales_df['avg_sales_per_year'] = new_col
    return book_sales_df


def add_columns_to_data_frame(book_sales_df,
                              polarity_scores,
                              subjectivity_scores,
                              cosine_tfidf_matrix,
                              nmf_similarity,
                              lda_similarity):
    '''
    Add columns to data frame

    INPUT:
        - book_sales_df: data frame of
            book sales data
        - polarity_scores: polarity score
            for each book in data frame
        - subjectivity_scores: subjectivity
            score for each book in data frame
    OUTPUT:
        - book_sales_df: final df for
            analysis

    '''
    book_sales_df['polarity'] = polarity_scores
    book_sales_df['subjectivity_score'] = subjectivity_scores
    book_sales_df['tfidf_similarity'] = cosine_tfidf_matrix
    book_sales_df['nmf_similarity'] = nmf_similarity
    book_sales_df['topic_distribution'] = lda_similarity
    book_sales_df.drop('years_in_print', axis=1, inplace=True)
    return book_sales_df


def vectorize_text_corpus(text_strings):
    '''
    Transform corpus into vectorized tfidf representation
    INPUT:
        - text_strings: list of path strings to text files
    OUTPUT:
        -tfidf_matrix: vectorized version of texts
    '''
    with open(
        '/Users/jrrd/Galvanize/Biblical-Book-Sales/pickled_models/tfidf_model.pkl') as f:
        tfidf_model = pickle.load(f)
    tfidf_matrix = tfidf_model.transform(text_strings)
    return tfidf_matrix


def tansform_vector_corpus(tfidf_matrix, nmf=True):
    '''
    Transform tfidf matrix to lda or nmf representations
    in topic space
    INPUT:
        -tfidf_matrix: vectorized version of texts
        - transform: string of 'lda' or 'nmf'
    OUTPUT
        - W: nmf topic-document matrix
        - doc_distr_matrix:
    '''
    if nmf:
        with open('/Users/jrrd/Galvanize/Biblical-Book-Sales/pickled_models/nmf_model.pkl') as g:
            nmf_model = pickle.load(g)
        W = nmf_model.transform(tfidf_matrix)
        return W
    else:
        with open(
            '/Users/jrrd/Galvanize/Biblical-Book-Sales/pickled_models/lda_model.pkl') as h:
            lda_model = pickle.load(h)
        doc_distr_matrix = lda_model.transform(tfidf_matrix)
        return doc_distr_matrix


if __name__ == '__main__':

    book_sales_file_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/book_sales.csv"

    directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

    book_sales_df = create_data_frame(book_sales_file_path)

    text_strings = list(book_sales_df['text_file'].values)

    text_list = create_list_text_strings(text_strings)

    print "***********"

    blobs = create_blobs_from_texts(text_list)

    polarity_scores = get_document_polarity(blobs)

    subjectivity_scores = get_document_subjectivity(blobs)

    print "***********"

    tfidf_matrix = vectorize_text_corpus(text_strings)
    bible_path = list(
        book_sales_df[book_sales_df['book'] == 'The_Bible'].text_file)
    tfidf_bible_vector = vectorize_text_corpus(bible_path)

    cosine_tfidf_matrix = calculate_cosine_similarity(
        tfidf_matrix.todense(), tfidf_bible_vector.todense())

    print "***********"

    W = tansform_vector_corpus(tfidf_matrix, nmf=True)
    nmf_bible_vector = tansform_vector_corpus(tfidf_bible_vector, nmf=True)

    nmf_similarity = calculate_cosine_similarity(
        W, nmf_bible_vector)

#    Issues with lda functioning, will fix in future
    doc_distr_matrix = tansform_vector_corpus(tfidf_matrix, nmf=False)
    lda_bible_vector = tansform_vector_corpus(tfidf_bible_vector, nmf=False)

    lda_similarity = calculate_cosine_similarity(
        W, lda_bible_vector)

    book_sales_df = add_columns_to_data_frame(book_sales_df,
                                              polarity_scores,
                                              subjectivity_scores,
                                              cosine_tfidf_matrix,
                                              nmf_similarity,
                                              lda_similarity)
#    save dataframe as csv
    book_sales_df.to_csv('book_sales_df.csv', index=False)
