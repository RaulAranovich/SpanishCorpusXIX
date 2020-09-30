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
from trec5commons import doctextSol
from trec5commons import confMatrix
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
    print "Usage: trec5confusionmatrix.py 0 606"
    print "OR     trec5confusionmatrix.py 0 0"
    quit()
print sys.argv[0] #Prints the Python Executable
print "Start:", sys.argv[1] #Prints Starting Location
print "End:", sys.argv[2] #Prints Stop Location
print "Program will read database table doctextSolutions and create/update confusion matrix"
print "First Parameter will be starting document location."
print "Second parameter is ending document location."
print "If ending location is same as start it will use all rows in doctextSolutions."
print "Program will also create/update Levenshtein Frequency Table (see database)"
print "Program will produce: \"confusionmatrix_output.txt\" with more information on process."

startLocation = int(sys.argv[1])
endLocation   = int(sys.argv[2])
currentLocation = startLocation
maxLocation=0
minLocation=0
currDoc="00000000-0-00000"
processedCount = 0
levenshteinFreq = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} #Will keep edit distance frequencies for statistical tracking in Python Dictionary


#This code has been movied to trec5common.py
'''
#Class To Store doctextSolution(word, wordOR, location, locationOR, docSource) after we read it in from the database
class doctextSol: #This class is similar to the one in alignment but contains less members and contains docsource.
    def __init__(self, word, wordOR, location, locationOR, docSource): 
	self.word	= word
	self.wordOR	= wordOR
	self.location	= location
	self.locationOR = locationOR
	self.docSource  = docSource
#    def __init__(self): 
#	self.word	= "Unknown"
#	self.wordOR	= "Unknown"
#	self.location	= -1
#	self.locationOR = -1
#	self.docSource  = "00000000-0-00000"
    def __repr__(self):
	return '\ndoctextSol(%s, %s, %d, %d, %s)' % (self.word, self.wordOR, self.location, self.locationOR, self.docSource)

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
    

#Note: I could use sets and a hash to improve speed here. Else we are looking at O(n*m) where n is error entries and m is size of confusionmatrix (so potentially n^2)
#      However with sets I cannot update the frequency of the entries...
#Note2: A dictionary may be a better way to store confusion matrix and solve the issue of sets. Would it improve speed?
confMatrixList = [] #Create the empty list 
entry = confMatrix(" "," ", 0)  #Create an object of type confMatrix to represent the Empty Item
confMatrixList.append(entry)    #insert it to the ongoing list


#Testing Set Version of Code (Unused)
#confMatrixList = set([])
#print "1", confMatrixList
#entry = confMatrix(" "," ", 0) 
#confMatrixList.add(entry)
#print "2", confMatrixList
#entry = confMatrix("rr","m", 1)
#confMatrixList.add(entry)
#print "3", confMatrixList
#entry = confMatrix("r","n", 21)
#confMatrixList.add(entry)
#print "4", confMatrixList
#entry = confMatrix("rr","m", 1)
#confMatrixList.add(entry)
#print "5", confMatrixList
#print "R", confMatrixList.pop(entry)
#print "5", confMatrixList
#quit()

#Levenshtein Function Test Code (Unused):
#a ="car"
#b ="cat"
#print "Levenshtein Distance between '"+a+"\' and \'"+b+"\' is", Levenshtein.distance(a,b), ".\n"
#quit()

#Start of Code:

#Get Max Location so we don't go too far.
cursor.execute("""SELECT MAX(doctextSolutions.location) FROM doctextSolutions, docErrorList 
		  WHERE doctextSolutions.location = docErrorList.location 
		  AND doctextSolutions.docsource = docErrorList.docsource 
		  AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList);""")
sqlcommandresults = cursor.fetchall()
for x in sqlcommandresults:
    if str(x[0]) != "None":
        maxLocation = x[0]
    else:
	maxLocation = 0 #Empty Database BAD!
	print "Database is Empty! Aborting"
	quit()
#Done
if endLocation == 0: #we need to create confusion matrix for full table so copy that over
    endLocation = maxLocation
if endLocation > maxLocation: #Out of range Error
    print "ERROR: End Location", endLocation,"is greater than Max Location",maxLocation, "in table!"
    quit()

#Get Min Location since it may not be 0 as first error may not be first word.
cursor.execute("""SELECT MIN(doctextSolutions.location) FROM doctextSolutions, docErrorList 
		  WHERE doctextSolutions.location = docErrorList.location 
		  AND doctextSolutions.docsource = docErrorList.docsource 
		  AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList);""")
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

#Let's write our confusion matrix output to a file
fout = open("output/confusionmatrix_output.txt", "a")

#We are going to do it by document. This makes it harder than it has to be but ensures we have full control

#Main Loop: 
while currentLocation <= endLocation:
    #First We have to get the next document name by checking our currentLocation
    cursor.execute("SELECT docsource FROM doctextSolutions WHERE location = "+str(currentLocation)+";")
    sqlcommandresults = cursor.fetchall()
    oldDoc = currDoc #Save last doc we were working with
    for x in sqlcommandresults:
	currDoc  = x[0]
    if oldDoc == currDoc: #Check if we received a new document different to last one we worked on
	break #we reached end of database so we are just getting back the same document so we are done!
    print "Processing Document:", currDoc
    fout.write("Processing Document: " + currDoc+"\n") #Writing to Output File
    #Next let's query all rows with that document name
    #Note, the reason we are doing NOT in matchfail is because we only want words that were aligned successfully.
    cursor.execute("""SELECT doctextSolutions.word, doctextSolutions.wordOR, doctextSolutions.location, 
		      doctextSolutions.locationOR, doctextSolutions.docsource FROM doctextSolutions, docErrorList 
		      WHERE doctextSolutions.location = docErrorList.location 
	              AND doctextSolutions.docsource = docErrorList.docsource 
		      AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList)
		      AND doctextSolutions.docsource = \""""+currDoc+"""\";""")
    doctextlist = cursor.fetchall()
    errorList = [ doctextSol(x[0], x[1], x[2], x[3], x[4]) for x in doctextlist ] #Create Objects and Fill them with row data

    #Insert to Confusion Matrix
    for errorentry in errorList:
	#errorList (word, wordOR, location, locationOR, docSource)
	#confMatrixList(fromletter, toletter, frequency)
	a =errorentry.word
	b =errorentry.wordOR
	LevenshteinDistance = Levenshtein.distance(a,b)
	if( 1 <= LevenshteinDistance <= 5 ): #Only add valid entries to our Dictionary - which is 0 to 5
	    levenshteinFreq[LevenshteinDistance] = levenshteinFreq[LevenshteinDistance] + 1 #Increase Frequency
	#print "\nLevenshtein Distance between '"+a+"\' and \'"+b+"\' is", LevenshteinDistance, "."
	fl = " "
	tl = " "
	fq = 0
	#a = "qabxxcd" #For Testing difflib
	#b = "abycdf"  #For Testing difflib
	s = difflib.SequenceMatcher(None, a, b) #from docs.python.org
	#print a, " -> ", b, "Distance:", Levenshtein.distance(a,b) #Regular print
	#print "%-12s -> %-17s Distance: %d" % ( a, b, Levenshtein.distance(a,b) ) #Spaced out Print to look nicer
	fout.write("\n%-12s -> %-17s Distance: %d\n" % ( a, b, LevenshteinDistance)) #Writing to Output File
	#Easy to read version of code:
	for tag, i1, i2, j1, j2 in s.get_opcodes():
	    if tag == 'equal': #a[i1:i2] == b[j1:j2] (the sub-sequences are equal).
		#print ("%7s (%s) -> (%s)" % (tag, a[i1:i2], b[j1:j2]))
		continue #Ignore equals
	    elif tag == 'replace': #a[i1:i2] should be replaced by b[j1:j2]
		fl = a[i1:i2]
		tl = b[j1:j2]
		fq = 1
		#print ("%7s (%s) -> (%s)" % (tag, a[i1:i2], b[j1:j2]))
	    elif tag == 'delete':  #a[i1:i2] should be deleted. Note that j1 == j2 in this case.
		fl = a[i1:i2]
		tl = b[j1:j2]
		fq = 1
		#print ("%7s (%s) -> (%s)" % (tag, a[i1:i2], b[j1:j2]))
	    elif tag == 'insert':  #b[j1:j2] should be inserted at a[i1:i1]. Note that i1 == i2 in this case.
		fl = a[i1:i2]
		tl = b[j1:j2]
		fq = 1
		#print ("%7s (%s) -> (%s)" % (tag, a[i1:i2], b[j1:j2]))
            else:
           	#raise RuntimeError, "unexpected tag in SequenceMatcher!"
		print "Unexpected tag in SequenceMatcher!"
	#Simplified Version of Code, but harder to read:
	#for tag, i1, i2, j1, j2 in s.get_opcodes():
	#    if tag != 'equal': #a[i1:i2] == b[j1:j2] (the sub-sequences are equal).
	#	fl = a[i1:i2]
	#	tl = b[j1:j2]
	#	fq = 1	
	#	print ("%7s (%s) -> (%s)" % (tag, a[i1:i2], b[j1:j2]))
	    fout.write("%7s (%s) -> (%s)\n" % (tag, a[i1:i2], b[j1:j2])) #Writing to Output File
	    entry = confMatrix(fl,tl, fq)
	    found = False
	    for sublist in confMatrixList:
	        if sublist == entry:
		    #print "Found Matching Entry, Updating Only the Frequency:", sublist, entry
		    sublist.frequency = sublist.frequency + fq
		    found = True
		    continue
	    if not found: #No match , new entry so let's add it
	    	confMatrixList.append(entry) 
	    #else we already found and updated frequency
	    #print "Current Confusion Matrix List:", confMatrixList
	    processedCount +=1
	#End of For Loop
    #Get the Location of next Document (next errorentry). 
    #To do this we send the last entry's location and then see the location of the one after that in database using MIN(location thats greater than last location
    lastLocation = errorList[-1].location

    rowCount = cursor.execute("""SELECT doctextSolutions.location FROM doctextSolutions, docErrorList 
		      WHERE doctextSolutions.location = docErrorList.location 
		      AND doctextSolutions.docsource = docErrorList.docsource 
		      AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList) AND doctextSolutions.location = 
		      (SELECT MIN(doctextSolutions.location) FROM doctextSolutions, docErrorList 
		      WHERE doctextSolutions.location = docErrorList.location 
		      AND doctextSolutions.docsource = docErrorList.docsource 
		      AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList) AND doctextSolutions.location > """+str(lastLocation)+");")
    sqlcommandresults = cursor.fetchall()
    for x in sqlcommandresults: 
        if str(x[0]) != "None":
	    currentLocation = x[0]
        else: #No rows returned so we are done
	    print "Reached End of Table:", cursor.fetchall(), rowCount
	    break


#Done Main Loop
#print "Completed Confusion Matrix List:\nconfMatrix(FROMerror, TOcorrect, FREQUENCY)", confMatrixList
fout.write("\nCompleted Confusion Matrix List:\nconfMatrix(FROMerror, TOcorrect, FREQUENCY) "+ str(confMatrixList)+"\n") #Writing to Output File

#Now send our confusion matrix to Database
print "Inserting/Updating Confusion Matrix to Database"

for entry in confMatrixList: #confMatrix(fromletter, toletter, frequency)
    fl=entry.fromletter
    tl=entry.toletter
    fq=entry.frequency
    if len(fl) > 4 or len(tl) > 4: continue #Since we are limiting to max of 4 letters we don't want to insert anything bigger.
						  #if I change this value I have to also change the CREATE Table VARCHAR size accordingly!!!
    sqlinsertcmd="INSERT INTO confusionmatrix VALUES (\""+fl+"\", \""+tl+"\", "+str(fq)+") ON DUPLICATE KEY UPDATE frequency = frequency+"+str(fq)+ ";"
    cursor.execute(sqlinsertcmd)
    #print "SQL Insert Command:",sqlinsertcmd #Uncomment to see SQL Command Being Executed

#Now Update the levenshteinFreq table
print "Updating Levenshtein Frequency Table with new Values"
for e in levenshteinFreq:
    if levenshteinFreq[e] != 0:
    	sqlinsertcmd="INSERT INTO levenshteinFrequency VALUES ("+str(e)+", "+str(levenshteinFreq[e])+""") 
				ON DUPLICATE KEY UPDATE frequency = frequency+"""+str(levenshteinFreq[e])+ ";"
    	cursor.execute(sqlinsertcmd)

#Commit Changes to MySQL Database
connection.commit()  #Comment this out for testing without committing changes!
#Close MySQL connection
cursor.close()
connection.close()

print "Number of Errors Inserted into Confusion Matrix:", processedCount
fout.write("\nNumber of Errors Inserted into Confusion Matrix: "+str(processedCount)+"\n")

print "Error Distribution by Levenshtein edit distance:"
fout.write("Error Distribution by Levenshtein edit distance:\n")
for e in levenshteinFreq:
    if levenshteinFreq[e] != 0:
	fout.write("Distance "+str(e)+" Frequency: "+str(levenshteinFreq[e])+"\n")
	print "Distance "+str(e)+" Frequency: "+str(levenshteinFreq[e])
fout.write("\n")

print "\nExecution Time:"
print timedelta(seconds=round((time.time() - time0)))
print "\nFinished "+sys.argv[0]+"\n"

