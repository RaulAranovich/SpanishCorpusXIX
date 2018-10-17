import nltk
import re
import os
import sys
from nltk.corpus import PlaintextCorpusReader as PTR
from nltk.corpus import SpanishReader


def get_tokens(root1, root2):
    """
        Create two text files from two root directories.
        
        :parameters: Two root directories.
        The first root should be wherever the Spanish Gutenberg texts are located.
        The second root should be where all newspaper OCR text files are located.

        This will create a new text file named 'SpGut_tokens.txt'
        and another named 'Newspaper_tokens.txt' and will call a separate function
        which will compare the two.
    """
    #First we open a file from the first argument passed to our program which is the Spanish
    #Gutenberg corpus that we are sampling from.
    text1 = 'SpGut_tokens.txt'
    #We get our Spanish Reader to find the sorted set of all words across the books.
    myreader = PTR(root1, '.*\.txt')
    myspreader = SpanishReader.SpanishPlaintextCorpusReader(root1, '.*\.txt')
    token_list1 = sorted(set(myspreader.words()))
    token_set1 = set(token_list1) 
    #Here we open the text file using unicode encoding (necessary for the Spanish alphabet)
    #and write to it with a newline character after each token.
    f1 = open(text1, 'w+', encoding = "utf-8") 
    for token in token_list1:
        f1.write("%s\n" % (token))
    f1.close()
    #We follow the same process for the other text file, which is comprised
    #of scanned newspapers.
    #Note that because of the nature of OCR scanning, there will be natural typos in this corpus.
    text2 = 'Newspaper_tokens.txt'
    myreader = PTR(root2, '.*\.txt')
    myspreader = SpanishReader.SpanishPlaintextCorpusReader(root2, '.*\.txt')
    token_list = sorted(set(myspreader.words()))
    token_set = set(token_list)
    f2 = open(text2, 'w+', encoding = "utf-8")
    for tokens in token_list:
        f2.write("%s\n" % (tokens))
    f2.close()
    #Here we call the next function which will compare our two text files and
    #create a new text file of all words that are in one corpus but not the other.
    compare_corpora(text1, text2)

def compare_corpora(text1, text2):
    #Opening or creating all needed text files. First is a results file which will print all
    #words in one list but not the other, and the other two are the files we are comparing.
    result = open('results.txt', 'w+', encoding = "utf-8")
    gut_text = open(text1, 'r', encoding = "utf-8")
    news_text = open(text2, 'r', encoding = "utf-8")
    gut_set = set(gut_text.readlines())
    news_set = set(news_text.readlines())
    #general expression that will iterate tokens of one text and compare them to the tokens of another text.
    diff = news_set - gut_set
    for token in diff:
        result.write(token)
    #Closing all text files.
    gut_text.close()
    news_text.close()
    result.close()

#File 1 will be where all of the Spanish Gutenberg books are stored.
root1 = sys.argv[1]
#File 2 will be a file where all newspaper texts are.
root2 = sys.argv[2]
get_tokens(root1, root2)





    
