import matplotlib.pyplot as pyplot
from scipy.stats import linregress
import csv

#Reads the times file and returns the times as a list
def readTimes():
	times = []
	with open("times.csv", newline = "") as saveFile:
		reader = csv.reader(saveFile, delimiter=",")
		for row in reader:
			times.append(row[0])

	times = [float(time) for time in times]
	return times

#Create a plot of the times
def plot(times, slope, intercept):
	pyplot.rcParams["figure.figsize"] = (16, 9)
	lineReg = [slope * i + intercept for i in [-1, len(times)]]
	pyplot.scatter(times.index(max(times)), max(times), color = "r", lw = 3.0)
	pyplot.scatter(times.index(min(times)), min(times), color = "r", lw = 3.0)
	pyplot.plot([-1, len(times)], lineReg, lw = 2.0, color = "r", label = "Trend")
	pyplot.plot(range(len(times)), times, lw = 2.0, color = "#0099ff")
	pyplot.axis([-1, len(times), min(times) - (min(times) / 10), max(times) + (max(times) / 10)])
	pyplot.annotate("Worst time: " + str(max(times)), xy = (times.index(max(times)), max(times)), xytext = (times.index(max(times)) + times.index(max(times)) / 100, max(times) + max(times) / 100))
	pyplot.annotate("Best time: " + str(min(times)), xy = (times.index(min(times)), min(times)), xytext = (times.index(min(times)), min(times) - min(times) / 30))
	pyplot.xlabel("Solves")
	pyplot.ylabel("Seconds")
	pyplot.savefig("plot.png", bbox_inches = "tight")
	#pyplot.show()

times = readTimes()
slope, intercept, r_value, p_value, std_err = linregress(range(len(times)), times)
plot(times, slope, intercept)