#!/bin/bash
#Google1T Find Script by Jorge.FonsecaCacho@UNLV.edu
echo "Google1T Find Script:"
# input: 3 words with the middle one being the mispelled word.
# output: all possible candidates from Google1T assuming first and third word are spelled correctly.

#check if correct arguments given
if [[ $# != 3 ]];
   then
	echo "Usage: ./findCandidates3gms word1 word2 word3"
	exit
fi

#check for empty string
if [ -z "$1" ]
   then
	echo "Usage: ./findCandidates3gms word1 word2 word3"
	exit
fi

echo "Input: $1 $2 $3. Word $2 is the mispelled word."

#Check Index to locate files to look in:

