from enum import Enum
import tkinter as tk
from browse_page import BrowsePage
from calendar import Calendar
from add_note_page import AddNotePage

class Pages(Enum):
	BROWSE_PAGE=0
	ADD_NOTE_PAGE=0

# https://www.pythontutorial.net/tkinter/tkraise/
class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.calendar = Calendar()
		self.add_note_page = AddNotePage(self, self.calendar)

		self.add_note_page.pack(fill=tk.BOTH)
		

		# self.browse_page = BrowsePage(self, self.calendar)
		# self.browse_page.pack(fill=tk.BOTH)
	

