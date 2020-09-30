#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

import sys
import re
#Check Argument amount is right
if len(sys.argv) != 2:
    print "Usage: separateDocs.py 'Source File'"
    quit()
print sys.argv[0] #Prints the Name of the File pwd/Filename
print sys.argv[1] #Prints original
print "Program will open file and split them by documents"
document = sys.argv[1]

if "degrade" in sys.argv[1]:
	prefix = "degrade."
else:
	if "original" in sys.argv[1]:
		prefix = "original."
	else:
		print "Please label file as 'degrade.filename' or 'original.filename'"

filepath = "output/source-docs/"
filename = None
subdoc = 0	# if file is too large, it will be split into subdocuments

# write wordlist to file path/prefix.name.subdoc
def writedoc(path, prefix, name, subdoc, wordlist):
	if subdoc == 0:
		file = open(filepath + prefix + name + ".000", 'w+')
	else:
		name = name + "."
		if subdoc < 10:
			name = name + "0"
		if subdoc < 100:
			name = name + "0"
		file = open(filepath + prefix + name + str(subdoc), 'w+')
	for word in wordlist:
		# single quotes alone or as a pair cause OCRSpell to hang
		if word == "\'":
			word = "\""
		if word == "\'\'":
			word = "\"\""
		if word == "\'\n":
			word = "\"\n"
		if word == "\'\'\n":
			word = "\"\"\n"
		file.write(word)
	file.close()



with open(document, 'r') as myfile:
    allwords=myfile.readlines()

parsingDoc = False
ignoringLine = False
isDocName = False
file = None
totalwords = 0
wordcount = 0
savedwords = []
for line in allwords:
        line = re.sub("(&blank;/?)+", " ", line)
	line = re.sub("(&hyph;/?)+", "-", line)			# Switch to space later
	line = re.sub("(&amp;/?)+", "&", line)
	words = line.split(' ')
	if words[0] == "<!--":					#Ignore tagline
		continue
	ignoringLine = False
	for word in words:
		if ignoringLine:
			continue
		if isDocName: 					# We are reading the name of the new document
			wordcount = 0
			filename = word
			isDocName = False
			continue
		if "<DOC>" in word and not parsingDoc:		# Ignore <DOC> if its a tag
			continue
		if "<DOCNO>" in word and not parsingDoc:	# Ignore <DOCNO> if its a tag and following word will be the filename
			isDocName = True
			continue
		if "</DOCNO>" in word and not parsingDoc:	# Ignore </DOCNO> if its a tag
			parsingDoc = True
			continue
		if "</DOC>" in word:				#ignore </DOC>, close file and stop parsing
			writedoc(filepath, prefix, filename, subdoc, savedwords)
			parsingDoc = False
			print len(savedwords)
			savedwords = []
			subdoc = 0
			continue
		if "<" in word and ">" in word:
			ignoringLine = True
			continue
		if word == ")" or word == " " or word == "\n" or word == "\r" or word == "":
			continue

		if word[len(word)-1] == "\n":
			savedwords.append(word)
		else:
			savedwords.append(word+" ")

		if len(savedwords) == 1500:
			writedoc(filepath, prefix, filename, subdoc, savedwords)
			savedwords = []
			subdoc += 1
			print "Limit reached"

