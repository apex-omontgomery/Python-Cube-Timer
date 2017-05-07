from time import sleep, process_time
from collections import OrderedDict
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import csv, sys

#The inspection time in seconds
#Change it to whatever suits you
inspectionTime = 15

#The time keys
#Change it to whatever suits you
timeKeys = [60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5]

def writeLatestTime(time):
	with open("times.txt", "a") as times:
		times.write(str(time) + ",")

def readTimes():
	times = [time for time in list(csv.reader(open("times.csv", "r")))[0]]
	times.pop()
	times = [float(time) for time in times]
	return times

def runTimer():
	start = process_time()
	input()
	return round(process_time() - start, 3)

def inspection(inspectionTime):
	sleep(inspectionTime)

def stats(times, timeKeys):
	#Based on code by https://www.reddit.com/user/yovliporat
	#https://drive.google.com/file/d/0B7qI7oJsiTPGcjY2VlpoQi1hLVU/view
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

class init(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		startButton = QPushButton("Start", self)
		timer = QLCDNumber(self)
		
		vbox = QVBoxLayout()
		vbox.addWidget(timer)
		vbox.addWidget(startButton)
		
		self.setLayout(vbox)
		
		self.setGeometry(300, 300, 250, 100)
		self.setWindowTitle("Python Cube Timer")
		self.setWindowIcon(QIcon("icon.png"))
		self.show()

app = QApplication(sys.argv)
initiation = init()
sys.exit(app.exec_())