from gensim import corpora, models, similarities
from topic_model_1 import make_s3_connection, create_path_directory, build_tfidf_vectorizer_model
import os, sys


#build corpus for lda model
def build_corpus():



#figure out the steps, inputs to build LDA model
#what hyper-paramters are there to tune?
#better to use sklearn or gensim?
def build_lda_model(corpus):
	'''
	Build LDA model
	INPUT:
		- number_topics: number of topics
		- corpus: 
	OUTPUT:
		-
	'''
	lda = models.ldamodel()



if __name__ == '__main__':

	#To do: figure out how to stream data from S3?;
	# All directory path, text paths will change to refelect this
