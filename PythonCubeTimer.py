from time import sleep, perf_counter
import datetime
from collections import OrderedDict
from math import ceil, floor, sqrt
import csv
import os
import configparser
from tkinter import *
from tkinter import ttk


def getConfig():
	configValues = dict()
	config = configparser.ConfigParser()
	config.read("config.ini")
	for key in config["DEFAULT"]:
		configValues[key] = config["DEFAULT"][key]
	
	return configValues


def clear():
	os.system("cls" if os.name == "nt" else "clear")


def writeTime(time):
	with open("times.csv", "a", newline="") as times:
		writer = csv.writer(times)
		writer.writerow([time, "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())])


def readTimes():
	times, timestamps = [], []
	with open("times.csv", newline = "") as saveFile:
		reader = csv.reader(saveFile, delimiter=",")
		for row in reader:
			times.append(row[0])
			timestamps.append(row[1])

	times = [float(time) for time in times]
	return times, timestamps


def toggleTimer():
	start =  perf_counter()
	end =  perf_counter()
	return round(end - start, 3)

	
def newBest(time):
	print("""
  _   _   ______  __          __    ____    ______    _____   _______   _ 
 | \ | | |  ____| \ \        / /   |  _ \  |  ____|  / ____| |__   __| | |
 |  \| | | |__     \ \  /\  / /    | |_) | | |__    | (___      | |    | |
 | . ` | |  __|     \ \/  \/ /     |  _ <  |  __|    \___ \     | |    | |
 | |\  | | |____     \  /\  /      | |_) | | |____   ____) |    | |    |_|
 |_| \_| |______|     \/  \/       |____/  |______| |_____/     |_|    (_)
	""")
	print(str(time))
	print("Enter to dismiss")
	input()
	
	
def stats(times, timestamps, configValues):
	clear()
	print("\n")
	#subx based on code by https://www.reddit.com/user/yovliporat
	#https://drive.google.com/file/d/0B7qI7oJsiTPGcjY2VlpoQi1hLVU/view
	if configValues["subx"] == "True":
		timeKeys = configValues["timekeys"].split(",")
		timeKeys = [int(key) for key in timeKeys]
		dictonary = OrderedDict()
		
		for value in timeKeys:
			dictonary[float(value)] = 0
	
		for key in dictonary.keys():
			for time in times:
				if time < key:
					dictonary[key] += 1
			
		for key, val in dictonary.items():
			print("Sub-{}: {} [{}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))
	
	
	if configValues["solves"] == "True":
		print("Solves: " + str(len(times)))
	
	
	if configValues["ao3"] == "True":
		last3Times = times[-3:]
		sumLast3Times = sum(last3Times)
		print("Ao3: " + str(round(sumLast3Times / len(last3Times), 3)))
	
	
	if configValues["ao5"] == "True": 
		last5Times = times[-5:]
		sumLast5Times = sum(last5Times)
		print("Ao5: " + str(round(sumLast5Times / len(last5Times), 3)))
		
	
	if configValues["ao12"] == "True":
		last12Times = times[-12:]
		last12Times.pop(last12Times.index(max(last12Times)))
		last12Times.pop(last12Times.index(min(last12Times)))
		sumLast12Times = sum(last12Times)
		print("Ao12: " + str(round(sumLast12Times / len(last12Times), 3)))
	
	
	if configValues["ao50"] == "True":
		last50Times = times[-50:]
		sumLast50Times = sum(last50Times)
		print("Ao50: " + str(round(sumLast50Times / len(last50Times), 3)))
	
	
	if configValues["ao100"] == "True":
		last100Times = times[-100:]
		sumLast100Times = sum(last100Times)
		print("Ao100: " + str(round(sumLast100Times / len(last100Times), 3)))
	
	
	if configValues["ao1000"] == "True":
		last1000Times = times[-1000:]
		sumLast1000Times = sum(last1000Times)
		print("Average: " + str(round(totalTime / len(times), 3)))
		
	
	if configValues["average"] == "True":
		totalTime = sum(times)
		print("Average: " + str(round(totalTime / len(times), 3)))
		
	
	if configValues["mean"] == "True":
		sortedTimes = sorted(times)
		if len(sortedTimes) % 2 == 0:
			mean = round(sortedTimes[ceil(len(sortedTimes) / 2)], 3)
		else:
			mean = round(sortedTimes[floor(len(sortedTimes) / 2)] + sortedTimes[ceil(len(sortedTimes) / 2)] / 2, 3)
		
		print("Mean: " + str(mean))
	
	
	if configValues["standarddeviation"] == "True":
		average = sum(times) / len(times)
		deviations = [(x - average) ** 2 for x in times]
		variance = sum(deviations) / len(deviations)
		standardDeviation = sqrt(variance)
		print("SD: " + str(round(standardDeviation, 3)))
	
	
	if configValues["best"] == "True":
		print("Best: " + str(min(times)))
		
	
	if configValues["worst"] == "True":
		print("Worst: " + str(max(times)))
	
	
	if configValues["latest"] == "True":
		print("Latest: " + str(times[-1]))

	
configValues = getConfig()

#while True:
#	try:
#		times, timestamps = readTimes()
#		stats(times, timestamps, configValues)
#	except IndexError:
#		print("Error, no recorded solves.")
#	except FileNotFoundError:
#		print("Error, file \"times.csv\n not found.")
#	except Exception as e:
#		print("Error: " + str(e))
#	
#	try:
#		time = runTimer()
#		if time < min(times):
#			newBest(time)
#		
#		writeTime(time)
#	except Exception as e:
#		print("Error: " + str(e))

root = Tk()
root.title("Cubing Timer")
mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)

ttk.Button(mainframe, text = "START", command = toggleTimer).grid(column = 1, row = 1, sticky = (S))
root.bind("<space>", toggleTimer)

root.mainloop()