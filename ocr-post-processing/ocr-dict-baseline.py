#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Nicole Dodd

Purpose of this script:
Get baseline for OCR errors
Compare OCR output to Spanish dictionary and calculate number of words that come up OOD (out of dictionary)

sys.argv[1] = .txt dict file (es-dict-bill.txt)
sys.argv[2] = path to directory with all .txt files to be processed
sys.argv[3] = name of processed .txt output file
sys.argv[4] = name of OOD .txt output file
'''

import sys, io, os, re
from nltk.corpus import SpanishReader


## Import dictionary ##########################################################

span_dict = []
with io.open(sys.argv[1], encoding = 'utf-8') as d:
    for word in d:
        word = word.rstrip('\n') # strip new line character from dict input
        span_dict.append(word)


## Open raw OCRed data to be processed ########################################

directory = sys.argv[2]
myspreader = SpanishReader.SpanishPlaintextCorpusReader(directory, '.*\.txt')
raw_span_text = myspreader.words()


## Process OCR output #########################################################
## (using data OCRd with Tesseract and cleaned with clean-ocr.py)

processed_text = []
OOD = []
for word in raw_span_text:
    if word in span_dict:
        processed_text.append(word)
    elif word not in span_dict:
        word = word + '<OOD>'
        processed_text.append(word)
        OOD.append(word)


## Output baseline stats ######################################################

total = int(len(processed_text))
missing = int(len(OOD))
accuracy = ((total - missing)/total)*100
print("OCR accuracy is " + str(round(accuracy)) + "%.")


## Write processed_text to file ###############################################

with io.open(sys.argv[3], 'w', encoding = 'utf-8') as f:
    f.write('\t'.join(processed_text))
f.close()

with io.open(sys.argv[4], 'w', encoding = 'utf-8') as f2:
    f2.write('\t'.join(OOD))
f2.close()
