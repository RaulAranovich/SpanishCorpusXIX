import os
import sys
import re

def removeNewlines(file):
	file1 = r"C:\Users\Daniel\Desktop\Research\la_iberia\iberia_results_final\undone\\" + file
	f = open(file1, 'r', encoding="utf-8")
	contents = f.read()
	f.close()
	new_contents = contents.replace('\n', '')
	file2 = r"C:\Users\Daniel\Desktop\Research\la_iberia\iberia_results_final\undone\cleanResults\\" + file
	f = open(file2, 'w', encoding="utf-8")
	f.write(new_contents)
	f.close()
	

file = sys.argv[1]
removeNewlines(file)