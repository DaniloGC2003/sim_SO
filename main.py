import tkinter as tk

window = tk.Tk()
window.geometry("1600x900")
window.title("Simulador de SO")
window.config(background="#95b88d")

label = tk.Label(window, text="Simulador de SO", font=("Arial", 24), bg="#95b88d")
label.pack(pady=20)

icon = tk.PhotoImage(file="images/logo.png")
window.iconphoto(False, icon)

print("terminating program")
window.mainloop()
