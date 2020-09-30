# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""
#
"""
This program will mimick OCRSpell output but instead run it using Google Web 1T's own Dictionary (1-gram).
"""
import time #Let's time how long it takes per search:
import sys  #For reading Command line arguments
import os
import subprocess

#python tools/scripts/1gmSpell.py output/source-docs/ GoogleWeb1T/Google1T-3gms/1gms/vocab

#Check Argument amount is right
if len(sys.argv) != 3:
    print "Usage: 1gmSpell.py output/source_docs/ GoogleWeb1T/Google1T-3gms/1gms/vocab"
    print "\noutput/source_docs must be the directory you regularly would feed OCRSpell."
    print "Any file in the given directory will be read here"
    print "vocab is the location of the Google1T 1-gram file"
    quit()
#print sys.argv[0] #Prints the Name of the File pwd/Filename
#print sys.argv[1] #Prints output/source_docs
#print sys.argv[2] #Prints the location of the 1-gram vocab file
print "Program will mimick OCRSpell output but instead run it using Google Web 1T's own Dictionary (1-gram)."
#For Efficiency we will read into memory the entire vocab file since it is <200MB.

startTotal = time.clock()

#Make output Directory
outdirectory = 'output/1gmSpell/'  #Output to store files in
if not os.path.exists(outdirectory):
	os.makedirs(outdirectory)

#Naming Convention:
#In:  degrade.FR940104-0-00001.000
#Out: degrade.FR940104-0-00001.000.output

#Read vocab into memory:
#Tuples vs Dictionarys vs List. Apparently tuple may be faster but in reality it makes no difference for retrieval purposes 
#as proven by looking at the byte code: https://stackoverflow.com/questions/68630/are-tuples-more-efficient-than-lists-in-python
vocabtime = time.clock()
vocab = []
vocabfile = open(sys.argv[2], "r")
for line in vocabfile:
    vocab.append(line.split()[0])

print "Total Time Taken to read vocab:", time.clock() - vocabtime, "seconds."
print "Words Read:", len(vocab)
#print vocab



files = os.listdir(sys.argv[1])
files.sort()
for file in files:


    infile  = sys.argv[1] + file
    outfile = outdirectory + file + ".output"
    #print infile
    #print outfile

    #Read in the file to process
    print >> sys.stderr, "Processing File:", file #This should print out to runscript the current file being processed.
    lines = [line.rstrip('\n') for line in open(infile)]
    print "Total Lines to Process:", len(lines)

    #Open file to write our output
    fout  = open(outfile, 'w+')

    fout.write("@(#) Google 1T 1-Gram Spell Correction and OCRSPell Output Emulator Version 1 11/22/2018 by JF")
    for currLine in lines:
        #print "Line:", currLine
        words = currLine.split() #split line into separate words
	for word in words:
	    #print "Processing:", word

	    #Because OCRSpell assumes all numbers are errors. For now we will mark them as such. Either way in other parts of the parsing
	    #we ignore digits when generating our 3-grams. However if this was standalone we should perhaps ignore this just to test against
	    #Google 1T's for things like numbers. That said how can a number be mispelled? so perhaps it's good that this stays here
	    if word.isdigit():
		#print "Word is Digit. Assume it is an error for now"
		towrite = "\n# " + word + " 0" #For now print out like no candidate choices.

	    #Check if Spell Error:
	    elif word in vocab:  #Not Error
		#print "Found in Google1T. Not Spelling Error"
		towrite = "\n* " #For now print out like no candidate choices.

	    else:
		#print "Not Found in Google1T. Is Spelling Error"		
		towrite = "\n# " + word + " 0" #For now print out like no candidate choices.
	
	    #print towrite
	    fout.write(towrite)

#    exit() #FOR DEBUGGING

#End of Main Loop.

fout.close() #close outfile

print "Total Time Taken by Program:", time.clock() - startTotal, "seconds."











