import os
import glob

sourcedir = "output/source-docs/"
ocrspelldir = "output/OCRSpell/"
threegramdir = "output/3gram/"
candidatedir = "output/Google1T/search/"
refinedir = "output/Google1T/refine/"
verifyfile = "output/Google1T/verify/verify.output"

verifyfile = open(verifyfile)

files = glob.glob("output/source-docs/degrade.*.000")
files.sort()

totalwords = 0
totalincorrect = 0
totalcaught = 0
totalrawcandidates = 0
totalrefcandidates = 0
totalsuggest = 0
totalfirstsuggest = 0
totalfalsepos = 0

for file in files:
    file = os.path.basename(file)
    tail = file[7:]
    orig = "original" + tail

    infile = open("output/source-docs/" + file)

    wordsinfile = 0
    for line in infile:
        words = line.rstrip().split(" ")
        wordsinfile += len(words)
        totalwords += len(words)
    infile.close()

    vline = verifyfile.readline().split(" ")
    if vline[0] == file + ".suggestions":
        print file
        print orig
    else:
        print "Files don't match", file, vline[0], "vs", file+"suggestions", "\n"
        continue

    firstinlist = int(vline[1])
    inlist = int(vline[2])

    # We will collect all words from a given degraded document into a list.
    # We will then remove all words in the original document from words in the degraded docuemt's list
    # The remaining words are all incorrect words.
    # We ignore numbers as we cannot correct numbers
    dwords = []
    owords = []

    subdocs = glob.glob(sourcedir+file[:-4]+"*")
    for subdoc in subdocs:
        myfile = open(subdoc)
        words = myfile.read().split()
        dwords.extend(words)
        myfile.close()

    subdocs = glob.glob(sourcedir+orig[:-4]+"*")
    for subdoc in subdocs:
        myfile = open(subdoc)
        words = myfile.read().split()
        owords.extend(words)
        myfile.close()

    incorrect = []
    for word in dwords:
        word = word.rstrip()
        if not str.isdigit(word):
            incorrect.append(word)

    del dwords

    for word in owords:
        word = word.rstrip()
        try:
            incorrect.remove(word)
        except ValueError:
            pass

    del owords

    # Calculate #detected/#incorrect
    # Count number of words with candidates
    # Calculate #WithCandidates/#WithoutCandidates
    # Count number of words with answer as first word
    # Calculate #withanswer/#withoutanswer

    fin = open(candidatedir+file+".candidates")

    rawwithcandidates = 0
    wrongwords = []
    idx = 0
    lookingforcand = False
    for line in fin:
        if lookingforcand and line[0:3] != "%%%":
            rawwithcandidates += 1
            lookingforcand = False
            continue
        else:
            if line[0:3] == "%%%":
                line = line.split(' ')
                lookingforcand = True
                wrongwords.append(line[2])

    incorrectbutnot = len(wrongwords)
    wrongwords = [word for word in wrongwords if word in incorrect]
    incorrectbutnot = incorrectbutnot - len(wrongwords)
    print "  Falsely marked as incorrect: ", incorrectbutnot

    falsepos = 100 - 100*(len(wrongwords)/float(len(incorrect)))
    fin.close()

    # After refinement, repeat the same calculations as above

    count = 0

    fin = open(refinedir+file+".suggestions")
    for line in fin:
        count += 1
    fin.close()

    # Print statistics
    print "  Actual incorrect words:", len(incorrect)

    print "  Words identified as wrong: ", len(wrongwords)
    print "  Percentage of incorrect words marked as correct ", falsepos, '%'

    print "  Words with candidates: ", rawwithcandidates
    print "  Percentage of identified misspellings with candidates: ", 100*rawwithcandidates/len(wrongwords), "%"
    print "  Percentage of incorrect words with candidats: ", 100*rawwithcandidates/float(len(incorrect)), "%"

    print "  Words with candidates(refined): ", count
    print "  Percentage of identified misspellings with candidates: ", 100*count/len(wrongwords), "%"
    print "  Percentage of incorrect words with candidates: ", 100*count/float(len(incorrect)), "%"

    print "  Words with correct word as first suggestion: ", firstinlist
    print "  Words with correct word in suggestions: ", inlist
    print "  Percentage of words with candidates with correct word as first suggestion: ", 100*firstinlist/float(count), "%"
    print "  Percentage of identified misspellings with correct word as first suggestion: ", 100*firstinlist/float(len(wrongwords)), "%"
    print "  Percentage of incorrect words with correct word as first suggestion: ", 100*firstinlist/float(len(incorrect)), "%"
    print "  Percentage of words with candidates with correct word in suggestions: ", 100*inlist/float(count), "%"
    print "  Percentage of identified misspellings with correct word in suggestions: ", 100*inlist/float(len(wrongwords)), "%"
    print "  Percentage of incorrect words with correct word in suggestions: ", 100*inlist/float(len(incorrect)), "%"

    print " "

    # Sum for averages
    totalincorrect += len(incorrect)
    totalcaught += len(wrongwords)
    totalrawcandidates += rawwithcandidates
    totalrefcandidates += count
    totalsuggest += inlist
    totalfirstsuggest += firstinlist
    totalfalsepos += incorrectbutnot

print "Total words: ", totalwords
print "Total incorrect: ", totalincorrect
print "Total identified incorrect: ", totalcaught
print "Total with raw candidates: ", totalrawcandidates
print "Total with refined candidates: ", totalrefcandidates
print "Total with word in suggestions: ", totalsuggest
print "Total with word as first suggestion: ", totalfirstsuggest

print " "

print "Percent caught were false positives: ", 100*float(totalfalsepos)/float(totalcaught), "%"
print "Percent incorrect identified as incorrect: ", 100*float(totalcaught)/float(totalincorrect), "%"
print "Percent incorrect with candidates (raw): ", 100*float(totalrawcandidates)/float(totalincorrect), "%"
print "Percent caught with candidates (raw): ", 100*float(totalrawcandidates)/float(totalcaught), "%"
print "Percent incorrect with candidates (refined): ", 100*float(totalrawcandidates)/float(totalincorrect), "%"
print "Percent caught with candidates (refined): ", 100*float(totalrefcandidates)/float(totalcaught), "%"
print "Percent incorrect with word in suggestions: ", 100*float(totalsuggest)/float(totalincorrect), "%"
print "Percent caught with word in suggestions: ", 100*float(totalsuggest)/float(totalcaught), "%"
print "Percent raw with word in suggestions: ", 100*float(totalsuggest)/float(totalrawcandidates), "%"
print "Percent refined with word in suggestions: ", 100*float(totalsuggest)/float(totalrefcandidates), "%"
print "Percent incorrect with word in as first suggestion: ", 100*float(totalfirstsuggest)/float(totalincorrect), "%"
print "Percent caught with word as first suggestion: ", 100*float(totalfirstsuggest)/float(totalcaught), "%"
print "Percent raw with word as first suggestion: ", 100*float(totalfirstsuggest)/float(totalrawcandidates), "%"
print "Percent refined with word as first suggestion: ", 100*float(totalfirstsuggest)/float(totalrefcandidates), "%"


