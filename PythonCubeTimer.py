from time import sleep, perf_counter
import datetime
from collections import OrderedDict
import csv, os

#Clears the console
clear = lambda: os.system("cls")

#The inspection time in seconds
#Change it to whatever suits you
inspectionTime = 15

#The time keys
#Change it to whatever suits you
timeKeys = [35, 30, 25, 24, 23, 22, 21, 20]

#Writes the passed value to the times file
def writeTime(time):
	with open("times.csv", "a", newline="") as times:
		writer = csv.writer(times)
		writer.writerow([time, "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())])
		
#Reads the times file and returns the times as a list
def readTimes():
	times, timestamps = [], []
	with open("times.csv", newline = "") as saveFile:
		reader = csv.reader(saveFile, delimiter=",")
		for row in reader:
			times.append(row[0])
			timestamps.append(row[1])

	times = [float(time) for time in times]
	return times, timestamps

#Starts the timer and waits for an interrupt
def runTimer():
	print("Press enter to start timer")
	input()
	start =  perf_counter()
	print("Press enter to stop timer")
	input()
	end =  perf_counter()
	return round(end - start, 3)

#Pauses the program for the specified amount of time
def inspection(inspectionTime):
	sleep(inspectionTime)

#Calculates the statistics
def stats(times, timeKeys, timestamps):
	#Based on code by https://www.reddit.com/user/yovliporat
	#https://drive.google.com/file/d/0B7qI7oJsiTPGcjY2VlpoQi1hLVU/view
	dictonary = OrderedDict()
	latestTime, last3Times, last5Times, last12Times = times[-1], times[-3:], times[-5:], times[-12:]
	totalTime, sumLast3Times, sumLast5Times, sumLast12Times = sum(times), sum(last3Times), sum(last5Times), sum(last12Times)
	
	for value in timeKeys:
		dictonary[float(value)] = 0

	for key in dictonary.keys():
		for time in times:
			if time < key:
				dictonary[key] += 1
	
	clear()
	print("\nSolves:   " + str(len(times)))
	for key, val in dictonary.items():
		print("Sub-{}: {} [{}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))
	
	print("Ao3:      " + str(round(sumLast3Times / len(last3Times), 3)))
	print("Ao5:      " + str(round(sumLast5Times / len(last5Times), 3)))
	print("Ao12:     " + str(round(sumLast12Times / len(last12Times), 3)))
	print("Average:  " + str(round(totalTime / len(times), 3)))
	print("Best:     " + str(min(times)))
	print("Worst:    " + str(max(times)))
	print("Latest:   " + str(latestTime))

while True:
	try:
		times, timestamps = readTimes()
		stats(times, timeKeys, timestamps)
	except:
		print("No solves on record")
	
	time = runTimer()
	writeTime(time)