#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Purpose of this script:
## Generate unified .txt files from OCRed data
## Author: Nicole Dodd

## sys.argv[1] = path to .txt files to concatenate
## sys.argv[2] = name of final .txt file

import sys, io, os, re, natsort as ns

## Import separate .txt files #################################################

directory = sys.argv[1]
raw_text = []
sorted_files = ns.natsorted(os.listdir(directory)) # get ordered list of files 
for filename in sorted_files:
    if filename.endswith('.txt'):
        f = open((directory + filename), encoding = 'utf-8')
        for line in f:
            toks = re.split(' ', str(line))
            for tok in toks:
                if len(tok) != 0: # skips empty lines
                    raw_text.append(tok)


## Output to single .txt file ################################################

with io.open(sys.argv[2], 'w', encoding = 'utf-8') as f:
    f.write(' '.join(raw_text))

