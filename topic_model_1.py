from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from boto.s3.connection import S3Connection
import os, sys
import numpy as np



#will most likely not implement this s3 connection function
#since these models will be employed on domino
def make_s3_connection():
	conn = S3Connection(aws_access_key_id=os.environ['AWS_ACCESS_KEY'],\
	 aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

	text_bucket = conn.get_bucket('project-gutenberg-texts')





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
		text_paths = [os.path.join(directory_path,text) for text in texts]
		return text_paths
	else:
		text_paths = [directory_path]
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

#Want to stem or lemmatize first maybe?



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
		#think you mean 'path_to_text_to_transform' there
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

	'''
	Okay, I think I get this but want to make sure.  vectorized_tests is going to output a list of vectorized texts.  Then cosine_sim_matrix is going to calculate the cosine similarity between each of those texts and the Bible.  So it's a matrix where each row is a text, but the only column is the cosine similarity between that text and the Bible?
	So, basically, it's a comparison of word frequencies between each text and the Bible?
	'''
