#Jorge Fonseca
#Support Vector Machine using LIBSVM-3.23
#Please See: https://www.csie.ntu.edu.tw/~cjlin/libsvm/ for details on how to use
#Classification using 5 Features To Predict if candidate is accepted or not
#Note: To Run Please have both the data file and this .py file in the python directory that
#      is inside the libsvm-3.23 folder. 
#RUN AS: python3 trec5svmSMOTE.py > ModifiedDataSets/SMOTE/svmTERMINALoutput.txt
#This version is strictly for running with the SMOTE edition of the data set and the reg version
#for comparison

import time #for timing code
from svmutil import *

Tstart = time.time()
####### Read data into python ########

#Different Versions Used (Uncomment Only 1 at a time):
file = open('ModifiedDataSets/SMOTE/regTrain_regression_matrix.txt', 'rU')   #Version with Normalized DataSet for comparison
#file = open('ModifiedDataSets/SMOTE/smoteTrain_regression_matrix.txt', 'rU')  #Version with SMOTE + Normalized

################################ Read Training Data ################################
lines_list = file.readlines() #Read each line into a list (strings)
matrixtrain = []
for line in lines_list: #for each line in the list
        row = []
        for val in line.split(','): #split them into individual numbers and add them to sublist
            #var = int(val)  #use for Regular DataSet
            var = float(val)  #Use for normalized/standarized DataSet
            row.append(var)
        matrixtrain.append(row)
file.close() #close file
matrixtrain_rows = len(matrixtrain) #see how many rows we have 
matrixtrain_cols = len(matrixtrain[0]) #see how many columns are by looking at first row

################################ Read Test Data ################################

#Test Data:
file2 = open('ModifiedDataSets/SMOTE/regTest_regression_matrix.txt', 'rU')   #Version with Normalized DataSet

lines_list2 = file2.readlines() #Read each line into a list (strings)
matrixtest = []
for line in lines_list2: #for each line in the list
        row = []
        for val in line.split(','): #split them into individual numbers and add them to sublist
            #var = int(val)  #use for Regular DataSet
            var = float(val)  #Use for normalized/standarized DataSet
            row.append(var)
        matrixtest.append(row)
file2.close() #close file
matrixtest_rows = len(matrixtest) #see how many rows we have 
matrixtest_cols = len(matrixtest[0]) #see how many columns are by looking at first row

#Store our y in a special column (train/test)
y_train      = [row[5] for row in matrixtrain]
y_test       = [row[5] for row in matrixtest]

#Store our features in x (train/test)
x_train = []
for row in matrixtrain:
    r = []
    r.append(row[0])  #distance
    r.append(row[1])  #confWeight
    r.append(row[2])  #uniFreq
    r.append(row[3])  #bkwdFreq
    r.append(row[4])  #fwdFreq 
    x_train.append(r)

x_test = []
for row in matrixtest:
    r = []
    r.append(row[0])  #distance
    r.append(row[1])  #confWeight
    r.append(row[2])  #uniFreq
    r.append(row[3])  #bkwdFreq
    r.append(row[4])  #fwdFreq 
    x_test.append(r)

#Data Instance Counts:
TotalInstances = int(matrixtest_rows + matrixtrain_rows)
TrainingInstances = int(matrixtrain_rows) #Since Test set is separate we run on all train 
TestingInstances  = int(matrixtest_rows) 

####### Train Model ########
#From Readme File:
prob  = svm_problem(y_train[0:TrainingInstances], x_train[0:TrainingInstances]) #pass dimensions

param = svm_parameter('-s 0 -c 10 -t 1 -g 1 -r 1 -d 3') #Classify a binary data with polynomial kernel (u'v+1)^3 and C = 10 
#param = svm_parameter('-s 0 -t 0 -h 0') #Linear binary classification C-SVC SVM"
model = svm_train(prob, param)

#Test on Train Dataset (Uncomment lines 92-95 and comment out lines 98-99):
#p_label, p_acc, p_val = svm_predict(y_train[0:TrainingInstances], 
#                                                x_train[0:TrainingInstances], model) #Train Accuracy
#y_test = y_train                     #So the metrics work
#TestingInstances = TrainingInstances #So the metrics work

