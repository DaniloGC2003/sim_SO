import classes as cl
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def upload_file(os_simulator, filename, window):
    print("File upload function called")
    string = "config_files/" + filename + ".txt"
    with open(string, 'r') as file:
        lines = file.readlines()

    # Remove newline characters (\n) from the end of each line
    lines = [line.strip() for line in lines]

    os_config = lines[0].split(";")
    print(lines)
    os_simulator.algorithm = os_config[0]
    os_simulator.quantum = int(os_config[1])

    for line in lines[1:]:
        task_info = line.split(";")
        name = task_info[0]
        color = task_info[1]
        start = int(task_info[2])
        duration = int(task_info[3])
        priority = int(task_info[4])
        event_list = task_info[5].split(",") if task_info[5] != '-' else []
        
        task = cl.Task(name, color, start, duration, priority, event_list)
        os_simulator.tasks.append(task)

    #plot initial chart
    os_simulator.fig, os_simulator.ax = plt.subplots()
    os_simulator.canvas = FigureCanvasTkAgg(os_simulator.fig, master=window)
    os_simulator.widget = os_simulator.canvas.get_tk_widget()
    os_simulator.widget.pack(padx=10, pady=10)
