# here is the place to write which python we use
# coding: utf-8
#__author__='julia sayapina'

"""

The script parces the files from the folder of user choice and writes id, title, text with type "UNPROC" 
(takes place if not <body></body>) and body if exists into the new files. 
Requires Python3, bs4, NLTK. nltk.download() should be run before the script execution.

"""

from bs4 import BeautifulSoup
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from itertools import zip_longest
# nltk.download()


folder = 'articles/'
# file = 'reut2-000.sgm'

for file in folder:
    filename = file.split('.')[0]

    def process(tag):
        """Processes tag content and writes it into the file"""
        if tag:
            tagval = tag.text
            if tag.name == 'title':
                newfile.write('\t\t<subject>'+tagval+'</subject>\n')
            else:
                sents = sent_tokenize(tagval)
                for s in sents:
                    newfile.write("\t\t<sentence>"+(s.replace('\n', ''))+"</sentence>\n")
            
            

    with open(file) as oldfile, open('output_'+filename+'.xml', 'w') as newfile:
        soup = BeautifulSoup(oldfile, 'html.parser')

        newfile.write('<articles>\n')
        for reuter in soup.find_all('reuters'):
            idval = reuter['newid']
            newfile.write('\n'+'\t<article id=”'+idval+'">\n')
            for title, text, body in zip_longest(reuter.find_all('title'), reuter.find_all('text', {'type' : 'UNPROC'}), reuter.find_all('body')):
                for instance in [title, text, body]: process(instance)
            newfile.write('\t</article>\n')
        newfile.write('</articles>')






# def main():
# 	if len(sys.argv) != 2:
#         print('usage: python script.py {--topwords} folder')
#         sys.exit(1)

#     option = sys.argv[1]
#     corpus = sys.argv[2]
#     if option == '--count':
#         print_words(corpus)
#     # else:
#     #     print('unknown option: ' + option)
#     sys.exit(1)


# if __name__ == '__main__':
#     main()
