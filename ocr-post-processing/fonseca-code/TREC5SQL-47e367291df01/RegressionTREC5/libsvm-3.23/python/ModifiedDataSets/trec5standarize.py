#Jorge Fonseca
#Program will standarize the data set using Xij = (Xij - meanj) / std_devj

#Imports:
import time #for timing code

#first I get the math library to do some math computations
import math #Documentation: https://docs.python.org/2/library/math.html

#Code Start:

Tstart = time.time() #Start Timing Code
####### Read data into python ########

# This opens a handle to data file, in 'r' read mode
#file = open('test_regression_matrix.txt', 'rU') #For testing with a small subset.
file = open('regression_matrix.txt', 'rU') #the U is to handle mac files that are not 
#using a line feed \n and instead are using \r  (I found this out the hard way.)

lines_list = file.readlines() #Read each line into a list (strings)
matrix = []
for line in lines_list: #for each line in the list
        row = []
        for val in line.split(','): #split them into individual numbers and add them to sublist
            var = int(val)
            row.append(var)
        matrix.append(row)
file.close() #close file
#print(matrix) #prints matrix out 
matrix_rows = len(matrix) #see how many rows we have 
matrix_cols = len(matrix[0]) #see how many columns are by looking at first row

print("Beginning Standardization of Data Set")

###########################STARTING Standarize Data ######################################
#Next I will standarize our dataset.
#To do this I will take each input variable and compute mean and stdev

#If I wanted to backup the original dataset I could make a deepcopy of it
#It's commented out since I don't really need it.
#import copy #Needed for deep copy library#
#original_matrix = copy.deepcopy(matrix) #deep copy of dataset#

#I will make a list that stores all of the means for each column
col_means = []
for col in range(matrix_cols):
    sum = 0
    for row in range(matrix_rows):
        sum = sum + matrix[row][col]
    #print(sum)
    col_means.append(sum/matrix_rows)
#print(col_means)

#I will make a list that stores all of the standard deviations for each column
#Stddev= Sqrt[ 1/N*SUMofAllN{(Xi-mean)^2} ]
#https://www.mathsisfun.com/data/standard-deviation-formulas.html
#Note we are doing Population Standard Deviation, not Sample Standard Deviation.
col_stddev = []
#Step 1, Get the mean(we have that from col_means already)
for col in range(matrix_cols):
    #Step 2: For each number, subtract the mean, and square the result
    sum = 0
    for row in range(matrix_rows):
        step2 = matrix[row][col] - col_means[col]  #number - mean
        sum += math.pow(step2, 2) #Step 2.5 Keep a running sum of all the numbers
    #print(sum)
    #Step 3: Get the mean of all those 
    variance = sum / matrix_rows 
    #Step 4: Finally just take the square root of that and we are done
    col_stddev.append(math.sqrt(variance))
#print(col_stddev)

#Now that we have both the mean and the standard deviation we can standarize our matrix

#For each instance Xi in the dataset Xij = (Xij - MEANi) / STDDEVj
for i in range(0,matrix_cols-1): #Don't Standarize the last column (output)!!!!!!!!!!!!!!
    for j in range(matrix_rows):
        #Split it into two steps so line didn't become so wide
        if col_stddev[i] == 0: #If standard deviation is = 0 then all values are equal. So useless feature
            #Let's think for a second, if all values are same then matrix[j][i] - mean will be 0 too. so this is 0/0
            #So at this point let's just make it worth to 0 or 1 so it doesn't mess with ML algo
            matrix[j][i] = 1 #I think 1 is better than 0 so multiplications don't get wonky. W will end up being 0 anyway.
        else:
            matrix[j][i] = (matrix[j][i] - col_means[i]) / col_stddev[i]

#For Reference
#print(matrix[0][1]) #Prints Second Column of First Row 
#print(matrix[1][1]) #Prints Second Column of Second Row
#print(matrix[2][1]) #Prints Second Column of Third Row

#for x in matrix:
#    print(x[1], end = ", ")  #Prints Comma Separated instead of new lines
#print("\n")

#Quick test to see if sumation is close to 0
print("Quick Test: Should be Close to 0:")
sum = 0
for x in matrix:
    sum += x[1]
print(sum) #-6.661338147750939e-16 (good thing as it's very close to 0, so standardization worked)
#exit() #For testing

#for x in matrix:
#    print(x)

##########################COMPLETED Standarize Data ######################################

#Let's make our new matrix file with the updated standarized values
fout2 = open("std_regression_matrix.txt", "w") #Overwrite Mode
for i in range(matrix_rows):
    for j in range(matrix_cols):
        fout2.write(str(matrix[i][j]))
        if j < matrix_cols-1:
            fout2.write(",\t ")
    fout2.write("\n")
fout2.close() #Close File
#Done.

print("\n"+str(matrix_rows)+" Rows Affected")
print("\nStandardization Complete.\n")

Tend = time.time()
print("Time:",Tend - Tstart, "seconds")
#END
