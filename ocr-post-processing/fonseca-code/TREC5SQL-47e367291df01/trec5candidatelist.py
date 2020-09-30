#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

import sys
import mysql.connector as mc
import Levenshtein  #pip install python-levenshtein
import difflib #apt-get install npm; npm install difflib
import time
from datetime import timedelta
time0 = time.time()

#Importing from our common file: trec5common
from trec5commons import confMatrix
from trec5commons import docErrorList
from trec5commons import candidates
#Importing Complete

#Check my sql connection
try:
    connection = mc.connect (host = "localhost",
                             user = "pythonuser",
                             passwd = "",
                             db = "TRECSample")
except mc.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)
cursor = connection.cursor()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone()
print("Server Version:", row[0])
#cursor.close()
#connection.close()
#Done Checking Sql

#Check Argument amount is right
if (len(sys.argv) != 3):
    print "Usage: trec5candidatelist.py 0 606"
    print "OR     trec5candidatelist.py 0 0"
    quit()
print sys.argv[0] #Prints the Python Executable
print "Start:", sys.argv[1] #Prints Starting Location
print "End:", sys.argv[2] #Prints Stop Location
print "Program will read database table docErrorList and matchfailList and "
print "create/update Candidate List with potential candidadtes "
print "First Parameter will be starting document location."
print "Second parameter is ending document location."
print "If ending location is same as start it will use all rows in doctextSolutions."
print "Program will produce: \"candidates_output.txt\" with more information on process."

startLocation = int(sys.argv[1])
endLocation   = int(sys.argv[2])
currentLocation = startLocation
maxLocation=0
minLocation=0
currDoc="00000000-0-00000"
processedCount = 0
candidateCount = 0
candidateDicList = {} #Create the empty candidateLists dictionary data structure
candidateList = [] #This will keep all candidates for all words, once we finish finding all then we push them all to database
MAX_CANDIDATE_COUNT = 6 #The following will limit the number of candidates to be printed in our candidates_output.txt file to this value
candidateCountPrinted = 0 #This is how we keep track of how many candidates are printed so we can stop at the max set above.
#Sample IF STATEMENT USED TO CHECK: if candidateCountPrinted <= MAX_CANDIDATE_COUNT:

MAX_CANDIDATES_ALLOWED = 20 #This is the maximum amount of candidates allowed per word (useful because some 1 or 2 letter words can give us like 1,000 candidates.

#This code has been movied to trec5common.py
'''
#Class to Store Confusion Matrix Entry (fromletter, toletter, frequency)
class confMatrix:
    def __init__(self, fromletter, toletter, frequency):
	self.fromletter = fromletter
	self.toletter 	= toletter
	self.frequency 	= frequency
#    def __init__(self):
#	self.fromletter = ""
#	self.toletter 	= ""
#	self.frequency	= 0
    def __repr__(self):
	return '\nconfMatrix(%s, %s, %d)' % (self.fromletter, self.toletter, self.frequency)
    def __eq__(self, other):
	if isinstance(other, confMatrix): #If both are same object type
	    return ( (self.fromletter == other.fromletter) and (self.toletter == other.toletter) ) #For equality compare from and to letters to ensure equality
	else:
	    return False #They are not same object type so don't even bother checking
    def __ne__(self, other): #for !equals
	return (not self.__eq__(other)) #rather than rewriting function just return opposite of what the above gives
    def __hash__(self):
	return hash(self.__repr__())
'''
#End of Code Moved to trec5common.py

#Confusion Matrix List incase we wish to store local copies to speed up program of entries that we have visited (saves overhead)
confMatrixList = [] #Create the empty list 
entry = confMatrix(" "," ", 0)  #Create an object of type confMatrix to represent the Empty Item
confMatrixList.append(entry)    #insert it to the ongoing list

#Levenshtein Function Test Code (Unused):
#a ="car"
#b ="cat"
#print "Levenshtein Distance between '"+a+"\' and \'"+b+"\' is", Levenshtein.distance(a,b), ".\n"
#quit()

#Start of Code:

#Get Max Location so we don't go too far.
cursor.execute("""SELECT MAX(docErrorList.location) FROM docErrorList 
		  WHERE docErrorList.location NOT IN(SELECT location FROM matchfailList);""")
sqlcommandresults = cursor.fetchall()
for x in sqlcommandresults:
    if str(x[0]) != "None":
        maxLocation = x[0]
    else:
	maxLocation = 0 #Empty Database BAD!
	print "Database is Empty! Aborting"
	quit()
#Done
if endLocation == 0: #we need to create candidates for full Error table so copy that over
    endLocation = maxLocation
