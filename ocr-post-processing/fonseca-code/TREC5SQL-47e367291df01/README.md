# TREC-5 SQL Database and Linear Regression Example

The following project will take the TREC-5 Database original and degrade files and Insert them into a MySQL Database. It will then align both files to create a ground truth that can be used for reference and testing. Next it will generate a confusion matrix from that alignment and then a candidate list for OCR Errors then using linear regression will try and fix errors and then compare to ground truth acquired from alignment.

## Getting Started

The project runs using mysql and python 2.7 so you will need to have both installed. MySQL Workbench is also recommended but not necessary. This project was done in an Ubuntu 16.04 LTS Virtual Machine. It has also been tested in Ubuntu 18.04 LTS running in a Virtual Machine and Natively.

### Prerequisites
-MySQL
-Python 2.7.12

The following Python Libraries/Imports are used throughout the program:
```
import sys
import mysql.connector as mc
import Levenshtein
import difflib
import time
```

In order to import successfully install the dependencies as follows:

MySQL Python Connector:
```
apt install python-pip
pip install mysql-connector-python
```

Levenshtein:
```
pip install python-levenshtein
```

Difflib: 
```
apt-get install npm
npm install difflib
```

To install mysql:
```
apt install mysql-workbench
apt-get install mysql-server
sudo mysql_secure_installation
```

To install python (should already be installed in ubuntu):

```
apt install python2.7
```


### Running the Project
Next to begin setting up the project, open up Workbench or a mysql terminal and execute the contained sql code:
```
mysqlcreatePythonuser
mysqlcreateDatabase
```
It will generate the database for you and create the appropriate credentials for python to work with the database.

Once you have cloned the repository, installed the necessary dependencies/software, and created the Database try running the following python program. If it runs successfully all dependencies have been installed correctly:
'''
python dependencyTester.py
''' 

Then to populate the database and run the experiment use the runScript on an individual pair of TREC-5 files:
```
./runScript.sh SourceTexts/original.FR940104.0 SourceTexts/degrade.FR940104.0 > output/runScript_output.txt
```
Each pair of TREC-5 Files has 100 documents. The above has over 155,000 words.

* All output text files are in the output folder.
* If you need to delete and remake the database merely run the mySQLcreateDatabase script again.
* If you need to only re-do the alignment part with the trec5alignment.py , run the mySQLclearalignment script.
* The confusion matrix will by default add to the existing matrix, if you need to reset it without deleting the entire database, run the mySQLcleanmatrixcandidates script.
* The output folder contains detailed output from the alignment and the confusion matrix generation. The alignment overwrites the file every time you run it. The confusion appends to the output file.
* To reset your root password in mysql run the mysqlreset script.
* Review the runScript_output.txt for any errors when you run the script.
* All the runScript does is run each individual python script with the right arguments. The code is very modular and you can manually run each step.
* mySQLqueries and mySQLqueries2 are scripts with several queries used throughout the project. They were useful for testing queries directly in mysql before adding them to python code to ensure they worked.

## TREC-5 Database
The TREC-5 database (~261mb) can be downloaded at
```
https://trec.nist.gov/data/t5_confusion.html
```
Only one set of files (the first one) is included for test purposes. Download the rest there for additional tests.

## Authors
* **Jorge Fonseca** 
* **Dr. Kazem Taghva**
