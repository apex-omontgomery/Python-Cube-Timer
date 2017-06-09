import matplotlib.pyplot as pyplot
import csv
try:
	from scipy.stats import linregress
	scipyExists = True
except:
	scipyExists = False

	
def plot(times, doTrend = 1, doBest = 1, doWorst = 1):
	pyplot.cla()
	pyplot.figure(figsize = (10, 5))
	
	#Worst time
	if doWorst == 1:
		pyplot.scatter(times.index(max(times)), max(times), color = "r", lw = 4.0)
		pyplot.annotate("Worst time: " + str(max(times)), xy = (times.index(max(times)), max(times)), xytext = (times.index(max(times)) + times.index(max(times)) / 100, max(times) + max(times) / 100))
	
	#Best time
	if doBest == 1:
		pyplot.scatter(times.index(min(times)), min(times), color = "r", lw = 4.0)
		pyplot.annotate("Best time: " + str(min(times)), xy = (times.index(min(times)), min(times)), xytext = (times.index(min(times)), min(times) - min(times) / 15))
	
	#All the times
	pyplot.plot(range(len(times)), times, lw = 2.0, color = "#0099ff", label = "Times")
	
	#Trend
	if scipyExists and doTrend == 1:
		slope, intercept, r_value, p_value, std_err = linregress(range(len(times)), times)
		trend = [slope * i + intercept for i in [0 - len(times) / 15, len(times) + len(times) / 15]]
		pyplot.plot([0 - len(times) / 15, len(times) + len(times) / 15], trend, lw = 2.0, color = "r", label = "Trend")
	
	pyplot.legend(loc = 2, borderaxespad = 1)
	pyplot.axis([0 - len(times) / 15, len(times) + len(times) / 15, min(times) - (min(times) / 10), max(times) + (max(times) / 10)])
	pyplot.xlabel("Solves")
	pyplot.ylabel("Seconds")
	pyplot.savefig("plot.png", bbox_inches = "tight", dpi = 100)