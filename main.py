from my_calendar.note import Note
import datetime as dt
from user_input_utils import get_alternative_from_user, get_date_from_user
from cli.main_menu import main_menu
import tkinter as tk
from tkinter import ttk
from gui.app import App
import os

if __name__ == '__main__':
	window = tk.Tk()
	window.minsize(1080, 720)
	app = App(window, window.destroy)
	app.pack(fill=tk.BOTH)
	window.mainloop()