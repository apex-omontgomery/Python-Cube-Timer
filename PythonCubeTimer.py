from time import sleep, perf_counter
import datetime
from collections import OrderedDict
from math import ceil, floor
import csv, os

#Clears the console
clear = lambda: os.system("cls" if os.name == "nt" else "clear")

#The inspection time in seconds
#Change it to whatever suits you
#inspectionTime = 15

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
#def inspection(inspectionTime):
#	sleep(inspectionTime)

#Calculates the statistics
def stats(times, timeKeys, timestamps):
	#Based on code by https://www.reddit.com/user/yovliporat
	#https://drive.google.com/file/d/0B7qI7oJsiTPGcjY2VlpoQi1hLVU/view
	dictonary = OrderedDict()
	latestTime, last3Times, last5Times, last12Times, last50Times, last100Times = times[-1], times[-3:], times[-5:], times[-12:], times[-50:], times[-100:]
	last12Times.pop(last12Times.index(max(last12Times)))
	last12Times.pop(last12Times.index(min(last12Times)))
	totalTime, sumLast3Times, sumLast5Times, sumLast12Times, sumLast50Times, sumLast100Times = sum(times), sum(last3Times), sum(last5Times), sum(last12Times), sum(last50Times), sum(last100Times)
	sortedTimes = times
	sortedTimes.sort()
	
	for value in timeKeys:
		dictonary[float(value)] = 0

	for key in dictonary.keys():
		for time in times:
			if time < key:
				dictonary[key] += 1
	
	
	if len(times) % 2 == 0:
		mean = sortedTimes[ceil(len(sortedTimes) / 2)]
	else:
		mean = sortedTimes[floor(len(sortedTimes) / 2)] + sortedTimes[ceil(len(sortedTimes) / 2)] / 2
	
	clear()
	print("\nSolves:   " + str(len(times)))
	for key, val in dictonary.items():
		print("Sub-{}: {} [{}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))
	
	print("Ao3:      " + str(round(sumLast3Times / len(last3Times), 3)))
	print("Ao5:      " + str(round(sumLast5Times / len(last5Times), 3)))
	print("Ao12:     " + str(round(sumLast12Times / len(last12Times), 3)))
	print("Ao50:     " + str(round(sumLast50Times / len(last50Times), 3)))
	print("Ao100:    " + str(round(sumLast100Times / len(last100Times), 3)))
	print("Average:  " + str(round(totalTime / len(times), 3)))
	print("Mean:     " + str(mean))
	print("Best:     " + str(min(times)))
	print("Worst:    " + str(max(times)))
	print("Latest:   " + str(latestTime))

while True:
	try:
		times, timestamps = readTimes()
	except FileNotFoundError:
		print("Error, file \"times.csv\n not found.")
	except Exception as e:
		print("Error: " + str(e))
		
	try:
		stats(times, timeKeys, timestamps)
	except IndexError:
		print("Error, no recorded solves.")
	except Exception as e:
		print("Error: " + str(e))
	
	try:
		time = runTimer()
	except Exception as e:
		print("Error: " + str(e))
	
	try:
		writeTime(time)
	except Exception as e:
		print("Error: " + str(e))