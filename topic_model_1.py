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



def calculate_cosine_similarity(vectorized_texts):
    
    '''
    Calculate cosine similarity among documents in 
    vectorized corpus of texts
    INPUT:
        - vectorized_texts: vectorized representation of corpus '
        of texts in topic space
    OUTPUT:
        - cosine_similarity_matrix: matrix relating
        texts to each other
    '''
    cosine_matrix = cosine_similarity(vectorized_texts)
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
    
    #To do: figure out how to stream data from S3;
    # All directory path, text paths will change to refelect this

    
    directory_path = '/Users/jrrd/Galvanize/Biblical-Book-Sales/data/model_texts'
    #directory_path = "/mnt/jkvalentine7695/Biblical_Book_Sales-Data/text_files/text_archives.tar.gz"
    
    #text_to_transform=['/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts/111_kjbible.txt']

    #path_to_text_to_transform = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

    text_paths = create_path_directory(directory_path)
    tfidf_vectorizer = build_tfidf_vectorizer_model(text_paths,
                                                    input='filename',
                                                    max_features=15000)
    #For a previous strategy to predict book sales
    #bible_vector = vectorizer.transform(text_to_transform)

    #Vectorized texts will take in best sellers texts
    #vectorized_texts = vectorize_text(vectorizer, path_to_text_to_transform, directory=True)

    #Will be used to compute cosine similarity of best selling texts relative to their
    #TFIDF topic-model vectorization
    #cosine_sim_matrix = calculate_cosine_similarity(bible_vector, vectorized_texts)

    #Will extract cosine similarity row vectors: do I need this?
    #Does tfidf row vector give me all the info I need?
    #z = cosine_similarity(vectorized_texts)

    save_model_as_pickle('tfidf_model.pkl', tfidf_vectorizer)