if endLocation > maxLocation: #Out of range Error
    print "ERROR: End Location", endLocation,"is greater than Max Location",maxLocation, "in table!"
    quit()

#Get Min Location since it may not be 0 as first error may not be first word.
cursor.execute("""SELECT MIN(docErrorList.location) FROM docErrorList 
		  WHERE docErrorList.location NOT IN(SELECT location FROM matchfailList);""")
sqlcommandresults = cursor.fetchall()
for x in sqlcommandresults:
    if str(x[0]) != "None":
        minLocation = x[0]
    else:
	minLocation = 0 #Empty Database BAD!
	print "Database is Empty! Aborting"
	quit()
#Done

if currentLocation < minLocation: #We are starting in the beginning but first word is not first error so update
    currentLocation = minLocation

#Next let's read in onegmsORIGINAL as this can be used in lieu of a dictionary.
print "Using onegmsORIGINAL in lieu of a dictionary for Candidate Generation."
onegmsOR = {" ": 0} #Create the empty dictionary 
cursor.execute("SELECT * FROM onegmsORIGINAL;")
sqlcommand1gmsOR = cursor.fetchall()
for row in sqlcommand1gmsOR:
    onegmsOR[str(row[0])] = int(row[1])
#Done

#Let's write our candidates output to a file
fout = open("output/candidates_output.txt", "a")

#We are going to do it by document. This makes it harder than it has to be but ensures we have full control and a manageable size query

