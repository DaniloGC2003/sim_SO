import classes as cl
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import queue as q

class OS_Simulator:
    def __init__(self):
        self.algorithm = ""
        self.quantum = 0
        self.tasks = []

        # Variables used for plotting the chart
        self.fig = None
        self.ax = None
        self.canvas = None
        self.widget = None
        self.df = None

        # Variables used for the simulation
        self.current_time = 0
        self.current_task = None

        # Variables for FCFS algorithm
        self.execution_queue = q.Queue()
        
    def print_self(self):
        print(f"Algorithm: {self.algorithm}, Quantum: {self.quantum}")
        for task in self.tasks:
            print(f"Task: {task.name}, Color: {task.color}, Start: {task.start}, Duration: {task.duration}, Priority: {task.priority}, Events: {task.event_list}")
    def update_chart(self):
        # Example implementation. Final version should plot Gantt chart
        #x = [1, 2, 3]
        #y = [1, 4, 9]
        #self.ax.clear()
        #self.fig = plt.barh([task.name for task in self.tasks], [task.duration for task in self.tasks], left=[task.start for task in self.tasks], color=[task.color for task in self.tasks])
        #self.ax.plot(x, y)
        #self.canvas.draw()
        if self.algorithm == "FCFS":
            # Enqueue tasks starting at current_time
            early_list = []
            for task in self.tasks:
                if task.start == self.current_time:
                    early_list.append(task)
            while len(early_list) > 0:
                earliest = None
                for task in early_list:
                    if earliest is None:
                        earliest = task
                    else:
                        if int(task.name[1:]) < int(earliest.name[1:]):
                            earliest = task
                early_list.remove(earliest)
                print("enqueuing task: " + earliest.name)
                self.execution_queue.put(earliest)
            
            # Find current task
            if not self.execution_queue.empty():
                self.current_task = self.execution_queue.queue[0]
            else:
                self.current_task = None

            # Execute current task
            if self.current_task is not None:
                print("current task: " + self.current_task.name)
                self.current_task.moments_in_execution.append(self.current_time)
                if len(self.current_task.moments_in_execution) >= self.current_task.duration:
                    finished_task = self.execution_queue.get()
                    print("finished task: " + finished_task.name)


            self.ax.clear()
            for task in self.tasks:
                for moment in task.moments_in_execution:
                    self.ax.barh(task.name, 1, left=moment, color=task.color, edgecolor="black")
            #self.fig = plt.barh([task.name for task in self.tasks], [task.duration for task in self.tasks], left=[task.start for task in self.tasks], color=[task.color for task in self.tasks], edgecolor="black")
            self.canvas.draw()
            self.current_time += 1
            print("FCFS selected")

class Task:
    def __init__(self, name, color, start, duration, priority, event_list):
        self.name = name
        self.color = color
        self.start = start
        self.duration = duration
        self.priority = priority
        self.event_list = event_list

        self.moments_in_execution = []