from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import cPickle as pickle
import os


def create_path_directory(directory_path, directory=True):
    '''
    Creates list of path directories for input
    INPUT:
        - directory_path: absolute directory path to location of
            text files
    OUTPUT:
        - text_paths: list of path strings to text files
    '''
    if directory:
        texts = os.listdir(directory_path)
        text_paths = [os.path.join(directory_path, text) for text in texts]

        return text_paths
    else:
        text_paths = [directory_path]
        return text_paths


def build_tfidf_vectorizer_model(text_paths, input='input'):
    '''
    Instantiate and fit tfidf vectorizer model
    INPUT:
        - text_paths: list of path strings to text file
    OUTPUT:
        - fit tfidf vectorizer
    '''
    vectorizer = TfidfVectorizer(input=input,
                                 stop_words='english',
                                 decode_error='ignore',
                                 max_features=15000
                                 )
    return vectorizer.fit(text_paths)


def vectorize_text(vectorizer, path_to_text_to_transform, directory=True):
    '''
    Vectorize text according to fitted model
    INPUT:
        - text_to_transform: string path to text files or
            directory of text files
        - vectorizer: tfidf vectorized model
        - directory: Boolean- if path to directory, True
                              if path to file, False
    OUTPUT:
        - vectorized_text: vector representation of
            vocabulary contained in document
    '''
    if directory == True:
        texts = os.listdir(path_to_text_to_transform)
        texts_to_transform = [os.path.join(path_to_text_to_transform, text) for text in texts]
        vectorized_texts = vectorizer.transform(texts_to_transform)
        return vectorized_texts
    else:
        texts_to_transform = [path_to_text_to_transform]
        vectorized_texts = vectorizer.transform(texts_to_transform)
        return vectorized_texts


def calculate_cosine_similarity(vectorized_texts, bible_vector):
    '''
    Calculate cosine similarity among documents in
    vectorized corpus of texts
    INPUT:
        - vectorized_texts: vectorized representation of corpus '
        of texts in topic space
        - bible_vector: vectorized representation of the Bible
    OUTPUT:
        - cosine_similarity_matrix: matrix relating
        texts to each other
    '''
    cosine_matrix = cosine_similarity(vectorized_texts, bible_vector)
    return cosine_matrix


def save_model_as_pickle(file_name, model_name):
    '''
    Save fit model as pickle file
    INPUT:
        - model_name: trained model
    OUTPUT:
        - pickle file
    '''
    with open(file_name, 'w') as bread:
        pickle.dump(model_name, bread)
        print "PICKLE!"


if __name__ == '__main__':


    directory_path = '/Users/jrrd/Galvanize/Biblical-Book-Sales/data/model_texts'

    text_paths = create_path_directory(directory_path)
    tfidf_vectorizer = build_tfidf_vectorizer_model(text_paths,
                                                    input='filename',
                                                    max_features=15000)

    save_model_as_pickle('tfidf_model.pkl', tfidf_vectorizer)