#Main Loop: 
while currentLocation <= endLocation:
    #First We have to get the next document name by checking our currentLocation
    cursor.execute("SELECT docsource FROM docErrorList WHERE location = "+str(currentLocation)+";")
    sqlcommandresults = cursor.fetchall()
    oldDoc = currDoc #Save last doc we were working with
    for x in sqlcommandresults:
	currDoc  = x[0]
    if oldDoc == currDoc: #Check if we received a new document different to last one we worked on
	break #we reached end of database so we are just getting back the same document so we are done!
    print "Processing Document:", currDoc
    fout.write("Processing Document: " + currDoc+"\n") #Writing to Output File

    #Next let's query all rows with that document name
    cursor.execute("""SELECT docErrorList.word, docErrorList.location, 
		      docErrorList.docsource FROM docErrorList 
		      WHERE docErrorList.location NOT IN(SELECT location FROM matchfailList)
		      AND docErrorList.docsource = \""""+currDoc+"""\";""")
    docElist = cursor.fetchall()
    errorList = [ docErrorList(x[0], x[1], x[2]) for x in docElist ] #Create Objects and Fill them with row data

    #Handle Each Entry in our Error List by generating appropriate candidates
    for errorentry in errorList:
	errorWord = str(errorentry.word)
	#errorList (word, location, docSource)
	#frequency = onegmsOR["word"]
	#onegmsOR.get("word", -1) #Will return -1 if key not found in dictionary
	fout.write("\nProcessing word: "+errorWord+" at Location "+str(errorentry.location)+"\n")

	#Step 1) We will compare our typo (ocr error word) to the dictionary/onegmsORIGINAL table and generate possible candidates 
	#where typo and dictionary have a max edit distance of 3 (for starters). We will store this in a dictionary of lists so that
	#We can use dynamic programming to speed up the process since we may see the same typo more than once. This however may get space intensive with a space
	#complexity of O(n*m) where n is size of our error list and m is size of dictionary. However our time complexity will go down from O(n*k) to O(n*logk)
	MAX_EDIT_DISTANCE = 3
	#Check if we already generated candidates for this word before (typo appeared more than once! Yay Dynamic Programming)
	if errorWord not in candidateDicList: #If it hasn't then go ahead and work it, else move on
	    candidateDicList.setdefault(errorWord, []) #If we haven't 
	    for wdic in onegmsOR:
	        if Levenshtein.distance(wdic, errorWord) <= MAX_EDIT_DISTANCE:  #Relevant to us since edit distance less than or equal to 3
		    candidateDicList[errorentry.word].append(wdic)

        candidateCount = len(candidateDicList[errorentry.word])  #Look up how many candidates for this word so the printing limits work
	fout.write("Found "+str(candidateCount)+" candidate words.")
	if candidateCount <= MAX_CANDIDATE_COUNT:
	  fout.write("\n")
	else:
	  fout.write(" But we are only printing the first "+str(MAX_CANDIDATE_COUNT)+" candidates (See "+str(sys.argv[0])+" to change this).\n")
	if candidateCount > MAX_CANDIDATES_ALLOWED:
		fout.write("More than the "+str(MAX_CANDIDATES_ALLOWED)+ " maximum allowed candidates found. ")
		fout.write(str(candidateCount - MAX_CANDIDATES_ALLOWED)+" will not be processed(See "+str(sys.argv[0])+" to change this).\n")			
	#At this point there is an entry in candidateDicList with all the possible words for our errorWord
	#print "CandidateDicList:", candidateDicList
	
	#Step 2) For each word we are going to generate a candidates entry and populated it. 
	#candidates (location, fromword, toword, distance, confWeight, uniFreq, bkwdFreq, fwdFreq, output, decision, docSource)
	candidateCountPrinted = 0 #reset candidates printed since it's new word
	for candidateWord in candidateDicList[errorWord]:
	    #Get Distance
	    dist = Levenshtein.distance(errorWord, candidateWord)

	    #Because some short words can give us huge amount of candidates we will cut down on them.
	    #if the candidate count is greater than our max allowed we will allow only Half the maximum allowed without restrictions,
	    #but for the rest we will only allow candidates with distance of 1. If even this way we reach our hard max then no more
	    #candidates will be allowed at all and we will move on to the next word.
	    if candidateCountPrinted > MAX_CANDIDATES_ALLOWED:
		fout.write("Reached Maximum Candidates Allowed: "+str(MAX_CANDIDATES_ALLOWED)+" Skipping rest.\n")
		break #We have a word with a lot of candidates and we printed as many as max so no more
	    if candidateCountPrinted > (MAX_CANDIDATES_ALLOWED / 2) and dist > 1 and candidateCount > MAX_CANDIDATES_ALLOWED:
		continue #We printed first 10 without limits but nowe we only print with dist 1, 
		#The last AND is incase candidateCount is <MAX but greater than MAX/2 in that case we don't restrict.
			

	    #Get confWeight (uses difflib / same code used in trec5confusionmatrix - I may end up doing this as a shared function eventually)
	    confWcount = 0 #For words with edit distances greater than 1 we will need to do some math based on number of weights, so keep count
			   #maybe we use sum, or average or take highest????
	    confW = 0
	    fl = " "
	    tl = " "
	    a = errorWord
	    b = candidateWord #To make code easier to read
	    s = difflib.SequenceMatcher(None, a, b) #from docs.python.org
	    #print "%-12s -> %-17s Distance: %d" % (errorWord, candidateWord, dist) #Spaced out Print to look nicer
	    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
	      fout.write("%-12s -> %-17s Distance: %d\n" % (errorWord, candidateWord, dist) ) #Writing to Output File

	    for tag, i1, i2, j1, j2 in s.get_opcodes():
	        if tag != 'equal': #a[i1:i2] == b[j1:j2] (the sub-sequences are equal).
		    fl = a[i1:i2]
		    tl = b[j1:j2]	
		    #print ("%7s (%s) -> (%s)" % (tag, a[i1:i2], b[j1:j2]))
		    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
	              fout.write("%7s (%s) -> (%s)\n" % (tag, a[i1:i2], b[j1:j2])) #Writing to Output File
		    confWcount += 1
	    	    #Now do a query with fl, and tl to find the corresponding confusion weight in database
		    cursor.execute("SELECT frequency FROM confusionmatrix WHERE fromletter=\""+fl+"\" AND toletter=\""+tl+"\";")
		    sqlcommandresults = cursor.fetchall()
		    if not sqlcommandresults: 
			#print "Confusion Weight: 0 (No Entry in Database)"
			if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
			  fout.write("Confusion Weight: 0 (No Entry in Database)\n")
		    for x in sqlcommandresults: #Could also save the confusion matrix entry locally to save overhead but maybe later on we can add that
		        if str(x[0]) != "None":
			    #print "Confusion Weight: "+str(x[0])
			    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
			      fout.write("Confusion Weight: "+str(x[0])+"\n")
			    confW = confW + int(x[0])
		        else:
			    #confW = conf + 0 #No Entry Found so 0 weight. (We need to punish this)
			    #print "Confusion Weight: 0 (No Entry in Database)"	
			    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
			      fout.write("Confusion Weight: 0 (No Entry in Database)\n")
	    if confWcount == 0: confWcount = 1 #normalize to avoid division by zero
	    confW = confW/confWcount
	    #print "Final Confusion Weight: "+str(confW)
	    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
	      fout.write("Final Confusion Weight: "+str(confW)+"\n")

