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

The best selling texts were challenging to obtain as well, mostly because of copyright issues. For this project, I chose fictional texts with narrative structures and excluded all others. Because these texts aren't available in any one place, I searched for each text on the internet and included all the texts I could find in my analysis. The texts I excluded from my analysis and their reasons are listed in `texts_excluded_and_why.txt`. Future work will include a larger corpus of texts representing a larger spread of sales data.

<H1 align="center">Topic Modeling</H1>

To extract latent topic features for this project, I chose to perform non-negative matrix factorization (NMF) and latent Dirichlet allocation (LDA). Both of these methods require a vectorized version of a corpus of texts; I trained a term-frequency inverse-document frequency (tfidf) vectorizer model using the Project Gutenberg english texts to produce a matrix where each row represents a document and the entries in each row vector represent the tfidf for each of the most frequent 15,000 words with common stop-words removed. To obtain this pickled model, I ran `topic_model_1.py` on an AWS EC2 instance with relevant path names changed as necessary.

![tfidf matrix diagram]()

To build and pickle my NMF and LDA models, I ran `topic_model_2.py` and `topic_model_3.py`, respectively, on an AWS EC2 instance because of the large vocabulary and significant run time for each model. 

<H3 align="center">NMF</H3>

In terms of topic modeling, NMF provides a powerful and easily interpretable way to extract topics from a corpus. I transformed the Project Gutenberg texts using the pickled tfidf model and then built an NMF model using this vectorized corpus. In this process, with our vectorized corpus represented by the matrix `X` with dimensions `(n x m)`, we find the matrices `W` with dimensions `(n x k)`, and `H` with deimensions `(k x m)` such that `X ≈ W * H`. In this application, `n` is the number of documents in our corpus, `m` is the number of words, and `k` is the number of latent topic features. For this project, I chose `k = 100` to give enough variety of tpoics for such a large number of texts. To compute `W` and `H`, the NMF algorithm initializes `W` and `H` with random small numbers and then performs gradient descent on each entry such that `|W * H| - |X|` is minimized and each entry converges to less than some very small threshold. Since this is non-deterministic, precise topics are not guaranteed to appear in the same column indices each time unless the same random seed is given each time.

<p align="center"><img src="https://github.com/jkvalentine/Biblical-Book-Sales/blob/master/images/nmf_diagram.png" width="600" /></p>

<H3 align="center">LDA</H3>

LDA is a probabilistic approach to topic modeling that uses Bayesian inference to offer another interpretation of latent topics contained in a corpus. Like before, I transformed the Project Gutenberg texts using the pickled tfidf model and then built an LDA model using this vectorized corpus. The words of the corpus are temporarily assigned to each of the `k = 100` topics I specified according to a Dirichlet distribution. For each document `d`, the LDA algorithm iterates through each word `w` and calculates `p(topic t|document d)` as the proportion of words in document `d` assigned to topic `t` and `p(word w| topic t)` as the proportion of assignments to topic `t` over all documents for `w`. Each word `w` is then assigned a new topic with probability `p(topic t|document d) * p(word w|topic t)` which amounts to the probability that topic `t` generated word `w` in document `d`. This process is repeated a large number of times until the model reaches equilibrium, with the result that each document is then represented as a distribution of topics based on each document's collection of words.

<p align="center"><img src="https://github.com/jkvalentine/Biblical-Book-Sales/blob/master/images/lda_process_diagram.png" width="600" /></p>
</br>
<p align="center"><img src="https://github.com/jkvalentine/Biblical-Book-Sales/blob/master/images/lda_matrix_diagram.png" width="600" /></p>



<H1 align="center">Sentiment Analysis</H1>
To give each text a polarity and subjectivty score, I performed sentiment analysis using TextBlob's polarity and subjectivity analyzers in `sentiment_analysis.py`. TextBlob uses the <a href="http://www.clips.ua.ac.be/pages/pattern-en#sentiment">Pattern</a> library to evaluate each word's polarity and subjectivity and then provides an average score based on the words in a string. The Pattern library has a database of words with associated polarity scores ranging from -1 as negative, 0 as neutral, and +1 as positive; similarly, subjectivity scores for each word range from 0, as highly objective, to +1, as highly subjective. The accuracy of of this library in classifying movie scripts that have been hand-labeled as positive, neutral, or negative is about 75%.   


<H1 align="center">Random Forest Regression</H1>
To make my sales predictions, I chose to use a random forest regressor because of the low number of predictors relative to the data points. In `create_data_frame.py`, I vectorize each best selling text using the pickled tfidf vectorizer, transform it using the pickled NMF and LDA models, and compare each to that of the transformed version of The Bible using a cosine similarity metric. To compare book sales for best selling texts throughout the years, I normalized their sales data by dividing by the number of years in publication, giving a target of average sales per year. 
</br>
I performed a test-train split using `train_test_val_split.py` with 20% of my data set aside as a testing set and the remaining 80% as my training set. To train the random forest regressor, I used the polarity and subjectivity scores, NMF and LDA cosine similarity scores, and each texts average sales per year. To train my model and make predictions, I used `random_forest_model.py`.

<H1 align="center">Results</H1>
The results of my model were found to be inconclusive. I used the random forest's out-of-bag error to calculate the r-squared error metric to evaluate my model. The r-squared score for the training data was `0.87` whereas the score for the test data was `-0.22`. This result indicates that my model is overfit to the data and that there is not enough data to distinguish the signal from the noise. Changing the testing and training data results in a testing r-squared score ranging from `-0.5` to `0.4` which shows that the error is highly dependent on the train-test split. This leads me to believe that I don't currently have enough data to confidently answer this question.
</br>
The most interesting component of this project is the topic modeling of the many thousands of english texts from Porject Gutenberg. The topics that arise from NMF and LDA seem to share some overlap, especially where religion and Christianity are concerned. Some obvious topical similarities include medical diseases, slavery in the U.S., French words, Old English words, and the U.S. Civil war. I find it very interesting that the topics that arose in these topic models aren't more universal themes of literature, like good versus evil or man versus nature, but rather highly nuanced and specific themes, like pirates or Eastern European folklore.

<H1 align="center">Future Work</H1>

To improve the results of this project, I would like to gather much more data to determine if there actually is a relationship between a text's topical similarity with The Bible and its sales data. I think my sales data is pretty biased towards best selling texts, and so in the future I would like to include a wider range of sales data, with more mid-range and low-selling texts as well. Obtaining sales data and the associated texts is the biggest challenge facing further work on project, but I think it is possible to expand on these findings.
