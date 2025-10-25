import tkinter as tk
from tkinter import ttk
import file_upload as fu
import classes as cl
import sys
import matplotlib.pyplot as plt
from utils import *


simulator = cl.OS_Simulator()



# Root window initial setup
root = tk.Tk()
root.title("OS simulator")
root.minsize(1304, 530)
root.config(background=GUI_MAIN_COLOR)

# Called after double-clicking on a cell
def edit_cell(event):
    fu.edit_cell(event, tree)

# Function called when closing the window
def on_close():
    width = root.winfo_width()
    height = root.winfo_height()
    print(width, height)
    plt.close('all') # Closes all matplotlib windows
    root.destroy()   # Closes Tkinter window
    sys.exit()       # Ensures the Python process stops

def upload_file():
    upload_button.pack_forget()
    notebook.pack(expand=True, fill="both", padx=5, pady=5)
    begin_simulation_button.pack(padx=5, pady=5)
    fu.configure_file(path_textbox.get("1.0", tk.END).strip(), tree, tree_simulator, simulator_data_label)

def begin_simulation():
    #manual_execution_button.pack_forget()
    #automatic_execution_button.pack_forget()
    notebook.pack_forget()
    begin_simulation_button.pack_forget()
    reset_simulation_button.pack(padx=5, pady=5)
    fu.begin_simulation(simulator, path_textbox.get("1.0", tk.END).strip(), image_frame, update_chart_button, tools_var, tree, tree_simulator)

def reset_simulation():
    simulator.reset()
    update_chart_button.pack_forget()
    reset_simulation_button.pack_forget()
    notebook.pack_forget()
    upload_button.pack(padx=5, pady=5)

image = tk.PhotoImage(file="images/logo.png")

# Tools frame
tools_frame = tk.Frame(root, bg=GUI_TAB_COLOR)
tools_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y) 

tk.Label(
    tools_frame,
    text="OS scheduler simulator",
    bg=GUI_TAB_COLOR,
).pack(padx=5, pady=5)

thumbnail_image = image.subsample(5, 5)
#tk.Label(tools_frame, image=thumbnail_image).pack(padx=5, pady=5)

path_label = tk.Label(tools_frame, text=".txt config file inside config_files folder:", bg=GUI_TAB_COLOR)
path_label.pack(padx=5)
path_textbox = tk.Text(tools_frame, height=1, width=30)
path_textbox.insert(tk.END, "ex1")
path_textbox.pack(padx=10, pady=10) 

upload_button = tk.Button(tools_frame, text="Upload config file", command=upload_file)
upload_button.pack(padx=5, pady=5)
begin_simulation_button = tk.Button(tools_frame, text="Begin simulation", 
                          command=begin_simulation)
reset_simulation_button = tk.Button(tools_frame, text = "Reset simulation", command=reset_simulation)
update_chart_button = tk.Button(tools_frame, text = "Update chart", 
                                command=lambda: simulator.update_chart())
#update_chart_button.pack(padx = 5, pady = 5)

# Tools and Filters tabs
notebook = ttk.Notebook(tools_frame)

tools_tab = tk.Frame(notebook, bg=GUI_TAB_COLOR)
tools_var = tk.StringVar(value=MANUAL_EXECUTION)

manual_execution_button = tk.Radiobutton(
        tools_tab,
        text=MANUAL_EXECUTION,
        variable=tools_var,
        value=MANUAL_EXECUTION,
        bg=GUI_TAB_COLOR,
    )
manual_execution_button.pack(anchor="w", padx=20, pady=5)
automatic_execution_button = tk.Radiobutton(
        tools_tab,  
        text=AUTOMATIC_EXECUTION,
        variable=tools_var,
        value=AUTOMATIC_EXECUTION,
        bg=GUI_TAB_COLOR,
    )
automatic_execution_button.pack(anchor="w", padx=20, pady=5)

simulator_data_label = ttk.Label(tools_tab, text="", background=GUI_TAB_COLOR)
simulator_data_label.pack(pady=10)

frame_table_simulator = ttk.Frame(tools_tab)
frame_table_simulator.pack(fill=tk.BOTH, expand=True)
tree_simulator = ttk.Treeview(frame_table_simulator)
tree_simulator.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree_simulator.bind("<Double-1>", edit_cell)
scroll_y = ttk.Scrollbar(frame_table_simulator, orient=tk.VERTICAL, command=tree_simulator.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree_simulator.configure(yscrollcommand=scroll_y.set)

frame_table = ttk.Frame(tools_tab)
frame_table.pack(fill=tk.BOTH, expand=True)
tree = ttk.Treeview(frame_table)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree.bind("<Double-1>", edit_cell)
scroll_y = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=tree.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scroll_y.set)

notebook.add(tools_tab, text="Tools")


'''
filters_tab = tk.Frame(notebook, bg="lightgreen")
filters_var = tk.StringVar(value="None")

for filter in ["Blurring", "Sharpening"]:
    tk.Radiobutton(
        filters_tab,
        text=filter,
        variable=filters_var,
        value=filter,
        bg="lightgreen",
    ).pack(anchor="w", padx=20, pady=5)
#notebook.add(filters_tab, text="Filters")
'''


# Image frame
image_frame = tk.Frame(root, bg=GUI_MAIN_COLOR)
image_frame.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)

display_image = image.subsample(2, 2)
'''
tk.Label(
    image_frame,
    text="Image",
    bg="grey",
    fg="white",
).pack(padx=5, pady=5)

tk.Label(image_frame, image=display_image).pack(padx=5, pady=5)
'''

# Make sure the program is terminated after closing the window
root.protocol("WM_DELETE_WINDOW", on_close)

# Initialize GUI
root.mainloop()

print("Terminating program")