import classes as cl
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import queue as q

X_AXIS_MIN_LENGTH = 15

class Scheduler:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.current_task = None

        # Variables for FCFS algorithm
        self.execution_queue = q.Queue()

    def exec(self, tasks, current_time):
        if self.algorithm == "FCFS":
            self.current_task = self.step_FCFS(tasks, current_time)
        return self.current_task
    
    def step_FCFS(self, tasks, current_time):
        # Enqueue tasks starting at current_time

        # List to store tasks starting at current_time
        new_tasks = []
        for task in tasks:
            if task.start == current_time:
                new_tasks.append(task)
        # Enqueue tasks in ascending order of their indexes
        while len(new_tasks) > 0:
            earliest = None
            for task in new_tasks:
                if earliest is None:
                    earliest = task
                else:
                    if int(task.name[1:]) < int(earliest.name[1:]):
                        earliest = task
            new_tasks.remove(earliest)
            print("enqueuing task: " + earliest.name)
            self.execution_queue.put(earliest)
        
        # Find current task
        if not self.execution_queue.empty():
            self.current_task = self.execution_queue.queue[0]
        else:
            self.current_task = None
        if self.current_task is not None:
            # Se clock tick for o ultimo necessario para completar a duracao da tarefa
            if len(self.current_task.moments_in_execution) == self.current_task.duration - 1:
                # Dequeue
                finished_task = self.execution_queue.get()

                print("finished task: " + finished_task.name)
                finished_task.end = current_time + 1
        print("FCFS selected")

        print('returning: ' + self.current_task.name if self.current_task else "returning None")
        return self.current_task


class OS_Simulator:
    def __init__(self):
        self.algorithm = ""
        self.quantum = 0
        self.tasks = []
        self.scheduler = None

        # Variables used for plotting the chart
        self.fig = None
        self.ax = None
        self.canvas = None
        self.widget = None
        self.df = None

        # Variables used for the simulation
        self.current_time = 0
        self.current_task = None
        self.total_simulation_time = 0

        # Variables for FCFS algorithm
        self.execution_queue = q.Queue()
        
    def print_self(self):
        print(f"Algorithm: {self.algorithm}, Quantum: {self.quantum}")
        for task in self.tasks:
            print(f"Task: {task.name}, Color: {task.color}, Start: {task.start}, Duration: {task.duration}, Priority: {task.priority}, Events: {task.event_list}")


    def update_chart(self):
        next_task = None
        if self.algorithm == "FCFS":
            next_task = self.scheduler.exec(self.tasks, self.current_time)
        if next_task is not None:    
            print("im here")
            next_task.moments_in_execution.append(self.current_time)
        # increment time
        if self.current_time < self.total_simulation_time:
            self.current_time += 1
    
        # plot chart
        self.ax.clear()
        self.ax.set_xlim(0, max(X_AXIS_MIN_LENGTH, self.current_time + 1))
        self.ax.set_xticks(range(int(self.ax.get_xlim()[0]), int(self.ax.get_xlim()[1]) + 1))
        for x in range(int(self.ax.get_xlim()[0]), int(self.ax.get_xlim()[1]) + 1):
            self.ax.axvline(x=x, color="gray", linestyle=":", linewidth=0.8)
        for task in self.tasks:
            self.ax.barh(task.name, 0, left=0)
            for i in range(self.current_time):
                if i in task.moments_in_execution:
                    self.ax.barh(task.name, 1, left=i, color=task.color, edgecolor="black")
                elif i >= task.start and i < task.end:
                    self.ax.barh(task.name, 1, left=i, color="white", edgecolor="black")
            
        #self.fig = plt.barh([task.name for task in self.tasks], [task.duration for task in self.tasks], left=[task.start for task in self.tasks], color=[task.color for task in self.tasks], edgecolor="black")
        self.canvas.draw()

        if self.current_time >= self.total_simulation_time:
            print("Simulation finished. Saving image")
            self.fig.savefig("image_output/output.png")
        
        print()

class Task:
    def __init__(self, name, color, start, duration, priority, event_list):
        self.name = name
        self.color = color
        self.start = start
        self.duration = duration
        self.priority = priority
        self.event_list = event_list

        self.moments_in_execution = []
        self.end = float('inf')