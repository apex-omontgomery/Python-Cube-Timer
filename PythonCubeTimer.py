import csv
import datetime
from math import floor, sqrt
from time import perf_counter
from tkinter import *
from tkinter import ttk
import plot


def write_time(time):
    with open("times.csv", "a", newline="") as times:
        writer = csv.writer(times)
        writer.writerow([time, "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())])


def read_times():
    times = []
    with open("times.csv", newline="") as saveFile:
        reader = csv.reader(saveFile, delimiter=",")
        for row in reader:
            times.append(row[0])

    times = [float(time) for time in times]
    return times


class TimerContainer:
    def __init__(self, int_val, times):
        self.int_val = int_val
        self.vals = times  # probably dont need
        self.avg = None  # probably don't need

    def last_n_times(self, times):
        sum_last_n_times = sum(times[-self.int_val:])
        self.avg = round((sum_last_n_times / self.int_val), 3)


class Application:
    def __init__(self):
        self.times = None
        self.timer_groups = [3, 5, 12, 50, 100, 1000]
        self.timer_containers = []
        self.timer_strings = [StringVar() for _ in self.timer_groups]
        self.timer_labels = []
        self.total_solves_avg = None
        self.total_solves_strings = StringVar()
        self.total_solves_avg_labels = None
        self.special_calc_groups = ['median', 'stdev', 'best', 'worst', 'latest']
        self.special_calc_vals_list = []
        self.special_calc_strings = [StringVar() for _ in self.timer_groups]
        self.special_calc_labels = []
        self.root = Tk()
        self.root.title("Cubing Timer")
        self.root.option_add("*tearOff", False)
        self.mainframe = None

        self.init_gui()
        self.root.config(menu=self.menuBar)
        self.root.resizable(0, 0)
        self.root.mainloop()

    def create_timer_group_objects(self):
        #  the partial
        self.timer_containers = [TimerContainer(int_val, self.times[-int_val:]) for int_val in self.timer_groups]

    def calc_stats(self, times):
        self.timer_containers.append(self.create_timer_group_objects())

        # total solves, median, stdev, best, worst, latest
        sorted_times = sorted(times)
        # total solves
        average = sum(times) / len(times)
        self.total_solves_avg.round(average, 3)
        # median
        ciel_median_index = len(sorted_times) // 2 + 1  # floor plus one.
        if len(sorted_times) % 2 == 0:
            median = round(sorted_times[ciel_median_index], 3)
        else:
            median = (sum(sorted_times[ciel_median_index] + sorted_times[ciel_median_index]) / 2, 3)
        self.special_calc_vals_list.append(median)
        # stdev
        deviations = [(x - average) ** 2 for x in times]
        variance = sum(deviations) / len(deviations)
        std_dev = sqrt(variance)
        self.special_calc_vals_list.append(round(std_dev, 3))
        # best
        self.special_calc_vals_list.append(min(times))
        # worst
        self.special_calc_vals_list.append(max(times))
        # most recent
        self.special_calc_vals_list.append(times[-1])

    def update_timer(self):
        self.elapsedTime = int(floor(perf_counter() - self.start))
        self.minutes, self.seconds = divmod(self.elapsedTime, 60)
        self.timerLabel.configure(text="%02d:%02d" % (self.minutes, self.seconds))
        self.root.after(1000, self.update_timer)

    def update_image(self, times):
        plot.plot(times)
        self.image = PhotoImage(file="plot.png")
        self.plotImage.configure(image=self.image)

    def timer(self):
        self.start = perf_counter()
        self.timerWindow = Toplevel(self.root)
        self.timerWindow.title("Timer")
        self.timerWindow.resizable(0, 0)
        self.timerLabel = ttk.Label(self.timerWindow, text="00:00", font=("Courier", 64))
        self.timerLabel.grid(column=0, row=0, sticky=(N, E, S, W))
        self.startButton = ttk.Button(self.timerWindow, text="START", width=40, command=self.update_timer)
        self.startButton.grid(column=0, row=1, sticky=S)

    # Need to add the actual string values to the string variables.
    def create_app_labels(self):
        self.total_solves_avg_labels = ttk.Label(self.mainframe, textvariable=self.total_solves_strings)
        self.total_solves_avg_labels.grid(column=1, row=1, sticky=E)

        for i in range(2, len(self.timer_groups) + 2):
            self.timer_labels.append(ttk.Label(self.mainframe, textvariable=self.timer_strings[i]))
            self.timer_labels[-1].grid(column=1, row=i, sticky=E)

        for j in range(1+len(self.timer_groups), 2 + len(self.timer_groups) + len(self.special_calc_strings)):
            self.special_calc_labels.append(ttk.Label(self.mainframe, textvariable=self.special_calc_strings[j]))
            self.timer_labels[-1].grid(column=1, row=j, sticky=E)

    def init_gui(self):
        self.menuBar = Menu(self.root)
        self.menuBar.add_command(label="Quit", command=self.root.quit)
        self.mainframe = ttk.Frame(self.root, padding="3 3 3 3")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.create_app_labels()
        self.times = read_times()
        plot.plot(self.times, 1, 1, 1)
        self.image = PhotoImage(file="plot.png")
        self.plotImage = ttk.Label(self.mainframe, image=self.image)
        self.plotImage.grid(column=2, row=1, rowspan=13, sticky=(E))

        self.lowerFrame = ttk.Frame(self.mainframe, padding="3 3 3 3")
        self.lowerFrame.grid(column=1, columnspan=2, row=14, sticky=(N, S))

        self.timerButton = ttk.Button(self.lowerFrame, text="TIMER", width=160, command=self.timer)
        self.timerButton.grid(column=0, row=0, sticky=(W, E))

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=2, pady=2)

        self.calc_stats(self.times)


application = Application()
