/* 
mySQLqueries4

Here we are finalizing the candidate table these are some queries we used to finish doing that

*/

/* Test to see where we are at */

USE TRECSample;
SELECT * FROM confusionmatrix LIMIT 10;
-- fromletter		VARCHAR(4),
-- toletter			VARCHAR(4),
--

SELECT * FROM candidates LIMIT 10;

/* Total errors we have candidates for */
SELECT count(fromword) FROM (SELECT DISTINCT fromword FROM candidates AS a) AS b;

/* all rows in candidates (bigger than number above because we have more than 1 candidate per word for many of them) */
SELECT count(*) from candidates;

select * from doctext where location = 0;
select * from doctextORIGINAL where location = 0;

SELECT * FROM candidates where location > 60 LIMIT 30;

/* *************************************************** */
/* Good Line: '63', 'lepartment', 'Department', '1', '1421', '38', '11', '32', '-1', '-1', 'FR940104-0-00002' */
SELECT * FROM candidates where location = 63 LIMIT 10;

SELECT * FROM threegmsORIGINAL WHERE wordtwo = "Department" 
AND wordone  = (SELECT word FROM doctext WHERE location = 63-1);

SELECT SUM(frequency) FROM threegmsORIGINAL WHERE wordtwo = "Department" 
AND wordone  = (SELECT word FROM doctext WHERE location = 63-1);

SELECT * FROM threegmsORIGINAL WHERE wordtwo = "Department" 
AND wordthree  = (SELECT word FROM doctext WHERE location = 63+1);

SELECT SUM(frequency) FROM threegmsORIGINAL WHERE wordtwo = "Department" 
AND wordthree  = (SELECT word FROM doctext WHERE location = 63+1);
/* *************************************************** */

SELECT * FROM doctextSolutions LIMIT 60;

SELECT * FROM candidates LIMIT 10;

/* Returns correct candidate line for each */
SELECT candidates.location, candidates.toword, candidates.distance, candidates.confusionweight,
candidates.unigramfrequency, candidates.forwardbigramfreq, candidates.output, candidates.decision, 
candidates.docsource, doctextSolutions.wordOR FROM candidates JOIN doctextSolutions on candidates.location = doctextSolutions.location
AND candidates.docsource = doctextSolutions.docsource WHERE toword=wordOR LIMIT 10;

-- send location and wordOR(candidate), return wordOR(if equal)

SELECT * FROM candidates WHERE location > 7 LIMIT 10;
-- 'tuesday1', 'tuesday,', '8', '15', 'FR940104-0-00001'
SELECT * FROM doctextSolutions LIMIT 10;

/* basically if this returns 0 then its not match, if it returns anything else (1) it's match! */
SELECT count(*) from doctextSolutions WHERE location=8 AND wordOR = "tuesday,";

SELECT count(*) from doctextSolutions WHERE location=8 AND wordOR = "tuesday";



SELECT * FROM candidates WHERE output = 1 LIMIT 100;

-- Regression Section:

SELECT MIN(location) FROM candidates;

SELECT * FROM candidates WHERE location > 0-1  AND location < 1000 + 1;

SELECT * FROM candidates LIMIT 100;

-- Test Query for updating candidate table
SELECT * FROM candidates WHERE location=1 AND fromword="hegister" AND toword="existed";
UPDATE candidates SET decision = -1 WHERE location=1 AND fromword="hegister" AND toword="existed";

;

/* Error Analysis */
USE TRECSample;

/* LIMIT A, B where A is Offset and B is number of rows to print after offset
   To convert back from normalized to original:
   X = min + y*(max - min). Where Y is normalized value and X is original value 
   To Find row number based on Index. We need to do 
   Index+TotalDataInstances*0.8 and take floor of it.  TotalDataInstances = 325,547 
   Note: the row number may be off by +/- 1.
*/
-- Sample:
SELECT 1+(   0.00196938501477   )*(11172-1); -- 23
SELECT (325547*0.8) + 1247  ; -- 261684
SELECT * FROM candidates LIMIT 261684, 8; -- Found in second row 23 unigram freq. Matched!





-- Errors:
USE TRECSample;

-- 1) False Positive Example:
SELECT 1+(   0.00196938501477   )*(11172-1); -- 23
SELECT (325547*0.8) + 1247  ; -- 261684

