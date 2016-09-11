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

corpus_root = r"articles/"
file_pattern = r"[A-Za-z0-9-]+.sgm"
ptb = BracketParseCorpusReader(corpus_root, file_pattern)
print (ptb.fileids())
# file = 'reut2-000.sgm'
# default_stopwords = set(stopwords.words('english'))
# custom_stopwords = set(('mln', 'reuter', 'dlrs', 'pct', 'the', 'bc', 'reute', 'cts', 'shr', 'feb', 'vs', 'would', 'will', 'inc', 'corp', 'ltd', 'net', 'billion'))
# stops = default_stopwords | custom_stopwords

# with open(file) as oldfile:
#     soup = BeautifulSoup(oldfile, 'html.parser')

#     tokenizer = RegexpTokenizer(r'\w+')
#     words = tokenizer.tokenize(soup.getText())
#     filtered_words = [word.lower() for word in words if (word.lower() not in stops and not word.isnumeric() and len(word)>1)]
#     fdist = FreqDist(filtered_words)
#     top_ten = fdist.most_common(10)
#     print("('word', count)")
#     for i in top_ten: print(i)