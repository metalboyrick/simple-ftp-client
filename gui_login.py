import tkinter as tk
from tkinter import messagebox
from model import *
import socket_lib as sk

class LoginSection():
    def __init__(self, window, state_model):
        self.current_state = state_model

         # LOGIN SECTION
        self.login_frame = tk.Frame(window)
        tk.Grid.rowconfigure(self.login_frame, 0, weight=1)
        self.login_frame.pack()

        # forms
        ip_form = tk.Entry(self.login_frame, textvariable=self.current_state.ip_addr, width=30)
        port_form = tk.Entry(self.login_frame, textvariable=self.current_state.port, width=30)
        user_form = tk.Entry(self.login_frame, textvariable=self.current_state.username)
        pwd_form = tk.Entry(self.login_frame, textvariable=self.current_state.password, show="*")
        ip_form.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        port_form.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
        user_form.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        pwd_form.grid(row=1, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

        # form labels
        ip_flabel = tk.Label(self.login_frame, text="IP")
        port_flabel = tk.Label(self.login_frame, text="Port")
        user_flabel = tk.Label(self.login_frame, text="Username")
        pwd_flabel = tk.Label(self.login_frame, text="Password")

        ip_flabel.grid(row=0, column=0, sticky=tk.W)
        port_flabel.grid(row=0, column=2, sticky=tk.W)
        user_flabel.grid(row=1, column=0, sticky=tk.W)
        pwd_flabel.grid(row=1, column=2, sticky=tk.W)

        # login, logout connect buttons
        login_button_frame = tk.Frame(window)
        tk.Grid.rowconfigure(login_button_frame, 0, weight=1)
        login_button_frame.pack()

        login_btn = tk.Button(login_button_frame, text="Login", command=lambda: self.login_btn_pressed(), width=20)
        connect_btn = tk.Button(login_button_frame, text="Connect", command=lambda: self.connect_btn_pressed(), width=20)
        login_btn.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        connect_btn.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # radio buttons
        conn_mode = tk.IntVar()
        pasv_rbtn = tk.Radiobutton(login_button_frame, text="PASV", variable=self.current_state.conn_mode, val=0)
        port_rbtn = tk.Radiobutton(login_button_frame, text="PORT", variable=self.current_state.conn_mode, val=1)

        pasv_rbtn.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        port_rbtn.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        # connection status
        connect_status_text = tk.Label(login_button_frame, textvariable=self.current_state.conn_status)
        connect_status_text.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # buttons
    def login_btn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if not sk.login(self.current_state):
            self.current_state.login_status = LoginStatus.LOGGED_IN
        else:
            messagebox.showerror(title="Error", message="Cannot login !")  

    def connect_btn_pressed(self):
        if self.current_state.conn_status.get() == "CONNECTED":
            messagebox.showerror(title="Error", message="Already connected!")
            return

        if not sk.connect(self.current_state):
            self.current_state.conn_status.set("CONNECTED")
        else:
            messagebox.showerror(title="Error", message="Cannot connect to server!")
        
        # success, update log
        # failed, update log

    def download_btn_pressed():
        pass

    def upload_btn_pressed():
        pass

    def newfolder_btn_pressed():
        pass

    def browse_btn_pressed():
        pass
