import classes as cl
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

t1name = "t1"
t1color = "#5f5c9e"
t1start = 0
t1duration = 2
t1priority = 1
t1event_list = []

t2name = "t2"
t2color = "#5f5c9e"
t2start = 5
t2duration = 2
t2priority = 2
t2event_list = []

fig, ax = plt.subplots()
fig = plt.barh([t1name, t2name], [t1duration, t2duration], left=[t1start, t2start], color=[t1color, t2color])
plt.show()
