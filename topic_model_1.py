from sklearn.feature_extraction.text import TfidfVectorizer
from klearn.metrics.pairwise import cosine_similarity
from boto.s3.connection import S3Connection
import os
import numpy as np



def make_s3_connection():
	conn = S3Connection(aws_access_key_id=os.environ['AWS_ACCESS_KEY'],\
	 aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

	text_bucket = conn.get_bucket('project-gutenberg-texts')
	


def create_path_directory(directory_path):
	'''
	Creates list of path directories for input to vectorizer

	INPUT:
		- directory_path: absolute directory path to location of
			text files
	OUTPUT:
		- text_paths: list of path strings to text files
	'''
	texts = os.listdir(directory_path)
	text_paths = [os.path.join(directory_path,text) for text in texts]
	return text_paths



def build_tfidf_vectorizer_model(text_paths):
	'''
	Instantiate and fit tfidf vectorizer model

	INPUT:
		- text_paths: list of path strings to text file
	OUTPUT:
		- fit tfidf vectorizer
	'''
	vectorizer = TfidfVectorizer(input='filename', stop_words='english',decode_error='ignore')
	return vectorizer.fit(text_paths)



def vectorize_text(vectorizer,path_to_text_to_transform, directory=False):
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
		texts_to_transform = [os.path.join(ath_to_text_to_transform,text) for text in texts]
		vectorized_texts = vectorizer.transform(texts_to_transform)
		return vectorized_texts
	else:
		texts_to_transform = [path_to_text_to_transform]
		vectorized_texts = vectorizer.transform(texts_to_transform)
		return vectorized_texts



def calculate_cosine_similarity(bible_vector, vectorized_texts):
	'''
	Calculate cosine similarity among documents in 
	vectorized corpus of texts
	
	INPUT:
		- bible_vector: vectorized representation of The Bible
		- vectorized_texts: vectorized representation of corpus '
		of texts in topic space
	OUTPUT:
		- cosine_similarity_matrix: matrix relating bible vector
			to vectorized texts
	'''
	cosine_matrix = cosine_similarity(bible_vector, vectorized_texts)
	return cosine_matrix



if __name__ == '__main__':
	
	#To do: figure out how to stream data from S3;
	# All directory path, text paths will change to refelect this

	directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"
	
	text_to_transform=['/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts/1_kjbible.txt']

	path_to_text_to_transform = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"


	text_paths = create_path_directory(directory_path)

	vectorizer = build_tfidf_vectorizer_model(text_paths)

	bible_vector = vectorizer.transform(text_to_transform)

	vectorized_texts = vectorize_text(vectorizer, path_to_text_to_transform, directory=True)

	cosine_sim_matrix = cosine_similarity_matrix(bible_vector, vectorized_texts)














