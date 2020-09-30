USE TRECSample;

/*
Table Names:
-onegms   (word, frequency)
-onegmsdocsource (word, docsource, frequency)
-threegms (wordone, wordtwo, wordthree, frequency)
-threegmsreps (location, docsource, wordone, wordtwo, wordthree)
-candidates (fromword,	toword, confusionweight, unigramfrequency,
			 backwarsbigramfreq, forwardbigramfreq, output, decision)
-test (num, str)
*/

/* The Following is a list of queries used to test the database and the different actions */

#SELECT * FROM onegms;
SELECT * FROM test;

INSERT INTO test VALUES (4, "testX")
ON DUPLICATE KEY UPDATE str = concat(str," testX");

INSERT INTO onegms VALUES ("sampleword", 1)
ON DUPLICATE KEY UPDATE frequency = frequency+1;

SELECT * FROM onegms;
SELECT * FROM onegms LIMIT 20;
SELECT * FROM onegmsORIGINAL LIMIT 20;
SELECT * FROM doctextORIGINAL LIMIT 30;
SELECT MAX(location) FROM doctextORIGINAL;

SELECT * FROM doctext LIMIT 20;
SELECT * FROM onegmsdocsource LIMIT 20;
SELECT * FROM threegms LIMIT 20;
SELECT * FROM threegms USE INDEX (threegramThirdFirst) LIMIT 20;
SELECT * FROM threegmsrepetitions LIMIT 20;

SELECT MAX(location) FROM doctext WHERE docsource= "FR940104-0-00002";
SELECT * FROM doctext WHERE location=619; #619 is last of that document

SELECT docsource FROM doctext WHERE location=619;
SELECT MIN(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location=30);

/* This query gives 4 rows with the values we need */
SELECT MIN(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location=30)
union
SELECT MAX(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location=30)
union
SELECT MIN(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location=30)
union
SELECT MAX(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location=30);

/* This query gives 1 row with the values we need in each column, does same as above just different output*/
SELECT
(SELECT MIN(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location=30)) as dstart,
(SELECT MAX(location) FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location=30)) as dend,
(SELECT MIN(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location=30)) as ostart,
(SELECT MAX(location) FROM doctextORIGINAL WHERE docsource = (SELECT docsource FROM doctext WHERE location=30)) as oend,
(SELECT docsource FROM doctext WHERE location=30) as doc;

SELECT word, location FROM doctext WHERE docsource = (SELECT docsource FROM doctext WHERE location=30);

SELECT * FROM doctext WHERE docsource ="FR940104-0-00002" and location=45; #locationOR should update to 34
UPDATE doctext SET locationOR=34 WHERE location=45;

INSERT INTO doctextSolutions VALUES("a", "b", -1, -1, "2121");
SELECT * FROM doctextSolutions LIMIT 30;
DELETE FROM doctextSolutions WHERE location=-1;
SELECT * FROM matchfailList LIMIT 30;
SELECT * FROM docErrorList LIMIT 30;

SELECT * FROM doctext where location=137;
SELECT * FROM doctextORIGINAL where location=125;

SELECT * FROM doctext WHERE word like "%Federal%" LIMIT 30;
SELECT * FROM onegms WHERE word like"%Federal%";

DELETE FROM onegms WHERE word = "sampleword";

TRUNCATE TABLE doctextORIGINAL;  /* Delete Entire Contents of a Table */

CREATE TABLE temp LIKE onegms;
ALTER TABLE onegms RENAME todelete;
ALTER TABLE temp RENAME onegms;
DROP TABLE todelete;

SELECT * FROM matchfailList LIMIT 30; #Line 13 appears
SELECT * FROM docErrorList LIMIT 30; #Line 13 appears
SELECT * FROM docErrorList WHERE location NOT IN(SELECT location FROM matchfailList) LIMIT 30; #No Line 13 since it appears in matchfail

SELECT * FROM doctextSolutions LIMIT 30;
SELECT doctextSolutions.word, doctextSolutions.wordOR, doctextSolutions.location, 
doctextSolutions.locationOR, doctextSolutions.docsource FROM doctextSolutions, docErrorList 
WHERE doctextSolutions.location = docErrorList.location 
AND doctextSolutions.docsource = docErrorList.docsource LIMIT 30;  #Should show line 13 but not line 3

/* Gives us all errors that were aligned so we can use to build our confusion matrix, in other words it removes match fails and it also
   joins tables so we get word, wordOR, location, locationOR and docsource. */
