#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Nicole Dodd

Purpose of this script:
Get misspelled words from OCR output (tagged as <OOD> with ocr-dict-processing.py)
Pull trigrams for each misspelled word

sys.argv[1] = path to .txt file to process
sys.argv[2] = name of output file 
'''

import sys, os, re, io

trigrams = []

punct = ['-', '--', '\'', '\"', ';', '[', '—', '✚', '§', '#', '´', '<', '>', '+',
        '’', '=', ':', '$', ',', '“', '”', '»', '«', '"', ';', '¿', '?', '¡', '!',
        '_', '.', '(', ')', '[', ']', '{', '}', '*', '^', '-', ']', '...']

def process_line(ocrlines, file_output):
    file = open(ocrlines, 'r')
    ocr_contents = file.read()
    ocr_words = ocr_contents.split()

    token_index = 0

    for word in ocr_words:
        if word.isdigit(): # skip correcting numbers
            token_index += 1
        # might not need the below if punct isn't tagged as OOD
        #elif word in punct: # skip correcting punctuation
        #    token_index += 1
        elif re.search('<OOD>', word):
            misspell_index = token_index
            word1 = ocr_words[token_index - 1]
            word2 = word
            word3 = ocr_words[token_index + 1]
            trigrams.append([str(misspell_index), word1, word2, word3])
            token_index += 1
        else:
            token_index += 1 # no error found; move on to next word

    with io.open(file_output, 'w', encoding = 'utf-8') as f:
        for gram in trigrams:
            f.write(('\t'.join(gram)) + '\n')

input = sys.argv[1]
output = sys.argv[2]

process_line(input, output)
