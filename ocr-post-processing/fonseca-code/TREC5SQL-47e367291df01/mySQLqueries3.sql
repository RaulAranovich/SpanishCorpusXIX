#Alignment Test Queries Useful to get info about alignment mismatches etc

#Will List both tables  (not aligned at all, but useful to get idea of text
SELECT doctext.word, doctextORIGINAL.word as wordOR, doctext.location, doctextORIGINAL.location as locationOR FROM doctext 
JOIN doctextORIGINAL on doctext.location = doctextORIGINAL.location 
WHERE doctext.docsource LIKE '%08' ORDER BY doctext.location LIMIT 285, 385;

#will list the alignment
SELECT doctext.word, doctextORIGINAL.word as wordOR, doctext.location, doctext.locationOR, doctext.docsource 
FROM doctext JOIN doctextORIGINAL ON doctext.locationOR = doctextORIGINAL.location 
WHERE doctext.docsource LIKE '%08' ORDER BY doctext.location LIMIT 285, 385;
#We can see that location 3227 matched with 3183 and that is an example of a FALSE NEGATIVE as it matched successfully.
#Same with 3467, 3307, 3382, 3385, 
#We notice that if there is a lot of numbers of same number of digits near each other, the alignment will run
# into problems as it may align it with another number

#List match failures
SELECT * FROM matchfailList WHERE docsource LIKE '%08' LIMIT 100;

#now we combine them to see what it could have tried to match to and failed to see if we can see any signs
SELECT doctext.word, doctextORIGINAL.word as wordOR, doctext.location, doctext.locationOR, doctext.docsource 
FROM doctext JOIN doctextORIGINAL ON doctext.locationOR = doctextORIGINAL.location 
JOIN matchfailList ON doctext.location = matchfailList.location 
WHERE doctext.docsource LIKE '%08' LIMIT 100;

#The big mismatch in file 8 is due to missing text in degrade leading to the following locations:
#3511 Degrade:  This order (l) deletes the
#3710 Original: This order (1) deletes the remaining

#Because of this 200 word missing gap. the matching gets lost and never gets re-aligned again.  The solution to this is I think is once he hit a
#serious failure of more than our typical NEARBY value of 20 (or we could make it like 2*NEARBY, then go back to the first few words where the
#Failures started and scan ahead up to 300 (for now then increase) ahead and try and see if we can find 4 out of the 5 words later on in the text
#if we do that then we wil go ahead and realize that there must be missing text in OCR and we can get back on track. if this works then we check
#to see if we keep getting matches and then we move on!

#How many match fails after 3511  #224
SELECT COUNT(*) FROM matchfailList WHERE docsource LIKE '%08' AND location >= 3511;
#Before that we only had 5 mismatches of which we saw were all false negatives.
SELECT COUNT(*) FROM matchfailList WHERE docsource LIKE '%08' AND location < 3511;

#just to check earlier in text
SELECT doctext.word, doctextORIGINAL.word as wordOR, doctext.location, doctext.locationOR, doctext.docsource 
FROM doctext JOIN doctextORIGINAL ON doctext.locationOR = doctextORIGINAL.location 
WHERE doctext.docsource LIKE '%08' ORDER BY doctext.location LIMIT 01, 185;

#Simple Alignment Queries For Paper Visuals:
USE TRECSample;
SELECT * FROM doctext LIMIT 24;
SELECT * FROM doctextORIGINAL LIMIT 19;
SELECT * FROM doctextSolutions LIMIT 24;
SELECT * FROM matchfailList LIMIT 1;
SELECT * FROM docErrorList LIMIT 14;









