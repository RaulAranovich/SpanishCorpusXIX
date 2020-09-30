#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

import sys
import mysql.connector as mc
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
if (len(sys.argv) != 3 or not(sys.argv[2].lower() == "original" or sys.argv[2].lower() == "degrade")):
    print "Usage: trec5sqlinsert.py SourceTexts/original.FR940104.0 original"
    print "OR     trec5sqlinsert.py SourceTexts/original.FR940104.0 degrade"
    quit()
print sys.argv[0] #Prints the Python Executable
print sys.argv[1] #Prints File Name
print sys.argv[2] #Decides whether we are reading an original document or a degraded (OCR document)
print "Program will open files and split them by documents, it will bundle more than one document if documents together are less than 1500 words"

fileoriginal = sys.argv[1]
fileName = fileoriginal.split("/")[-1] #the last part of filename after the last '/' is the document name

fileIsDegrade = True if sys.argv[2].lower() == "degrade" else False
#fileIsDegrade = False
#if sys.argv[2].lower() == "degrade":
#    fileIsDegrade = True
    

#Read file with OCR'd Text
with open(fileoriginal, 'r') as myfile:
    wordsfull=myfile.read()
#.replace('\n', '')

words = wordsfull.split() #split line into list of words

prevCutCount=0
prevTrueCutCount=0
prevCount=0
prevTrueCount=0
wordcount=0
truecount=0
ignoringline=False
nextisDocNo=False
currdocNo="00000000-0-00000"
nextisParentDoc=False
currParentDocNo="00000000-0-00000"
docCount=0
docwordcount=0
sqlcommand1=""  #onegms or onegmsORIGINAL
sqlcommand2="" #doctext OR doctextORIGINAL
sqlcommand3="" #threegms
sqlcommand4="" #threegmsrepetitions
sqlcommand5="" #onegmsdocsource
insertWordCount=0
#success=False

#Get Word Count so we insert in order multiple files
if fileIsDegrade:
    cursor.execute("SELECT MAX(location) FROM doctext")
else:
    cursor.execute("SELECT MAX(location) FROM doctextORIGINAL")
sqlcommandresults = cursor.fetchall()
for x in sqlcommandresults:
    if str(x[0]) != "None":
        insertWordCount = x[0] + 1
	print "Starting Insertion of new File in Location: " + str(x[0]) + "."
    else:
	insertWordCount = 0 #First Doc
	print "Starting Insertion of new File in Location: 0."
previnsertTotal = insertWordCount
#Done

word1=""
word2=""
word3=""

for word in words:
	wordcount+=1
