#Remove empty text files from model texts
import os

i = 0
directory_path = '/Users/jrrd/Galvanize/Biblical-Bok-Sales/data/model_texts/english_texts'
texts_to_remove = []
for name in os.listdir(''):
    file_name = os.path.join(directory_path, name)
    with open(file_name) as f:
        if len(f.read()) == 0:
            os.remove(file_name)
            #keep tally of how many files removed
            i += 1

print "YAY!!! ENGLISH ONLY"
