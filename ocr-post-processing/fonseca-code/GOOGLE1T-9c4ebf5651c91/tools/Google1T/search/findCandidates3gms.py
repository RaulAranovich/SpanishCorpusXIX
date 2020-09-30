# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""
#
"""
Future Work: Right now we check each file individual. This is good because 
we can parallel process each line; however if we do not choose to go that way
we should first run through all 3gms, make our file list. Then for each file run
all of the searches we need so we only open a file once and save all that loading in
"""
import time #Let's time how long it takes per search:
import sys  #For reading Command line arguments
import os
import subprocess

#Check Argument amount is right
if len(sys.argv) != 2:
    print "Usage: findCandidates3gms.py 3gm.idx"
    print "3gm.idx must be the official Google1T version of file"
    print "and be located in the 3gms folder along with all of the uncompressed google1T-3gms files"
    quit()
#print sys.argv[0] #Prints the Name of the File pwd/Filename
#print sys.argv[1] #Prints 3gm.idx
#print sys.argv[2] #Prints .output.3gms
print "Program will open file with 3 words on each line and locate for each one the candidate 3gms in Google1T"
print "To do this it will look in the index file to locate the right files to search before then searching through them."

fileindex = sys.argv[1]

files = os.listdir("output/3grams/")
files.sort()
for file in files:
    filename = "output/Google1T/search/" + file[:-4] + "candidates"
    file = "output/3grams/"+file
    outlines = [line.rstrip('\n') for line in open(file)]

    print >> sys.stderr, "File:", file

    fout = open(filename, 'w+')

    startTotal = time.clock()

    print "Total Lines to Process:", len(outlines)

    # We will store the index from 3gm.idx in order to search for our 3gram candidates
    # Each line in the file will be stored as [[words in line 1], [words in line 2], ...]
    indexlines = [line.rstrip('\n') for line in open(fileindex)]
    index = []
    for x in indexlines:
        index.append(x.split()) #split line into separate words
    print "Read", len(index), "lines from",fileindex, "That means a range of 0 -", len(index)-1

    print "Starting to process..."
    for currentLine in outlines:		### currentLine is a 3-gram associated with an incorrectly spelled middle word
        startFull = time.clock()		### We will time how long each line takes to process
        #Start of Timed Code ###

        fout.write("%%% "+currentLine+"\n") #Print %%% 3-gram in its own line to delinate start
        fout.flush() #Flush to avoid grep subprocess writing out of order

        words = currentLine.split() #split line into separate words

        #Start  searching right file(s) using index
        filesToCheck = []
        currLine = 0
        while currLine < len(index): #while not searched full index
            #Use first word to find candidate files
            if words[0] < index[currLine][1]: #First word is in the file before it
                if currLine == 0: #It's in the beggining so just saved that one
                    print words[0] + "is not in our database. Skipping it."
                    break
                else: #else add the one before it
                    print "Added Previous File for '"+words[0]+"' Prev File's first word was: '"+index[currLine-1][1]+"'"
                    print "and the current File's first word was '"+index[currLine][1]+"' which is after '"+words[0]+"'"
                    filesToCheck.append(index[currLine-1][0])

                # Word may exist in multiple files. Continue backwards to add previous files
                # until the current index is not equal to our word
                prevLines = currLine-1
                while prevLines > 0 and words[0] == index[prevLines][1]:
                    print "More than one candidate file found:"
                    print "was searching for: '"+words[0]+"' Prev File's first word was: '"+index[currLine][1]+"' so it was included"
                    filesToCheck.append(index[prevLines-1][0])
                    prevLines -= 1
                break

            if currLine == len(index)-1: #we reached the last file and it wasn't in the file before so maybe it's in this last one?
                if words[0] >= index[currLine][1]:
                    filesToCheck.append(index[currLine][0])
                    print "Added last file to search list as item was after the last index. Word:", words[0], "was after",index[currLine][1]
                if not filesToCheck: #if our list is still empty then it has to be in the last one
                    print "Warning: did not find any file to search in. This should never happen!"
                    print "was searching for: '"+words[0]+"' Last File's first word was: '"+index[currLine][1]+"'"
            currLine += 1
        #End of searching right file using index, answers should be in filesToCheck
        print "Finished Searching. Files to check:", filesToCheck

        #Checking files now... this is where the fun begins

        for currFile in filesToCheck:
            print "Checking in File: '"+currFile+"'"
            currFileAddr = fileindex[:-7]+currFile[:-3] #Add full address + remove the ending .gz since its uncompressed
            print "Expected File Path for File:", currFileAddr

            comment = ''' Cheat to comment out a block of code! ######################################################
###START OF SEARCH USING PYTHON METHOD
        #Open File (100mb), Expected to be found in same directory as index
        curr3gmFile = [line.rstrip('\n') for line in open(currFileAddr)]
        print "Total Lines to Process:", len(curr3gmFile)

        startpython = time.clock() #Time Python Process
        matchCount  = 0
        for currEntry in curr3gmFile:
            entry3gm = currEntry.split() #split line into separate words

            #Code can be made quicker by only checking the first few letters instead of using split function
            #print "Word Being Searched:", words[0]
            #print "Entry being Compared:", currEntry
            #print "Word Being Compared to (first word of entry):", entry3gm[0]

            if words[0] == entry3gm[0]: #Search Using Python string comparison
                matchCount += 1
                fout.write(currEntry+"\n") #Save Match Found in its own line
                #print "MATCH:", currEntry
        print "Total Matches Found:", matchCount

        #x= 0
        #while x < 10000:
        #    x +=1
        #    fout.write("\n")
        fout.flush()
        print "Search(python) Took:", time.clock() - startpython, "seconds."
###END OF SEARCH USING PYTHON METHOD
''' ##############################################################################################################



###START OF SEARCH USING GREP
            #grep '^WORD0 \w* WORD2' 3gm-0031
            #grep '^WORD0 ' 3gm-0031
            startGREP = time.clock()
            query1word = '^'+words[0]+' ' #Finds all Candidates with first word matching.
            if len(words) >= 3:
                query3word = "^" + words[0] + " \\w* " + words[2] #Finds all Candidates with First and Third word matching.
                #subprocess.call(["/bin/grep", query1word , currFileAddr ], stdout = fout)
            elif len(words) > 0:
                query3word = '^'+words[0]+' ' #Finds all Candidates with first word matching.
                print words, "is not a 3-gram"

            subprocess.call(["/bin/grep", query3word , currFileAddr ], stdout = fout)
            print "Search(grep) Took:", time.clock() - startGREP, "seconds."
###END OF SEARCH USING GREP

    #tempbreak += 1
    #if tempbreak > 10: break

    #End of Timed Code   ###
        print "Search Took:", time.clock() - startFull, "seconds." ### How long it took to process this line

    #Finished Checking File, Move on to the next 3gms line

    #if lineCount > 5: break #temporary to not process full file until code is done

    print "Finishing Process"  

    print "Total Time Taken by Program:", time.clock() - startTotal, "seconds."

    fout.close()
    print "End\n"
