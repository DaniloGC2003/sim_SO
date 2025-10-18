import tkinter as tk
from tkinter import ttk
import file_upload as fu
import classes as cl
import sys
import matplotlib.pyplot as plt


simulator = cl.OS_Simulator()

# Root window initial setup
root = tk.Tk()
root.title("OS simulator")
root.minsize(768, 432)
root.config(background="#95b88d")

# Function called when closing the window
def on_close():
    plt.close('all') # Closes all matplotlib windows
    root.destroy()   # Closes Tkinter window
    sys.exit()       # Ensures the Python process stops

image = tk.PhotoImage(file="images/logo.png")

# Tools frame
tools_frame = tk.Frame(root, bg="skyblue")
tools_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y) 

tk.Label(
    tools_frame,
    text="RECEBA",
    bg="skyblue",
).pack(padx=5, pady=5)

thumbnail_image = image.subsample(5, 5)
tk.Label(tools_frame, image=thumbnail_image).pack(padx=5, pady=5)

path_label = tk.Label(tools_frame, text=".txt config file inside config_files folder:", bg="skyblue")
path_label.pack(padx=5)
path_textbox = tk.Text(tools_frame, height=1, width=30)
path_textbox.insert(tk.END, "ex1")
path_textbox.pack(padx=10, pady=10)

upload_button = tk.Button(tools_frame, text="Upload config file", 
                          command=lambda: fu.upload_file(simulator, path_textbox.get("1.0", tk.END).strip(), image_frame))
upload_button.pack(padx=5, pady=5)
update_chart_button = tk.Button(tools_frame, text = "Update chart", 
                                command=lambda: simulator.update_chart())
update_chart_button.pack(padx = 5, pady = 5)

# Tools and Filters tabs
notebook = ttk.Notebook(tools_frame)
notebook.pack(expand=True, fill="both")

tools_tab = tk.Frame(notebook, bg="lightblue")
tools_var = tk.StringVar(value="None")

for tool in ["Resizing", "Rotating"]:
    tk.Radiobutton(
        tools_tab,
        text=tool,
        variable=tools_var,
        value=tool,
        bg="lightblue",
    ).pack(anchor="w", padx=20, pady=5)

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

notebook.add(tools_tab, text="Tools")
notebook.add(filters_tab, text="Filters")

# Image frame
image_frame = tk.Frame(root, bg="grey")
image_frame.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)

display_image = image.subsample(2, 2)

tk.Label(
    image_frame,
    text="Image",
    bg="grey",
    fg="white",
).pack(padx=5, pady=5)

tk.Label(image_frame, image=display_image).pack(padx=5, pady=5)

#make sure the program is terminated after closing the window
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
print("terminating program")
simulator.print_self()