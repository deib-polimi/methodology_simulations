from datetime import datetime
import os
import time

def create_log():
    global execution_log
    if not os.path.exists("logs"):
        os.makedirs("logs")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    execution_log = os.path.join("logs", f"file_{timestamp}.txt")

def print_log(text):
    global execution_log
    with open(execution_log, "a") as file:
        file.write(f'[{time.time()}]: {text}\n')

def print_log_newline():
    global execution_log
    with open(execution_log, "a") as file:
        file.write(f'\n')
