![Title Slide](https://github.com/jkvalentine/Biblical-Book-Sales/blob/master/images/title_side.png)

<H1 align="center">Motivation</H1>
<p>One of my favorite podcasts, Harry Potter and the Sacred Text, examines each chapter of Harry Potter through a different thematic lens relating to one or several sacred texts. With the Harry Potter as the most popular book series of all time and The Bible as the best selling book of all time, I wanted to explore the topical overlap of this best selling series and, by extension, other best selling texts, to determine whether topical similarity to The Bible is a good predictor of sales.</p>

<p align="center"><img src="https://github.com/jkvalentine/Biblical-Book-Sales/blob/master/images/diagram.png" width="600" /></p>

<H1 align="center">The Data</H1>
The data for this project fall into three categories.

<H3 align="center"> Topic Model Texts</H3>
To create the topic models for this project, I used the entire corpus of english texts from <a href="https://www.gutenberg.org/">Project Gutenberg</a>. There are several ways to obtain this corpus; I downloaded the 2010 Dual Layer DVD ISO via <a href="http://www.gutenberg.org/cdproject/pgdvd042010.iso.torrent">torrent</a> using the <a href="https://transmissionbt.com/download/">Transmission Torrent Client</a>, mounted the image onto my computer, and extracted all the plain text files. After I extracted all the plain text files from the ISO, I created a tar.gz file of all the texts in a single directory.

I  used `topic_model_data_clean.py` to check each text's language, as well as to remove the Project Gutenberg information at the beginning and end of each text. Each text has a different cahracter length of beginning and ending information, and not all texts have the same pattern of text marking their beginning and end, so to determine an average number of characters to remove, I inspected roughly 50 texts and counted the character length from the beginning of the file to the actual start of the text, and from the end of the text to the end of the file: I removed 550 characters from the beginning of each file and 13000 characters from the end. In the future, I may need to increase the number removed from the end given some of the most frequent words from a few topics found in topic modeling.
Finally, after expanding the tar.gz file, I removed empty text files from the corpus using `remove_empty_files.py`.  
 
<H3 align="center"> Sales Data</H3>

Highly accurate, publicly available book sales data is unfortunately unavilable. <a href="http://www.nielsenbookdataonline.com/bdol/">Nielson Book Scan Data</a> is proprietarily available, but is very expensive. As such, I used Wikipedia's <a href="https://en.wikipedia.org/wiki/List_of_best-selling_books">list of best selling books</a> to get approximate aggregate sale data from each text's time of publication. The sales data for this project is collected in `book_sales.csv` because of the formatting difficulties encountered while trying to web-scrape Wikipedia or use its API. To be able to compare one text's sales data to another's, I found the average amount of sales per year by dividing the total sales number by the years in publication and used this number in my regression analysis. Given the challenge of finding sales data, this may prove to be the limiting factor in future work on this project. 

<H3 align="center"> Best Selling Texts</H3>

The best selling texts were challenging to obtain as well, mostly because of copyright issues. For this project, I chose fictional texts with narrative structures and excluded all others. Because these texts aren't available in any one place, I searched for each text on the internet and included all the texts I could find in my analysis. The texts I excluded from my analysis and their reasons are listed in `texts_excluded_and_why.txt`. 

