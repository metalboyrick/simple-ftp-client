import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
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
        self.current_state.conn_mode.set(0)
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

        listbox_frame = tk.Frame(status_box_frame)
        tk.Grid.rowconfigure(listbox_frame, 0, weight=1)
        listbox_frame.pack()

        toolbar_frame = tk.Frame(status_box_frame)
        tk.Grid.rowconfigure(toolbar_frame, 0, weight=1)
        toolbar_frame.pack()

        # CWD indicator
        self.display_cwd = tk.StringVar()
        self.display_cwd.set("CWD: None")
        self.cwd_text = tk.Label(toolbar_frame, textvariable=self.display_cwd, width=20)
        self.cwd_text.grid(row=0, column=0, sticky=tk.E)

        # up a folder button
        self.up_btn = tk.Button(toolbar_frame, text="Go up", command=lambda: self.up_btn_pressed(), width=10)
        self.up_btn.grid(row=0, column=1, sticky=tk.W)

        # scrollbar
        self.scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)

        # files display
        self.files_box = tk.Listbox(listbox_frame, width=100, height=15, yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.files_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_box.pack()

        # select
        self.files_box.bind("<Double-1>", lambda event: self.goto_folder())

        # set up right click menu
        # right click menu
        self.rc_menu = tk.Menu(self.files_box, tearoff=0)
        self.rc_menu.add_command(label="Rename", command=lambda: self.rc_rename())
        self.rc_menu.add_command(label="Delete", command=lambda: self.rc_delete())

        # bind right click menu to files_box
        self.files_box.bind("<Button-3>", lambda event: self.pop_rc_menu(event))



        # Status bar label
        self.cli_label = tk.Label(status_box_frame, text="Status: ", height=2, fg='blue')
        self.cli_label.pack()

        # status bar
        self.cli_box = tk.Label(status_box_frame, textvariable=self.current_state.status_bar)
        self.cli_box.pack()

        # FOOTER
        # download segment
        self.download_button_frame = tk.Frame(window)
        tk.Grid.rowconfigure(self.download_button_frame, 0, weight=1)
        self.download_button_frame.pack()

        self.download_btn = tk.Button(self.download_button_frame, text="Download", command=lambda: self.download_btn_pressed(), width=30)
        self.newfolder_btn = tk.Button(self.download_button_frame, text="New folder", command=lambda: self.newfolder_btn_pressed(), width=30)
        self.download_btn.grid(row=0, column=0)
        self.newfolder_btn.grid(row=0, column=1)

        # upload segment
        self.upload_button_frame = tk.Frame(window)
        tk.Grid.rowconfigure(self.upload_button_frame, 0, weight=1)
        self.upload_button_frame.pack()

        self.specs_btn = tk.Button(self.upload_button_frame, text="Server info", width=30,
                                   command=lambda: self.specs_btn_pressed())
        self.specs_btn.grid(row=0,column=0)

        self.upload_btn = tk.Button(self.upload_button_frame, text="Upload", command=lambda: self.upload_btn_pressed(), width=30)
        self.upload_btn.grid(row=0,column=1)

    # ============================================ right click options ==============================================
    # right click menu for file box
    def pop_rc_menu(self, event):
        # right click menu only appears if files are the and one file is selected.
        if len(self.current_state.file_list) > 0 and self.files_box.get(tk.ACTIVE):
            self.rc_menu.tk_popup(event.x_root, event.y_root)

    # renaming
    def rc_rename(self):
        current_filename = self.files_box.get(tk.ACTIVE)
        index = self.current_state.file_list.index(current_filename)
        new_name = simpledialog.askstring(title="Rename", prompt="Enter new name")

        if not new_name:
            return

        try:
            sk.rename(self.current_state, current_filename, new_name)
        except Exception as err:
            messagebox.showerror(title="Error", message="Error renaming!: " + str(err))

        self.current_state.file_list[index] = new_name

        self.refresh_list()

    # deleting
    def rc_delete(self):
        target_filename = self.files_box.get(tk.ACTIVE)
        index = self.current_state.file_list.index(target_filename)

        # if it is folder
        if target_filename.find(".") == -1:
            try:
                sk.delete(self.current_state, target_filename)
            except Exception as err:
                messagebox.showerror(title="Error", message="Error deleting!: " + str(err))
        else:
            messagebox.showerror(title="Error", message="Non-folder deletions are currently unsupported.")

        del self.current_state.file_list[index]

        self.refresh_list()

    # ============================================= double click ====================================================

    def goto_folder(self):
        target_filename = self.files_box.get(tk.ACTIVE)
        if target_filename.find(".") == -1:
            try:
                sk.goto_folder(self.current_state, target_filename)
            except Exception as err:
                messagebox.showerror(title="Error", message="Error navigating!: " + str(err))
        else:
            messagebox.showerror(title="Error", message="Please select a folder.")

        self.display_cwd.set("CWD: " + self.current_state.cwd)

        self.refresh_list()

    # updates the file list if any
    def refresh_list(self):
        self.files_box.delete(0, tk.END)
        for item in self.current_state.file_list:
            self.files_box.insert(tk.END, item)

    # ============================================== buttons ========================================================
    def login_btn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return
        
        if self.current_state.login_status == LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Already logged in!")
            return

        user_response, pass_response = sk.login(self.current_state)

        # server responds OK.
        if user_response[0] == "3" and pass_response[0] =="2":
            self.current_state.login_status = LoginStatus.LOGGED_IN
            self.login_btn.configure(bg="green", fg="white", text="Logged in")
            self.display_cwd.set("CWD: /")
            self.refresh_list()

        # server responds 5XX Error.
        elif user_response[0] == "5" or pass_response[0] == "5":
            messagebox.showerror(title="Error", message="Authentication failed!")

        # other exceptions
        else:
            messagebox.showerror(title="Error", message="Unknown Error!")

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

        sk.set_pasv(self.current_state)


    def port_rbtn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        sk.set_port(self.current_state)

    def up_btn_pressed(self):

        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        if self.current_state.cwd == "/":
            messagebox.showerror(title="Error", message="You are on root!")

        try:
            sk.goto_folder(self.current_state, "..")
        except Exception as err:
            messagebox.showerror(title="Error", message="Error navigating!: " + str(err))

        self.display_cwd.set("CWD: " + self.current_state.cwd)

        self.refresh_list()

    def newfolder_btn_pressed(self):

        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        # get new folder name
        new_folder = simpledialog.askstring(title="New folder", prompt="Enter new folder name")
        if not new_folder:
            return

        try:
            sk.new_folder(self.current_state, new_folder)
        except Exception as err:
            messagebox.showerror("Error", str(err))

        self.refresh_list()

    def download_btn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        filename = self.files_box.get(tk.ACTIVE)
        destination = filedialog.askdirectory()
        print(destination)

        if not filename or not destination:
            return

        try:
            sk.download(self.current_state, filename, destination, self.trf_progress)
        except Exception as err:
            messagebox.showerror("Error", str(err))

    def upload_btn_pressed(self):

        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        filename = filedialog.askopenfilename()

        try:
            sk.upload(self.current_state, filename)
        except Exception as err:
            messagebox.showerror("Error", str(err))

        self.refresh_list()

    def specs_btn_pressed(self):
        if self.current_state.conn_status.get() == "NOT CONNECTED":
            messagebox.showerror(title="Error", message="Please connect first!")
            return

        if self.current_state.login_status != LoginStatus.LOGGED_IN:
            messagebox.showerror(title="Error", message="Please log in first!")
            return

        messagebox.showinfo("Server specifications", sk.view_specs(self.current_state))



