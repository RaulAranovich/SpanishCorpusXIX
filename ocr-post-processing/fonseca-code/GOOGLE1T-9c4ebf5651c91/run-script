#!/bin/bash
#Google1T Run Script by Jorge.FonsecaCacho@UNLV.edu
#This script will run all of the modules of the Google 1T 3gms Project + More
#Type chmod +x runScript before running!
echo "Google1T Run Script"

#check if correct arguments given
if [ $# = 3 ]
then
   if [ $1 = "-o" ]
   then
      ocr="yes"
      TREC=$2
      idx=$3
   else
      echo "Usage: ./runScript [-o] 'TREC-5 Folder Location' 'Path to 3gm.idx'"
      echo "Example: ./runScript -o TRECSample/TREC-5 Google1T/3gms/3gm.idx"
      echo "NOTE: '-o' option will run OCRSpell. You should only need to use this opt"
      exit
   fi
else
   if [ $# = 2 ]
   then
      ocr="no"
      TREC=$1
      idx=$2
   else
      echo "Usage: ./runScript [-o] 'TREC-5 Folder Location' 'Path to 3gm.idx'"
      echo "Example: ./runScript -o TRECSample/TREC-5 Google1T/3gms/3gm.idx"
      echo "NOTE: -o option will run OCRSpell. You should only need to use this opt once"
      exit
   fi
fi

#Step 0: Find and uncompress the specified file and save it to SourceText
for dir in $(ls  $TREC/confusion_track/original/); do
   for file in $(ls $TREC/confusion_track/original/$dir/); do
      gunzip -c $TREC/confusion_track/original/$dir/$file > SourceTexts/original.${file:0:-3}
   done
done

for dir in $(ls $TREC/confusion_track/degrade5/); do
   for file in $(ls $TREC/confusion_track/degrade5/$dir/); do
      gunzip -c $TREC/confusion_track/degrade5/$dir/$file > SourceTexts/degrade.${file:0:-3}
   done
done

#Step 1: Split the file into manageable chunks of about 1500 words each, cut at the end of the closest DOCUMENT to not split pages.
#Run the script

mkdir output > /dev/null 2>&1
mkdir output/3grams >/dev/null 2>&1
mkdir output/logs >/dev/null 2>&1
mkdir output/Google1T/search >/dev/null 2>&1
mkdir output/Google1T/refine >/dev/null 2>&1
mkdir output/Google1T/verify >/dev/null 2>&1
mkdir output/OCRSpell > /dev/null 2>&1
mkdir output/source-docs > /dev/null 2>&1

for file in $(ls SourceTexts/); do
   echo "Separating $file"
   python tools/separateDocs.py SourceTexts/$file > output/logs/separate.log
   cat SourceTexts/$file | sed '/^</ d' | wc -l -w
done

if [[ $ocr == "yes"  ]]
then
   echo "Running OCRSpell. . ."
   tools/scripts/OCRSpell
   echo "Done."
   echo " "
fi

echo "Getting 3-grams. . ."
python tools/get3gram.py > output/logs/3grams.log
echo "Done."
echo " "

echo "Finding candidates. . ."
python tools/Google1T/search/findCandidates3gms.py $idx > output/logs/candidates.log
echo "Done."
echo " "

echo "Refining candidates. . ."
python tools/Google1T/refine/refineCandidates.py > output/logs/refine.log
echo "Done."
echo " "

echo "Verifying and generating statistics. . ."
python tools/Google1T/verify/verifyCandidates.py > output/logs/verify.log


C=0
for (( ; C<1000; C++)); do
    if [ ! -f statistics.align$C.txt ]
    then
 	python tools/scripts/stats.py > statistics.align$c.txt
	break
    fi
done

echo "Done."
