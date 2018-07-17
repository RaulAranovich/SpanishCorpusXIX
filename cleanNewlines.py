import os
import sys
import re

def removeNewlines(file):
    f = open(file, 'r')
    contents = f.read()
    f.close()
    new_contents = contents.replace('\n', '')
    f = open(file, 'w')
    f.write(new_contents)
    f.close()

file = sys.argv[1]
removeNewlines(file)
