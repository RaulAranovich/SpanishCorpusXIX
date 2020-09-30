#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

import sys
import mysql.connector as mc
import Levenshtein  #pip install python-levenshtein
import time
from datetime import timedelta
time0 = time.time()

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
    print "Usage: trec5sqlinsert.py 0 606"
    print "OR     trec5sqlinsert.py 0 0"
    quit()
print sys.argv[0] #Prints the Python Executable
print "Start:", sys.argv[1] #Prints Starting Location
print "End:", sys.argv[2] #Prints Stop Location
print "Program will align original-degrade locations in Database."
print "First Parameter will be starting document location to align."
print "Second parameter is ending document location to stop aligning."
print "If ending location is same as start it will align until end of database."
print "Program will produce: \"alignment_output.txt\" with more information on process."

startLocation = int(sys.argv[1])
endLocation   = int(sys.argv[2])
currentLocation = startLocation
maxLocation=0
currDoc="00000000-0-00000"
dstart = 0 #Degrade Document Start
dend   = 0 #Degrade Document End
ostart = 0 #Original Document Start
oend   = 0 #Original Document End
totalMatchFailures = 0
processedCount = 0

#Class To Store outputs of alignment before sending to database #doctextSolution(word, wordOR, location, locationOR, confidence, isError)
class doctextSolution:
    def __init__(self, word, location): 
	self.word	= word
	self.wordOR	= "Unknown"
	self.location	= location
	self.locationOR = -1
	self.confidence = 0.0
	self.isError	= True #Assume it's an error until proven otherwise
	self.isMatchFail= False #Assume it's not a match failure because we are that good
#    def __init__(self): 
#	self.word	= "Unknown"
#	self.wordOR	= "Unknown"
#	self.location	= -1
#	self.locationOR = -1
#	self.confidence = 0.0
#	self.isError	= True #Assume it's an error until proven otherwise
#	self.isMatchFail= False #Assume it's not a match failure because we are that good
    def __repr__(self):
	return '\ndoctextSolutions(%s, %s, %d, %d, %.2f, %s, %s)' % (self.word, self.wordOR, self.location, self.locationOR, 
								     self.confidence, self.isError, self.isMatchFail)

#Levenshtein Function Test Code:
#a ="car"
#b ="cat"
#print "Levenshtein Distance between '"+a+"\' and \'"+b+"\' is", Levenshtein.distance(a,b), ".\n"
#quit()

#Start of Code:

#Get Max Location so we don't go too far.
cursor.execute("SELECT MAX(location) FROM doctext")
sqlcommandresults = cursor.fetchall()
for x in sqlcommandresults:
    if str(x[0]) != "None":
        maxLocation = x[0]
    else:
	maxLocation = 0 #Empty Database BAD!
	print "Database is Empty! Aborting"
	quit()
#Done
if endLocation == 0: #we need to align until end so copy that over
    endLocation = maxLocation
if endLocation > maxLocation: #Out of range Error
    print "ERROR: End Location", endLocation,"is greater than Max Location",maxLocation, "in database!"
    quit()

#Let's write our alignment output to a file
fout = open("output/alignment_output.txt", "w")

#Let's make a list to store all individual success rates so we can print it out at the end
successRateList = []

