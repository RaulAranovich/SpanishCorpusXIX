# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

import sys
import os
#Check Argument amount is right
if len(sys.argv) != 1:
    print "Usage: get3gram.py"
    quit()
#print sys.argv[0] #Prints the Name of the File pwd/Filename
print "Program will open OCRSpell output files and find for all entries the preceding word and the word after along with line/word number"


def process_line(words, ocrlines, file_output):
        #words = [x for x in words if x != ')' and x != '.' and x != ' ' and x != '']
        fout = open(file_output, 'w+')

        print "Number of words in cleaned OCR file: ", len(words)
        print "Total words parsed in OCRSpell File: ", len(ocrlines)-1 #Minus 1 because first line of OCRSpell is @Program Title
	if len(words) != len(ocrlines)-1:
		print "Warning: Number of Lines Do Not Match", len(words), " ", len(ocrlines)-1

	alignmentErrors = 0
	alignmentFixes = 0
        currentword = 0
	docOffset = 0 #To keep track of offset due to misalignments!
        for currentline in ocrlines[1:]:
                if currentline[0] == '*':
                        print "Marked as correct by OCRSpell. Skipping. . ."
                        currentword += 1
                        continue

                # Found either a digit or an incorrectly spelled word
                parts = currentline.split() #This is so we can grab the incorrectly spelled word which is the 2nd token in a line in ocrspell
                print "OCRSPELL: ", parts[1], " DOC: ",  words[currentword] #Print out the word we are working with
                if parts[1].isdigit(): #check if its a number
                        print "Cannot correct a number ", parts[1], ". Skipping. . ."
                        currentword += 1
                        continue

		#If we got this far it's not a number, so it means it must be a mispelled word
                if currentword < 1 or currentword + 1 >= len(words): #beginning or end so we can't get surrounding words for 3gms, so skip it
                        print "Skipped one"
                        #fout.write("* " + parts[1])
                        currentword += 1
                        continue

		#Ok so we know it's a mispelled word so let's make sure it matches the location in our clean file before trying to grab the
		#neighboring words
                if parts[1] != words[currentword]:
                        print "Alignment Error: "  #This means that the words don't match! This is bad!
                        print "\t OCR word: " + parts[1]
                        print "\t Doc word: " + words[currentword]
			alignmentErrors += 1 

			#Let's try to fix it. It's most likely due to OCRSpell having skipped a word in it's output. 
			#Like with the single ) parenthesis so let's go ahead and check words[currentword-1] which
			# is the word before it to see if we match and if so then we're good to go.
			matchfound = False
			print "Checking Previous 5 word in DOC:"
			for n in range(1,6):
				if currentword-n < 0:
					break #End of document, fail otherwise will access outside of range
				if parts[1] == words[currentword-n]: #If it matches we're saved!
					print "Match Found!:", parts[1], words[currentword-n], " Aligned at: ", n
					docOffset = docOffset - n	
					currentword -= n
					alignmentFixes += 1
					matchfound = True
					break	
			if not matchfound: #if we found match then we don't need to do this.
				print "Checking Next 5 word in DOC:"				
				for n in range(1,6):
					if currentword+n >= len(words):
						break #End of document, fail otherwise will access outside of range
					if parts[1] == words[currentword+n]: #If it matches we're saved!
						print "Match Found!:", parts[1], words[currentword+n], " Aligned at: ", n
						docOffset = docOffset + n	
						currentword += n
						alignmentFixes += 1
						matchfound = True
						break	
			#Next, let's add Levenshtein with an edit distance for tokens greater than 4 characters
			if len(parts[1]) > 4 and not matchfound:	#Don't forget to check if we already found a match, if so we are done!
       				import editdistance # pip install editdistance
				if len(parts[1]) > 5:
					ldist = 3
				else:
					ldist = 2
				print "Checking Previous 5 word in DOC with edit distance ", ldist, ":"
				for n in range(0,6): #range is 0 since we want to check same word
					if currentword-n < 0:
						break #End of document, fail otherwise will access outside of range
					if editdistance.eval(parts[1], words[currentword-n]) <= ldist: #If it matches we're saved!
						print "Match Found!:", parts[1], words[currentword-n], " Aligned at: ", n
						docOffset = docOffset - n	
						currentword -= n
						alignmentFixes += 1
						matchfound = True
						break	
				if not matchfound: #if we found match then we don't need to do this.
					print "Checking Next 5 word in DOC with edit distance ", ldist, ":"			
					for n in range(0,6): #range is 0 since we want to check same word
						if currentword+n >= len(words):
							break #End of document, fail otherwise will access outside of range
						if editdistance.eval(parts[1], words[currentword+n]) <= ldist: #If it matches we're saved!
							print "Match Found!:", parts[1], words[currentword+n], " Aligned at: ", n
							docOffset = docOffset + n	
							currentword += n
							alignmentFixes += 1
							matchfound = True
							break	

			if not matchfound:
				print "Error: No Match Found for '", parts[1], "'. Skipping. . ."
                        	currentword += 1
                        	continue
			

                print "Word Before: '" + words[currentword - 1] + "' \nWord After: '"+words[currentword+1]+"' Location:",currentword
                print words[currentword - 1], parts[1], words[currentword + 1], str(currentword) #equivalent written to file
                fout.write(words[currentword - 1]+" "+parts[1]+" "+words[currentword + 1]+" "+str(currentword)+"\n")
                currentword += 1

        fout.close()
	print "Alignment Errors: ", alignmentErrors
	print "Alignment Fixes: ", alignmentFixes
	print "Offset: ", docOffset


files = os.listdir("output/source-docs")
totalFiles = len(os.listdir("output/OCRSpell"))
currentFile = 0
# We will need the files sorted by name in order to join subdocuments into a single document
files.sort()

subdoc = False
words = []
ocrlines = []
for file in files:
        print "Processing:", currentFile, "of", totalFiles
	# IF it is a subdocument, merge back into one document
	# IF we find a standalone document, process what we have and start anew
	if int(file[-3:]) > 0:
		subdoc = True
	else:
		if words != []:
			process_line(words, ocrlines, file_output)
			words = []
			ocrlines = []
		subdoc = False

	if not subdoc:
		file_output = "output/3grams/" + file + ".3gms"

	file_ocr = "output/OCRSpell/" + file + ".output"
        file = "output/source-docs/" + file
        if not os.path.isfile(file_ocr):
		print file, "has not been run through OCRSpell yet. SKipping"
		continue

	currentFile += 1

	words.extend(open(file, 'r').read().replace('\n', ' ').split())

	ocrlines.extend([line.rstrip() for line in open(file_ocr)])


"""
What we want is to take FR9401040.0.output and for each entry that is not a number, we want to find the word before it and after.
We then want to output a file that has format:


number word1 word2 word3

number is the location in text (to add later on)

word1 and word3 are surrounding words

word2 is our misspelled word

"""
