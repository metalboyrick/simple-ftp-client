import socket
import random
from model import *

BUFFER_SIZE = 1024
FORMAT = 'utf-8'

def connect(current_state):
    ip_addr = current_state.ip_addr.get()
    port = current_state.port.get()
    try:
        current_state.socket.connect((ip_addr, port))
        current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        return 0
    except socket.error as err:
        return 1, err

def set_pasv(current_state):
    try:
        current_state.socket.send("PASV\r\n".encode(FORMAT))
        pasv_addr = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)

        # parse address returned by server
        start = pasv_addr.index("(")
        end = pasv_addr.index(")")
        parse_addr_list = pasv_addr[start + 1: end].split(",")
        port = int(parse_addr_list[4]) * 256 + int(parse_addr_list[5])

        # load address to state model
        current_state.pasv_addr[1] = port

        return 0, "ok"
    except socket.error as err:
        return 1, err

def login(current_state):
    USER_command = ("USER " + current_state.username.get() + "\r\n").encode(FORMAT)
    PASS_command = ("PASS " + current_state.password.get() + "\r\n").encode(FORMAT)

    try:
        current_state.socket.sendall(USER_command)
        current_message = current_state.status_bar.get()
        user_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        current_state.status_bar.set(current_message + user_response)
        
        current_state.socket.send(PASS_command)
        current_message = current_state.status_bar.get()
        pass_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        current_state.status_bar.set(current_message + pass_response)
        
        set_pasv(current_state)
        
        return user_response, pass_response
    except socket.error as err:
        return err


def set_port(current_state):
    ip_addr = current_state.port_addr[0].get().split(".")
    port = random.randint(20000,65535)
    p1 = port // 256 
    p2 = port % 256
    info_tuple = "("+ ip_addr[0] +","+ ip_addr[1] +","+ ip_addr[2] +","+ ip_addr[3] + "," + str(p1) + "," + str(p2) + ")"
    print(info_tuple)

    try:
        current_state.socket.send(("PORT " + info_tuple + "\r\n").encode(FORMAT))
        port_status = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        if port_status[0] == "2":
            current_state.port_addr[1] = port
            return 0, "ok"
        else:
            return 1, "PORT Error"
        
    except socket.error as err:
        return 1, err
