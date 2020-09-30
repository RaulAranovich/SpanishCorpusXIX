/* This Script will Clear all Alignment Tables */
USE TRECSample;

CREATE TABLE temp LIKE doctextSolutions;
ALTER TABLE doctextSolutions RENAME todelete;
ALTER TABLE temp RENAME doctextSolutions;
DROP TABLE todelete;
SELECT * FROM doctextSolutions LIMIT 30;

CREATE TABLE temp LIKE docErrorList;
ALTER TABLE docErrorList RENAME todelete;
ALTER TABLE temp RENAME docErrorList;
DROP TABLE todelete;
SELECT * FROM docErrorList LIMIT 30;

CREATE TABLE temp LIKE matchfailList;
ALTER TABLE matchfailList RENAME todelete;
ALTER TABLE temp RENAME matchfailList;
DROP TABLE todelete;
SELECT * FROM matchfailList LIMIT 30;

/* End of Alignment Code Clearing */