SELECT * FROM candidates LIMIT 261684, 8; -- Found in second row 23 unigram freq. Matched!
SELECT * FROM doctext WHERE location >= 116527 LIMIT 6; -- 5-gram OCR'd Text
SELECT * FROM doctextORIGINAL WHERE location >= 114963 LIMIT 6; -- 5-gram Original Text
/*
prodects1 was predicted as products, but instead it was projects, 
the confusionweights were similar (1674, 1793 respectively), but products, had a higher unigram frequency (23 vs 1)
and a higher forward bigram frquency (5  vs 1). projects, did have one instance of backwards bigram vs none for products.
Ultimately both are very similar and context is necesary to see which one is correct. 
If we look at the 6-gram (for more clarity) of each we see: 
Original 6-gram:
bany protection, projects, and NMFS anticipates
OCR'd text 6-gram:
bank protection, prodects1, and NMFS anticipates

That both projects and products would fit the context of even the 6-gram. 
In this sense the algorithm made the human choice to pick the more common word and hope for the best.
It is doubtful a human would know which of the two to pick with just this information.

So what could we have done? Do we give up? Of course not, we could look further than the bigrams and try and see what 
the document is about in future models.
*/

-- 2) False Negative Example:
SELECT 1+(   0.000805657506042   )*(11172-1); -- 10
SELECT (325547*0.8) + 54  ; -- 260491

SELECT * FROM candidates LIMIT 260491, 8; -- Found in second row 10 unigram freq. Matched!
SELECT * FROM doctext WHERE location >= 115766 LIMIT 5; -- 5-gram OCR'd Text
SELECT * FROM doctextORIGINAL WHERE location >= 114205 LIMIT 5; -- 5-gram Original Text
/*
Here the suggested candidate of sprlng (l instead of i): Spring was found to be not the correct candidate by the 
model.

If we look at the 5-gram of each we see: 
Original 5-gram:
to enlarge Spring Creek Debris
OCR'd text 5-gram:
. enlarge Sprlng Creey Lebris

Such simple correction l->i are typically found by simple models using confusion matrix. The main reason why
we had trouble with this is due to two main factors.
First, its an edit distance of two techinically since Spring is also capitalized s->S. A major improvement we could
do to improve corrections is merge all word frequencies that match in everything but additional punctuation 
surround them and capitalization (For example, merge the Spring and Spring, candidates). This way these do not inflate
the Levenshtein Edit Distance between the candidate and error word. 
The second we had trouble with this is because, as mentioned in the Google 1T experiemnts, having words with errors
in our trigram of the word creates problems for accurately measuring bigram frequencies.A solution
to this is doing multiple passes when correcting in order to try and use our previouis corrections to correct neighboring
words by tackling the easy problems and then the harder ones.
Another solution could be using ensemble learning where a confusion matrix model would certainly have corrected this
error instance and by having different models we hope over 50% of them correct the error essentially allowing flaws in
one model to not decrease our accuracy. 

Ultimately the same issues as google 1t appearing in this version is a testatment to how machine learning is a way to 
automate corrections, but not a magic solution to it all.
*/
SELECT count(*) from candidates where output=1;
SELECT count(*) from candidates;
SELECT count(*) from candidates where output=0;
SELECT DISTINCT docsource FROM candidates;
SELECT * from candidates LIMIT 10;
SELECT * FROM confusionmatrix ORDER BY frequency DESC LIMIT 100;
SELECT * FROM confusionmatrix ORDER BY frequency DESC LIMIT 5;
SELECT * FROM confusionmatrix WHERE frequency = 594;

SELECT * FROM candidates
WHERE
    confusionweight = 918
        AND unigramfrequency = 215
        AND backwardbigramfreq = 16
        AND forwardbigramfreq = 1
        AND output = 1;

SELECT * FROM candidates LIMIT 121,1;
SELECT count(*) FROM candidates WHERE output = 1; -- 14,864
SELECT count(*) FROM candidates WHERE output = 0; -- 310,683
SELECT count(*) FROM candidates; -- 325,547
SELECT count(*) FROM candidates WHERE output != 1 and output != 0;  -- 0

;
/*
*/
;

/*
TABLE doctextSolutions
	word		VARCHAR(30),
	wordOR		VARCHAR(30),
	location	INT,
	locationOR	INT,
	docsource	VARCHAR(30),
	PRIMARY KEY(location)
*/

/*
DROP TABLE IF EXISTS candidates;
CREATE TABLE candidates (
    location			INT,
	fromword			VARCHAR(30),
    toword				VARCHAR(30),
    distance			INT,
    confusionweight		INT,
	unigramfrequency	INT,
    backwardbigramfreq	INT,
	forwardbigramfreq	INT,
    output				INT,		
    decision			DOUBLE,     
    docsource			VARCHAR(30),
	PRIMARY KEY (location, fromword, toword),
    INDEX candidatewordsF (fromword, toword), 
    INDEX candidatewordsT (toword, fromword)
);
*/