SELECT doctextSolutions.word, doctextSolutions.wordOR, doctextSolutions.location, 
doctextSolutions.locationOR, doctextSolutions.docsource FROM doctextSolutions, docErrorList 
WHERE doctextSolutions.location = docErrorList.location 
AND doctextSolutions.docsource = docErrorList.docsource 
AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList) LIMIT 30;  #Should not show line 13 and line 3

SELECT doctextSolutions.word, doctextSolutions.wordOR, doctextSolutions.location, 
doctextSolutions.locationOR, doctextSolutions.docsource FROM doctextSolutions, docErrorList 
WHERE doctextSolutions.location = docErrorList.location 
AND doctextSolutions.docsource = docErrorList.docsource 
AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList)
AND doctextSolutions.docsource = "FR940104-0-00001";  #Should not show line 13 and line 3


SELECT doctextSolutions.location FROM doctextSolutions, docErrorList 
WHERE doctextSolutions.location = docErrorList.location 
AND doctextSolutions.docsource = docErrorList.docsource 
AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList) AND doctextSolutions.location = 
(SELECT MIN(doctextSolutions.location) FROM doctextSolutions, docErrorList 
WHERE doctextSolutions.location = docErrorList.location 
AND doctextSolutions.docsource = docErrorList.docsource 
AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList) AND doctextSolutions.location > 15801);

SELECT docsource FROM doctextSolutions WHERE location = 0;

SELECT docsource FROM doctextSolutions WHERE location = (SELECT MIN(location) FROM doctextSolutions WHERE location > 23); #22 gives doc 1

SELECT MIN(location) FROM doctextSolutions WHERE location > 23;

SELECT * FROM doctextSolutions where location=(SELECT MAX(location) FROM doctextSolutions);
SELECT * FROM doctextSolutions LIMIT 2 OFFSET 155281;

SELECT MIN(doctextSolutions.location) FROM doctextSolutions, docErrorList 
WHERE doctextSolutions.location = docErrorList.location 
AND doctextSolutions.docsource = docErrorList.docsource 
AND doctextSolutions.location NOT IN(SELECT location FROM matchfailList);  #Should not show line 13 and line 3

INSERT INTO confusionmatrix VALUES ("iii", "m", 1) ON DUPLICATE KEY UPDATE frequency = frequency + 1;
SELECT * FROM confusionmatrix ORDER BY frequency DESC LIMIT 100;
SELECT SUM(frequency) FROM confusionmatrix;
SELECT SUM(frequency) FROM (SELECT frequency FROM confusionmatrix ORDER BY frequency DESC LIMIT 10) AS matrixfreq; 
SELECT SUM(frequency) FROM (SELECT frequency FROM confusionmatrix ORDER BY frequency DESC LIMIT 22) AS matrixfreq; 



SELECT * FROM doctextSolutions WHERE location= 155280;
SELECT MAX(docErrorList.location) FROM docErrorList 
		  WHERE docErrorList.location NOT IN(SELECT location FROM matchfailList);

SELECT docsource FROM docErrorList WHERE location=1;

SELECT docErrorList.word, docErrorList.location, 
		      docErrorList.docsource FROM docErrorList 
		      WHERE docErrorList.location NOT IN(SELECT location FROM matchfailList)
		      AND docErrorList.docsource = "FR940104-0-00001";



#Unigram Frequency Query
SELECT frequency FROM onegms WHERE word = "Federal";


#Backward Bigram Frequency Query  (2-part, first we need to get the word before it, 
#then use those two words to query all reps and add all of them together and return a single value
#Example to use: Federal @ location 820
select * FROM doctextORIGINAL WHERE location = 807;

#This gets word before ours
SELECT word FROM doctext WHERE location = 820 - 1;

#This gets us all backward bigrams  (building on last query)
SELECT * FROM threegms WHERE wordtwo = "Federal" AND wordone  = (SELECT word FROM doctext WHERE location = 820 - 1);

#THis adds all the frequencies together from last query (building on last query) to give us our final query that we need
SELECT SUM(frequency) FROM threegms WHERE wordtwo = "Federal" AND wordone  = (SELECT word FROM doctext WHERE location = 820 - 1);

#Forward Bigram Frequency Query (similar to backward Bigram frequency
#Example to use: Federal @ location 820
#This gets word before ours
SELECT word FROM doctext WHERE location = 820 + 1;

#This gets us all forward bigrams  (building on last query)
SELECT * FROM threegms WHERE wordtwo = "Federal" AND wordthree  = (SELECT word FROM doctext WHERE location = 820 + 1);

#THis adds all the frequencies together from last query (building on last query) to give us our final query that we need
SELECT SUM(frequency) FROM threegms WHERE wordtwo = "Federal" AND wordthree  = (SELECT word FROM doctext WHERE location = 820 + 1);









