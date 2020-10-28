import tkinter as tk
import enum
import socket


# enumerations
class LoginStatus(enum.Enum):
    LOGGED_OUT = 0
    LOGGED_IN = 1


class ConnectionMode(enum.Enum):
    PASV = 0
    PORT = 1


# general state model
class State():
    def __init__(self):
        # declare the values in terms of tk variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.ip_addr = tk.StringVar()
        self.conn_status = tk.StringVar()
        self.login_status = LoginStatus.LOGGED_OUT
        self.port = tk.IntVar()
        self.conn_mode = tk.IntVar()
        self.file_list = []
        self.status_bar = tk.StringVar()
        self.upload_path = tk.StringVar()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_conn_socket = None
        self.data_conn_addr = None
        self.pasv_addr = ["", 0]
        self.port_addr = ["", 0]
        self.cwd = ""
        self.trf_progress = tk.DoubleVar()

        # initialise some values
        self.conn_status.set("NOT CONNECTED")
        self.conn_mode.set(ConnectionMode.PASV)

        # some test values
        self.username.set("android")
        self.password.set("android")
        self.ip_addr.set("192.168.5.8")
        self.port.set(6969)