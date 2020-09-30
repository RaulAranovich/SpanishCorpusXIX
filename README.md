# Spanish Corpus XIX & XX - a longitudinal study of American vs. Peninsular Spanish
## Authors: Nicole Dodd (ncdodd@ucdavis.edu), Daniel Lavados, and Raul Aranovich (raranovich@ucdavis.edu)

This project is a collection of XIX and XX century Spanish news and novels sourced from Project Gutenberg.

## /analysis
**keyness**
analysis of keyness of American vs. Peninsular dialects using a suite of statistical tests: chi-squared,
log likelihood ratio, odds ratio, KL divergence

TODO: add dispersion metric to frequency

**ust-vos**
analysis of the distribution of tu/usted and vosotros/ustedes by dialect (American and Peninsular) and
various domain splits


## /corpora-files
all corpora files
File name example: a-xix-d-gorostiza-pg12368.txt

First label: dialect
  a = American
  p = Peninsular
Second label: century
  xix = 19th century
  xx = 20th century
Third label: domain
  d = drama
  f = fiction
  n = non-fiction
  p = poem
  j = journal/news

TODO: finish OCR of El Imparcial


## /files

**google-ngrams**
ngram downloads

**ground-truth-sets**
hand-corrected OCR documents
(NB: aligned docs used specifically for training weighted Levenshtein edit matrices)

**ocr**
original OCRed documents to be corrected


## /newspapers
original newspapers from Project Gutenberg


## /ocr-post-processing
scripts and data used to develop OCR post-processing model

**fonseca-code**
baseline code used as inspiration for the current model (Fonseca, 2019) - courtesy of Dr. Jorge Fonseca

**levenshtein-edits**
code to create and matrices output for weighted Levenshtein edit distance

**output**
output from OCR post-processing model

TODO: finalize model (pseudocode already written)


## /scripts
other miscellaneous scripts

**clean-ocr.py**
clean OCR output - remove new lines, combine hyphenated words, export to new file with '-clean.txt' tag

**unified-file.py**
generate a single unified .txt file from multiple .txt files after OCR

**SpanishReader.py**
a specialized corpus reader for Spanish text, built as a class of nltk.corpus

**SpanishCorpusReader.ipynb**
Jupyter Notebook with SpanishReader tutorial

## /spanish-dict
all files and scripts used in creating the dictionary used for baseline OCR output
