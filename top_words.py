# coding: utf-8
#__author__='julia sayapina'

import nltk
import sys
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus import stopwords #new
from nltk.probability import FreqDist #new
from nltk.tokenize import word_tokenize #new
from nltk.tokenize import RegexpTokenizer #new
from nltk.corpus import BracketParseCorpusReader #new
from itertools import zip_longest


default_stopwords = set(stopwords.words('english'))
custom_stopwords = set(('mln', 'reuter', 'dlrs', 'pct', 'the', 'bc', 'reute', 'cts', 'shr', 'feb', 'vs', 'would', 'will', 'inc', 'corp', 'ltd', 'net', 'billion'))
stops = default_stopwords | custom_stopwords
corpus_root = r"articles/"
file_pattern = r"[A-Za-z0-9-]+.sgm"
ptb = BracketParseCorpusReader(corpus_root, file_pattern)
filtered_words = []
onlyfiles = [join(corpus_root, f) for f in ptb.fileids()]

# file = 'reut2-000.sgm'


for file in onlyfiles:
	with open(file) as file:
	    soup = BeautifulSoup(file, 'html.parser')

	    tokenizer = RegexpTokenizer(r'\w+')
	    words = tokenizer.tokenize(soup.getText())
	    for word in words:
	    	word = word.lower()
	    	if word not in stops and not word.isnumeric() and len(word)>1:
	    		filtered_words.append(word)
fdist = FreqDist(filtered_words)
top_ten = fdist.most_common(10)
print("word – count")
for i in top_ten: print('{0} – {1}'.format(i[0], i[1]))