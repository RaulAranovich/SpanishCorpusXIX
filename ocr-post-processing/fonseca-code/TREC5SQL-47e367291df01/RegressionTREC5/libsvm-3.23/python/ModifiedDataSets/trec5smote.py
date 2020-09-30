#Jorge Fonseca
#Program will up-sample the output 1s using SMOTE
#RUN AS: python trec5smote.py
#Needs to have in same directory as python file the normalized data set: norm_regression_matrix.txt
#Also needs a directory called SMOTE where it will place output.
#Order:
#1)read matrix:
#2)Split Training and Test Data Files
#4)SMOTE the training data and output new file.
#5)save smote and test data files.

#Imports:
import time #for timing code

#Code Start:

Tstart = time.time() #Start Timing Code
####### Read data into python ########

# This opens a handle to data file, in 'r' read mode
file = open('norm_regression_matrix.txt', 'rU') #the U is to handle mac files that are not 

lines_list = file.readlines() #Read each line into a list (strings)
matrix = []
for line in lines_list: #for each line in the list
        row = []
        for val in line.split(','): #split them into individual numbers and add them to sublist
            var = float(val)
            row.append(var)
        matrix.append(row)
file.close() #close file
#print(matrix) #prints matrix out 
matrix_rows = len(matrix) #see how many rows we have 
matrix_cols = len(matrix[0]) #see how many columns are by looking at first row

##########################Split and Create Training/Test Sets: 80% / 20% ##########################
print("Creating Train and Test files: regTrain and regTest.")
print("Also creating temporary file: smoteTempTrain")

testrange = int(matrix_rows*0.8)+1
trainrange = testrange-1
testsize = int(matrix_rows*0.2)
testend  = matrix_rows-1
trainsize = testrange

print("Total Size: "+str(matrix_rows))
print("Train Size: "+str(trainsize))
print("Test  Size: "+str(testsize))
print("Train Range: 0-"+str(trainrange))
print("Test  Range: "+str(testrange)+"-"+str(testend))

#Let's make our test file with the last 20% of the file
fout2 = open("SMOTE/regTest_regression_matrix.txt", "w") #Overwrite Mode
for i in range(testrange, matrix_rows): #Test Count    #testrange - testend + 1 since it range doesnt include the end
    for j in range(matrix_cols):
        fout2.write(str(matrix[i][j]))
        if j < matrix_cols-1:
            if matrix[i][j] != 0 and matrix[i][j] != 1:
                fout2.write(",\t ")
            else:
                fout2.write(",\t\t\t ")
    fout2.write("\n")
fout2.close() #Close File
#Done.

#Let's make our train file with the first 80% of the file (regTrain)
#We will also make a temp file for SMOTE that we will delete later (smoteTempTrain)
fout3 = open("SMOTE/smoteTempTrain_regression_matrix.txt", "w") #Overwrite Mode
fout4 = open("SMOTE/regTrain_regression_matrix.txt", "w") #Overwrite Mode
fout3.write("distance,confWeight,uniFreq,bkwdFreq,fwdFreq,output\n")
for i in range(0, testrange): #Test Count 
    for j in range(matrix_cols):
        fout3.write(str(matrix[i][j]))
        fout4.write(str(matrix[i][j]))
        if j < matrix_cols-1:
            if matrix[i][j] != 0 and matrix[i][j] != 1:
                fout3.write(",\t ")
                fout4.write(",\t ")
            else:
                fout3.write(",\t\t\t ")
                fout4.write(",\t\t\t ")
    fout3.write("\n")
    fout4.write("\n")
fout3.close() #Close File
fout4.close() #Close File
#Done.

########################## Run SMOTE ##########################
print("\nBeginning SMOTE Process")

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

input_file = "SMOTE/smoteTempTrain_regression_matrix.txt"
data = pd.read_csv(input_file, header = 0)

#Could Normalize or drop columns with these:
#data['normconfWeight'] = StandardScaler().fit_transform(data['confWeight'].values.reshape(-1, 1))  #Normalizes a column
#data = data.drop(['fwdFreq'], axis=1) # drops a column if we wanted

print("\nSample:")
print(data.head(5))

X = np.array(data.ix[:, data.columns != 'output'])
y = np.array(data.ix[:, data.columns == 'output'])

#We could split data set here but we already did so just smote the full thing
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0, random_state=42) #same seed for consistency 

#Run Smote
sm = SMOTE(random_state=42)
X_train_smote, y_train_smote = sm.fit_sample(X_train, y_train.ravel())

newsize = sum(y_train_smote==1) + sum(y_train_smote==0)

print("\nClass Distribution Before SMOTE:")
print("0: "+str(sum(y_train==0)[0])+"\n1: "+str(sum(y_train==1)[0]))  #the [0] is because it was a list

print("\nClass Distribution After SMOTE:")
print("0: "+str(sum(y_train_smote==0))+"\n1: "+str(sum(y_train_smote==1)))

print("\nNew Size: "+str(newsize))

print("\nSMOTE Complete.\n")
########################## SMOTE Complete ##########################

#Delete Temporary File
import os
os.remove("SMOTE/smoteTempTrain_regression_matrix.txt")
print("Removed Temporary File: smoteTempTrain")

########################## Create our SMOTE train file ##########################

#Let's make our new matrix file with the new SMOTE values
fout5 = open("SMOTE/smoteTrain_regression_matrix.txt", "w") #Overwrite Mode
for i in range(0, newsize):
    for entry in X_train_smote[i]:
        fout5.write(str(entry))
        if entry != 0 and entry != 1:
            fout5.write(",\t ")
        else:
            fout5.write(",\t\t\t ")
    fout5.write(str(y_train_smote[i])+"\n")
fout5.close() #Close File
#Done.

print("\nFinished Writing smoteTrain.\nAll Done.\n")

Tend = time.time()
print("Time: "+str(Tend - Tstart)+" seconds")
#END
