/* Temp File to make multiple queries that run at once for the sake of testing */
USE TRECSample;

SELECT * FROM doctextORIGINAL LIMIT 80;
SELECT * FROM doctext LIMIT 80;


SELECT * FROM doctextSolutions WHERE docsource LIKE '%99%';
SELECT * FROM doctextSolutions where location > 155280; #So max location is 155281
SELECT COUNT(*) FROM confusionmatrix;

SELECT COUNT(*) FROM doctext;

SELECT * FROM onegmsORIGINAL LIMIT 10;
SELECT COUNT(*) FROM onegmsORIGINAL;


SELECT * FROM docErrorList WHERE word= "hegister" LIMIT 10;
SELECT * FROM docErrorList WHERE word= " " LIMIT 10;

SELECT frequency FROM confusionmatrix WHERE fromletter="h" AND toletter="R";
SELECT frequency FROM confusionmatrix WHERE fromletter="" AND toletter="ed";


SELECT * FROM onegms WHERE word = "Register";

SELECT * FROM candidates WHERE docsource LIKE '%99' LIMIT 10;
SELECT * FROM candidates WHERE toword = "register" LIMIT 50;
SELECT * FROM doctext WHERE location = 9;

#Query to see Database size
SELECT table_schema AS DatabaseName, ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS Size_in_MB
FROM information_schema.tables WHERE table_schema = "TRECSample" GROUP BY table_schema;
#Suprisingly Database is only 248MB so far!











