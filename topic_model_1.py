from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from boto.s3.connection import S3Connection
from view_topics import print_top_words_for_topic_model
import os, sys
import numpy as np
import os, sys



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


def build_tfidf_tfidf_vectorizer_model(text_paths):
	'''
	Instantiate and fit tfidf tfidf_vectorizer model

	INPUT:
		- text_paths: list of path strings to text file
	OUTPUT:
		- fit tfidf tfidf_vectorizer
	'''
	tfidf_vectorizer = TfidfVectorizer(input='filename',
								 stop_words='english',
								 decode_error='ignore',
								 min_df=50)
	return tfidf_vectorizer.fit(text_paths)



def vectorize_text(tfidf_vectorizer,path_to_text_to_transform, directory=True):
	'''
	Vectorize text according to fitted model

	INPUT:
		- text_to_transform: string path to text files or 
			directory of text files
		- tfidf_vectorizer: tfidf vectorized model
		- directory: Boolean- if path to directory, True
							  if path to file, False
	OUTPUT:
		- vectorized_text: vector representation of
			vocabulary contained in document
	'''
	if directory == True:
		texts = os.listdir(path_to_text_to_transform)
		texts_to_transform = [os.path.join(path_to_text_to_transform,text) for text in texts]
		vectorized_texts = tfidf_vectorizer.transform(texts_to_transform)
		return vectorized_texts
	else:
		texts_to_transform = [path_to_text_to_transform]
		vectorized_texts = tfidf_vectorizer.transform(texts_to_transform)
		return vectorized_texts



def calculate_cosine_similarity(vectorized_texts):
	'''
	Calculate cosine similarity among documents in 
	vectorized corpus of texts
	
	INPUT:
		- vectorized_texts: vectorized representation of corpus '
		of texts in topic space
	OUTPUT:
		- cosine_similarity_matrix: matrix relating bible vector
			to vectorized texts
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
	with open(file_name) as f:
		pickle.dump(model_name, f)



if __name__ == '__main__':
	
	#To do: figure out how to stream data from S3;
	# All directory path, text paths will change to refelect this

	directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"
	
	text_to_transform=['/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts/111_kjbible.txt']

	path_to_text_to_transform = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

	text_paths = create_path_directory(directory_path)

	tfidf_vectorizer = build_tfidf_vectorizer_model(text_paths)

	bible_vector = tfidf_vectorizer.transform(text_to_transform)

	vectorized_texts = vectorize_text(tfidf_vectorizer, path_to_text_to_transform, directory=True)

	cosine_sim_matrix = calculate_cosine_similarity(bible_vector, vectorized_texts)

	z = cosine_similarity(vectorized_texts)

	save_model_as_pickle('tfidf_model.pkl', tfidf_vectorizer)












