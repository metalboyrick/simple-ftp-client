import tkinter as tk

# initialise tk object
window = tk.Tk()

# some basic metadata
window.title("FTP Client")
window.geometry("500x800")

# WIDGETS

# buttons
login_btn = None
logout_btn = None
connect_btn = None
download_btn = None
upload_btn = None
newfolder_btn = None
browse_btn = None

# radio buttons
port_rbtn = None
pasv_rbtn = None

# WHITEBOXES
files_wb = None
status_wb = None

# form inputs
ip_form = None
port_form = None
user_form = None
pass_form = None
upload_form = None

# right click menu
rc_menu = None

# texts
cwd_text = None
upload_text = None
connect_status_text = None

# run application event loop
window.mainloop()