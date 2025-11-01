import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Scrollable List Example")
root.geometry("300x300")

# --- Create a canvas and scrollbar ---
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Configure scrolling region
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# Create window inside canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Connect canvas to scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Pack everything
container.pack(fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Add multiple text elements ---
for i in range(30):
    label = ttk.Label(scrollable_frame, text=f"Item {i+1}", padding=5)
    label.pack(anchor="w")

root.mainloop()
