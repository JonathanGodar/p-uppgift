import tkinter as tk
from my_calendar import Calendar

class AddNotePage(tk.Frame):
	def __init__(self, root: tk.Frame, calendar: Calendar):
		super().__init__(root)
		
		note_text_entry = tk.Entry(self)
		note_text_entry.pack()
		tk.Button(self, )
	



