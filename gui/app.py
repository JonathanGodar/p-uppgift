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

class App(MultipageFrame):
	def __init__(self, root, quit_program_fn, *args, **kwargs):
		super().__init__(root, *args, **kwargs)
		self.quit_program_function = quit_program_fn

		load_calendar_page = LoadCalendarPage(self, self.on_calendar_loaded, quit_program_fn)
		self.switch_to_page(load_calendar_page)
	
	def on_calendar_loaded(self, calendar, calendar_save_function):
		self.switch_to_page(BrowsePage(self, calendar, calendar_save_function, self.on_exit_browse_page))
		
	
	def on_exit_browse_page(self):
		self.switch_to_page(LoadCalendarPage(self, self.on_calendar_loaded, self.quit_program_function))
		
	

