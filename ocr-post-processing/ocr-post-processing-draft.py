#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Nicole Dodd (ncdodd@ucdavis.edu)

Purpose of this script:
Process OCR output and generate suggestions for error correction

Step 1: Check words against Spanish dictionary for misspellings
Step 2: Extract trigrams of misspelled words
Step 3: Find candidates for correction of word from Google ngrams
Step 4: Refine and prioritize candidates based on a frequency-based Levenshtein
edit distance (previously trained on data)
Step 5: Accept or reject edits
"""

import sys, io, re, os
from nltk.corpus import SpanishReader

## Set directory
directory = 'C:/Users/nicol/OneDrive/Documents/Education/Graduate - UCD/2020 Summer/GSR Spanish Corpus/'

## Import dictionary
span_dict = []
with io.open((directory + 'files/spanish-dict/es-dict-bill.txt'), encoding = 'utf-8') as d:
    for word in d:
        word = word.rstrip('\n') # strip new line character from dict input
        span_dict.append(word)

## Import weighted Levenshtein distances

## Get file list
corpus = directory + 'files/ocr/'
file_list = os.listdir(corpus)

## Define punctuation list
punct = ['-', '--', '\'', '\"', ';', '[', '—', '✚', '§', '#', '´', '<', '>', '+',
        '’', '=', ':', '$', ',', '“', '”', '»', '«', '"', ';', '¿', '?', '¡', '!',
        '_', '.', '(', ')', '[', ']', '{', '}', '*', '^', '-', ']', '...']

## Start function def #########################################################

def OCR_postprocess(file, output):
    words = []
    contents = SpanishReader.SpanishPlaintextCorpusReader(corpus, file)
    for word in contents.words():
        words.append(word) # makes sure words are a list of strings and not nltk format

## STEP 1: Check words against Spanish dictionary for misspellings
    token_index = 0
    for word in words:
        if word == '4':
            words[token_index] = 'á' # hand correcting a well-known error
            token_index += 1
        elif word in punct:
            token_index += 1 # skips tagging punctuation
        elif word in span_dict:
            token_index += 1 # skips tagging words in dict
        elif word not in span_dict:
            words[token_index] = word + '<OOD>' # tag misspelled word
            token_index += 1

## STEP 2: Extract trigrams of misspelled words
    trigrams = []
    token_index = 0 # reset index
    for word in words:
        if re.search('<OOD>', word):
            misspell_index = token_index
            word1 = words[token_index - 1]
            word2 = word
            word3 = words[token_index + 1]
            trigrams.append([str(misspell_index), word1, word2, word3])
            token_index += 1
        else:
            token_index += 1 # no error found; move on to next word

## STEP 3: Find candidates for correction of word
    candidates = []

# TODO: finish rest of model 

## STEP 4: Refine and prioritize candidates

## STEP 5: Accept or reject edits


##### WHEN WE FINALLY RUN IT#################################################

for file in file_list:
    OCR_postprocess(file, output)
