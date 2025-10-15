import classes as cl

def upload_file(os_simulator):
    print("File upload function called")
    string = "config_files/ex1.txt"
    with open(string, 'r') as file:
        lines = file.readlines()

    # Remove newline characters (\n) from the end of each line
    lines = [line.strip() for line in lines]

    os_config = lines[0].split(";")
    print(lines)
    os_simulator.algorithm = os_config[0]
    os_simulator.quantum = int(os_config[1])
