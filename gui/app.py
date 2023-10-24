from enum import Enum
import tkinter as tk
from gui.browse_page.browse_page import BrowsePage
from gui.load_calendar_page import LoadCalendarPage
from gui.multipage_frame import MultipageFrame
from my_calendar.my_calendar import Calendar
from my_calendar.note import Note
from gui.add_note_page import AddNotePage

class Pages(Enum):
	BROWSE_PAGE=0
	ADD_NOTE_PAGE=0

# https://www.pythontutorial.net/tkinter/tkraise/
class App(MultipageFrame):
	def __init__(self, root, quit_progrm_fn, *args, **kwargs):
		super().__init__(root, *args, **kwargs)
		self.quit_program_function = quit_progrm_fn
		calendar = Calendar()

		load_calendar_page = LoadCalendarPage(self, self.on_calendar_loaded)
		self.switch_to_page(load_calendar_page)


		# self.add_note_page = AddNotePage(self, lambda: print("Done :D"))
		# self.add_note_page.pack(fill=tk.BOTH)

		# self.browse_page = BrowsePage(self, self.calendar)
		# self.browse_page.pack(fill=tk.BOTH)
	
	def on_calendar_loaded(self, calendar, calendar_save_function):
		self.switch_to_page(BrowsePage(self, calendar, calendar_save_function, self.on_exit_browse_page))
		
	
	def on_exit_browse_page(self):
		self.quit_program_function()
		
	

