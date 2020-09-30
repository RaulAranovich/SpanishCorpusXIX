#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu

This File contains common classes shared between different python scripts.
"""

import sys
import mysql.connector as mc
import Levenshtein  #pip install python-levenshtein
import difflib #apt-get install npm; npm install difflib
import time
from datetime import timedelta



#Class To Store doctextSolution(word, wordOR, location, locationOR, docSource) after we read it in from the database
class doctextSol: #This class is similar to the one in alignment but contains less members and contains docsource and matches database table columns.
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
#    def __eq__(self, other):
#	if isinstance(other, doctextSol): #If both are same object type
#	    #For equality compare all members to ensure equality
#	    return ( (self.word == other.word) and (self.wordOR == other.wordOR) and (self.location == other.location) ) 
#	else:
#	    return False #They are not same object type so don't even bother checking
#    def __ne__(self, other): #for !equals
#	return (not self.__eq__(other)) #rather than rewriting function just return opposite of what the above gives
#    def __hash__(self):
#	return hash(self.__repr__())



#Class to Store Confusion Matrix Entry (fromletter, toletter, frequency)
class confMatrix: #This Class Matches the table in database for confusion matrix.
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
    


#Class to Store docErrorList Entry (word, location, docSource) after we read it in from the database
class docErrorList: #This Class Matches the table in database for docErrorList
    def __init__(self, word, location, docSource):
	self.word	= word
	self.location	= location
	self.docSource  = docSource
#    def __init__(self):
#	self.word	= "Unknown"
#	self.location	= -1
#	self.docSource  = "00000000-0-00000"
    def __repr__(self):
	return '\ndocErrorList(%s, %d, %s)' % (self.word, self.location, self.docSource)
    def __eq__(self, other):
	if isinstance(other, docErrorList): #If both are same object type
	    #For equality compare all members to ensure equality
	    return ( (self.word == other.word) and (self.location == other.location) and (self.docSource == other.docSource) ) 
	else:
	    return False #They are not same object type so don't even bother checking
    def __ne__(self, other): #for !equals
	return (not self.__eq__(other)) #rather than rewriting function just return opposite of what the above gives
    def __hash__(self):
	return hash(self.__repr__())


 
#Class to Store candidates Entry(location, fromword, toword, distance, confusionWeight, unigramFreq, backwardsBigramFreq, forwardBigramFreq, output, decision, docSource) 
#candidates(location, fromword, toword, distance, confWeight, uniFreq, bkwdFreq, fwdFreq, output, decision, docSource)
class candidates: #This Class Matches the table in database for candidates
    def __init__(self, location, fromword, toword, distance, confWeight, uniFreq, bkwdFreq, fwdFreq, output, decision, docSource):
	self.location	= location
	self.fromword 	= fromword
	self.toword 	= toword
	self.distance 	= distance
	self.confWeight = confWeight
	self.uniFreq 	= uniFreq
	self.bkwdFreq 	= bkwdFreq
	self.fwdFreq 	= fwdFreq
	self.output 	= output
	self.decision 	= decision
	self.docSource  = docSource
#    def __init__(self):
#	self.location	= -1
#	self.fromword 	= "Unknown"
#	self.toword 	= "Unknown"
#	self.distance 	= 100
#	self.confWeight = 0
#	self.uniFreq 	= 0
#	self.bkwdFreq 	= 0
#	self.fwdFreq 	= 0
#	self.output 	= 0.0
#	self.decision 	= 0.0
#	self.docSource  = "00000000-0-00000"
    def __repr__(self):
	return '\ncandidates(%d, %s, %s, %d, %d, %d, %d, %d, %.2f, %.2f, %s)' % (self.location, self.fromword, self.toword, self.distance, 
				self.confWeight, self.uniFreq, self.bkwdFreq, self.fwdFreq, self.output, self.decision, self.docSource)
    def __eq__(self, other):
	if isinstance(other, candidates): #If both are same object type
	    #For equality compare all members to ensure equality
	    return ( (self.location == other.location) and (self.fromword == other.fromword) and 
			(self.toword == other.toword) and (self.distance == other.distance) and 
			(self.confWeight == other.confWeight) and (self.uniFreq == other.uniFreq) and 
			(self.bkwdFreq == other.bkwdFreq) and (self.fwdFreq == other.fwdFreq) and 
			(self.output == other.output) and (self.decision == other.decision) and (self.docSource == other.docSource) ) 
	else:
	    return False #They are not same object type so don't even bother checking
    def __ne__(self, other): #for !equals
	return (not self.__eq__(other)) #rather than rewriting function just return opposite of what the above gives
    def __hash__(self):
	return hash(self.__repr__())



#Class to Store onegmsORIGINAL (word, frequency). This is a dictionary of all words seen in ground truth. Can be used in lieu of a dictionary.
'''
class onegmsORIGINAL: #This Class Matches the onegmsORIGINAL table in the database
    def __init__(self, word, frequency):
	self.word 	= word
	self.frequency 	= frequency
#    def __init__(self):
#	self.word 	= ""
#	self.frequency	= 0
    def __repr__(self):
	return '\nonegmsORIGINAL(%s, %d)' % (self.word, self.frequency)
    def __eq__(self, other):
	if isinstance(other, onegmsORIGINAL): #If both are same object type
	    return ( (self.word == other.word) and (self.frequency == other.frequency) ) #For equality compare word and frequency to ensure equality
	else:
	    return False #They are not same object type so don't even bother checking
    def __ne__(self, other): #for !equals
	return (not self.__eq__(other)) #rather than rewriting function just return opposite of what the above gives
    def __hash__(self):
	return hash(self.__repr__())
'''



#

