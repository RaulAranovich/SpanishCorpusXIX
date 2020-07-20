import os
import sys
import re

def removeNewlines(file):
    f = open(file, 'r', encoding="utf-8")
    contents = f.read()
    f.close()
    new_contents = contents.replace('\n', ' ')
    f = open(file, 'w', encoding="utf-8")
    f.write(new_contents)
    f.close()

file = sys.argv[1]
removeNewlines(file)
