"""
Author      : Trenton Hurd
Date        : 7 December 2024
Class       : CSCI-3601
"""

import threading
import subprocess

def run_client(request_type, content=None):
    """Executes the client command and captures output"""
    if content:
        cmd = f"python client.py {request_type} {content}" # command for WRITE requests
    else:
        cmd = f"python client.py {request_type}" # command for READ requests
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True) # subprocess to capture and print output
    print(result.stdout.strip())  # rints output without whitespace

read_threads = [threading.Thread(target=run_client, args=("READ",)) for _ in range(1)] # list of threads for running READ requests concurrently
write_threads = [threading.Thread(target=run_client, args=("WRITE", "CSCI-3911")) for _ in range(1)] # list of threads for running WRITE requests concurrently

print("Starting READ test...")
for t in read_threads:
    t.start() # starts each thread and triggers run_client for READ
for t in read_threads:
    t.join() # waits for each thread to complete before continuing

# Start and join WRITE threads
print("Starting WRITE test...")
for t in write_threads:
    t.start() # starts each thread and triggers run_client for WRITE
for t in write_threads:
    t.join() # waits for each thread to complete before continuing

print("Tests completed.") # prints a message after the tests are finished