#Main Loop:
while currentLocation <= endLocation:
    #First, let's get the location range of the first document we are dealing with

    #Alternative Query that places each item on it's own row
    #cursor.execute("SELECT MIN(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    #+str(currentLocation)+") union SELECT MAX(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    #+str(currentLocation)+") union SELECT MIN(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    #+str(currentLocation)+") union SELECT MAX(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    #+str(currentLocation)+");")

    #Returns 1 row 4 columns(dmin, dmax, omin, omax)
    cursor.execute("SELECT (SELECT MIN(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    +str(currentLocation)+")) as dstart, (SELECT MAX(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    +str(currentLocation)+")) as dend, (SELECT MIN(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    +str(currentLocation)+")) as ostart, (SELECT MAX(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location="
    +str(currentLocation)+")) as oend, (SELECT docsource FROM doctext WHERE location="+str(currentLocation)+") as doc;")

    sqlcommandresults = cursor.fetchall()
    #print "SQL:", sqlcommandresults
    for x in sqlcommandresults:
	dstart  = x[0]
	dend    = x[1]
	ostart  = x[2]
	oend    = x[3]
	currDoc = x[4]
    print "Processing Document:", currDoc, "\nDegrade Range ["+str(dstart)+","+str(dend)+"] and Original Range ["+str(ostart)+","+str(oend)+"]."
    #Writing to Output File
    fout.write( "Processing Document: "+ currDoc+ "\nDegrade Range ["+str(dstart)+","+str(dend)+"] and Original Range ["+str(ostart)+","+str(oend)+"].\n" ) 

    #Second, let's get all the word/location values from those ranges into two lists and then create objects of doctext to have ready
    cursor.execute("SELECT LOWER(word), location FROM doctext WHERE docsource = \""+currDoc+"\";")
    degList = cursor.fetchall()
    #print "Degrade List:",  degList
    cursor.execute("SELECT LOWER(word), location FROM doctextORIGINAL WHERE docsource = \""+currDoc+"\";")
    orgList = cursor.fetchall()
    #print "Original List:", orgList

    #To Print both Lists Side by Side for Easy Checking Just Uncomment these 2 lines
    #for x in range(len(orgList) if len(degList) > len(orgList) else len(degList)):
    #    print '{0: <32}'.format(degList[x][0]), '{0: <10}'.format(degList[x][1]), '{0: <32}'.format(orgList[x][0]), '{0: <10}'.format(orgList[x][1])

    degSolList = [ doctextSolution(x[0], x[1]) for x in degList ] #Create Objects and Fill them with word and location

    #Third, now we can do our algorithm
    count = 0
    matchFailures = 0
    entryIndex = -1
    for entry in degSolList:  #For Reference: doctextSolution(word, wordOR, location, locationOR, confidence, isError)
	processedCount +=1 #For Statistical Purposes
	entryIndex += 1 #Keeps the index of current entry. useful for Location2Check
	#if count > 1: print degSolList[count-1] #For Printing each doctextSolution processed, uncomment this line.
	#print "Processing:", entry.word

	#Step1: Check the OCR'd Word Against a Dictionary to see if it is a real word. If it is increase confidence by .5
	#       (in our case we can  search through all words in orgList and if it's present we know it's correct!
	inDictionary = False
	for wdic in orgList:
	    if entry.word == wdic[0]:
	    #if entry.word.lower() == wdic[0].lower():  #In our Select Query we use LOWER. Alternatively can do it instead
	    	#print "Match Found in Dictionary!" #For Printing Match Success Notification
		entry.wordOR = wdic[0]
		entry.locationOR = wdic[1]
		entry.confidence += 0.5
		entry.isError = False
		inDictionary = True
		#print entry
	    else:
		entry.wordOR = "Unknown"
	#Step2: Check Previous word Aligned for the last location (0 if this is first document word).
	#       Using that location we check the immediate next word to see if's a match
	Location2Check = 0 #First in Document so Compare to first in orgList
	if count > 0: #Not First so check last CORRECT location + 1
	    Location2Check = degSolList[count-1].locationOR + 1 -ostart

	if Location2Check > len(orgList) -1:
	    Location2Check = len(orgList) -1 #Degrade has more words than Original so we can't go further than last member.


	#if entry.location == 7242:#################################USEFUL DEBUG FOR CHECKING A SPECIFIC ERROR#######################################DEBUG#
	#	print "????????????", Location2Check, "INDEX", entryIndex

	FLEX = 15 #This Value allows how much offset 2 words can be. This is to avoid an ever growing offset as stuff gets shifted!
		  #This really helps to fix all errors!!!!
	if entry.word != orgList[Location2Check][0]: #If it's a match then just let it be.
	    if FLEX < abs(Location2Check - entryIndex): #If the Location we are checking is greater than our flexibility, cut it back
	    #if    FLEX > abs(Location2Check - entry.location-dstart):
	    	#Location2Check = entry.location-dstart + 1
	    	Location2Check = entryIndex

	if Location2Check > len(orgList) -1: #Check again incase FLEX changed anything
	    Location2Check = len(orgList) -1 #Degrade has more words than Original so we can't go further than last member.


	#Check Word
	if entry.word == orgList[Location2Check][0]: #match?
	#if entry.word.lower() == orgList[Location2Check][0].lower(): #match? #In our Select Query we use LOWER. Alternatively can do it instead
	    #Success!
	    if count > 0: #if we aren't first word
	        degSolList[count-1].confidence += 0.25
	    entry.confidence += 0.25
	    entry.wordOR = orgList[Location2Check][0]
	    entry.locationOR = orgList[Location2Check][1]
	    entry.isError = False
	    count +=1 #Done!
	    continue  #Done!
	else: #Not Match
	    entry.confidence -= 0.25
	    if entry.confidence >= 0.25: #Was a match in dictionary and yet somehow we didn't find it!
	    	if count > 0: #if we aren't first word
	            degSolList[count-1].confidence -= 0.25
	#Step3: Since it was not a match we begin to look for words in a nearby location,
	# 	We search for exact matches after the word for N words (Variable NEARBY stands for N and for now will be 50)
	NEARBY = 20
	if inDictionary: NEARBY *= 2 #If it was in the dictionary we should try to search further out before messing with edit distance 
	Success = False
	for N in range(Location2Check, Location2Check+NEARBY, 1):
	    if N > len(orgList) -1: break #We reached the end of the doument
	    if entry.word == orgList[N][0]:
	    #if entry.word.lower() == orgList[N][0].lower(): #In our Select Query we use LOWER. Alternatively can do it instead
		#Success!
		Success = True
	    	entry.confidence += 0.25
	    	entry.wordOR = orgList[N][0]
	    	entry.locationOR = orgList[N][1]
	    	entry.isError = False
		break
	if Success:
	    #Success = False
	    count +=1 #Done!		
	    continue  #Done!
	#Didn't find a matching candidate so we will search for exact matches BEFORE the word in same fashion
	for N in range(Location2Check, Location2Check-NEARBY, -1):


	    #if entry.location == 7242: #################################USEFUL DEBUG FOR CHECKING A SPECIFIC ERROR#######################################DEBUG#
	    #	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	    #	print "N:", N, "orgLoc:", orgList[N][1], "Word:", orgList[N][0]

	    if N < 0: break #We reached the beginning of the doument
	    if entry.word == orgList[N][0]:
		#Success!
		Success = True
	        if count > 0: #if we aren't first word
	            degSolList[count-1].confidence += 0.4 #We have no faith in previous word since the match we found was before prev word
	    	entry.confidence += 0.1
	    	entry.wordOR = orgList[N][0]
	    	entry.locationOR = orgList[N][1]
	    	entry.isError = False
		break
	if Success:
	    #Success = False
	    count +=1 #Done!		
	    continue  #Done!

	#Step4: No Match for words either immediately after or in the neighboring words. So we are  going to repeat Step 3, but rather than
	#	search for exact matches we are going to search for words that have an edit distance of E. E can be greater than 1 but we
	#	will iterate starting with edit distance of 1 and increase until we reach a max of E. (Variable EDIT stands for max E that
	#	we will allow, for now it will be 5.
	EDIT = 4
	if inDictionary: EDIT /= 2 #If it was in the dictionary we should limit the edit distance to a low value
	for E in range(1, EDIT, 1):
	    for N in range(Location2Check, Location2Check+NEARBY, 1): #Check Ahead first
	    	if N > len(orgList) -1: break #We reached the end of the doument
		if Levenshtein.distance(entry.word, orgList[N][0]) <= E: #check edit distance using the Levenshtein Function
		#if Levenshtein.distance(entry.word.lower(), orgList[N][0].lower()) <= E: #In our Select Query we use LOWER. Alternatively can do it instead
		    #Success!
		    Success = True
	    	    entry.confidence += 0.1
	    	    entry.wordOR = orgList[N][0]
	    	    entry.locationOR = orgList[N][1]
	    	    entry.isError = True
		    break
	    if Success:		
	    	break  #Exit Edit Distance Loop
	if Success:
	    #Success = False
	    count +=1 #Done!		
	    continue  #Done!

	#Step5: Since we didn't find any ahead of the word with edit distance now we check before the word like we did in Step 3, 
	#	but this time allowing edit distance E. 
	for E in range(1, EDIT, 1):
	    #Didn't find a matching candidate so we will search for exact matches BEFORE the word in same fashion
	    for N in range(Location2Check, Location2Check-NEARBY, -1):
	    	if N < 0: break #We reached the beginning of the doument
		if Levenshtein.distance(entry.word, orgList[N][0]) <= E: #check edit distance using the Levenshtein Function
		#if Levenshtein.distance(entry.word.lower(), orgList[N][0].lower()) <= E: #In our Select Query we use LOWER. Alternatively can do it instead
		    #Success!
		    Success = True
	            if count > 0: #if we aren't first word
	            	degSolList[count-1].confidence += 0.3 #We have no faith in previous word since the match we found was before prev word
	    	    entry.confidence += 0.1
	    	    entry.wordOR = orgList[N][0]
	    	    entry.locationOR = orgList[N][1]
	    	    entry.isError = True
		    break
	    if Success:		
	    	break  #Exit Edit Distance Loop
	if Success:
	    #Success = False
	    count +=1 #Done!		
	    continue  #Done!

	#Step6: If after all this we do not find a match then we give it a confidence of -1 and store the location of the previous word plus 1
	#entry.wordOR = "Unknown"
	#entry.wordOR = orgList[Location2Check][0]
	entry.locationOR = orgList[Location2Check][1]
	entry.isMatchFail = True
	matchFailures +=1
    	#print "Match Failure:",entry
	fout.write("Match Failure:"+ str(entry) +"\n" )#Writing to Output File
	if matchFailures > NEARBY: #Choose how to handle a lot of failures. Ignore, Skip Document, or Halt Program fully.
		#print "ERROR: We have had too many matching failures in ", currDoc, ". Try increasing NEARBY value."
		fout.write( "ERROR: We have had too many matching failures in "+ currDoc +". Try increasing NEARBY value.\n" ) #Writing to Output File
		#continue #We can try and skip to the next document or
		#quit()   #We can just abort and see what is happening, but for now we will just notify and keep going onwards to victory!
	count += 1
    #End Of Alignment
    successRate = 1-matchFailures/float(dend-dstart) #Gets us a percentage of success. So 1 - Errors / Total Words
    successRateList.append(successRate)
    print "Match Failures: "+ str(matchFailures)+ ". Local Success Rate in Document: %.2f%%" % float(successRate*100)
    fout.write("Match Failures: "+ str(matchFailures)+". Local Success Rate in Document: %.2f%%" % float(successRate*100)+"\n\n" ) #Writing to Output File
    totalMatchFailures += matchFailures

    #Fourth, let's save the results in our database by updating locationOR in doctext for all our words
    #print degSolList #degSolList has all our matched data. Uncomment to view all entries
    for entry in degSolList:
	sqlupdatecommand = "UPDATE doctext SET locationOR="+str(entry.locationOR)+" WHERE location="+str(entry.location)+";" 
	#print "SQL Update Command:",sqlupdatecommand #Uncomment to see SQL Command Being Executed
	cursor.execute(sqlupdatecommand)

    #Fifth, let's create doctextSolutions with all our error-solution matches and save. 
    #Also create docErrorList and save.
    #Also create a table matchfailList and save all the match failures
    for entry in degSolList:
	# SAMPLE sqlcommand1="INSERT INTO doctextSolutions VALUES(\""+word+"\", \""+word+"\", "+str(number)+", "+str(number)+", \""+word+"\");"
	sqlcommand1="INSERT INTO doctextSolutions VALUES(\""+entry.word+"\", \""+entry.wordOR+"\", "+str(entry.location)+", "+str(entry.locationOR)+", \""+currDoc+"\");"
	#print "SQL Command 1:",sqlcommand1 #Uncomment to see SQL Command Being Executed
	cursor.execute(sqlcommand1)
	if entry.isError: #Add Error to docErrorList to List
	    sqlcommand2="INSERT INTO docErrorList VALUES(\""+entry.word+"\","+str(entry.location)+", \""+currDoc+"\");"
	    #print "SQL Command 2:",sqlcommand2 #Uncomment to see SQL Command Being Executed
	    cursor.execute(sqlcommand2)
	if entry.isMatchFail: #Add Match Failure to List
	    sqlcommand3="INSERT INTO matchfailList VALUES(\""+entry.word+"\","+str(entry.location)+", \""+currDoc+"\");"
	    #print "SQL Command 3:",sqlcommand3 #Uncomment to see SQL Command Being Executed
	    cursor.execute(sqlcommand3)

    #Sixth, be sure that currentLocation points to the next position which should be the  first of the next document so next iteration starts sucessful on next doc
    currentLocation = dend + 1
    #if currentLocation != dend+1:
    #	print "ERROR: Current Location",currentLocation,"is not pointing to next document at",int(dend+1),". This should not happen!"
    #	quit()

#End Main Loop

#Commit Changes to MySQL Database
#if success:
#	connection.commit()
connection.commit()  #Comment this out for testing without committing changes!
#Close MySQL connection

cursor.close()
connection.close()

print "Total Match Failures: ", totalMatchFailures
fout.write("Total Match Failures: "+ str(totalMatchFailures)+"\n" ) #Writing to Output File
print "Number of words processed: ", processedCount
fout.write("Number of words processed:" + str(processedCount)+"\n" ) #Writing to Output File
print "Success Rate: %.2f%%" % (100-float(totalMatchFailures)/float(processedCount)*100.00)
fout.write( "Success Rate: %.2f%%\n" % (100-float(totalMatchFailures)/float(processedCount)*100.00) ) #Writing to Output File

fout.write("Individual Alignment Success Rates per Document:\n") #Writing to Output File
low = 1
high = 0
for s in successRateList:
    fout.write("%.2f%%" % float(s*100)+"\n") #Writing to Output File
    if s < low:  low  = s #Save the lowest success
    if s > high: high = s #Save the highest success
print "Lowest  Individual Success Rate: %.2f%%" % float(low*100 )
fout.write("\nLowest  Individual Success Rate:  %.2f%%" % float(low*100 ))  #Writing to Output File
print "Highest Individual Success Rate: %.2f%%" % float(high*100)
fout.write("\nHighest Individual Success Rate: %.2f%%" % float(high*100))  #Writing to Output File
print "Execution Time:"
print timedelta(seconds=round((time.time() - time0)))
print "\nFinished "+sys.argv[0]+"\n"

