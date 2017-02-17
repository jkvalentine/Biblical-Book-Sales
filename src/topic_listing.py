import cPickle as pickle


def print_top_words(model, feature_names, n_top_words):
    '''
    Print top words for each topic in NMF and LDA
    topic models to get a sense of what the topics are
    about
    INPUT:
        - model: NMF or LDA model loaded from pickle file
        - feature_names: tfidf feature names
        - n_top_words: number of top words in topic
                       to view
    '''
    for topic_index, topic in enumerate(model.components_):
        print "Topic #{}:".format(topic_index)
        words = " ".join([feature_names[i]
                         for i in topic.argsort()[:-n_top_words - 1:-1]])
        print words
        print "################"


if __name__ == '__main__':

    with open('pickled_models/tfidf_model.pkl') as f:
        tfidf = pickle.load(f)

    with open('pickled_models/nmf_model.pkl') as g:
        nmf = pickle.load(g)

    with open('pickled_models/lda_model.pkl') as h:
        lda = pickle.load(h)

    feature_names = tfidf.get_feature_names()

    print_top_words(nmf, feature_names, 50)

    print_top_words(lda, feature_names, 50)
