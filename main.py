import tkinter as tk
import file_upload as fu
import classes as cl

simulator = cl.OS_Simulator()

window = tk.Tk()
window.geometry("600x600")
window.title("Simulador de SO")
window.config(background="#95b88d")

label = tk.Label(window, text="Simulador de SO", font=("Arial", 24), bg="#95b88d")
label.pack(pady=20)

icon = tk.PhotoImage(file="images/logo.png")
window.iconphoto(False, icon)

button = tk.Button(window, text="Upload config file", font=("Arial", 14), bg="#51634d", fg="white", command=fu.upload_file)
button.pack(pady=20)

window.mainloop()
print("terminating program")
