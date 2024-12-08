"""
Author      : Trenton Hurd
Date        : 7 December 2024
Class       : CSCI-3601
"""

import socket
import sys


def client_request(request_type, content=None):
    """Sends a reader/writer request to the server"""
    server_address = ('127.0.0.1', 65432) # server IP address and port number

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # TCP/IP socket using IPv4
            print(f"Connecting to server at {server_address}...")
            sock.connect(server_address) # establishes a connection to the server 
            print(f"Connected to server.")

            if request_type == "READ": # checks if the request is a READ operation
                print(f"Sending request type: {request_type}")
                sock.sendall(request_type.encode()) # sends READ request to server.py

                # Receive and print the response
                response = sock.recv(4096).decode() # receives server.py's response and decodes it
                print("\nResponse from server (READ):") # displays server.py's response
                print(response)

            elif request_type == "WRITE" and content: # checks if requests is a WRITE operation
                message = f"{request_type} {content.strip()}" # formatiing for WRITE request
                print(f"Sending request: {message}")
                sock.sendall(message.encode()) # sends request to server.py

                response = sock.recv(1024).decode() # receive and print the response and decodes it 
                print(f"Server response: {response}") # displays server.py's response

            else:
                print("Invalid WRITE request. Content is missing.") # handling for missing connect

    except ConnectionError as e: # handling for connection errors
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}") # handling for exceptions 


if __name__ == "__main__":
    if len(sys.argv) < 2: # makes sure the user has provide the correct number of command-line args
        print("Usage: python client.py <READ/WRITE> [content]") # displays instructions on how to use the program
        sys.exit(1) # exits program and displays error code
 
    request_type = sys.argv[1].upper() # gets reader/write request and converts to uppercase
    content = " ".join(sys.argv[2:]).strip() if len(sys.argv) > 2 else None # additonal content for writer

    if request_type not in ["READ", "WRITE"]: # validation for request type
        print("Invalid request type. Use 'READ' or 'WRITE'.")
        sys.exit(1) # exits the program with an error code

    client_request(request_type, content) # calls client_request function
