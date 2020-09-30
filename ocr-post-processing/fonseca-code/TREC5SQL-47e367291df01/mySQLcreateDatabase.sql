/* MySql Code To Create our TREC Database */
DROP DATABASE IF EXISTS TRECSample;
CREATE DATABASE TRECSample;
USE TRECSample;

/* Table that keeps a copy of all the text in order. Any word that is entered into a table should be recorded here */
CREATE TABLE doctext (
	word		VARCHAR(30),
	location	INT,
    locationOR 	INT,
	docsource	VARCHAR(30),
	PRIMARY KEY(location)
);

/* Dictionary of all seen words and their frequency */
CREATE TABLE onegms (
	word		VARCHAR(30),
    frequency	INT,
    PRIMARY KEY(word)
);

/* Dictionary of all seen words and their frequency PER DOCUMENT */
CREATE TABLE onegmsdocsource (
	word		VARCHAR(30),
    docsource	VARCHAR(30),
	frequency	INT,
    PRIMARY KEY(word, docsource)
);

/* Keeps track of the all 3gms, 1 entry per each along with their frequency */
CREATE TABLE threegms (
	wordone		VARCHAR(30),
    wordtwo		VARCHAR(30),
	wordthree	VARCHAR(30),
    frequency	INT,
    FOREIGN KEY(wordone) 	REFERENCES onegms (word) ON DELETE CASCADE,
    FOREIGN KEY(wordtwo) 	REFERENCES onegms (word) ON DELETE CASCADE,
    FOREIGN KEY(wordthree) 	REFERENCES onegms (word) ON DELETE CASCADE,
    PRIMARY KEY(wordone, wordtwo, wordthree),
    INDEX threegramSecondFirst 		  (wordtwo, wordthree, wordone),
    INDEX threegramSecondFirstThenOne (wordtwo, wordone, wordthree),    
    INDEX threegramThirdFirst 		  (wordthree, wordone, wordtwo)
);

/* Keeps track of the all 3gms and where they appeared */
CREATE TABLE threegmsreps (
	location	INT,
    docsource	VARCHAR(30),
	wordone		VARCHAR(30),
    wordtwo		VARCHAR(30),
	wordthree	VARCHAR(30),
    FOREIGN KEY(wordone) 	REFERENCES onegms (word) ON DELETE CASCADE,
    FOREIGN KEY(wordtwo) 	REFERENCES onegms (word) ON DELETE CASCADE,
    FOREIGN KEY(wordthree) 	REFERENCES onegms (word) ON DELETE CASCADE,  
    PRIMARY KEY (docsource, location),
    INDEX threegramLocation (docsource, location, wordone, wordtwo, wordthree),
    INDEX threegramReps (wordone, wordtwo, wordthree, docsource, location)
);

/* Keeps the Confusion Matrix */
CREATE TABLE confusionmatrix (
	fromletter			VARCHAR(4),
	toletter			VARCHAR(4),
    frequency			INT,
    PRIMARY KEY (fromletter, toletter),
    INDEX tolettercandidates (toletter, fromletter)
);

/* Creates an Entry for Every Candidate Correction Suggested */
CREATE TABLE candidates (
    location			INT,
	fromword			VARCHAR(30),
    toword				VARCHAR(30),
    distance			INT,
    confusionweight		INT,
	unigramfrequency	INT,
    backwardbigramfreq	INT,
	forwardbigramfreq	INT,
    output				INT,		/* Has 1 for the correct solution, used for testing/training the machine learning. */
    decision			DOUBLE,     /* Output of the machine learning algorithm. we then compare with decision to see if we got it right */
    docsource			VARCHAR(30),
	/* FOREIGN KEY(toword) 	REFERENCES onegms (word) ON DELETE CASCADE, */ /* maybe we meant fromword  */
	PRIMARY KEY (location, fromword, toword),
    INDEX candidatewordsF (fromword, toword), 
    INDEX candidatewordsT (toword, fromword)
);

/* Tables to Keep the Original Document (Not Degrade) for Testing Accuracy */

/* Table that keeps a copy of all the text in order. Any word that is entered into a table should be recorded here */
CREATE TABLE doctextORIGINAL (
	word		VARCHAR(30),
	location	INT,
	docsource	VARCHAR(30),
	PRIMARY KEY(location)
);

