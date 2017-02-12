from sklearn.decomposition import LatentDirichletAllocation
from topic_model_1 import create_path_directory,\
    save_model_as_pickle
import cPickle as pickle


def build_LDA_model(tfidf_vectorizer, text_paths, n_topics=100):
    '''
    Build LDA model
    INPUT:
        - number_topics: number of topics
    OUTPUT:
        - fit LDA model
    '''
    lda_model = LatentDirichletAllocation(n_topics=n_topics)
    vectorized_model_texts = tfidf_vectorizer.transform(text_paths)
    return lda_model.fit(vectorized_model_texts)


def transform_LDA_corpus(tfidf_vectorizer,
                         corpus_text_paths,
                         lda_model):
    '''
    Transform corpus of documents to
    document-topic distribution matrix
    INPUT:
        - corpus_text_paths: list of path strings to
            corpus of texts
        - lda_model: fitted lda model
        - tfidf_vectorizer: fit tfidf vectorizer
    OUTPUT:
        - doc_topic_distribution: document-topic distribution matrix
    '''
    corpus_docs = create_path_directory(corpus_text_paths)
    X = tfidf_vectorizer.transform(corpus_docs)
    doc_topic_distribution = lda_model.transform(X)
    return doc_topic_distribution


if __name__ == '__main__':

    directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/model_texts"

    text_paths = create_path_directory(directory_path)

    with open('/Users/jrrd/Galvanize/Biblical-Book-Sales/pickled_models/tfidf_model.pkl') as f:
        tfidf_vectorizer = pickle.load(f)

    lda_model = build_LDA_model(tfidf_vectorizer, text_paths)

    save_model_as_pickle('lda_model.pkl', lda_model)
