# Using the Google Web 1T 5-Gram Data Set for OCR Error Correction

The following project will take the Google Web 1T 1-Gram and 5-Gram Data set and use the context to suggest and auto-correct OCR generated errors.

## Getting Started

The project runs using bash and python 2.7 so you will need to have both installed. The Google Web 1T Data Set is not provided due to copyright, but is required. This project was done in an Ubuntu 16.04 LTS Virtual Machine. It has also been tested in Ubuntu 18.04 LTS running in a Virtual Machine and Natively.

### Prerequisites
-Google Web 1T 1-Gram and 5-Gram Data Set
-Python 2.7.12

The following Python Libraries/Imports are used throughout the program:
```
import Levenshtein
```

In order to import successfully install the dependencies as follows:

Levenshtein:
```
pip install python-levenshtein
pip install editdistance
```

To install python (should already be installed in ubuntu):

```
apt install python2.7
```


### Running the Project
Type chmod +x runScript before running!

Each File in TREC-5 FILE is saved in 3 versions:
original, degrade5 and degrade20 (we will be using original and degrade5). They decide the kind of scan quality (20 is less quality)
They are then divided into different numbered folders 01-12
Inside of those folders are each file FR940104.0-FR940104.2 and then FR940105.0 to .2 and so on.
Each of those is compressed in a .gz format

Inside of these files which for this case we take the first one "FR940104.0" original and degrade5 and in them are the separate documents separated by
the example tag: <DOCNO> FR940104-0-00002 </DOCNO>
Which means within the FR940104-0 file each documment has a number after: FR940104-0-00002  (meaning the second document in this file)
Each file contains 99 documents

We can now take each of those documents and compare the OCR'd degrade5 version with the original. We take the most amount of documents we can while 
keeping the word count to about 1200 words.

In order to keep things organized we will use lowercase for the original and upercase for the OCR'd one.
(Update, to avoid issues with windows and dropbox and git, we will change this to add degrade5.  and correct. infront of names:
ie: degrade.FR940104.0 and correct.FR940104.0 )


The code is written in modules that perform separate task and is then all runned in order by the master script which we call runScript.
The code for each module is in its own numbered folder indicating the order that it is run. Inside of that folder is the code and a folder that stores
temporary files or output files that the master script can copy into other modules. That folder is called WorkFolder.

Now follow each step with explanation:

STEP0: First runScript (master script) will select the filename, locate it in TREC-5 and uncompress it saving the uncompressed copy to SourceTexts under:
degrade.FR940104.0 and correct.FR940104.0


Step 1: Split the file into manageable chunks of about 1500 words each, cut at the end of the closest DOCUMENT to not split pages.
Separates the Files into sizeable chunks by splitting at the end of the nearest document under 1500 words.

```
sudo time ./run-script TRECSample/TREC-5/ GoogleWeb1T/Google1T-3gms/3gms/3gm.idx |& tee GoogleWeb1TOUTPUT.txt

sudo time python tools/Google1T/verify/verifyCandidates.py  |& tee verifyCandidates_output.txt

1gmSpell.py degrade.FR940104-0-00001.000 GoogleWeb1T/Google1T-3gms/1gms/vocab

for permission:
sudo chown -R $USER output/source-docs
sudo chown -R $USER output/logs
sudo chmod -R a+rX *
sudo chown -R $USER output/Google1T


```

can use grep -i "degrade" refine.log
to see where it is in process.

can use tail candidates.log to see where it is as for findcandidates


## TREC-5 Database
The TREC-5 database (~261mb) can be downloaded at
```
https://trec.nist.gov/data/t5_confusion.html
```
Only one set of files (the first one) is included for test purposes. Download the rest there for additional tests.

#Google Web 1T 1-Gram and 5-Gram Data Set
Google Web 1T 1-Gram and 5-Gram Data Set can be downloaded at
```
https://catalog.ldc.upenn.edu/LDC2006T13
```


## Authors
* **Jorge Fonseca** 
* **Dr. Kazem Taghva**
