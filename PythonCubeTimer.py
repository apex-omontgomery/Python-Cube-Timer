from time import sleep, process_time
from collections import OrderedDict
#from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *
import csv

#The inspection time in seconds
#Change it to whatever suits you
inspectionTime = 15

#The time keys
#Change it to whatever suits you
timeKeys = [35, 30, 25, 24, 23, 22, 21, 20]

#Writes the passed value to the times file
def writeTime(time):
	with open("times.txt", "a") as times:
		times.write(str(time) + ",")
		
#Reads the times file and returns the times as a list
def readTimes():
	times = [time for time in list(csv.reader(open("times.csv", "r")))[0]]
	times.pop()
	times = [float(time) for time in times]
	return times

#Starts the timer and waits for an interrupt
def runTimer(timerDisplay):
	start = process_time()
	input()
	return round(process_time() - start, 3)

#Pauses the program for the specified amount of time
def inspection(inspectionTime):
	sleep(inspectionTime)

#Calculates the statistics
def stats(times, timeKeys):
	#Based on code by https://www.reddit.com/user/yovliporat
	#https://drive.google.com/file/d/0B7qI7oJsiTPGcjY2VlpoQi1hLVU/view
	dictonary = OrderedDict()
	last3Times, last5Times, last12Times = times[-3:], times[-5:], times[-12:]
	totalTime, sumLast3Times, sumLast5Times, sumLast12Times = sum(times), sum(last3Times), sum(last5Times), sum(last12Times)
	
	for value in timeKeys:
		dictonary[float(value)] = 0

	for key in dictonary.keys():
		for time in times:
			if time < key:
				dictonary[key] += 1
	
	print("Solves: " + str(len(times)))
	print("Ao3: " + str(round(sumLast3Times / len(last3Times), 3)))
	print("Ao5: " + str(round(sumLast5Times / len(last5Times), 3)))
	print("Ao12: " + str(round(sumLast12Times / len(last12Times), 3)))
	print("Average: " + str(round(totalTime / len(times), 3)))
	print("Best: " + str(min(times)))
	print("Worst: " + str(max(times)))
	for key, val in dictonary.items():
		print("Sub-{}: {} [{}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))

times = readTimes()
stats(times, timeKeys)