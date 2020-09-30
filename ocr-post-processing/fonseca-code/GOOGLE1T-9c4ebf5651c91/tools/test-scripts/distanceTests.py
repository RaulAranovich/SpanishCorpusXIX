# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 19:58:03 2017

@author: Jorge Fonseca
"""

print "Python Script to compare Levenshtein and Ratcliff/Overshelp"

import editdistance #Install with:  pip install editdistance
word1 = 'Mountain'
word2 = 'iiiountain'
print word1, word2
print "Levenshtein distance: ", editdistance.eval(word1, word2)

import Levenshtein #need to download from: https://pypi.python.org/pypi/python-Levenshtein 
print "Levenshtein Ratio (correct letters / total letters):", Levenshtein.ratio(word1, word2)

import difflib #Ratcliff/Obershelp
print "Ratcliff/Obershelp Ratio:", difflib.SequenceMatcher(None, word1, word2).ratio()




word1 = 'mountain'
word2 = 'rnountain'
print word1, word2
print "Levenshtein distance: ", editdistance.eval(word1, word2)

import Levenshtein #need to download from: https://pypi.python.org/pypi/python-Levenshtein 
print "Levenshtein Ratio (correct letters / total letters):", Levenshtein.ratio(word1, word2)

import difflib #Ratcliff/Obershelp
print "Ratcliff/Obershelp Ratio:", difflib.SequenceMatcher(None, word1, word2).ratio()




word1 = 'mountain'
word2 = 'mou'
print word1, word2
print "Levenshtein distance: ", editdistance.eval(word1, word2)

import Levenshtein #need to download from: https://pypi.python.org/pypi/python-Levenshtein 
print "Levenshtein Ratio (correct letters / total letters):", Levenshtein.ratio(word1, word2)

import difflib #Ratcliff/Obershelp
print "Ratcliff/Obershelp Ratio:", difflib.SequenceMatcher(None, word1, word2).ratio()
