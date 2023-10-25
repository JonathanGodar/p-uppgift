# Niklasson Godar, Jonathan | jonathan.godar@ug.kth.se

from my_calendar.note import Note
import datetime as dt
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