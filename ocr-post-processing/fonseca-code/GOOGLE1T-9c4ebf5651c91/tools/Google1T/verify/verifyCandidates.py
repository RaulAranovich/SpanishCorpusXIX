# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

"""
Load In correct word file and use that to compare to our candidates words to
check accuracy and effectiveness of using Google1T to create our suggestions.
"""

import os
import glob
import re

print "Program will open file with correct word and compare it with our suggestions."

files = glob.glob("output/Google1T/refine/*.suggestions")
files.sort()
outfile = open("output/Google1T/verify/verify.output", "w+")

map = open('doctextSolutions.txt')
mapentries = []
mapline = []

for filename in files:
    name = os.path.basename(filename)
    print name

    name=name[8:24]
    if mapline == []:
        mapline = map.readline().rstrip()
        mapline = re.findall("\S+", mapline)

    while mapline[len(mapline)-1] == name:
        mapentries.append([mapline[0], mapline[1]])
        mapline = map.readline()
        if not mapline:
            break
        mapline = re.findall("\S+", mapline)


    candfile = open(filename)
    correctinfirst = 0
    correctinlist = 0
    for line in candfile:
        suggestions = re.findall("\S+", line)

        idx = 0
        while idx < len(suggestions):
            suggestions[idx] = suggestions[idx].lower()
            idx += 1

        incorrect = suggestions[0]

        # Open correct mapping, find word in question, check if correct is in our suggestions
        idx = 0
        end = len(mapentries)
        while idx < end:
            if mapentries[idx][0] == incorrect:
                # Correct word found. Check if it is in our suggestions
                if mapentries[idx][1].lower() == suggestions[1]:
                    correctinfirst += 1
                    correctinlist += 1
                elif mapentries[idx][1].lower() in suggestions:
                    correctinlist += 1
                # IMPORTANT. We delete the word as two instances of the same mispelling are possibly two different corrected words.
                del mapentries[idx]
                break
            idx += 1

    outfile.write(os.path.basename(filename) + " " + str(correctinfirst) + " " + str(correctinlist) + "\n")
