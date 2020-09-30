#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Purpose of this script:
## Remove new lines from OCRed data
## Clean hyphenated words
## Export to new .txt file in 'clean/' folder w/in directory; same file name
## but with -clean.txt tag

## sys.argv[1] = path to directory of files to process

import os, sys, re, io

def clean_ocr(filename):
    new_contents = contents.replace('\n', ' ') # remove new lines, replace with space
    clean_contents = new_contents.replace('- ', '') #join hyphenated words

    return clean_contents


## NOTE: comment out one of the two following options

# if only reading in one file:
# file = open(sys.argv[1], encoding = 'utf-8')
# contents = file.read()
# clean_contents = clean_ocr(contents)

# with io.open((str(filename[:-4]) + '-clean.txt'), 'w', encoding = 'utf-8') as nf:
# 	nf.write(clean_contents)
# nf.close()

# if reading in multiple files:
directory = sys.argv[1]
end_directory = (directory + 'clean/') # must have 'clean/' folder beforehand
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        f = open((directory + filename), encoding = 'utf-8')
        contents = f.read()
        clean_contents = clean_ocr(contents)
        with io.open((end_directory + str(filename[:-4]) + '-clean.txt'), 'w', encoding = 'utf-8') as nf:
            nf.write(clean_contents)
            nf.close()
