
class OS_Simulator:
    def __init__(self):
        self.algorithm = ""
        self.quantum = 0
        self.tasks = []
    
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority