import tkinter as tk

root = tk.Tk()
root.title("Number Input Example")

# Label
tk.Label(root, text="Enter a number:").pack(pady=5)

# Entry box
entry = tk.Entry(root)
entry.pack(pady=5)

def show_number():
    try:
        number = float(entry.get())  # or int(entry.get()) if you only want integers
        print("Number entered:", number)
    except ValueError:
        print("Please enter a valid number!")

tk.Button(root, text="Submit", command=show_number).pack(pady=5)

root.mainloop()
