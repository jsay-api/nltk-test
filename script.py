
# coding: utf-8
#__author__='julia sayapina'

"""

The script parces the files from the folder of user choice and writes id, title, text with type "UNPROC" 
(takes place if not <body></body>) and body if exists into the new files. 
Requires Python3, bs4, NLTK. nltk.download() should be run before the script execution. 
Usage: python script.py [--topwords] folderpath

"""

import nltk
import sys
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import BracketParseCorpusReader
from itertools import zip_longest
# nltk.download()


def parse_corpus(folderpath, option):
    """Opens files in corpus, parses them; acts like the mainthread"""

    onlyfiles = [join(folderpath, f) for f in listdir(folderpath) if (isfile(join(folderpath, f)) and (join(folderpath, f)).endswith('.sgm'))]  #gets th list of filenames (not dirs) with path 
    filtered_words = []
    default_stopwords = set(stopwords.words('english'))
    custom_stopwords = set(('mln', 'reuter', 'dlrs', 'pct', 'the', 'bc', 'reute', 'cts', 'shr', 'feb', 'vs', 'would', 'will', 'inc', 'corp', 'ltd', 'net', 'billion'))
    stops = default_stopwords | custom_stopwords

    for file in onlyfiles:
        filename = file.split('.')[0].split('/')[-1] #extracts the filename without path and extention to use in the name of the new file

        with open(file) as oldfile, open(join(folderpath, 'output_'+filename+'.xml'), 'w') as newfile:
            soup = BeautifulSoup(oldfile, 'html.parser')    #parses the document with BS

            make_xml(soup, newfile)
            if option: filtered_words = word_tokenizer(soup, stops, filtered_words)
            


    if option: top_words(filtered_words)


def process(tag, file):
    """Processes tag content and writes it into the file"""

    if tag:
        tagval = tag.text
        if tag.name == 'title':
            file.write('\t\t<subject>'+tagval+'</subject>\n')
        else:
            sents = sent_tokenize(tagval)
            for s in sents:
                file.write("\t\t<sentence>"+(s.replace('\n', ''))+"</sentence>\n")


def make_xml(soup, newfile):
    """Exctracts id, title, text, body of the article, devides them into sentences and writes all of that in the format required """

    newfile.write('<articles>\n')
    for reuter in soup.find_all('reuters'): #finds each <REUTERS ...> witch means the beginning of the new article
        idval = reuter['newid']
        newfile.write('\t<article id=”'+idval+'">\n')
        for title, text, body in zip_longest(reuter.find_all('title'), reuter.find_all('text', {'type' : 'UNPROC'}), reuter.find_all('body')):  
        #iterates through the title, text, body elements (even if one of them doesn't exist) and processes them
            for instance in [title, text, body]: process(instance, newfile) 
        newfile.write('\t</article>\n')
    newfile.write('</articles>')



def word_tokenizer(soup, stops, filtered_words):
    """Tokenises each file into words, add words of each file into the list"""

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(soup.getText())
    for word in words:
        word = word.lower()
        if word not in stops and not word.isnumeric() and len(word)>1:
            filtered_words.append(word)
    return filtered_words
    
def top_words(filtered_words):
    """Counts top 10 frequent words in the whole corpus"""

    fdist = FreqDist(filtered_words)    #finds the words qrequency disctribution
    top_ten = fdist.most_common(10)     #finds top 10 of them 
    print("""Top 10 frequent words\n_____________________\nword – count\n____________""")
    for i in top_ten: print('{0} – {1}'.format(i[0], i[1]))






def main():
    """Exctracts terminal commands"""
    args = sys.argv[1:]
    option = False

    if not args:
        print('usage: python script.py folderpath [--topwords]')
        sys.exit(1)

    if len(args) == 2: 
        option = True

    folderpath = args[0]
    parse_corpus(folderpath, option)

    sys.exit(1)


if __name__ == '__main__':
    main()
