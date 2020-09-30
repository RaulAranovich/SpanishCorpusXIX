#Jorge Fonseca
#Support Vector Machine using SciKit-learn's LIBSVM
#Classification using 5 Features To Predict if candidate is accepted or not
#Note: To Run Please have both the data file and this .py file in the python directory
#      Run as: python trec5svm.py

#TO INSTALL: pip install numpy scipy scikit-learn

import time #for timing code

from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

import numpy as np
import pandas as pd

Tstart = time.time()
####### Read data into python ########
#distance, confWeight, uniFreq, bkwdFreq, fwdFreq, output

#SciKit Code Template and Style In part From: 
#https://stackoverflow.com/questions/16927964/how-to-calculate-precision-recall-and-f-score-with-libsvm-in-python
#https://stackoverflow.com/questions/11023411/how-to-import-csv-data-file-into-scikit-learn/30813195#30813195
input_file = "norm_regression_matrix.txt"
# comma delimited is the default
df = pd.read_csv(input_file, header = 0)

# for space delimited use:
# df = pd.read_csv(input_file, header = 0, delimiter = " ")

# for tab delimited use:
# df = pd.read_csv(input_file, header = 0, delimiter = "\t")

# put the original column names in a python list
original_headers = list(df.columns.values)

# remove the non-numeric columns
df = df._get_numeric_data()

# put the numeric column names in a python list
numeric_headers = list(df.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
numpy_array = df.as_matrix()
print(numpy_array)
print("\n")

# prepare dataset
#iris = load_iris()
#X = iris.data[:, :2]
X = numpy_array[:, :5]
print(X)
print("\n")
#y = iris.target
y = numpy_array[:,5]
print(y)
print("\n")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# svm classification
#clf = svm.SVC(kernel='rbf', gamma=0.7, C = 1.0).fit(X_train, y_train)
clf = svm.SVC(cache_size=8000, C = 10.0, kernel='poly', gamma=1.0, coef0 = 1, degree = 3).fit(X_train, y_train)
y_predicted = clf.predict(X_test)

# performance
print "Classification report for %s" % clf
print
print metrics.classification_report(y_test, y_predicted)
print
print "Confusion matrix"
print metrics.confusion_matrix(y_test, y_predicted)

Tend = time.time()
print("Time:",Tend - Tstart, "seconds")
