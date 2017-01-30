from textblob.blob import TextBlob
from topic_model_1 import create_path_directory
import os
from io import open



def create_list_text_strings(text_paths):
	'''
	Create list of strings of texts

	INPUT:
		- text_paths: list of file path strings
	OUTPUT:
		- text_list: list of text strings
	'''
	text_list = []
	for path in text_paths:
		if '.DS_Store' in path:
			continue
			with open(path, 'r', encoding='utf8', errors='ignore') as f:
				text_list.append(f.read())
	return text_list

#Maybe I just don't understand control flow, but why is the continue statement necessary?



def create_blobs_from_texts(text_list):
	'''
	Create text blobs from list of text strings

	INPUT:
		- text_list: list of text strings
	OUTPUT:
		- blobs: list of blob objects
	'''
	blobs = []
	for text in text_list:
		blob = TextBlob(text)
		blobs.append(blob)
	return blobs

#Wooooo blobs


def get_document_polarity(blobs):
	'''
	Get polarity score for each document's text
	as a float in range [-1.0, 1.0]

	INPUT:
		- blobs: list of text blob objects
	OUTPUT:
		- polarity_scores: list of polarity scores,
			one score for each text
	'''
	polarity_scores = []
	for blob in blobs:
		polarity_score = blob.polarity
		polarity_scores.append(polarity_score)
	return polarity_scores



def get_document_subjectivity(blobs):
	'''
	Get subjectivity score for each document's text
	as a float in range [0.0, 1.0]; 0.0 is very
	objective, 1.0 is very subjective

	INPUT:
		- blobs: list of text blob objects
	OUTPUT:
		- sentiment_scores: list of sentiment scores,
			one score for each text
	'''
	subjectivity_scores = []
	for blob in blobs:
		subjectivity_score = blob.subjectivity
		subjectivity_scores.append(subjectivity_score)
	return subjectivity_scores



def get_title_and_index(text_paths):
	'''
	Return book title and index number

	INPUT:
		- text_paths: list of file path strings
	OUTPUT:
		- title_index_list: list of tuples of
			book title and index
	'''
	title_index_list = []
	for index, text in enumerate(text_paths):
		title = text.split('/')[-1]
		title_index_list.append((title, index))
	return title_index_list



'''
Yup, code looks squeaky clean to me.  One potential thing to think about is going beyond polarity and subjectivity for the sentiment analysis.  For instance, what about the emotional content of the story?  You can use this lexicon (http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm) to get how happy/sad/angry/fearful etc. each text is.  Maybe you'll find there's some pattern with that - like, books that have a similar emotional composition to the Bible are more popular?  Here is an example of someone who did this with movies (hence how I know about it becuase her project is like mine): https://github.com/AnnaVM/Project_Plotline.
'''

if __name__ == '__main__':

	directory_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"

	text_paths = create_path_directory(directory_path)

	text_list = create_list_text_strings(text_paths)

	blobs = create_blobs_from_texts(text_list)

	polarity_scores = get_document_polarity(blobs)

	subjectivity_scores = get_document_subjectivity(blobs)

	title_index_list = get_title_and_index(text_paths)

	#create list of tuples of the form:
	# (title, subjectivity_score, polarity_score)