#########################################################################################################################################################
#FOR MORE THAN 1 DISTANCE WE WILL HAVE MULTIPLE CONFUSION WEIGHTS. SHOULD I TAKE AVERAGE? SUM? MAX? ASK DR. TAGHVA! 					#
#THE UNIGRAM, BACKWARD BIGRAM, AND FORWARD BIGRAM FREQUENCIES WERE TAKEN FROM A TRAINING CORPUS IN BIRDBOOK. MAYBE I SHOULD USE GROUND TRUTH FOR THESE	#
#OR MAYBE GOOGLE-1T???????????????? ASK DR. TAGHVA #Fow now I am using just the same ocr'd text								#
#ALSO ASK ABOUT MAX CANDIDATES PER WORD I SHOULD ALLOW BECAUSE THINGS LIKE 391 becoming 9, GIVE ME LIKE 1,000 CANDIDATES AND SLOW THINGS DOWN A LOT!!!	#
#########################################################################################################################################################

	    #Get uniFreq
	    uniFq = 0
	    cursor.execute("SELECT frequency FROM onegmsORIGINAL WHERE word = \""+candidateWord+"\";")
	    sqlcommandresults = cursor.fetchall()
	    if not sqlcommandresults: 
		#print "Unigram Frequency: 0 (No Entry in Database)"
		if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		  fout.write("Unigram Frequency: 0 (No Entry in Database)\n")
	    for x in sqlcommandresults: #Could also save the unigram frequency locally to save overhead for repeat calls but maybe later on we can add that
		if str(x[0]) != "None":
		    #print "Unigram Frequency: "+str(x[0])
		    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		      fout.write("Unigram Frequency: "+str(x[0])+"\n")
		    uniFq = int(x[0])
		else:
		    #uniFq = 0 #No Entry Found.
		    #print "Unigram Frequency: 0 (No Entry in Database)"
		    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		      fout.write("Unigram Frequency: 0 (No Entry in Database)\n")

	    #Get bkwdFreq
	    bkwdFq = 0
	    cursor.execute("SELECT SUM(frequency) FROM threegmsORIGINAL WHERE wordtwo = \""+candidateWord+"""\" 
				AND wordone  = (SELECT word FROM doctext WHERE location = """+str(errorentry.location)+" - 1);")
	    sqlcommandresults = cursor.fetchall()
	    if not sqlcommandresults: 
		#print "Backward Bigram Frequency: 0 (No Entry in Database)"
		if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		  fout.write("Backward Bigram Frequency: 0 (No Entry in Database)\n")
	    for x in sqlcommandresults: #Could also save the backward bigram frequency locally to save overhead for repeat calls but maybe later on we can add that
		if str(x[0]) != "None":
		    #print "Backward Bigram Frequency: "+str(x[0])
		    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		      fout.write("Backward Bigram Frequency: "+str(x[0])+"\n")
		    bkwdFq = int(x[0])
		else:
		    #bkwdFq = 0 #No Entry Found.
		    #print "Backward Bigram Frequency: 0 (No Entry in Database)"
		    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		      fout.write("Backward Bigram Frequency: 0 (No Entry in Database)\n")

	    #Get fwdFreq
	    fwdFq = 0
	    cursor.execute("SELECT SUM(frequency) FROM threegmsORIGINAL WHERE wordtwo = \""+candidateWord+"""\" 
				AND wordthree  = (SELECT word FROM doctext WHERE location = """+str(errorentry.location)+" + 1);")
	    sqlcommandresults = cursor.fetchall()
	    if not sqlcommandresults: 
		#print "Forward Bigram Frequency: 0 (No Entry in Database)"
		if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		  fout.write("Forward Bigram Frequency: 0 (No Entry in Database)\n")
	    for x in sqlcommandresults: #Could also save the forward bigram frequency locally to save overhead for repeat calls but maybe later on we can add that
		if str(x[0]) != "None":
		    #print "Forward Bigram Frequency: "+str(x[0])
		    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		      fout.write("Forward Bigram Frequency: "+str(x[0])+"\n")
		    fwdFq = int(x[0])
		else:
		    #fwdFq = 0 #No Entry Found.
		    #print "Forward Bigram Frequency: 0 (No Entry in Database)"
		    if candidateCountPrinted <= MAX_CANDIDATE_COUNT:
		      fout.write("Forward Bigram Frequency: 0 (No Entry in Database)\n")

	    #Get output  (This is the one we set to  1 for correct solutions to 'train' our data in preparation for regression)
	    #In other words if the candidate is the correct one, we set output to one else we set it to zero.
	    output = 0
	    #First we querty doctextSolutions with the current candidate word to see if it matches the correct solution
	    #If it does it will return us a value of 1, otherwise it will return a value of 0.
	    cursor.execute("SELECT count(*) from doctextSolutions WHERE location="+str(errorentry.location)+" AND wordOR = \""+candidateWord+"\";")
	    sqlcommandresults = cursor.fetchall()
	    for x in sqlcommandresults: #This query returns a number, if that number is 0 then we store 0 in output. 
					#otherwise if we get a 1 then we store a 1 in the output.
		if str(x[0]) != "None":
			output = int(x[0])
		else:
			output = 0      #error catch all

	    #end of code for output

	    #Get decision (This is the one that the linear regression will return, for now we set to -1 meaning undecided since we haven't run the regression.
	    #Once the regression is run we will get a range from 0 to 1 meaning likelyhood it is correct. Or if logistic regression then 0 for no and 1 for yes.
	    decision = -1

	    #Generate Candidate Entry with acquired data
	    candidateList.append( candidates(errorentry.location, errorWord, candidateWord, dist, confW, uniFq, bkwdFq, fwdFq, output, decision, currDoc) )
	    candidateCountPrinted += 1 #Increment Candidates we have printed
	#End of candidateWord in candidateDicList[errorWord] For Loop

	#print "\n
	fout.write("\n")
	processedCount +=1 #Increment words processed

    #End of errorentry in errorList For loop

    #Get the Location of next Document (next errorentry). 
    #To do this we send the last entry's location and then see the location of the one after that in database using MIN(location thats greater than last location
    lastLocation = errorList[-1].location

    rowCount = cursor.execute("""SELECT docErrorList.location FROM docErrorList 
		      WHERE docErrorList.location NOT IN(SELECT location FROM matchfailList) AND docErrorList.location = 
		      (SELECT MIN(docErrorList.location) FROM docErrorList 
		      WHERE docErrorList.location NOT IN(SELECT location FROM matchfailList) AND docErrorList.location > """+str(lastLocation)+");")
    sqlcommandresults = cursor.fetchall()
    for x in sqlcommandresults: 
        if str(x[0]) != "None":
	    currentLocation = x[0]
        else: #No rows returned so we are done
	    print "Reached End of Table:", cursor.fetchall(), rowCount
	    break

