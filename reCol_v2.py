#Author: Daniel Lavados, working under Professor Raul Aranovich
#This Python script serves to rebuild columns scanned by Tesseract for our research
# by scanning for the pipe character and putting it into one of two variables, which
# then get recombined in their proper order.
#The use of our old removeNewlines script can easily be erased if need be as well.
#Please forgive any sloppy style, I'm still learning Python! Haha!

import os
import sys
import re
import string


def removeNewlines(file, newFile):
    f = open(file, 'r')
    contents = f.read()
    f.close()
    new_contents = contents.replace('\n', '') #This removes all newlines
    wipe1 = new_contents.replace(' |', '|') #This line removes all instances of a space followed by a pipe
    wipe2 = wipe1.replace('| ', '|') #This line removes all instances of a pipe followed by a space.
    f = open(newFile, 'w+') #We write this all to the new file.
    f.write(wipe2)      
    f.close()

    #The importance of having everything together comes into play in the rebuildColumns function.
    
#Our cleanUp function will take the end result of putting the text into blocks
# and then check if there is punctuation followed by any letters (e.g. "Hello!Mary!")
# and separate them by putting a space in between the punctuation and the following text.
# Example from my test file:
# "I'm testing a script right now! | This second sentence wi | Back to colOne! | ll test separation! | he?llo?\n"
# 
# and result from this program:
# "I'm testing a script right now! Back to colOne! he? llo? 
# This second sentence will test separation!"
#
#As per the program logic, the first, third, and fifth segment all compose the first column
# and the second and fourth segments both compose the second column.

def cleanUp(endResult):
    tempCount = 0
    testVar = ''
    tempColOne = ""
    tempColTwo = ""
    testResult = endResult
    for token in endResult:
        if (token == '!') or (token == '?') or (token == ',') or (token == '.'):
            #print('Found punctuation:', token, "at space:", tempCount)
            tempColOne = testResult[:tempCount+1]
            tempColTwo = testResult[tempCount+1:] #Replaced endResult w/ testResult
            testResult = tempColOne + ' ' + tempColTwo
            #print("tempColOne = ", tempColOne)
            #print("tempColTwo = ", tempColTwo)
            #print("Test result = ", testResult)
            tempCount = tempCount + 1
        tempCount = tempCount + 1
        #print("tempCount = ", tempCount)
    endResult = testResult    
    return endResult


#rebuildColumns will check the input file for all pipes
# and begin to separate them into either column 1 or column 2.
#After that finishes, I insert a newLine character between the two so that
# our output will be something akin to:
# "Column one is this!
# Column two is this!"
# as opposed to: "Column one is this! Column two is this!"

def rebuildColumns(newFile):
    f = open(newFile, 'r')
    contents = f.read()
    f.close()
    colOne = ""
    colTwo = ""
    count = 1 #If 1, then we are placing into first column. If 2, the second. If 0, then we end program.
    startVar = 0 #Starting location
    colRead = 0 #Location at which we read in a pipe.
    while count != 0:
        colRead = contents.find('|', startVar)  #find() will return position of pipe
        if colRead == -1:                       # if a pipe wasn't found, it returns -1.
            if count == 1:                      #So we do error cases because this means that we've
                colOne += contents[startVar:]   # reached the end of the file.
                count = 0
                #print(colOne)
            elif count == 2:
                colTwo += contents[startVar:]   #Here we check if the count was 1 or 2, to determine
                #print(colTwo)                   # which of the two columns the last bit of our scan
                count = 0                       # goes into.
        elif count == 1:                        #Here it is assumed that we had a valid find,
            colOne += contents[startVar:colRead]# thus we calculate where it was and copy from the last
            count = 2                           # position where we encountered a pipe until the current
            #print(colOne)                       # position.
        elif count == 2:
            colTwo += contents[startVar:colRead]
            count = 1
            #print(colTwo)
        startVar = colRead + 1
        #print("colRead =", colRead)  #testing material
        #print("startVar =", startVar)
    endResult = colOne
    endResult += '\n'
    endResult += colTwo
    #print("colOne = ", colOne)
    #print("colTwo = ", colTwo)
    #print("endResult = ", endResult)
    #print(endResult[1:10])
    endResult = cleanUp(endResult) #Call to clean up any bad punctuation that may have happened.
    #newFile = file[:len(file)-4] + 'Result' + '.txt' #Making new file with original name, just appending "result" to it
    #print(newFile)
    f = open(newFile, "w+") #Will write new separated columns into file
    f.write(endResult)  #Remember to look up how to make a new file so as to not overwrite the 
    f.close()           # initial one entirely!
    




file = sys.argv[1]
newFile = file[:len(file)-4] + 'Result' + '.txt' #Making new file with original name, just appending "result" to it
removeNewlines(file, newFile)
rebuildColumns(newFile)



#CREATOR'S NOTES:
# This program assumes that there are only two columns.
# Maybe another program could be done with more than 2 columns that uses an array?
# Will have to try

#Must decide how to space out pipes. Do we want "| ", " |", and "|"?

# This script also uses removeNewlines for clarity and ease of use.
















