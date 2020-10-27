import socket
from model import *

BUFFER_SIZE = 1024
FORMAT = 'utf-8'

def connect(current_state):
    ip_addr = current_state.ip_addr.get()
    port = current_state.port.get()
    try:
        current_state.socket.connect((ip_addr, port))
        return 0
    except socket.error as err:
        return 1

def login(current_state):
    USER_command = ("USER " + current_state.username.get() + "\r\n").encode(FORMAT)
    PASS_command = ("PASS " + current_state.password.get() + "\r\n").encode(FORMAT)

    try:
        current_state.socket.sendall(USER_command)
        current_message = current_state.status_bar.get()
        current_state.status_bar.set(current_message + current_state.socket.recv(BUFFER_SIZE).decode(FORMAT))

        current_state.socket.send(PASS_command)
        current_message = current_state.status_bar.get()
        current_state.status_bar.set(current_message + current_state.socket.recv(BUFFER_SIZE).decode(FORMAT))

        return 0
    except socket.error as err:
        return 1
