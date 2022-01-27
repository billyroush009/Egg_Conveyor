import csv
import json

import time

# global static vars, not enforced
case = 360 # eggs
conveyor_speed_min = 10 # inches per minute
conveyor_speed_max = 100 # inches per minute
run_time = 0 # total run time, seconds
current_row_running = 0
debug = 0
counter_high = 0
counter_low = 0

#function that reads 'Example_Data.csv' into a dictionary (key = 'inch', value = list of 'counter's)
def read_csv(csv_filepath):
    #file = open('Example_Data.csv') #declaring file to open, static example
    file = open(csv_filepath)
    csvreader = csv.reader(file) #declaring csv reader with example file

    header = [] #initializing header list
    header = next(csvreader) # first row, column headers, *also pops first row out of reader*
    #print(header) #Test output

    csv_dict = {} #dictionary to hold ALL row csv_dict
    rows = [] #initializing array of .csv list

    #filling 'rows' list with each row of data
    for row in csvreader:
        rows.append(row)
    
    for row in rows:
        result = [] #list to hold data for a single row
        
        #for loop to modify each rows data then add into 'csv_dict', starting at index 1 so 'result' ignores primary key at index 0
        for x in range(1,len(row)):
            #building list of read row result, 'counters'
            result.append(row[x])

            #if last element in row has been appended
            if x == (len(row)-1):
                csv_dict[int(row[0])] = result #populating 'csv_dict' dictionary with each 'result' (key = 'inches', value = list of 'counter#' values)
                
    return csv_dict
#END read_csv

#function to quickly calculate and return the sum of a single row from the .csv dict
def sum_row(result):
    sum = 0 #temporary variable to hold row's sum
    
    #reading and adding each 'counter' value to the rows 'sum'
    for x in range(len(result)):
        sum += int(result[x])

    #print(sum)
    return sum
#END sum_row

#function to do one "scan", iterating through the .csv data at the current "speed" for 10 seconds
def scan(csv_dict, results, current_speed, current_row):
    #print(csv_dict)
    #print(current_speed)
    global current_row_running
    current_row_running += current_speed
    sum_scan = 0

    if(debug > 0):
        print('SCAN: %d' %(results['scan_count']))

    for x in range(current_row, (current_row + current_speed)):
        #print('Row %d : %d' % (x, sum_row(csv_dict[x])))
        sum_scan += sum_row(csv_dict[x])
        
    results['scan_count'] += 1
    results['conveyor_speed_sum'] += current_speed
    results['egg_count_sum'] += sum_scan
    results['last_scan_throughput'] = (((sum_scan * 6)*60)/360)

    if(debug > 0):
        print('Scan Sum: %d' % (sum_scan))
        print('Total Egg Sum: %d\n' % (results['egg_count_sum']))
        print('Cases per hours: %.2f\n' % (results['last_scan_throughput'])) #one scan is 10 sec, times 6 is per min, that times 60 is per hour, divide by 360 so units are in 'cases'

    #time.sleep(1)

    #print()
    return results

#END scan

#function that increases or decreases 'conveyor_speed_current' based on what the last scans throughput-rate is compared to the target throughput-rate
def adjust_speed(last_scan_throughput, throughput_target, conveyor_speed_current):
    global counter_high, counter_low
    #speed adjustment begins after scan
    #if latest throughput-rate is less than the target, increase speed by 1; if less, decrease by 1; if same, no speed adjustment
    if(last_scan_throughput < throughput_target):
        if(debug > 0):
            print('Last Scan Throughput was below target rate(%d vs %d), speed up! (%d to %d)' % (last_scan_throughput, throughput_target, conveyor_speed_current, conveyor_speed_current+1))
        conveyor_speed_current += 1
        counter_high += 1
        return conveyor_speed_current
    elif(last_scan_throughput > throughput_target):
        if(debug > 0):
            print('Last Scan Throughput was above target rate(%d vs %d), slow down! (%d to %d)' % (last_scan_throughput, throughput_target, conveyor_speed_current, conveyor_speed_current-1))
        conveyor_speed_current -= 1
        counter_low += 1
        return conveyor_speed_current
    else:
        if(debug > 0):
            print('Last Scan rate is equal to target rate, no change...')
        return conveyor_speed_current
    pass
