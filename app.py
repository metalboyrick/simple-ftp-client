import tkinter as tk
from event_handler import * 

# initialise tk object
window = tk.Tk()

# some basic metadata
window.title("FTP Client")
window.geometry("500x570")
window.resizable(False, False)

# WIDGETS

# LOGIN SECTION
login_frame = tk.Frame(window)
tk.Grid.rowconfigure(login_frame, 0, weight=1)
login_frame.pack()

# forms
ip = tk.StringVar()
port = tk.StringVar()
user = tk.StringVar()
pwd = tk.StringVar()
ip_form = tk.Entry(login_frame, textvariable=ip, width=30)
port_form = tk.Entry(login_frame, textvariable=port, width=30)
user_form = tk.Entry(login_frame, textvariable=user)
pwd_form = tk.Entry(login_frame, textvariable=pwd, show="*")
ip_form.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
port_form.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
user_form.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
pwd_form.grid(row=1, column=3, sticky=tk.N+tk.S+tk.E+tk.W)

# form labels
ip_flabel = tk.Label(login_frame, text="IP")
port_flabel = tk.Label(login_frame, text="Port")
user_flabel = tk.Label(login_frame, text="Username")
pwd_flabel = tk.Label(login_frame, text="Password")

ip_flabel.grid(row=0, column=0, sticky=tk.W)
port_flabel.grid(row=0, column=2, sticky=tk.W)
user_flabel.grid(row=1, column=0, sticky=tk.W)
pwd_flabel.grid(row=1, column=2, sticky=tk.W)

# login, logout connect buttons
login_button_frame = tk.Frame(window)
tk.Grid.rowconfigure(login_button_frame, 0, weight=1)
login_button_frame.pack()

login_btn = tk.Button(login_button_frame, text="Login", command=login_btn_pressed, width=20)
logout_btn = tk.Button(login_button_frame, text="Logout", command=logout_btn_pressed, width=20)
connect_btn = tk.Button(login_button_frame, text="Connect", command=connect_btn_pressed, width=20)
login_btn.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
logout_btn.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
connect_btn.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

# radio buttons
conn_mode = tk.IntVar()
pasv_rbtn = tk.Radiobutton(login_button_frame, text="PASV", variable=conn_mode, val=0)
port_rbtn = tk.Radiobutton(login_button_frame, text="PORT", variable=conn_mode, val=1)

pasv_rbtn.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
port_rbtn.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

# connection status
conn_status = tk.StringVar()
conn_status.set("NOT CONNECTED")
connect_status_text = tk.Label(login_button_frame, textvariable=conn_status)
connect_status_text.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)


# STATUS BOXES
status_box_frame = tk.Frame(window)
tk.Grid.rowconfigure(status_box_frame, 0, weight=1)
status_box_frame.pack()

cwd = "something"
cwd_text = tk.Label(status_box_frame, text="Current directory: " + cwd)
cwd_text.pack()

files_box = tk.Listbox(status_box_frame, width=100, height=15)
files_box.pack()

cli_label = tk.Label(status_box_frame, text="Status: ") 
cli_label.pack()

cli_box = tk.Text(status_box_frame, state=tk.DISABLED,width=100, height=5)
cli_box.pack()

# FOOTER
# download segment
download_button_frame = tk.Frame(window)
tk.Grid.rowconfigure(download_button_frame, 0, weight=1)
download_button_frame.pack()

download_btn = tk.Button(download_button_frame, text="Download", command=download_btn_pressed, width=30)
newfolder_btn = tk.Button(download_button_frame, text="New folder", command=newfolder_btn_pressed, width=30)
download_btn.grid(row=0, column=0)
newfolder_btn.grid(row=0, column=1)

# upload segment
upload_button_frame = tk.Frame(window)
tk.Grid.rowconfigure(upload_button_frame, 0, weight=1)
upload_button_frame.pack()

on = tk.StringVar()
on.set("sup")

browse_form = tk.Entry(upload_button_frame, textvariable=on, width=30)
browse_btn = tk.Button(upload_button_frame, text="Browse", command=browse_btn_pressed)
upload_btn = tk.Button(upload_button_frame, text="Upload", command=upload_btn_pressed)
browse_form.grid(row=0,column=0)
browse_btn.grid(row=0,column=1)
upload_btn.grid(row=0,column=2)


# right click menu
rc_menu = tk.Menu(window, tearoff = 0)
rc_menu.add_command(label ="Rename") 
rc_menu.add_command(label ="Delete")  

# texts

upload_text = tk.Label(window, text="Upload files:")




# run application event loop
window.mainloop()