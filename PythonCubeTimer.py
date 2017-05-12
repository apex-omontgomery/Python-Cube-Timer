from time import sleep, process_time
from collections import OrderedDict
#from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *
import csv#, sys

#The inspection time in seconds
#Change it to whatever suits you
inspectionTime = 15

#The time keys
#Change it to whatever suits you
timeKeys = [60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]

#Writes the passed value to the times file
def writeLatestTime(time):
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
	totalTime = 0
	
	for value in timeKeys:
		dictonary[float(value)] = 0

	for key in dictonary.keys():
		for time in times:
			if time < key:
				dictonary[key] += 1
	
	for time in times:
		totalTime += time
	
	print("Solves: " + str(len(times)))
	print("Average: " + str(round(totalTime / len(times), 3)))
	for key, val in dictonary.items():
		print("Sub-{}: {} [{}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))

times = readTimes()
stats(times, timeKeys)