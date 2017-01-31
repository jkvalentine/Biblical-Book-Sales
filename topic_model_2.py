from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from boto.s3.connection import S3Connection
from topic_model_1 import make_s3_connection,\
 create_path_directory, build_tfidf_vectorizer_model,\
 calculate_cosine_similarity, save_model_as_pickle
from sklearn.metrics.pairwise import euclidean_distances
from view_topics import print_top_words_for_topic_model
import os, sys



def build_Count_vectorizer_model(text_paths):
	'''
	Instantiate and fit Count vectorizer model

	INPUT:
		- text_paths: list of path strings to text files
	OUTPUT:
		- fit count vectorizer model
	'''
	count_vectorizer = CountVectorizer(input='filename',
									 stop_words='english', 
									 decode_error='ignore',
									 min_df=50)
	return count_vectorizer.fit(text_paths)


def build_NMF_model(count_vectorizer, text_paths,n_components=100):
	'''
	Instantiate and fit NMF model

	INPUT:
		- count_vectorizer: fit Count vectorizer model
	OUTPUT:
		- fit NMF model 
	'''
	nmf_model = NMF(n_components=100)
	vectorized_model_texts = count_vectorizer.transform(text_paths)
	return nmf_model.fit(vectorized_model_texts)



def transform_NMF_corpus(count_vectorizer, corpus_text_paths, nmf_model):
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
	X = count_vectorizer.transform(corpus_docs)
	W = nmf_model.transform(X)
	return W



def compute_distance_between_vectors(W):
	'''
	Compute distance bewteen row vector representing
	bible projected into topic space with all other 
	documents projected into topic space

	INPUT:
		- W: corpus of texts represented as vectors,
			projected onto topic space
	OUTPUT:
		- distances: numpy array representing
			distance between document-topic-space
			vectors
	'''
	bible_vector = W[0] #with Bible as first document of corpus
	distances = euclidean_distances(bible_vector, W[1:])
	return distances



if __name__ == '__main__':

	#To do: figure out how to stream data from S3?;
	#All directory path, text paths will change to refelect this
	#Tune hyper-parameters of model to find best number of topics
	#to model

	directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

	text_paths = create_path_directory(directory_path)

	corpus_text_paths = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

	count_vectorizer = build_Count_vectorizer_model(text_paths)
	
	nmf_model = build_NMF_model(count_vectorizer, text_paths)

	W = transform_NMF_corpus(count_vectorizer, corpus_text_paths, nmf_model)

	distances = euclidean_distances(W)

	cosine_similarities = calculate_cosine_similarity(W)

	save_model_as_pickle('nmf_model.pkl', nmf_model)

	



	
