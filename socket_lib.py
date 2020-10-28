import socket
import random
import re
import os
from model import *

BUFFER_SIZE = 32768
FORMAT = 'utf-8'
HOST_IP = None

def get_host_ip():
    return "127.0.0.1"
#     global HOST_IP
#     if not HOST_IP:
#         try:
#             s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             s.connect(('8.8.8.8', 80))
#             ip = s.getsockname()[0]
#             HOST_IP = ip
#             return HOST_IP
#         finally:
#             s.close()
#     else:
#         return HOST_IP

def connect(current_state):
    ip_addr = current_state.ip_addr.get()
    port = current_state.port.get()
    try:
        current_state.socket.connect((ip_addr, port))
        welcome_msg = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        current_state.status_bar.set(welcome_msg)
        current_state.pasv_addr[0] = current_state.ip_addr.get()
        current_state.port_addr[0] = get_host_ip()
        return 0
    except socket.error as err:
        return 1, err


def close_global_socket(current_state):
    # close the socket
    current_state.socket.close()
    # restart
    current_state.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def close_data_socket(current_state):
    # close the socket
    current_state.data_socket.close()
    # restart
    current_state.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_data_socket(current_state):
    if current_state.conn_mode == ConnectionMode.PASV.value:

        # send pasv request
        current_state.socket.sendall("PASV\r\n".encode(FORMAT))
        pasv_addr = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)

        if pasv_addr[0] != "2":
            raise Exception("PASV request failed!")

        # parse address returned by server
        start = pasv_addr.index("(")
        end = pasv_addr.index(")")
        parse_addr_list = pasv_addr[start + 1: end].split(",")
        port = int(parse_addr_list[4]) * 256 + int(parse_addr_list[5])
        ip = parse_addr_list[0] + "." + parse_addr_list[1] + "." +  parse_addr_list[2] + "." + parse_addr_list[3]

        # connect to data socket
        current_state.data_socket.connect((ip, port))

    elif current_state.conn_mode == ConnectionMode.PORT.value:
        # pick a port
        current_state.data_socket.bind(('', 0))
        ip, port = current_state.data_socket.getsockname()

        # listen to picked port
        current_state.data_socket.listen(1)

        # format port
        ip_addr = get_host_ip().replace('.', ',')
        p1 = port // 256
        p2 = port % 256
        info_tuple = ip_addr + "," + str(p1) + "," + str(p2)
        PORT_command = "PORT " + info_tuple + "\r\n"

        # pass PORT command
        current_state.socket.sendall(PORT_command.encode(FORMAT))
        port_status = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT)
        current_state.status_bar.set(port_status.replace("\r\n", "\n"))


def set_pasv(current_state):
    current_state.conn_mode = ConnectionMode.PASV.value


def set_port(current_state):
    current_state.conn_mode = ConnectionMode.PORT.value


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

        # send transfer type to user
        current_state.socket.sendall("TYPE I\r\n".encode(FORMAT))
        type_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
        current_state.status_bar.set(type_response)

        set_pasv(current_state)

        get_file_list(current_state)
        
        return user_response, pass_response
    except socket.error as err:
        return err


# retain only the filename of the entries
def format_file(filename):
    filename = filename.strip()
    while '  ' in filename:
        filename = filename.replace('  ', ' ')
    stripped = filename.split(' ', 8)

    return stripped[-1]

def get_file_list(current_state):

    connect_data_socket(current_state)

    current_state.socket.sendall("LIST\r\n".encode(FORMAT))
    current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))

    # accept connections
    if current_state.conn_mode == ConnectionMode.PORT.value:
        conn, addr = current_state.data_socket.accept()
        current_state.data_socket = conn

    current_state.file_list = current_state.data_socket.recv(BUFFER_SIZE).decode(FORMAT).split("\r\n")
    current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))

    close_data_socket(current_state)

    i = 0
    for filename in current_state.file_list:
        current_state.file_list[i] = format_file(filename)
        i += 1


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


def goto_folder(current_state, target_filename):
    # go to new CWD
    current_state.socket.sendall(("CWD " + target_filename + "\r\n").encode(FORMAT))
    cwd_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(cwd_response)
    if cwd_response[0] != "2":
        raise Exception("Navigating error !")

    # get new cwd
    current_state.socket.sendall("PWD\r\n".encode(FORMAT))
    pwd_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(pwd_response)

    # record the path name within the state model
    path_name = re.findall(r'\"(.+?)\"', pwd_response)
    current_state.cwd = path_name[0]

    # get file list
    get_file_list(current_state)


def new_folder(current_state, new_folder_name):
    current_state.socket.sendall(("MKD " + new_folder_name + "\r\n").encode(FORMAT))
    make_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(make_response)
    if make_response[0] != "2":
        raise Exception("Make folder error!")

    get_file_list(current_state)

def view_specs(current_state):
    current_state.socket.sendall("SYST\r\n".encode(FORMAT))
    syst_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(syst_response)

    return syst_response

def upload(current_state, filename):
    # connect to data socket
    connect_data_socket(current_state)

    get_file = filename.split("/")

    # send command to notify servers
    current_state.socket.sendall(("STOR " + get_file[-1] + "\r\n").encode(FORMAT))
    current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))

    # accept connections if PORT
    if current_state.conn_mode == ConnectionMode.PORT.value:
        conn, addr = current_state.data_socket.accept()
        current_state.data_socket = conn
        current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))

    total_data = []

    filename = filename.replace('/', '\\')

    with open(filename, 'rb') as f:
        try:
            while True:
                chunk = f.read(BUFFER_SIZE)
                total_data.append(chunk)
                if not chunk:
                    break
        except:
            raise Exception("File read error!")

    for section in total_data:
        current_state.data_socket.sendall(section)

    close_data_socket(current_state)

    get_file_list(current_state)


def download(current_state, filename, destination, bar):
    # connect to data socket
    connect_data_socket(current_state)

    # send command to notify servers
    current_state.socket.sendall(("RETR " + filename + "\r\n").encode(FORMAT))
    current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))

    # accept connections if PORT
    if current_state.conn_mode == ConnectionMode.PORT.value:
        conn, addr = current_state.data_socket.accept()
        current_state.data_socket = conn
        current_state.status_bar.set(current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", ""))

    total_data = []
    while True:
        data = current_state.data_socket.recv(BUFFER_SIZE)
        total_data.append(data)
        if not data:
            break

    destination = destination.replace('/', '\\')

    # write to file
    with open(os.path.join(destination, filename), 'wb') as f:

        for chunks in total_data:
            f.write(chunks)

    close_data_socket(current_state)


def disconnect(current_state):
    current_state.socket.sendall("QUIT\r\n".encode(FORMAT))
    quit_response = current_state.socket.recv(BUFFER_SIZE).decode(FORMAT).replace("\r\n", "")
    current_state.status_bar.set(quit_response)

    close_data_socket(current_state)
    close_global_socket(current_state)


def destroy(current_state):
    current_state.socket.close()
    current_state.data_socket.close()