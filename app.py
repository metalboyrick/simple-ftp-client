import tkinter as tk
from model import *
from window import * 

def main():
    

    # initialise tk object
    window = tk.Tk()
    window.title("FTP Client")
    window.geometry("500x570")
    window.resizable(False, False)

    # initialise state object
    current_state = State()

    main_window = MainWindow(window, current_state)

    # run application event loop
    window.mainloop()


    

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



    

if __name__ == "__main__":
    main()