#Jorge Fonseca
#Program will Normalize the data set using y = (x - min) / (max - min)  (MINMAX)

#Imports:
import time #for timing code

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

print("Beginning Normalization of Data Set")

###########################STARTING Normalize Data ######################################
#Next I will normalize our dataset.
#To do this I will take each input variable and compute the minimum and maximum value of each feature

#If I wanted to backup the original dataset I could make a deepcopy of it
#It's commented out since I don't really need it.
#import copy #Needed for deep copy library#
#original_matrix = copy.deepcopy(matrix) #deep copy of dataset#

#I will make a list that stores all of the min and max for each column
col_mins = []
col_maxs = []
for col in range(matrix_cols):
    cmin = matrix[0][col] #initalize to first value
    cmax = matrix[0][col] #initialize to first value
    for row in range(matrix_rows):
        if matrix[row][col] < cmin:        #Deal with Min First
            cmin = matrix[row][col]
        if matrix[row][col] > cmax:        #Deal with Max First
            cmax = matrix[row][col]
    col_mins.append(cmin)
    col_maxs.append(cmax)
print("Mins: "+str(col_mins)+"\nMaxs: "+str(col_maxs))

#For each instance Xi in the dataset Xij = (Xij - min) / (max - min) where max and min are the column's max and min.
for i in range(0,matrix_cols-1): #Don't Standarize the last column (output)!!!!!!!!!!!!!!
    maxmin = col_maxs[i] - col_mins[i]
    for j in range(matrix_rows):
        if maxmin == 0: #If max - min = 0 then all values are equal. So useless feature
            #Let's think for a second, if all values are same then matrix[j][i] - mean will be 0 too. so this is 0/0
            #So at this point let's just make it worth to 0 or 1 so it doesn't mess with ML algo
            matrix[j][i] = 1 #I think 1 is better than 0 so multiplications don't get wonky. W will end up being 0 anyway.
        else:
            matrix[j][i] = (matrix[j][i] - col_mins[i]) / (col_maxs[i] - col_mins[i])

#For Reference
#print(matrix[0][1]) #Prints Second Column of First Row 
#print(matrix[1][1]) #Prints Second Column of Second Row
#print(matrix[2][1]) #Prints Second Column of Third Row

#for x in matrix:
#    print(x[1], end = ", ")  #Prints Comma Separated instead of new lines
#print("\n")

#for x in matrix:
#    print(x)

##########################COMPLETED Normalize Data ######################################

#Let's make our new matrix file with the updated standarized values
fout2 = open("norm_regression_matrix.txt", "w") #Overwrite Mode
for i in range(matrix_rows):
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

print("\n"+str(matrix_rows)+" Rows Affected")
print("\nNormalization Complete.\n")

Tend = time.time()
print("Time:",Tend - Tstart, "seconds")
#END
