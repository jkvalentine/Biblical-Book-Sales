![Title Slide](https://github.com/jkvalentine/Biblical-Book-Sales/blob/master/images/title_side.png)

<H1 align="center">Motivation</H1>
<p>One of my favorite podcasts, Harry Potter and the Sacred Text, examines each chapter of Harry Potter through a different thematic lens relating to one or several sacred texts. With the Harry Potter as the most popular book series of all time and The Bible as the best selling book of all time, I wanted to explore the topical overlap of this best selling series and, by extension, other best selling texts, to determine whether topical similarity to The Bible is a good predictor of sales.</p>

<p align="center"><img src="https://github.com/jkvalentine/Biblical-Book-Sales/blob/master/images/diagram.png" width="600" /></p>

<H1 align="center">The Data</H1>
<p>The data for this project fall into three categories.</p>

<H3 align="center"> Topic Model Texts</H3>
<p>To create the topic models for this project, I used the entire corpus of english texts from <a href="https://www.gutenberg.org/">Project Gutenberg</a>. There are several ways to obtain this corpus; I downloaded the 2010 Dual Layer DVD ISO via <a href="http://www.gutenberg.org/cdproject/pgdvd042010.iso.torrent">torrent</a> using the <a href="https://transmissionbt.com/download/">Transmission Torrent Client</a>, mounted the image onto my computer, and extracted all the plain text files. After I extracted all the plain text files from the ISO, I created a tar.gz file of all the texts in a single directory.</p>
<p>I  used `topic_model_data_clean.py` to check each text's language, as well as to remove the Project Gutenberg information at the beginning and end of each text. Each text has a different cahracter length of beginning and ending information, and not all texts have the same pattern of text marking their beginning and end, so to determine an average number of characters to remove, I inspected roughly 50 texts and counted the character length from the beginning of the file to the actual start of the text, and from the end of the text to the end of the file: I removed 550 characters from the beginning of each file and 13000 characters from the end. In the future, I may need to increase the number removed from the end given some of the most frequent words from a few topics found in topic modeling.</p>
<p>After expanding the tar.gz file, I then removed empty text files from the corpus using `remove_empty_files.py` </p>   
<H3 align="center"> Sales Data</H3>
<H3 align="center"> Best Selling Texts</H3>


