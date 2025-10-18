
class OS_Simulator:
    def __init__(self):
        self.algorithm = ""
        self.quantum = 0
        self.tasks = []
    def print_self(self):
        print(f"Algorithm: {self.algorithm}, Quantum: {self.quantum}")
        for task in self.tasks:
            print(f"Task: {task.name}, Color: {task.color}, Start: {task.start}, Duration: {task.duration}, Priority: {task.priority}, Events: {task.event_list}")

class Task:
    def __init__(self, name, color, start, duration, priority, event_list):
        self.name = name
        self.color = color
        self.start = start
        self.duration = duration
        self.priority = priority
        self.event_list = event_list