/* Dictionary of all seen words and their frequency of ORIGINAL (Not Degrade)*/
CREATE TABLE onegmsORIGINAL (
	word		VARCHAR(30),
    frequency	INT,
    PRIMARY KEY(word)
);

/* Dictionary of all seen words and their frequency of ORIGINAL PER DOCUMENT (Not Degrade) */
CREATE TABLE onegmsdocsourceORIGINAL (
	word		VARCHAR(30),
    docsource	VARCHAR(30),
	frequency	INT,
    PRIMARY KEY(word, docsource)
);

/* Keeps track of the all 3gms, 1 entry per each along with their frequency in ORIGINAL (Not Degrade) */
CREATE TABLE threegmsORIGINAL (
	wordone		VARCHAR(30),
    wordtwo		VARCHAR(30),
	wordthree	VARCHAR(30),
    frequency	INT,
    FOREIGN KEY(wordone) 	REFERENCES onegmsORIGINAL (word) ON DELETE CASCADE,
    FOREIGN KEY(wordtwo) 	REFERENCES onegmsORIGINAL (word) ON DELETE CASCADE,
    FOREIGN KEY(wordthree) 	REFERENCES onegmsORIGINAL (word) ON DELETE CASCADE,
    PRIMARY KEY(wordone, wordtwo, wordthree),
    INDEX threegramSecondFirst 		  (wordtwo, wordthree, wordone),
    INDEX threegramSecondFirstThenOne (wordtwo, wordone, wordthree),    
    INDEX threegramThirdFirst 		  (wordthree, wordone, wordtwo)
);

/* Keeps track of the all 3gms and where they appeared in ORIGINAL (Not Degrade) */
CREATE TABLE threegmsrepsORIGINAL (
	location	INT,
    docsource	VARCHAR(30),
	wordone		VARCHAR(30),
    wordtwo		VARCHAR(30),
	wordthree	VARCHAR(30),
    FOREIGN KEY(wordone) 	REFERENCES onegmsORIGINAL (word) ON DELETE CASCADE,
    FOREIGN KEY(wordtwo) 	REFERENCES onegmsORIGINAL (word) ON DELETE CASCADE,
    FOREIGN KEY(wordthree) 	REFERENCES onegmsORIGINAL (word) ON DELETE CASCADE,  
    PRIMARY KEY (docsource, location),
    INDEX threegramLocation (docsource, location, wordone, wordtwo, wordthree),
    INDEX threegramReps (wordone, wordtwo, wordthree, docsource, location)
);

INSERT INTO onegms VALUES ("", 1); /* Empty Value to avoid issues inserting 3gms that are not  complete */
INSERT INTO onegmsORIGINAL VALUES ("", 1); /* Empty Value to avoid issues inserting 3gms that are not  complete */

/* Table Containing all doctext locations that contain an error for easy access */
CREATE TABLE docErrorList (
	word		VARCHAR(30),
	location	INT,
    docsource	VARCHAR(30),
    PRIMARY KEY(location)
);

/* Table to keep incorrect word and correct word from original after aligned (useful for testing candidates against ground truth)*/
CREATE TABLE doctextSolutions (
	word		VARCHAR(30),
	wordOR		VARCHAR(30),
	location	INT,
	locationOR	INT,
	docsource	VARCHAR(30),
	PRIMARY KEY(location)
);

/* Table to keep frequency of edit distance between word and wordOR in doctextSolutions, mostly for statistical purposes */
CREATE TABLE levenshteinFrequency (
	distance 	INT,
    frequency 	INT,
	PRIMARY KEY(distance)
);

/* Table Containing all matching failures so we can manually fix them or ignore them */
CREATE TABLE matchfailList (
	word		VARCHAR(30),
	location	INT,
    docsource	VARCHAR(30),
    PRIMARY KEY(location)
);

/* End */

CREATE TABLE test (
	num 	INT,
    str 	VARCHAR(30),
    PRIMARY KEY (num)
);

INSERT INTO test (num, str) VALUES
(1, "test1"),
(2, "test2"),
(3, "test1");

/* Query to see Database size */
/*
SELECT table_schema AS DatabaseName, ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS Size_in_MB
FROM information_schema.tables WHERE table_schema = "TRECSample" GROUP BY table_schema;
*/

/*END*/

/* Create SQL User */
/* Must do this as root user:
CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'pythonuser'@'localhost';
FLUSH PRIVILEGES;
*/
