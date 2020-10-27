import tkinter as tk
from model import *
from gui_login import * 

def main():
    

    # initialise tk object
    window = tk.Tk()
    window.title("FTP Client")
    window.geometry("500x570")
    window.resizable(False, False)

    # initialise state object
    current_state = State()

    # login section
    login_section = LoginSection(window, current_state)

    # run application event loop
    window.mainloop()


    # # STATUS BOXES
    # status_box_frame = tk.Frame(window)
    # tk.Grid.rowconfigure(status_box_frame, 0, weight=1)
    # status_box_frame.pack()

    # cwd = tk.StringVar()
    # cwd_text = tk.Label(status_box_frame, textvariable=cwd)
    # cwd_text.pack()

    # files_box = tk.Listbox(status_box_frame, width=100, height=15)
    # files_box.pack()

    # cli_label = tk.Label(status_box_frame, text="Status: ") 
    # cli_label.pack()

    # cli_box = tk.Text(status_box_frame, state=tk.DISABLED,width=100, height=5)
    # cli_box.pack()

    # # FOOTER
    # # download segment
    # download_button_frame = tk.Frame(window)
    # tk.Grid.rowconfigure(download_button_frame, 0, weight=1)
    # download_button_frame.pack()

    # download_btn = tk.Button(download_button_frame, text="Download", command=download_btn_pressed, width=30)
    # newfolder_btn = tk.Button(download_button_frame, text="New folder", command=newfolder_btn_pressed, width=30)
    # download_btn.grid(row=0, column=0)
    # newfolder_btn.grid(row=0, column=1)

    # # upload segment
    # upload_button_frame = tk.Frame(window)
    # tk.Grid.rowconfigure(upload_button_frame, 0, weight=1)
    # upload_button_frame.pack()

    # on = tk.StringVar()
    # on.set("sup")

    # browse_form = tk.Entry(upload_button_frame, textvariable=on, width=30)
    # browse_btn = tk.Button(upload_button_frame, text="Browse", command=browse_btn_pressed)
    # upload_btn = tk.Button(upload_button_frame, text="Upload", command=upload_btn_pressed)
    # browse_form.grid(row=0,column=0)
    # browse_btn.grid(row=0,column=1)
    # upload_btn.grid(row=0,column=2)

    # # right click menu
    # rc_menu = tk.Menu(window, tearoff = 0)
    # rc_menu.add_command(label ="Rename") 
    # rc_menu.add_command(label ="Delete")  

    

if __name__ == "__main__":
    main()