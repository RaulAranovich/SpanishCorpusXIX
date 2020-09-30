#Jorge Fonseca
#Support Vector Machine using LIBSVM-3.23
#Please See: https://www.csie.ntu.edu.tw/~cjlin/libsvm/ for details on how to use
#Classification using 5 Features To Predict if candidate is accepted or not
#Note: To Run Please have both the data file and this .py file in the python directory that
#      is inside the libsvm-3.23 folder. Run as: python trec5svm.py

import time #for timing code
from svmutil import *

Tstart = time.time()
####### Read data into python ########

# This opens a handle to data file, in 'r' read mode
#Different Versions Used (Uncomment Only 1 at a time)
#file = open('test_regression_matrix.txt', 'rU')                   #For testing with small data set
#file = open('regression_matrix.txt', 'rU')                        #Regular Version of DataSet from MySQL query
#file = open('ModifiedDataSets/std_regression_matrix.txt', 'rU')   #Version with Standardized DataSet
file = open('ModifiedDataSets/norm_regression_matrix.txt', 'rU')   #Version with Normalized DataSet

#using a line feed \n and instead are using \r  (I found this out the hard way.)

lines_list = file.readlines() #Read each line into a list (strings)
matrix = []
for line in lines_list: #for each line in the list
        row = []
        for val in line.split(','): #split them into individual numbers and add them to sublist
            #var = int(val)  #use for Regular DataSet
            var = float(val)  #Use for normalized/standarized DataSet
            row.append(var)
        matrix.append(row)
file.close() #close file
#print(matrix) #prints matrix out 
matrix_rows = len(matrix) #see how many rows we have 
matrix_cols = len(matrix[0]) #see how many columns are by looking at first row

####### Split Data ########
#now that we read the data let's split it into separate list by feature
distance     = [row[0] for row in matrix]
confWeight   = [row[1] for row in matrix]
uniFreq      = [row[2] for row in matrix]
bkwdFreq     = [row[3] for row in matrix]
fwdFreq      = [row[4] for row in matrix]
output       = [row[5] for row in matrix]

#put features in one 150x5 matrix  (150 is the number of data instances)
x = []
for row in matrix:
    r = []
    r.append(row[0])  #distance
    r.append(row[1])  #confWeight
    r.append(row[2])  #uniFreq
    r.append(row[3])  #bkwdFreq
    r.append(row[4])  #fwdFreq 
    x.append(r)

TotalInstances = matrix_rows #150
TrainingInstances = int(matrix_rows*.8) #120  # 80% Train, 20% Test
#TrainingInstances = int(matrix_rows*1.0) #120 # Used for Training with full data set (EXP4, EXP5 and EXP11) (in pair with 72)
TestingInstances  = int(matrix_rows - TrainingInstances) #30

####### Train Model ########
#From Readme File:
prob  = svm_problem(output[0:TrainingInstances], x[0:TrainingInstances]) #first 120 instances

param = svm_parameter('-s 0 -c 10 -t 1 -g 1 -r 1 -d 3') #Classify a binary data with polynomial kernel (u'v+1)^3 and C = 10 
#param = svm_parameter('-s 0 -t 0 -h 0') #Linear binary classification C-SVC SVM"
model = svm_train(prob, param)

#p_label, p_acc, p_val = svm_predict(output[0:150], x[0:150], model)
#TrainingInstances = 0 #Uncomment this line to test only Training Accuracy (in pair with line 59/60 switch)
p_label, p_acc, p_val = svm_predict(output[TrainingInstances:TotalInstances], 
                                                x[TrainingInstances:TotalInstances], model) #Test Accuracy

##########Begin Metrics##########
print("\nMetrics:")

#Total Instances:
m_total = TotalInstances - TrainingInstances
print("Total Instances: "+ str(m_total))

#True Positive  (Output:1 | Predicted: 1)
m_tp = 0
for i in range(m_total):
    if output[i+TrainingInstances] == 1 and p_label[i] == 1:
        m_tp += 1
print("True Positive:   "+str(m_tp))

#False Positive (Output:0 | Predicted: 1)
m_fp = 0
for i in range(m_total):
    if output[i+TrainingInstances] == 0 and p_label[i] == 1:
        m_fp += 1
print("False Positive:  "+str(m_fp))

#False Negative (Output:1 | Predicted: 0)
m_fn = 0
for i in range(m_total):
    if output[i+TrainingInstances] == 1 and p_label[i] == 0:
        m_fn += 1
print("False Negative:  "+str(m_fn))

#True Negative  (Output:0 | Predicted: 0)
m_tn = 0
for i in range(m_total):
    if output[i+TrainingInstances] == 0 and p_label[i] == 0:
        m_tn += 1
print("True Negative:   "+str(m_tn))

#Confusion Matrix
#TP FP
#FN TN
print("\nConfusion Matrix:")
print("__________________")
print("| "+str(m_tp)+" \t| "+str(m_fp)+" \t |")
print("|_______|________|")
print("| "+str(m_fn)+" \t| "+str(m_tn)+" \t |")
print("|_______|________|")

#Precision
m_prec = 0
if m_tp != 0: #Avoid Division by Zero
    m_prec = m_tp / ( m_tp + m_fp )
print("\nPrecision: "+str(m_prec*100)+"%")

#Recall
m_rec = 0
if m_tp != 0: #Avoid Division by Zero
    m_rec = m_tp / ( m_tp + m_fn )
print("Recall:    "+str(m_rec*100)+"%")

#Accuracy
m_acc = 0
if m_total !=0: #Avoid Division by Zero
    m_acc = ( m_tp + m_tn ) / m_total
print("Accuracy:  "+str(m_acc*100)+"%")

#F-Score
m_fs = 0
m_denominator  = 2*m_tp + m_fp + m_fn
if m_denominator != 0: #Avoids Division by Zero
    m_fs = 2*m_tp / m_denominator
print("F-Score:   "+str(m_fs)+"\n")

print("End Metrics")
##########End Metrics##########

print("\nWriting Output/Predicted Classes to svmoutput.txt")
fout = open("svmoutput.txt", "w")
fout.write("Output \t Predicted\n")
for i in range(len(p_label)):
    fout.write(str(output[i+TrainingInstances])+" \t "+str(p_label[i])+"\n")
fout.close()

print("\np_label:")
print(p_label)
print("\np_acc:")
print(p_acc)
print("\np_val:")
print(p_val)
print("\nAll Done.\n")

svm_save_model('libsvm.model', model)
#model = svm_load_model('libsvm.model')

Tend = time.time()
print("Time:",Tend - Tstart, "seconds")



####SAMPLE OUTPUT:#####
'''
optimization finished, #iter = 26043700
nu = 0.044441
obj = -1033776563990009085952.000000, rho = -1896287955440235.250000
nSV = 11840, nBSV = 11439
Total nSV = 11840
Accuracy = 93.6231% (60958/65110) (classification)

Metrics:
Total Instances: 65110
True Positive:   494
False Positive:  85
False Negative:  4067
True Negative:   60464

Confusion Matrix:
__________________
| 494 	| 85 	 |
|_______|________|
| 4067 	| 60464  |
|_______|________|

Precision: 85.31951640759931%
Recall:    10.830958123218593%
Accuracy:  93.62309937029643%
F-Score:   0.19221789883268484

End Metrics

Writing Output/Predicted Classes to svmoutput.txt

All Done.

Time: 18892.750891447067 seconds
'''
####END OF OUTPUT #######
