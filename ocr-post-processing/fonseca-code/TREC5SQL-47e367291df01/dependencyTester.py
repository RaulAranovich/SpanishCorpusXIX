#apt-get install npm
#npm install difflib

import sys
import mysql.connector as mc
import Levenshtein
import difflib
import time
from datetime import timedelta
time0 = time.time()

#Levenshtein Function Test Code:
a ="car"
b ="cat"
print "Levenshtein Distance between '"+a+"\' and \'"+b+"\' is", Levenshtein.distance(a,b), ".\n"
#Done Checking Levenshtein


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
cursor.close()
connection.close()
#Done Checking Sql


if (len(sys.argv) != 3):
    pass
else:
    pass

#difflib Test Code:
def show_diff(seqm):    #from docs.python.org
    """Unify operations between two compared strings
seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output= []
    for opcode, i1, i2, j1, j2 in seqm.get_opcodes():
        if opcode == 'replace':  #a[i1:i2] should be replaced by b[j1:j2]
	    output.append(" <rep>" + seqm.a[i1:i2] + "2" + seqm.b[j1:j2] + "</rep> ")
        elif opcode == 'delete': #a[i1:i2] should be deleted. Note that j1 == j2 in this case.
            output.append(" <del>" + seqm.a[i1:i2] + "</del> ")
            #raise NotImplementedError, "what to do with 'replace' opcode?"
        elif opcode == 'insert': #b[j1:j2] should be inserted at a[i1:i1]. Note that i1 == i2 in this case.
            output.append(" <ins>" + seqm.b[j1:j2] + "</ins> ")
        elif opcode == 'equal': #a[i1:i2] == b[j1:j2] (the sub-sequences are equal).
            output.append(seqm.a[i1:i2])
        else:
            raise RuntimeError, "unexpected opcode"
    return ''.join(output)

sm= difflib.SequenceMatcher(None, "appie", "apple")
print show_diff(sm)

sm= difflib.SequenceMatcher(None, "appple", "apple")
print show_diff(sm)

sm= difflib.SequenceMatcher(None, "aple", "apple")
print show_diff(sm)

sm= difflib.SequenceMatcher(None, "apple", "apple")
print show_diff(sm)

sm= difflib.SequenceMatcher(None, "appiie", "apple")
print show_diff(sm)

sm= difflib.SequenceMatcher(None, "oppiie", "apple")
print show_diff(sm)

sm= difflib.SequenceMatcher(None, "aappplee", "apple")
print show_diff(sm)




a = "qabxxcd"
b = "abycdf"
s = difflib.SequenceMatcher(None, a, b)
for tag, i1, i2, j1, j2 in s.get_opcodes():
    print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %
           (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))
# delete a[0:1] (q) b[0:0] ()
#  equal a[1:3] (ab) b[0:2] (ab)
#replace a[3:4] (x) b[2:3] (y)
#  equal a[4:6] (cd) b[3:5] (cd)
# insert a[6:6] () b[5:6] (f)

print a, " - > ", b
for tag, i1, i2, j1, j2 in s.get_opcodes():
   # if tag != 'equal': #Ignore equals
        print ("%7s (%s) -> (%s)" %
	(tag, a[i1:i2], b[j1:j2]))

#String formatting
#print "%-12s -> %-17s Distance: %d" % ( a, b, 1 )
#Done Checking difflib

print "Execution Time:"
print timedelta(seconds=round((time.time() - time0)))
print "\nFinished Successfully!\n"+sys.argv[0]+"\n"