#Done Main Loop

fout.write("\nCompleted Candidate List for all Error Words:\n")
fout.write("candidates (location, fromword, toword, distance, confWeight, uniFreq, bkwdFreq, fwdFreq, output, decision, docSource)\n")
fout.write(str(candidateList)+"\n") #Writing to Output File

#Now send our Candidate List to Database
print "Inserting/Updating Candidates Table in Database"

candidatesPrinted = 0
for c in candidateList:
    candidatesPrinted += 1
    c0  = c.location #Copying values to shorter variable names so query is easier to read
    c1  = c.fromword
    c2  = c.toword
    c3  = c.distance
    c4  = c.confWeight
    c5  = c.uniFreq
    c6  = c.bkwdFreq
    c7  = c.fwdFreq
    c8  = c.output
    c9  = c.decision
    c10 = c.docSource
    #Insert new row with candidate data, if we find a duplicate, overwrite it
    sqlinsertcmd="INSERT INTO candidates VALUES ("+str(c0)+", \""+c1+"\", \""+c2+"\", "+str(c3)+", "+str(c4)+", "+str(c5)+", "+str(c6)+""", 
			"""+str(c7)+", "+str(c8)+", "+str(c9)+", \""+c10+"\") ON DUPLICATE KEY UPDATE distance = "+str(c3)+""", 
			confusionweight = """+str(c4)+", unigramfrequency = "+str(c5)+", backwardbigramfreq = "+str(c6)+""", 
			forwardbigramfreq = """+str(c7)+", output = "+str(c8)+", decision = "+str(c9)+", docsource = \""+c10+"\";"
    cursor.execute(sqlinsertcmd)
    #print "SQL Insert Command:",sqlinsertcmd #Uncomment to see SQL Command Being Executed

#Commit Changes to MySQL Database
connection.commit()  #Comment this out for testing without committing changes!
#Close MySQL connection
cursor.close()
connection.close()

fout.write("\nSuccessfully inserted all candidate rows into Candidate Table in Database.\n")

print "Number of OCR-Error words processed:", processedCount
fout.write("Number of OCR-Error words processed: " + str(processedCount))
print "Number of rows (candidates) Inserted into Candidates Table:", candidatesPrinted
fout.write("Number of rows (candidates) Inserted into Candidates Table: " + str(candidatesPrinted))
print "Execution Time:"
print timedelta(seconds=round((time.time() - time0)))
print "\nFinished "+sys.argv[0]+"\n"

