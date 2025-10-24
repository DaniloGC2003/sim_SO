import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create Tkinter window
window = tk.Tk()
window.title("Scrollable Matplotlib Plot")

X_AXIS_MIN_LENGTH = 50

# Create a Tkinter Canvas to hold the Matplotlib figure
outer_canvas = tk.Canvas(window)
outer_canvas.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

# Add a horizontal scrollbar
h_scroll = ttk.Scrollbar(window, orient=tk.HORIZONTAL, command=outer_canvas.xview)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
outer_canvas.configure(xscrollcommand=h_scroll.set)

# Create a frame inside the canvas
plot_frame = ttk.Frame(outer_canvas)
outer_canvas.create_window((0, 0), window=plot_frame, anchor="nw")

# --- Create Matplotlib figure and axes ---
fig, ax = plt.subplots(figsize=(9, 4))
ax.set_xlim(0, X_AXIS_MIN_LENGTH)
ax.set_xticks(range(int(ax.get_xlim()[0]), int(ax.get_xlim()[1]) + 1))

for x in range(int(ax.get_xlim()[0]), int(ax.get_xlim()[1]) + 1):
    ax.axvline(x=x, color="gray", linestyle=":", linewidth=0.8)

# Example bar chart
ax.barh("Task A", 10, left=5)
ax.barh("Task B", 20, left=15)

# Embed Matplotlib in Tkinter
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Update scroll region dynamically
def update_scroll_region(event=None):
    outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))

plot_frame.bind("<Configure>", update_scroll_region)

# Resize scroll region based on figure size
outer_canvas.bind(
    "<Configure>",
    lambda e: outer_canvas.itemconfig(1, width=max(e.width, fig.get_size_inches()[0] * fig.dpi))
)

window.mainloop()
