import socket
import random
from model import *

BUFFER_SIZE = 8192
FORMAT = 'utf-8'
HOST = socket.gethostbyname(socket.gethostname())

def connect(current_state):
    ip_addr = current_state.ip_addr.get()
    port = current_state.port.get()
    try:
        current_state.socket.connect((ip_addr, port))
        current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        current_state.pasv_addr[0] = current_state.ip_addr.get()
        current_state.port_addr[0] = HOST
        return 0
    except socket.error as err:
        return 1, err


def set_pasv(current_state):
    try:
        if current_state.conn_mode == ConnectionMode.PORT.value:
            current_state.data_conn_socket.close()

        current_state.socket.sendall("PASV\r\n".encode(FORMAT))
        pasv_addr = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)

        # parse address returned by server
        start = pasv_addr.index("(")
        end = pasv_addr.index(")")
        parse_addr_list = pasv_addr[start + 1: end].split(",")
        port = int(parse_addr_list[4]) * 256 + int(parse_addr_list[5])

        # load address to state model
        current_state.pasv_addr[1] = port

        current_state.status_bar.set(pasv_addr.replace("\r\n", "\n"))

        current_state.conn_mode.set(ConnectionMode.PASV.value)

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
        current_state.status_bar.set(user_response.replace("\r\n", "\n"))
        
        current_state.socket.sendall(PASS_command)
        current_message = current_state.status_bar.get()
        pass_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        current_state.status_bar.set(pass_response.replace("\r\n", "\n"))

        if user_response[0] == "5" or pass_response[0] == "5":
            return user_response, pass_response

        set_pasv(current_state)

        get_file_list(current_state)
        
        return user_response, pass_response
    except socket.error as err:
        return err


def set_port(current_state):
    ip_addr = current_state.port_addr[0].split(".")
    port = random.randint(20000,65535)
    p1 = port // 256 
    p2 = port % 256
    info_tuple = ip_addr[0] +","+ ip_addr[1] +","+ ip_addr[2] +","+ ip_addr[3] + "," + str(p1) + "," + str(p2)
    PORT_command = "PORT " + info_tuple + "\r\n"

    try:
        current_state.socket.sendall(PORT_command.encode(FORMAT))
        port_status = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        current_state.status_bar.set(port_status.replace("\r\n", "\n"))
        if port_status[0] == "2":
            current_state.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            current_state.data_socket.bind((current_state.port_addr[0],port))
            current_state.port_addr[1] = port
            current_state.data_socket.listen()
            current_state.conn_mode.set(ConnectionMode.PORT.value)
            return 0, "ok"
        else:
            return 1, "PORT Error"
        
    except socket.error as err:
        return 1, err


def build_data_socket(current_state):
    current_state.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if current_state.conn_mode == ConnectionMode.PASV:
            current_state.data_socket.connect((current_state.pasv_address[0],current_state.pasv_address[1]))
        elif current_state.conn_mode == ConnectionMode.PORT:
            current_state.data_conn_socket, current_state.data_conn_addr = current_state.data_socket.accept()

        return 0
    except socket.error as err:
        return 1


def format_file(filename):
    length = len(filename)
    return filename[57:length]

def get_file_list(current_state):
    selected_folder = current_state.cwd
    current_state.socket.sendall(("LIST" + selected_folder + "\r\n").encode(FORMAT))
    current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))
    # build_data_socket(current_state)
    try:
        
        if current_state.conn_mode.get() == ConnectionMode.PASV.value:
            current_state.data_socket.connect((current_state.pasv_addr[0],current_state.pasv_addr[1]))
            current_state.file_list = current_state.data_socket.recv(BUFFER_SIZE).decode(FORMAT).split("\r\n")
            current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))
            current_state.data_socket.close()
            
        elif current_state.conn_mode.get() == ConnectionMode.PORT.value:
            current_state.file_list = current_state.data_socket.recv(BUFFER_SIZE).decode(FORMAT).split("\r\n")
            current_state.data_conn_socket.close()
            current_state.data_socket.close()

        i = 0
        for filename in current_state.file_list:
            current_state.file_list[i] = format_file(filename)
            i += 1

        return 0
    except socket.error as err:
        return 1


def rename(current_state, old_name, new_name):
    # set rename from for RNFR
    current_state.socket.sendall(("RNFR " + old_name + "\r\n").encode(FORMAT))
    staging_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(staging_response)
    if staging_response[0] != "3":
        raise Exception("Rename error !")

    # set rename to for RNTO
    current_state.socket.sendall(("RNTO " + new_name + "\r\n").encode(FORMAT))
    staging_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(staging_response)
    if staging_response[0] != "2":
        raise Exception("Rename error !")


def delete(current_state, target_filename):
    current_state.socket.sendall(("RMD " + target_filename + "\r\n").encode(FORMAT))
    delete_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(delete_response)
    if delete_response[0] != "2":
        raise Exception("Delete error!")
