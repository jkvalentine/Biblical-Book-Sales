#Remove empty text files from model texts
import os

i = 0
directory_path = '/Users/jrrd/Galvanize/Biblical-Bok-Sales/data/model_texts/english_texts'
texts_to_remove = []
for name in os.listdir(''):
    file_name = os.path.join(directory_path, name)
    with open(file_name) as f:
        text_string = f.read()
        if len(text_string) == 0:
            os.remove(file_name)
            #keep tally of how many files removed
            i += 1

print "yay non-empty text files!"