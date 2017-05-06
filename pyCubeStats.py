from timeit import default_timer as timer
from time import sleep
from collections import OrderedDict
import csv

#The inspection time in seconds
inspectionTime = 15

#The time keys
timeKeys = [60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]

def writeLatestTime(time):
	with open("times.txt", "a") as times:
		times.write(str(time) + ",")

def readTimes():
	return list(csv.reader(open("times.csv", "r"), delimiter=","))[0]

def runTimer():
	start = timer()
	input()
	end = timer()
	time = round(end - start, 3)
	print(str(time))
	
	return time

def inspection(inspectionTime):
	sleep(inspectionTime)

def stats(times, timeKeys):
	#Based on code by https://www.reddit.com/user/yovliporat
	dictonary = OrderedDict()

	for value in timeKeys:
		dictonary[float(value)] = 0

	for key in dictonary.keys():
		for time in times:
			if time < key:
				dictonary[key] += 1
	
	print("Total number of solves: " + str(len(times)))
	for key, val in dictonary.items():
		print("Sub-{}: {} solves [{}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))

times = readTimes()
stats(times, timeKeys)