#TEMP (2 Stop Execution and review)
#	if wordcount > 300:
#		break
#
#TEMP
	if '<' in word:
		ignoringline = True
	#if not ignoringline and '&' not in word:
	if not ignoringline and len(word) < 30 and not nextisDocNo and not nextisParentDoc:
		#print(word)
		truecount+=1
		docwordcount+=1
		
		word1=word2
		word2=word3
		word3=word
		#insert	to sql word

		if fileIsDegrade:
		    #onegms, doctext, threegms, threegmsreps, onegmsdocsource
		    sqlcommand1="INSERT INTO onegms VALUES (\""+word+"\", 1) ON DUPLICATE KEY UPDATE frequency = frequency+1;"
		    sqlcommand2="INSERT INTO doctext (word, location, docsource) VALUES (\""+word+"\", "+str(insertWordCount)+", \""+currdocNo+"\");"
		    sqlcommand3="INSERT INTO threegms VALUES (\""+word1+"\", \""+word2+"\", \""+word3+"\", 1) ON DUPLICATE KEY UPDATE frequency = frequency+1;"
		    sqlcommand4="INSERT INTO threegmsreps VALUES ("+str(insertWordCount)+", \""+currdocNo+"\", \""+word1+"\", \""+word2+"\", \""+word3+"\");"
		    sqlcommand5="INSERT INTO onegmsdocsource VALUES (\""+word+"\", \""+currdocNo+"\", 1) ON DUPLICATE KEY UPDATE frequency = frequency+1;"
		else:
		    sqlcommand1="INSERT INTO onegmsORIGINAL VALUES (\""+word+"\", 1) ON DUPLICATE KEY UPDATE frequency = frequency+1;"
		    sqlcommand2="INSERT INTO doctextORIGINAL (word, location, docsource) VALUES (\""+word+"\", "+str(insertWordCount)+", \""+currdocNo+"\");"
		    sqlcommand3="INSERT INTO threegmsORIGINAL VALUES (\""+word1+"\", \""+word2+"\", \""+word3+"\", 1) ON DUPLICATE KEY UPDATE frequency = frequency+1;"
		    sqlcommand4="INSERT INTO threegmsrepsORIGINAL VALUES ("+str(insertWordCount)+", \""+currdocNo+"\", \""+word1+"\", \""+word2+"\", \""+word3+"\");"
		    sqlcommand5="INSERT INTO onegmsdocsourceORIGINAL VALUES (\""+word+"\", \""+currdocNo+"\", 1) ON DUPLICATE KEY UPDATE frequency = frequency+1;"



		cursor.execute(sqlcommand1)
		cursor.execute(sqlcommand2)
		cursor.execute(sqlcommand3)
		cursor.execute(sqlcommand4)
		cursor.execute(sqlcommand5)
		insertWordCount += 1 #Increase The insertion count

		#success=True
		if  wordcount % 10000 == 0:
		    print(str(truecount)+" Words Inserted")

		#print("Word "+ str(word) +".")
	#	print("3 Gram: Word "+ str(word1) +" "+str(word2)+" "+str(word3) + "    "+str(docCount)+","+ str(docwordcount-2))

	if '>' in word:
		ignoringline = False
	if nextisDocNo:
		currdocNo = word
	#	print("New DOCNO "+str(currdocNo) )
		nextisDocNo = False
	if word == "<DOCNO>":
		nextisDocNo = True
	if nextisParentDoc:
		currParentDocNo = word
	#	print("New PARENTDOCNO "+str(currParentDocNo) )
		nextisParentDoc = False
	if word == "<PARENT>":
		nextisParentDoc = True
	if word == "</DOC>": #End of a Document
		#print ("Document ended at word "+ str(wordcount) +", real count "+ str(truecount) )
		docwordcount=0
		if truecount - prevTrueCutCount > 1500: #Time to split, so split at previous document
			#print("Splitting at Previous DOC ending at word "+ str(wordcount)+" with a total of "+ str(prevTrueCount - prevTrueCutCount)+" true words.")
			#print("Start Cut: "+str(prevCutCount)+" , End Cut at: "+str(prevCount)+".")
			#Call Split here 
			prevTrueCutCount = prevTrueCount
			prevCutCount = prevCount
			docCount+=1
		
		prevCount = wordcount
		prevTrueCount = truecount


#if prevCount != prevCutCount:
	#print("Saving remainder of file")
	#print("Start Cut: "+str(prevCutCount)+" , End Cut at: "+str(prevCount)+".")
	#Call Save Here

#cat SourceTexts/original.$1 | sed '/^</ d' | wc -l -w

#words = words.split() #split line into parts
#words = [x for x in words if x != ')']  #Remove all entries with just a parenthesis for cleanup
#words = [x for x in words if x != '.']  #Remove all entries with just a period for cleanup

#Commit Changes to MySQL Database
#if success:
#	connection.commit()
connection.commit()
#Close MySQL connection

cursor.close()
connection.close()

print "Number of words inserted:", insertWordCount-previnsertTotal, ". Total inserted:", insertWordCount
print "Execution Time:"
print timedelta(seconds=round((time.time() - time0)))
print "\nFinished "+sys.argv[0]+"\n"

