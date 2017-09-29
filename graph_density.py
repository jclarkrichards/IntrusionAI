import numpy as np
import matplotlib.pyplot as plt
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Input text file")
ap.add_argument("-t", "--time", required=False, help="Bin size in units of minutes")
args = vars(ap.parse_args())
try:
    binsize = int(args["time"])
except TypeError:
    binsize = 10 #default to 10 minutes
print binsize
binsize = binsize * 60 #convert to seconds

data = open(args["file"], "r").read()
data_lines = data.split("\n")
dt = 0
times = []
for i in range(1, len(data_lines)):
    if len(data_lines[i]) > 0:
        #print len(data_lines[i])
        month = data_lines[i][:3].lower()
        day = int(data_lines[i][4:6])
        hour = int(data_lines[i][7:9])
        minute = int(data_lines[i][10:12])
        second = int(data_lines[i][13:15])
        monthDict = {"jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6,
                     "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12}
        month = monthDict[month]
        seconds = second + 60 * (minute + 60 * (hour + 24 * (day + 30 * month)))
        times.append(seconds)

#Normalize the times such that the first one is 0
times = np.array(times) - times[0]

bins = []
num = 0
for i in range(len(times)):
    if times[i] <= binsize:
        num += 1
    else:
        bins.append(num)
        num = 1
        times -= times[i]

print bins
print "Start Time"
print data_lines[1][:16]
print "End Time"
print data_lines[-2][:16]
plt.plot(bins)
plt.xlabel("Time per unit = " + str(binsize/60) + " minutes")
plt.ylabel("Number of Entries")
plt.title("Number of Log Entries per unit of Time")
plt.show()
    
