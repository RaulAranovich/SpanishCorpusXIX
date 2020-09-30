/* This script will create the necessary credentials so that python can connect to the Database 
	if you know MySQL you can modify the privileges, otherwise leave as is.
*/

/* Create SQL User */
CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON * . * TO 'pythonuser'@'localhost';
FLUSH PRIVILEGES;
