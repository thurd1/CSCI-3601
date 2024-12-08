"""
Author      : Trenton Hurd
Date        : 7 December 2024
Class       : CSCI-3601
"""

import socket
import threading
from LamportClock import LamportClock

lamport = LamportClock()

critical_section = threading.Lock() # lock for mutual exlcusion in the critical section
readers_count = 0 # counter for active readers
readers_lock = threading.Lock() # lock for to protect readers_count from race conditions

AOS_FILE = "C:\\Users\\XoxoTrent\\Desktop\\Distributed Mutual Exclusion\\schedule.txt"  # path to schedule.txt


def read_file(client_socket):
    """Handles read requuests and sends the contents of the file to the client"""
    try:
        with open(AOS_FILE, "r") as file: # opens file in read mode
            file_contents = file.read() # reads entire file 
        client_socket.sendall(file_contents.encode()) # sends the file contents to client.py
    except FileNotFoundError:
        error_message = "File not found." # prints error if file does not exist
        client_socket.sendall(error_message.encode())
    except Exception as e:
        error_message = f"An error occurred: {str(e)}" # print error if any other error occurs
        client_socket.sendall(error_message.encode())


def write_file(client_socket, course_code):
    """Handles write requests, registers a student for a course, and updates the file"""
    try:
        with open(AOS_FILE, "r+") as file: # opens file for reading/writing
            lines = file.readlines() # reads entire file
            updated_lines = [] # list to hold file content
            course_found = False # flag to check if the course exists

            for line in lines:
                if line.startswith(course_code.strip()): # checks if the line matches the course code
                    course_found = True
                    parts = line.strip().split("|") # splits the lines in to parts
                    seats = int(parts[-1])  # seats assumed to be in the last column
                    if seats > 0: # checks if seats are available
                        parts[-1] = f" {seats - 1}" # decreases the seat count
                        updated_line = "|".join(parts) # updates the line
                        updated_lines.append(updated_line + "\n")
                        response = f"Registered for {course_code}. Seats remaining: {seats - 1}"
                    else:
                        response = f"Course {course_code} is full."
                        updated_lines.append(line) #
                else:
                    updated_lines.append(line)

            if not course_found:
                response = f"Course {course_code} not found."

        with open(AOS_FILE, "w") as file: # writes updated data back to file
            file.writelines(updated_lines)

        client_socket.sendall(response.encode()) # response back to client.py

    except Exception as e:
        client_socket.sendall(f"Error: {str(e)}".encode()) # error handling


def handle_client(client_socket):
    """Handles incoming client requests, determines reader/writer, continues depending on which was selected"""
    global readers_count # accesses the reader_count
    try:
        request = client_socket.recv(1024).decode().strip() # request from client
        lamport.increment() # increments lamport clock 

        if request.startswith("READ"): # handles READ requests
            with readers_lock: # lock to modify readers_count 
                readers_count += 1 
                if readers_count == 1: # if the user is the first reader
                    critical_section.acquire() # locks the critical section

            read_file(client_socket) # calls the function in order to read/send file contents

            with readers_lock: # lock to modify readers_count 
                readers_count -= 1 
                if readers_count == 0: # if there are no readers
                    critical_section.release() # releases the critical section

        elif request.startswith("WRITE"): # handles WRITE requests
            parts = request.split(maxsplit=1) # splits the request to get the course code
            if len(parts) == 2: # makes sure the format is correct
                _, course_code = parts
                critical_section.acquire() # locks the critical section for exclusive access
                write_file(client_socket, course_code) # calls the function to handle the WRITE function
                critical_section.release() # realeases the critical section
            else:
                client_socket.sendall("Invalid WRITE request format.".encode()) # error if format is wrong
        else:
            client_socket.sendall("Invalid request.".encode()) # error for any other request

    except Exception as e:
        client_socket.sendall(f"Error: {str(e)}".encode()) # graceful error handling
    finally:
        client_socket.close() # closes the client.py connection


def start_server(host, port):
    """Start the server to accept, listens for connections, creates threads to handle each client"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
    server.bind((host, port)) # binds socket to the host and port
    server.listen(5) # listen for incoming connections, max is set to 5
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept() # accepts new client connections
        print(f"Connection from {addr}") # prints the clients address
        threading.Thread(target=handle_client, args=(client_socket,)).start() # starts a new thread to handle the client


if __name__ == "__main__":
    HOST = "127.0.0.1" # local host address
    PORT = 65432 # port number for the server 
    start_server(HOST, PORT) # starts server.py
