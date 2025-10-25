import classes as cl
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import *
import re

def edit_cell(event, tree):
    item = tree.identify_row(event.y)
    coluna = tree.identify_column(event.x)
    if not item or not coluna:
        return

    # Column index
    col_index = int(coluna.replace('#', '')) - 1
    valor_atual = tree.item(item, "values")[col_index]

    # cell coordinates
    x, y, width, height = tree.bbox(item, coluna)
    
    # Entry field over the cell
    entry = tk.Entry(tree)
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, valor_atual)
    entry.focus()

    def save(event=None):
        novo_valor = entry.get()
        valores = list(tree.item(item, "values"))
        valores[col_index] = novo_valor
        tree.item(item, values=valores)
        entry.destroy()

    def cancel_writing(event=None):
        entry.destroy()

    entry.bind("<Return>", save)
    entry.bind("<Escape>", cancel_writing)
    entry.bind("<FocusOut>", save)

def configure_file(filename, tree, tree_simulator, simulator_data_label):
    path = "config_files/" + filename + ".txt"
    if validate_file(filename):
        for item in tree.get_children():
            tree.delete(item)
        for item in tree_simulator.get_children():
            tree_simulator.delete(item)
        with open(path, "r", encoding="utf-8") as f:
            lines = [linha.strip() for linha in f if linha.strip()]
        algoritmo, quantum = lines[0].split(";")
        simulator_data_label["text"] = f"Algoritmo: {algoritmo} | Quantum: {quantum}"

        colunas_simulator = ["algorithm", "quantum"]
        tree_simulator["columns"] = colunas_simulator
        tree_simulator["show"] = "headings"

        colunas = ["id", "cor", "ingresso", "duracao", "prioridade", "lista_eventos"]
        tree["columns"] = colunas
        tree["show"] = "headings"

        for col in colunas:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100, anchor="center")
        for col in colunas_simulator:
            tree_simulator.heading(col, text=col.capitalize())
            tree_simulator.column(col, width=100, anchor="center")

        for linha in lines[1:]:
            valores = linha.split(";")
            if len(valores) == len(colunas):
                tree.insert("", "end", values=valores)
        values_simulator = lines[0].split(";")
        tree_simulator.insert("", "end", values=values_simulator)
    else:
        print("Bad config file")

def validate_file(filename):
    path = "config_files/" + filename + ".txt"
    try:
        with open(path, "r", encoding="utf-8") as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return False

    if len(linhas) < 2:
        print("Arquivo muito curto.")
        return False

    # ===== Validação da primeira linha =====
    primeira = linhas[0].split(";")
    if len(primeira) != 2:
        print("Primeira linha deve ter 2 campos: algoritmo;quantum")
        return False

    algoritmo, quantum = primeira
    if not algoritmo.isalpha():
        print("Algoritmo inválido (deve conter apenas letras).")
        return False
    if not quantum.isdigit() or int(quantum) <= 0:
        print("Quantum deve ser um número inteiro positivo.")
        return False

    # ===== Validação das tarefas =====
    padrao_cor = re.compile(r"^#[0-9a-fA-F]{6}$")
    for i, linha in enumerate(linhas[1:], start=2):
        partes = linha.split(";")
        if len(partes) != 6:
            print(f"Linha {i}: número incorreto de campos ({len(partes)}).")
            return False

        id_, cor, ingresso, duracao, prioridade, eventos = partes

        if not id_:
            print(f"Linha {i}: ID vazio.")
            return False
        if not padrao_cor.match(cor):
            print(f"Linha {i}: cor inválida ({cor}).")
            return False
        for campo, nome in [(ingresso, "ingresso"), (duracao, "duracao"), (prioridade, "prioridade")]:
            if not campo.isdigit() or int(campo) < 0:
                print(f"Linha {i}: campo '{nome}' inválido ({campo}).")
                return False
        # lista_eventos pode ser '-' ou lista separada por vírgulas
        if eventos != "-" and not all(e.strip() for e in eventos.split(",")):
            print(f"Linha {i}: lista_eventos inválida ({eventos}).")
            return False

    print("Arquivo válido!")
    return True

def begin_simulation(os_simulator, filename, window, chart_button, simulation_mode, tree, tree_simulator):
    print("File upload function called")
    simulation_lines = []
    for row_id in tree.get_children():
        simulation_lines.append(tree.item(row_id, "values"))

    os_data = []
    os_data = tree_simulator.item(tree_simulator.get_children()[0], "values")
    print(os_data)
    os_simulator.algorithm = os_data[0]
    os_simulator.quantum = int(os_data[1])
    os_simulator.simulation_mode = simulation_mode.get()



    for line in simulation_lines:
        print('creating new task')
        task = cl.Task(line[0], line[1], int(line[2]), int(line[3]), int(line[4]), line[5])
        print(task.name)
        os_simulator.tasks.append(task)
        os_simulator.total_simulation_time += int(line[3])
    
    earliest_start = None
    for task in os_simulator.tasks:
        if earliest_start is None or task.start < earliest_start.start:
            earliest_start = task
    os_simulator.total_simulation_time += earliest_start.start
    
    if os_simulator.algorithm == "FCFS":
        os_simulator.scheduler = cl.Scheduler("FCFS", os_simulator.quantum)

    #plot initial chart
    os_simulator.fig, os_simulator.ax = plt.subplots(figsize=(PLOT_INITIAL_WIDTH,PLOT_INITIAL_HEIGHT))
    os_simulator.ax.set_xlim(0, X_AXIS_MIN_LENGTH)
    os_simulator.ax.set_xticks(range(int(os_simulator.ax.get_xlim()[0]), int(os_simulator.ax.get_xlim()[1]) + 1))
    for x in range(int(os_simulator.ax.get_xlim()[0]), int(os_simulator.ax.get_xlim()[1]) + 1):
        os_simulator.ax.axvline(x=x, color="gray", linestyle=":", linewidth=0.8)
    for task in os_simulator.tasks:
        os_simulator.ax.barh(task.name, 0, left=0)
    os_simulator.canvas = FigureCanvasTkAgg(os_simulator.fig, master=window)
    os_simulator.widget = os_simulator.canvas.get_tk_widget()
    os_simulator.widget.pack(padx=10, pady=10)


    # Different behavior based on execution mode
    if simulation_mode.get() == MANUAL_EXECUTION:
        print("im here")
        chart_button.pack(padx = 5, pady = 5)
    elif simulation_mode.get() == AUTOMATIC_EXECUTION:
        while os_simulator.simulation_finished == False:
            os_simulator.update_chart()