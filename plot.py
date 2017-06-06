import matplotlib.pyplot as pyplot
from scipy.stats import linregress
import csv


def plot(times):
	slope, intercept, r_value, p_value, std_err = linregress(range(len(times)), times)
	pyplot.rcParams["figure.figsize"] = (20, 10)
	print("Plotting...")
	pyplot.scatter(times.index(max(times)), max(times), color = "r", lw = 4.0)
	pyplot.scatter(times.index(min(times)), min(times), color = "r", lw = 4.0)
	pyplot.annotate("Worst time: " + str(max(times)), xy = (times.index(max(times)), max(times)), xytext = (times.index(max(times)) + times.index(max(times)) / 100, max(times) + max(times) / 100))
	pyplot.annotate("Best time: " + str(min(times)), xy = (times.index(min(times)), min(times)), xytext = (times.index(min(times)), min(times) - min(times) / 15))
	pyplot.plot(range(len(times)), times, lw = 2.0, color = "#0099ff", label = "Times")
	trend = [slope * i + intercept for i in [-1, len(times)]]
	pyplot.plot([-1, len(times)], trend, lw = 2.0, color = "r", label = "Trend")
	pyplot.legend(loc = 2, borderaxespad = 1)
	pyplot.axis([-1, len(times), min(times) - (min(times) / 10), max(times) + (max(times) / 10)])
	pyplot.xlabel("Solves")
	pyplot.ylabel("Seconds")
	print("Done!\nSaving...")
	pyplot.savefig("plot.png", bbox_inches = "tight", dpi = 200)
	print("Done!")