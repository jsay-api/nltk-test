# here is the place to write which python we use
# coding: utf-8
#__author__='julia sayapina'

"""

The script parces the files from the folder of user choice and writes id, title, text with type "UNPROC" 
(takes place if not <body></body>) and body if exists into the new files. 
Requires Python3, bs4, NLTK. nltk.download() should be run before the script execution. 
Please check if there are no meta files in folder with corpus files (e.g., .DS_Stores).
Usage: python script.py [--topwords] folderpath

"""

import nltk
import sys
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from itertools import zip_longest
# nltk.download()


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


def make_xml(folderpath):
    onlyfiles = [join(folderpath, f) for f in listdir(folderpath) if (isfile(join(folderpath, f)) and (join(folderpath, f)).endswith('.sgm'))]

    for file in onlyfiles:
        filename = file.split('.')[0].split('/')[1]

        with open(file) as oldfile, open(join(folderpath, 'output_'+filename+'.xml'), 'w') as newfile:
            soup = BeautifulSoup(oldfile, 'html.parser')

            newfile.write('<articles>\n')
            for reuter in soup.find_all('reuters'):
                idval = reuter['newid']
                newfile.write('\n'+'\t<article id=”'+idval+'">\n')
                for title, text, body in zip_longest(reuter.find_all('title'), reuter.find_all('text', {'type' : 'UNPROC'}), reuter.find_all('body')):
                    for instance in [title, text, body]: process(instance, newfile)
                newfile.write('\t</article>\n')
            newfile.write('</articles>')



def top_words(folderpath):
    pass


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: python script.py folderpath [--topwords]')
        sys.exit(1)

    folderpath = args[0]
    make_xml(folderpath)

    if len(args) == 2: 
        top_words(folderpath)

    sys.exit(1)


if __name__ == '__main__':
    main()
