import csv
import numpy as np
import time

file = open('Example_Data.csv') #declaring file to open

csvreader = csv.reader(file) #declaring csv reader with example file

header = [] #initializing header list
header = next(csvreader) # first row, column headers, also pops first row out of reader

#print(header) #Test output

rows = [] #initializing array of .csv list

#filling 'rows' list with each row of data
for row in csvreader:
    rows.append(row)

#print(rows)
#print('Rows: ' + str(len(rows)))
#print(rows[100])
#print('Inch: ' + str(rows[100][0]) + ', Counter1: ' + str(rows[100][1]))

#result = []
results = {}
counter = 0

for row in rows:
    result = []
    
    #for loop to modify each rows data then add into 'results'
    for x in range(1,len(row)):
        #building list of read row result, 'counters'
        result.append(row[x])

        #if last element in row has been appended
        if x == (len(row)-1):
            results[int(row[0])] = result #populating 'results' dictionary with each 'result' (key = 'inches', value = list of 'counter#')


#print(result)
#print(results)
#print(results[0])
#print(results[1800])

for result in results:
    sum = 0
    #print(results[result])

    #print(len(results[result]))

    for x in range(0, len(results[result])):
        sum += int(results[result][x])
       #break
    print(sum)
