#!/bin/bash
#Remove Outputs Script by Jorge.FonsecaCacho@UNLV.edu
#Be sure to type chmod +x removeoutputsScript.sh in order to be able to run the script without typing bash ahead of file name!
echo "Remove Outputs Script:"
# input: 
# output: 

echo -e "\nRemoving all output.txt files in this folder\n"

timestart=$SECONDS # Execution Timer Start 

#Execution

echo -e "Removing runScript Output File...\n"
rm -f -- runScript_output.txt

echo -e "Removing Alignment Output File...\n"
rm -f -- alignment_output.txt

echo -e "Removing Confusion Matrix Output File...\n"
rm -f -- confusionmatrix_output.txt

echo -e "Removing Candidates Output File...\n"
rm -f -- candidates_output.txt

#End of Execution
timeduration=$(( $SECONDS - timestart )) #Execution Timer End
echo -e "Total Time in Seconds: $timeduration"
echo -e "\nEnd of Script.\n"
