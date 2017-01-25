from sklearn.feature_extraction.text import TfidfVectorizer
import glob, os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from boto.S3.connection import S3Connection

conn = S3Connection(WS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

text_bucket = conn.get_bucket('project-gutenberg-texts')

dir_path = "/Users/jrrd/Galvanize/Biblical-Book-Sales/data/best_sellers_texts"
texts = os.listdir(dir_path)

text_paths = [os.path.join(dir_path,text) for text in texts]

lemmatizer =WordNetLemmatizer()
analyzer = CountVectorizer().build_analyzer()

#Attempt to add lemmatization as preprocessing,
#more complex function for fitting model from raw documents as filenames

#def lemmatized_words(doc):
#	return (lemmatizer.lemmatize(word) for word in analyzer(doc))

vectorizer = TfidfVectorizer(input='filename', stop_words='english',decode_error='ignore')
vectorizer.fit(text_paths)

print vectorizer.vocabulary_