#Test on Test Dataset
p_label, p_acc, p_val = svm_predict(y_test[0:TestingInstances], 
                                                x_test[0:TestingInstances], model) #Test Accuracy

#### Error Analysis Output Files ####
print("\nWriting Error Analysis to svmanalysis1.txt (FP/FN) and svmanalysis2.txt (TP/TN)")
fout2 = open("ModifiedDataSets/SMOTE/svmanalysis1.txt", "w")
fout3 = open("ModifiedDataSets/SMOTE/svmanalysis2.txt", "w")
fout2.write("Index \t distance \t confWeight \t uniFreq \t bkwdFreq \t fwdFreq \t Output \t Predicted\n")
fout3.write("Index \t distance \t confWeight \t uniFreq \t bkwdFreq \t fwdFreq \t Output \t Predicted\n")

##########Begin Metrics##########
print("\nMetrics:")

#Total Instances:
m_total = TestingInstances
print("Total Instances: "+ str(m_total))

#True Positive  (Output:1 | Predicted: 1)
m_tp = 0
for i in range(m_total):
    if y_test[i] == 1 and p_label[i] == 1:
        m_tp += 1
        fout3.write(str(i)+" \t"+str(x_test[i][0])+" \t"+str(x_test[i][1])
            +" \t"+str(x_test[i][2])+" \t"+str(x_test[i][3])+" \t"+str(x_test[i][4])+" \t")
        fout3.write(str(y_test[i])+" \t "+str(p_label[i])+"\n")
print("True Positive:   "+str(m_tp))
fout3.write("\n\n\n\n\n\n\n\n\n\n")

#False Positive (Output:0 | Predicted: 1)
m_fp = 0
for i in range(m_total):
    if y_test[i] == 0 and p_label[i] == 1:
        m_fp += 1
        fout2.write(str(i)+" \t"+str(x_test[i][0])+" \t"+str(x_test[i][1])
            +" \t"+str(x_test[i][2])+" \t"+str(x_test[i][3])+" \t"+str(x_test[i][4])+" \t")
        fout2.write(str(y_test[i])+" \t "+str(p_label[i])+"\n")
print("False Positive:  "+str(m_fp))
fout2.write("\n\n\n\n\n\n\n\n\n\n")

#False Negative (Output:1 | Predicted: 0)
m_fn = 0
for i in range(m_total):
    if y_test[i] == 1 and p_label[i] == 0:
        m_fn += 1
        fout2.write(str(i)+" \t"+str(x_test[i][0])+" \t"+str(x_test[i][1])
            +" \t"+str(x_test[i][2])+" \t"+str(x_test[i][3])+" \t"+str(x_test[i][4])+" \t")
        fout2.write(str(y_test[i])+" \t "+str(p_label[i])+"\n")
print("False Negative:  "+str(m_fn))

#True Negative  (Output:0 | Predicted: 0)
m_tn = 0
for i in range(m_total):
    if y_test[i] == 0 and p_label[i] == 0:
        m_tn += 1
        fout3.write(str(i)+" \t"+str(x_test[i][0])+" \t"+str(x_test[i][1])
            +" \t"+str(x_test[i][2])+" \t"+str(x_test[i][3])+" \t"+str(x_test[i][4])+" \t")
        fout3.write(str(y_test[i])+" \t "+str(p_label[i])+"\n")
print("True Negative:   "+str(m_tn))

fout2.close() #Close Error Analysis File svmanalysis1.txt
fout3.close() #Close Error Analysis File svmanalysis2.txt

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
fout = open("ModifiedDataSets/SMOTE/svmoutput.txt", "w")
fout.write("Output \t Predicted\n")
for i in range(len(p_label)):
    fout.write(str(y_test[i])+" \t "+str(p_label[i])+"\n")
fout.close()

print("\np_label:")
print(p_label)
print("\np_acc:")
print(p_acc)
print("\np_val:")
print(p_val)
print("\nAll Done.\n")

svm_save_model('ModifiedDataSets/SMOTE/libsvm.model', model)
#model = svm_load_model('ModifiedDataSets/SMOTE/libsvm.model')

Tend = time.time()
print("Time:",Tend - Tstart, "seconds")



####SAMPLE OUTPUT:#####
'''

'''
####END OF OUTPUT #######
