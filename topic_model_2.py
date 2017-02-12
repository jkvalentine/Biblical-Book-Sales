from sklearn.decomposition import NMF
from topic_model_1 import create_path_directory,\
    build_tfidf_vectorizer_model, calculate_cosine_similarity,\
    save_model_as_pickle, build_tfidf_vectorizer_model,



def build_NMF_model(tfidf_vectorizer,
                    text_paths,
                    n_components=100):
    '''
    Instantiate and fit NMF model

    INPUT:
        - count_vectorizer: fit Count vectorizer model
    OUTPUT:
        - fit NMF model
    '''
    nmf_model = NMF(n_components=100)
    vectorized_model_texts = tfidf_vectorizer.transform(text_paths)
    return nmf_model.fit(vectorized_model_texts)


def transform_NMF_corpus(tfidf_vectorizer, corpus_text_paths, nmf_model):
    '''
    Transform corpus of documents, project them onto
    topic/latent feature space

    INPUT:
        - corpus_text_paths: list of path strings to
            corpus of texts
    OUTPUT:
        - W: transformed data, rows of which represent
            how much each latent feature (column space)
            is represented in each document (row space)
    '''
    corpus_docs = create_path_directory(corpus_text_paths)
    X = tfidf_vectorizer.transform(corpus_docs)
    W = nmf_model.transform(X)
    return W


if __name__ == '__main__':


    directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/model_texts"

    text_paths = create_path_directory(directory_path)

    with open(
        '/Users/jrrd/Galvanize/Biblical-Book-Sales/pickled_models/tfidf_model.pkl') as f:
        tfidf_vectorizer = pickle.load(f)

    nmf_model = build_NMF_model(tfidf_vectorizer, text_paths)

    save_model_as_pickle('nmf_model.pkl', nmf_model)
