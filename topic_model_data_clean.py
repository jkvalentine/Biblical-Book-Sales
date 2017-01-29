import tarfile
from StringIO import StringIO
import os

#Need to update this for use with domino file path
#An probably make it more generalizable

#Create output tar.gz archive to write files to
output = tarfile.open('/Users/jrrd/Galvanize/Biblical-Book-Sales/data/gutenberg_texts.tar.gz', mode='w:gz')

#Open tar.gz archive of Gutenberg Texts
with tarfile.open('/Users/jrrd/Galvanize/Biblical-Book-Sales/data/archive.tar.gz', mode='r:gz') as f:
	
	    for entry in f:
	    	
	    	text = f.extractfile(entry)
	    	
	    	if text == None:
	    		continue
	    	else:

		        text_string = text.read()
		        
		        #Remove beginning portion of each text
		        #containing intro Gutenberg info
		        first_pass_text = text_string[550:]
		        
		        #Remove final portion of each text
		        #containing Gutenberg info
		        final_text = first_pass_text[:-13000]

		        #Make text string into temp string file
		        #to write to archive tar.gz text
		        string_file = StringIO()
		        string_file.write(final_text)		  
		        string_file.seek(0)
		        file_size = len(string_file.buf)

		        #Creat tarinfo object for new
		        #tarfile object from string file object
		        info = tarfile.TarInfo(name=entry.name)
		        info.size = file_size
		        
		        #Sanity check
		        print entry.name
		        print file_size
		        print info.size
		        print '###############'

		        #Add processed file to tar.gz archive file
		        output.addfile(tarinfo=info, fileobj=string_file)

output.close()