#!/bin/bash
#Run Script by Jorge.FonsecaCacho@UNLV.edu
#Be sure to type chmod +x runScript.sh in order to be able to run the script without typing bash ahead of file name!
echo "Run Script:"
# input: 
# output: 

#check if correct arguments given
if [[ $# != 2 ]];
   then
	echo "Usage: ./runScript OriginalFile DegradeFile"
	#Example: ./runScript.sh SourceTexts/original.FR940104.0 SourceTexts/degrade.FR940104.0
	#or if you want to save output via linux redirection: 
	#./runScript.sh SourceTexts/original.FR940104.0 SourceTexts/degrade.FR940104.0 > output/runScript_output.txt
	exit
fi

#check for empty string
if [ -z "$1" ]
   then
	echo "Usage: ./runScript OriginalFile DegradeFile"
	exit
fi

echo "Input Files: Original: $1 Degrade: $2"

timestart=$SECONDS # Execution Timer Start
#sleep .5 #Sleeps for .5 Seconds, use it to test our timer. 

#Execution

echo -e "\nRemoving Old Output Files...\n"
rm -f -- output/runScript_output.txt
rm -f -- output/alignment_output.txt
rm -f -- output/confusionmatrix_output.txt
rm -f -- output/candidates_output.txt

echo -e "\nRunning Insertion into Database of file...\n"
python trec5sqlinsert.py $1 original; python trec5sqlinsert.py $2 degrade

echo -e "\nRunning Alignment...\n"
python trec5alignment.py 0 0

echo -e "\nCreating/Updating Confusion Matrix...\n"
python trec5confusionmatrix.py 0 0

echo -e "\nCreating/Updating Candidate List...\n"
python trec5candidatelist.py 0 0

echo -e "\nRunning Data Error Analysis/Regression...\n"
python trec5regression.py 0 0

echo -e "\nRunning Experiment...\n"
#PASTE COMMAND HERE

echo -e "\nRunning Precision and Recall...\n"
#PASTE COMMAND HERE

#End of Execution
timeduration=$(( $SECONDS - timestart )) #Execution Timer End
echo -e "\nTotal Time in Seconds: $timeduration"
echo -e "\nEnd of Script.\n"
