# PMSI Coding Challenge

# To Run
- Confirm you have Python and Git installed
- Navigate to where you'd like to save the program in a git-friendly terminal (I used powershell)
```
git clone https://github.com/billyroush009/Egg_Conveyor.git
cd Egg_Conveyor
python main.py
```

    - Ensure you have the "config.txt" and the "Example_Data.csv" files

## Objective(s)
- Read in data from a .csv file and run a conveyor-belt simulation based on the contents
- Manipulate the 'speed' at which the belt is moving depending on the rate of eggs being counted
- Display the results and relevant metrics once the simulation ends (all rows have been read)

### Description

I decided to re-approach this problem using Python. I opted to create a "config" file instead of utilizing an external UI. 
The config file contains fields that dictate the starting speed of the belt (inches/min), desired throughput (cases/hr), maximum allowed rate (cases/hr), desired time (seconds), and 
a flag that controls how much console output is produced during the simulation (0 = off, >0 = on). The results are displayed as terminal output, which include: number of scans (10 sec intervals), average speed (inches/scan), total egg/case count, average count per scan (eggs/scan), average throughput per scan (cases/hr), count of scans where throughput was above target, and count of scans where throughput was below target. Overall the simulation runs through, reading the .csv file to the end and displaying the results tallied up along the way.

#### Program Flow
1. The "config.txt" file is read and relevant variables are set
2. The data .csv (Example_Data.csv in this case) is read in and parsed into a dictionary via the 'read_csv' function
3. A "while" loop is run until the most recent row of the .csv read + the current speed surpass the length of the .csv (scan goes passed end of data)
    1. Each loop calls the "scan" function, which calls the "sum_row" function based on the current speed, to then return aggregate sums and metrics for all the simulations "scans"
    2. The throughput of that "scan" is added to the running sum (for averaging/arithmetic once sim is complete)
    3. The current speed is set to the result of the "adjust_speed" function. For simplicity I made this function check the throughput of the last scan, if that's below the target then the speed is increased by 1, if it's above then the speed is decreased by 1, and if it matches then the speed is not adjusted.
4. The results are printed with one key-metric per line

##### Additional Notes
- I wrote and tested this using Python 3.9.6 64-bit on a desktop running Windows 10
- There is virtually no error handling built into this
- This setup uses "config.txt" to represent user input and console output to display the run/results
- I'm sure there's a better way to adjust speed than by crudely adding/subtracting one to it's value based on a last-read/target rate
- I didn't get around to adding graphic/GUI elements to this but could extrapolate the results into visual results with more time
- There are a few variables that I didn't end up using as I didn't get far enough into the speed adjustment or math filters
- "csv_read.py" was a file I used to test reading in the .csv data but plays no role in the actual simulation run