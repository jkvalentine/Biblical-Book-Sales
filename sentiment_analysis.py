from textblob.blob import TextBlob
from topic_model_1 import create_path_directory
import os
from io import open



def create_list_text_strings(text_strings):
    '''
    Create list of strings of texts

    INPUT:
        - text_paths: list of file path strings
    OUTPUT:
        - text_list: list of text strings
    '''
    text_list = []
    for path in text_strings:
        # if '.DS_Store' in path:
        #     continue
        with open(path, 'r', encoding='utf8', errors='ignore') as j:
            text_list.append(j.read())
    return text_list



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
