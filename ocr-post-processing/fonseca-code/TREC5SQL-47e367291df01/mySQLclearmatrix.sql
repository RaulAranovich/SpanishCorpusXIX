/* This Script will Clear Confusion Matrix And Levenshtein Frequency Tables */
USE TRECSample;

CREATE TABLE temp LIKE confusionmatrix;
ALTER TABLE confusionmatrix RENAME todelete;
ALTER TABLE temp RENAME confusionmatrix;
DROP TABLE todelete;
SELECT * FROM confusionmatrix LIMIT 30;

CREATE TABLE temp LIKE levenshteinFrequency;
ALTER TABLE levenshteinFrequency RENAME todelete;
ALTER TABLE temp RENAME levenshteinFrequency;
DROP TABLE todelete;
SELECT * FROM levenshteinFrequency LIMIT 30;
