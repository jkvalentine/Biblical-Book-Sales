from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from boto.s3.connection import S3Connection
from topic_model_1 import make_s3_connection, create_path_directory, build_tfidf_vectorizer_model
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import os



def build_Count_vectorizer_model(text_paths):
	'''
	Instantiate and fit Count vectorizer model

	INPUT:
		- text_paths: list of path strings to text files
	OUTPUT:
		- none
	'''
	count_vectorizer = CountVectorizer(input='filename', stop_words='english', decode_error='ignore')
	return count_vectorizer.fit(text_paths)


def build_NMF_model(count_vectorizer):
	'''
	Instantiate and fit NMF model

	INPUT:
		- count_vectorizer: fit Count vectorizer model
	OUTPUT:
		- fit NMF model
	'''
	nmf_model = NMF()
	return nmf_model.fit(count_vectorizer)

def transform_corpus(corpus_text_paths, nmf_model):
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
	X = create_path_directory(corpus_text_paths)
	count_vectorizer = CountVectorizer(X)
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

	#To do: figure out how to stream data from S3;
	# All directory path, text paths will change to refelect this

	directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

	text_paths = create_path_directory(directory_path)

	corpus_text_paths = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

	count_vectorizer = build_Count_vectorizer_model(text_paths)

	nmf_model = build_NMF_model(count_vectorizer)

	W = transform_corpus(corpus_text_paths, nmf_model)

	distances = euclidean_distances(W)

	
