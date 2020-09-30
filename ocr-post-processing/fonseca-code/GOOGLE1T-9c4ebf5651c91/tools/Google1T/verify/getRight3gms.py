# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

"""
Will load in our 3gms and will locate the correct middle word from the ground
truth file and ocrd file in order to create a list of the correct 3gms, output 
that to a file, then output a 2nd file with just the correct middle word
(for flexibility)

"""

import sys  #For reading Command line arguments
#Check Argument amount is right
if len(sys.argv) != 4:
    print "Usage: getRight3gms.py file.output.3gms fr940104.0.clean FR940104.0.clean"
    quit()
#print sys.argv[0] #Prints the Name of the File pwd/Filename
#print sys.argv[1] #Prints the file.output.3gms of the OCR'd Version
#print sys.argv[2] #Prints file.clean (ground truth correct file)
#print sys.argv[3] #Prints FILE.clean (OCR'd source file)
print "Program will open file with correct word and compare it with our suggestions."

file3gms = sys.argv[1]
fileorg  = sys.argv[2]
fileocrd = sys.argv[3]