#END adjust_speed

def main():
    #opening config file, populating into 'config_vars' dict
    with open('config.txt') as config_file:
        config_data = config_file.read()
        config_vars = json.loads(config_data)

    global debug, current_row_running
    #global current_row_running # variable to track which row will be first in the next 'scan()', declared global for scope simplification
    debug = config_vars['debug_output']

    #print(config_vars) #TEST OUTPUT, json config file into a dictionary
    #print(config_vars['start_speed'])
    #print(conveyor_speed_max)
    print('Starting Params (in config file):')
    print('Starting Speed: %d (inches/min) | Target Rate: %d (cases/hr) | Max Rate: %d (cases/hr) | Target Time: %d (seconds) | Debug Messages: %d' % (config_vars['start_speed'], config_vars['target_rate'], config_vars['max_rate'], config_vars['target_time'], config_vars['debug_output']))

    conveyor_speed_current = config_vars['start_speed'] # initializing 'current speed' to 'starting speed' specified in config file, in inches / min
    conveyor_speed_current = int(conveyor_speed_current / 6) # converting speed to inches per 10 seconds (scan-time)

    conveyor_rate_target = config_vars['target_rate'] #target rate (cases per hour) to strive for
    #print('Target Rate: %.2f (Cases / Hour)' % (conveyor_rate_target))
    

    csv_dict = {}
    csv_dict = read_csv(config_vars['csv_file']) #holds parsed .csv data
    #print(csv_dict)

    #returns sum of first row (7)
    #sum_row_0 = sum_row(csv_dict[0])
    #print(sum_row_0)

    #initializing dictionary variable to hold running metrics
    results = {'scan_count' : 0, 'egg_count_sum' : 0, 'conveyor_speed_sum' : 0, 'last_scan_throughput' : 0}

    throughput_sum = 0

    print('\nStarting Run...')
    #START SCAN
    #'scan' until the next 'scan' would index beyond the upper limit of 'csv_dict'
    while((current_row_running + conveyor_speed_current) < (len(csv_dict))):
        #each 'scan' will update the 'results' dictionary with cumulative data
        results = scan(csv_dict, results, conveyor_speed_current, current_row_running)
        #print('Real Speed: %.2f | Target Speed: %.2f | Latest Scan Throughput: %.2f' % (conveyor_speed_current, conveyor_speed_target, results['last_scan_throughput']))
        throughput_sum += results['last_scan_throughput']
        # adjusting current speed based on throughput of last scan (speed up / down)
        conveyor_speed_current = adjust_speed(results['last_scan_throughput'], conveyor_rate_target, conveyor_speed_current)


    print('Run complete!\nResults:')
    #output 'results' dict in meaningful ways (metrics)
    print('Scans: %d (%d seconds)' % (results['scan_count'], (results['scan_count']*10)))
    #print('Sum of Speed(s): %d' % (results['conveyor_speed_sum']))
    print('Average Speed: %.2f inches per scan' % (((results['conveyor_speed_sum']) / results['scan_count'])))
    print('Total Eggs Counted: %d (%.2f Cases) ' % (results['egg_count_sum'], (results['egg_count_sum']/case)))
    print('Average Count per Scan: %.2f eggs counted per scan' % (((results['egg_count_sum']) / results['scan_count'])))
    print('Average Throughput over ALL scans: %d cases per hour (%.2f / %d)' % ((throughput_sum / results['scan_count']), throughput_sum, results['scan_count']))
    print('Scans with throughput above target: %d (%d seconds)' % (counter_high, (counter_high*10)))
    print('Scans with throughput below target: %d (%d seconds)' % (counter_low, (counter_low*10)))

    #sum = 0
    #print out each row's sum
    #for x in range(len(csv_dict)):
        #if statement to find the highest 'sum'
        #print(str(x) + ' ' + str(sum_row(csv_dict[x])))
        #sum+=sum_row(csv_dict[x])

    #printing out sum and average of ALL ROWS
    #print(sum)
    #print(sum / len(csv_dict))
    

if __name__ == '__main__':
    main()