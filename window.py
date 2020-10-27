import tkinter as tk
from tkinter import messagebox
from model import *
import socket_lib as sk

class MainWindow():
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

        self.login_btn = tk.Button(login_button_frame, text="Login", command=lambda: self.login_btn_pressed(), width=20)
        self.connect_btn = tk.Button(login_button_frame, text="Connect", command=lambda: self.connect_btn_pressed(), width=20)
        self.login_btn.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.connect_btn.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # radio buttons
        self.pasv_rbtn = tk.Radiobutton(login_button_frame, text="PASV", variable=self.current_state.conn_mode, value=ConnectionMode.PASV.value, command=lambda: self.pasv_rbtn_pressed())
        self.port_rbtn = tk.Radiobutton(login_button_frame, text="PORT", variable=self.current_state.conn_mode, value=ConnectionMode.PORT.value, command=lambda: self.port_rbtn_pressed())

        self.pasv_rbtn.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.port_rbtn.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        # connection status
        self.connect_status_text = tk.Label(login_button_frame, textvariable=self.current_state.conn_status, fg="red")
        self.connect_status_text.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # # STATUS BOXES
        status_box_frame = tk.Frame(window)
        tk.Grid.rowconfigure(status_box_frame, 0, weight=1)
        status_box_frame.pack()

        toolbar_frame = tk.Frame(status_box_frame)
        tk.Grid.rowconfigure(toolbar_frame, 0, weight=1)
        toolbar_frame.pack()

        cwd_text = tk.Label(toolbar_frame, textvariable=self.current_state.cwd)
        cwd_text.grid(row=0, column=0)

        self.files_box = tk.Listbox(status_box_frame, width=100, height=15)
        self.files_box.pack()

        cli_label = tk.Label(status_box_frame, text="Status: ", height=2, fg='blue') 
        cli_label.pack()

        cli_box = tk.Label(status_box_frame, textvariable=self.current_state.status_bar) 
        cli_box.pack()

    def refresh_list(self):
        i = 1
        for item in self.current_state.file_list:
            self.files_box.insert(i, item)
            i += 1

    # buttons
    def login_btn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return
        
        if self.current_state.login_status == LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Already logged in!")
            return

        user_response, pass_response = sk.login(self.current_state)

        if user_response[0] == "3" and pass_response[0] =="2":
            self.current_state.login_status = LoginStatus.LOGGED_IN
            self.login_btn.configure(bg="green", fg="white", text="Logged in")
            self.refresh_list()
        elif user_response[0] == "5" or pass_response[0] == "5":
            messagebox.showerror(title="Error", message="Incorrect credentials!")  
        else:
            messagebox.showerror(title="Error", message="Cannot login!")  

    def connect_btn_pressed(self):
        if self.current_state.conn_status.get() == "CONNECTED":
            messagebox.showerror(title="Error", message="Already connected!")
            return

        if not sk.connect(self.current_state):
            self.current_state.conn_status.set("CONNECTED")
            self.connect_status_text.configure(fg="green")
        else:
            messagebox.showerror(title="Error", message="Cannot connect to server!")
        
    def pasv_rbtn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        func_res, error = sk.set_pasv(self.current_state)

        if func_res:
            self.current_state.conn_mode.set(ConnectionMode.PORT.value)
            messagebox.showerror(title="Error", message="Error! : " + str(error))
            return

    def port_rbtn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        func_res, error = sk.set_port(self.current_state)

        if func_res:
            self.current_state.conn_mode.set(ConnectionMode.PASV.value)
            messagebox.showerror(title="Error", message="Error! : " + str(error))
            return


