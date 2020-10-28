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


if __name__ == "__main__":
    main()