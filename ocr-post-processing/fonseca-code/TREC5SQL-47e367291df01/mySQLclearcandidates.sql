/* This Script will Clear Candidates Table */
USE TRECSample;

CREATE TABLE temp LIKE candidates;
ALTER TABLE candidates RENAME todelete;
ALTER TABLE temp RENAME candidates;
DROP TABLE todelete;
SELECT * FROM candidates LIMIT 30;
