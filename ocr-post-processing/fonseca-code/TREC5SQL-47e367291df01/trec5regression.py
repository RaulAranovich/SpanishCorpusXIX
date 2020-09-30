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
#from trec5commons import confMatrix   #Unused
#from trec5commons import docErrorList #Unused
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
    print "Usage: trec5regression.py 0 606"
    print "OR     trec5regression.py 0 0"
    quit()
print sys.argv[0] #Prints the Python Executable
print "Start:", sys.argv[1] #Prints Starting Location
print "End:", sys.argv[2] #Prints Stop Location
print ("Program will read database table candidates ")
print ("and then run regression algorithm on the data ")
print ("it will update the decision column with output. ")
print ("First Parameter will be starting document location.")
print ("Second parameter is ending document location.")
print ("If ending location is same as start it will use all rows in candidates table.")
print ("Program will produce: \"regression_output.txt\" with more information on process.")

startLocation = int(sys.argv[1])
endLocation   = int(sys.argv[2])
currentLocation = startLocation
maxLocation=0
minLocation=0
currDoc="00000000-0-00000"
processedCount = 0
candidateCount = 0
#candidateDicList = {} #Create the empty candidateLists dictionary data structure
candidateList = [] #This will keep all candidates for all words, once we finish finding all then we push them all to database
MAX_CANDIDATE_COUNT = 6 #The following will limit the number of candidates to be printed in our candidates_output.txt file to this value
candidateCountPrinted = 0 #This is how we keep track of how many candidates are printed so we can stop at the max set above.
#Sample IF STATEMENT USED TO CHECK: if candidateCountPrinted <= MAX_CANDIDATE_COUNT:

MAX_CANDIDATES_ALLOWED = 20 #This is the maximum amount of candidates allowed per word (useful because some 1 or 2 letter words can give us like 1,000 candidates.

#Start of Code:

#Get Max Location so we don't go too far.
cursor.execute("""SELECT MAX(location) FROM candidates;""")
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
cursor.execute("""SELECT MIN(location) FROM candidates;""")
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

#Let's write our candidates output to a file
fout = open("output/regression_output.txt", "a")

#Query Database for candidates table
print ("Querying Candidate Table and copying contents...")	 #Writing to Terminal
fout.write("Querying Candidate Table and copying contents...\n") #Writing to Output File

cursor.execute("SELECT * FROM candidates WHERE location > "+str(startLocation)+"-1 AND location < "+str(endLocation)+"+1;")
sqlcommandresults = cursor.fetchall()

candidateTableSize = 0 
for x in sqlcommandresults:
    #Create an object of type candidates and insert data in it
    #Order: location, fromword, toword, distance, confWeight, uniFreq, bkwdFreq, fwdFreq, output, decision, docSource
    candidateList.append( candidates(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10]) )
    candidateTableSize += 1

print "Finished Copying Candidate Table with Size:", candidateTableSize	 	     #Writing to Terminal
fout.write("Finished Copying Candidate Table with Size: " + str(candidateTableSize)+"\n") #Writing to Output File

#Test: Should Print: ('1', 'hegister', 'Register', '1', '918', '83', '83', '0', '1', '-1', 'FR940104-0-00001')
print candidateList[1]
print candidateList[1].fromword

#Let's make a little file with all Xi and Y (features and expected output)
fout2 = open("output/regression_matrix.txt", "w") #Overwrite Mode
for candidate in candidateList:
    fout2.write (str(candidate.distance)+", " +str(candidate.confWeight)+", "
		 +str(candidate.uniFreq)+", "+str(candidate.bkwdFreq)+", "
		 +str(candidate.fwdFreq)+", "+str(candidate.output)+"\n")
fout2.close() #Close File
#Done.



#Now we can start regression

##############################
##REGRESSION # STARTS # HERE##

#Labels:  location  fromword    toword     distance  confWeight  uniFreq  bkwdFreq  fwdFreq  output  decision      docSource
#Values:  ('1',    'hegister', 'Register',    '1',     '918',      '83',     '83',    '0',    '1',     '-1',   'FR940104-0-00001')

#At This POINT WE CAN SETUP SCRIPTS HERE TO CONNECT WITH RegressionTREC5 once we have it linked. for now manually copy the regression_matrix.txt
#to TREC5SQL/RegressionTREC5/libsvm-3.23/python
#Please see Quick Start Guide for more information



##REGRESSION # ENDS   # HERE##

#######START#TEMP###########START#TEMP#####START#TEMP#########
fout.close()						######
cursor.close()						######
connection.close()					######
print "Execution Time:" 				######
print timedelta(seconds=round((time.time() - time0)))	######
print "\nFinished "+sys.argv[0]+"\n"			######
exit()							######
#########END#TEMP#############END#TEMP#######END#TEMP#########

#Now send our decision (solution column) to the database by updating the Candidate Table
print "Inserting/Updating Candidates Table in Database."
fout.write("Inserting/Updating Candidates Table in Database.\n")

candidatesUpdated = 0
for c in candidateList:
    candidatesUpdated += 1
    c0  = c.location #Copying values to shorter variable names so query is easier to read
    c1  = c.fromword
    c2  = c.toword
    c9  = c.decision
    #Update Decision Column of Candidate Table
    sqlupdatecmd="UPDATE candidates SET decision = "+str(c9)+" WHERE location="+str(c0)+" AND fromword=\""+str(c1)+"\" AND toword=\""+str(c2)+"\";"
    cursor.execute(sqlupdatecmd)
    #print "SQL Insert Command:",sqlupdatecmd #Uncomment to see SQL Command Being Executed

#Commit Changes to MySQL Database
connection.commit()  #Comment this out for testing without committing changes!
#Close MySQL connection
cursor.close()
connection.close()

print "Number of rows (candidates) Updated in Candidates Table:",candidatesUpdated
fout.write("Number of rows (candidates) Updated in Candidates Table: " + str(candidatesUpdated))
fout.close() #Close File We are Writing to!

print "Execution Time:"
print timedelta(seconds=round((time.time() - time0)))
print "\nFinished "+sys.argv[0]+"\n"

