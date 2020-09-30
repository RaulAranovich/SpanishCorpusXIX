# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

"""
Future Work: Right now we are reducing the candidates by levenshtein distance, then
once that is done we want to apply it to frequency to make it more manageable
also prioritize cases where the third word matches exactly as well.
"""

ldist = 4  ##MAX LEVENSHTEIN DISTANCE VALUE TO USE FOR SELECTING CANDIDATES!##

import time #Let's time how long it takes per 3gms
import sys  #For reading Command line arguments
#Check Argument amount is right
if len(sys.argv) != 2:
    print "Usage: refineCandidates.py file.candidates"
    quit()
#print sys.argv[0] #Prints the Name of the File pwd/Filename
#print sys.argv[1] #Prints file.candidates
print "Program will open file with 3gms phrase and possible candidates and reduce"
print "the amount of them based on levenstein distance and frequency"

startTotal = time.clock()

fileCandidates = sys.argv[1]

#Read in the file to process
lines = [line.rstrip('\n') for line in open(fileCandidates)]

#Open a file to write our refined andidates to
fout = open(fileCandidates+".clean", 'w')

#Open a file to write just the word suggestions to (for statistics)
fout2 = open(fileCandidates+".suggestions", 'w')

print "Total Lines to Process:", len(lines)

totCand = 0 #Counts Total Candidates Before Refining
newCand = 0 #Counts Total Candidates Kept after Refining

tempcount = 0 # Temp Variable to only run x iterations while we test code

#Some statistics
totCandALL = 0 #Counts Total Candidates Before Refining of All 3gms ran
newCandALL = 0 #Counts Total Candidates Kept after Refining of All 3gms ran
candCountList = [] #List of Number of Candidates.
noCandCount = 0 #Counts how many 3gms had no candidates to begin with

#Main Loop:

currPhrase = '' #Current Phrase being processed
currWord = ''   #Current Word being processed (the one we are trying to correct)
candidateWords = [] #Stores Candidate Words we think may the correct answer

for currLine in lines:         
    #print "Line:", currLine

    words = currLine.split() #split line into separate words    
    if words[0] == '%%%':
        if tempcount > 0:
#            print "Finished 3gms phrase: '"+currPhrase+"'."
            if len(candidateWords) > 0:
                print "Reduced from", totCand, "candidates to", newCand, "candidates." 
                print "Candidates for '"+currWord+"':", candidateWords        
            else:
                print "No Reduction achieved for this 3gms"

            fout.write("&&& ")
            for word in candidateWords: fout.write("%s " % word) #Write Candidates
            fout.write("\n")
            
            #Write suggestions to 2nd file for statistics (its a copy)
            if len(candidateWords) > 0: #only write if candidates remain
                fout2.write(currWord+":          \t") 
                for word in candidateWords: fout2.write("%s, " % word)
                fout2.write("\n")
        
        #Print Candidate words at the bottom of 
        #candidates, the &&& signify special line... btw I should go back to old scripts
        #and make %%% instead of % to avoid possible errors incase thats part of the 3gm!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!NOTE, TODO!!!!!!!!!!!##

        #Stats
            newCandALL = newCandALL + newCand #Update our running Count
            totCandALL = totCandALL + totCand #Update our running Count
            candCountList.append(newCand) #Add to our list of candidate counts
            if totCand == 0: noCandCount +=1
        
        totCand = 0 #Reset Counter for new phrase
        newCand = 0 #Reset Counter for new phrase
        candidateWords = [] #Reset list for new words
        currPhrase = currLine #Load in new current Phrase
        currWord = words[2] # Load in new word to compare to
        print "Starting new 3gms phrase:", currPhrase
        fout.write(currLine+"\n") #Print % 3 gram in its own line to delinate start

        tempcount +=1 #need to increase our tempcount since we have a continue        
        continue #To avoid using an else statement and having to tab the code
    
    #Process Candidate, use Levenshtein Distance
    #print "Current Mispelled Word:", currWord, "from '"+currPhrase+"'"
    #print "and comparing to correct word '"+words[1]+"'"
    totCand +=1 #For Candidate being checked

    import editdistance
    if editdistance.eval(currWord, words[1]) <= ldist: #If words[1] has levenshtein distance of ldist or less:
        fout.write(currLine+"\n") #Print Candidate since we are keeping it
        if words[1] not in candidateWords: #Avoid adding duplicates
            candidateWords.append(words[1])  
            newCand +=1 #For Candidates kept
#            print "Added Candidate Word:", words[1]

#sudo apt-get install python-setuptools
#sudo python setup.py install

#Levenshtein
# import Levenshteinprint "Reduced from", totCand, "candidates to", newCand, "candidates." 
# Levenshtein.ratio('hello world', 'hello')
#Result: 0.625     (RATIO IS correct letters DIVIDED BY TOTAL)


#Ratcliff/Obershelp:
# import difflib
# difflib.SequenceMatcher(None, 'hello world', 'hello').ratio()
#Result: 0.625


#sudo apt install python-pip
#pip install editdistance
#Levenshtein Edit Distance:
#import editdistance
#editdistance.eval('banana', 'bahama')
#Result: 2L

    comment = ''' Cheat to comment out a block of code!

TODO: right now we have a hardcoded levenshtein value. What I will do next is
make that section into a recursive function where the value of levenshtein is
increased one at a time until size of word. This way I only get the best 
candidates possible and they are organized in a mix of distance and frequency.


import editdistance

editdistance.eval('banana', 'bahama')
Out[3]: 2L

import Levenshtein

Levenshtein.ratio('banana', 'bahama')
Out[5]: 0.6666666666666666
print "Reduced from", totCand, "candidates to", newCand, "candidates." 
import difflib

difflib.SequenceMatcher(None, 'banana', 'bahama').ratio()
Out[7]: 0.6666666666666666

Levenshtein.ratio('banana', 'banama')
Out[9]: 0.8333333333333334

6/7
Out[10]: 0

6/5
Out[11]: 1

6.0/5
Out[12]: 1.2

5/6.0
Out[13]: 0.8333333333333334

'''




#SEE:   http://stackoverflow.com/questions/17388213/find-the-similarity-percent-between-two-strings
#       https://pypi.python.org/pypi/editdistance
#       http://stackoverflow.com/questions/6690739/fuzzy-string-comparison-in-python-confused-with-which-library-to-use
#       https://pypi.python.org/pypi/python-Levenshtein
    
    #if tempcount > 30: break #Temp break to only run x iterations while we test code
    tempcount +=1    
    

    
    
#End Main Loop.  
print "Finishing Process"  
print "Reduced from", totCandALL, "candidates to", newCandALL,"candidates."
print "That's a", float(newCandALL)/totCandALL ,"% reduction."


candCountList.sort() #Sort List 
print "Candidate Counts:", candCountList

print noCandCount, "3gms had 0 candidates given from Google1T."

print "Candidates found for", len(candCountList) - candCountList.count(0), "of",len(candCountList),"3gms."
print candCountList.count(0) - noCandCount, "3gms had candidates but were all lost with the current Levenshtein value."

print "The largest number of candidates for a singe 3gms is:", candCountList[-1]
print "The second largest is:", candCountList[-2]

print "Total Time Taken by Program:", time.clock() - startTotal, "seconds."


#fileCandidates.close()
fout.close()
fout2.close()
print "End"