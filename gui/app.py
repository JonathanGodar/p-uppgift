from enum import Enum
import tkinter as tk
from gui.browse_page.browse_page import BrowsePage
from gui.main_menu_page import MainMenuPage
from gui.multipage_frame import MultipageFrame
from my_calendar.my_calendar import Calendar
from my_calendar.note import Note
from gui.add_note_page import AddNotePage

class App(MultipageFrame):
	""" Contains the top level frame of the window. Switches between the main menu and the browse view"""

	def __init__(self, root, quit_program_fn, *args, **kwargs):
		""" Constructs the views and switches to the main view
		Parameters
		----------
		root : tkinter.Frame
			The root to which this frame should attach to
		quit_program_fn :
			A function that takes not arguments and returns None that should shut down the program when called
		*args, **kwargs : 
			Are passed to MultipageFrame as args and kwargs
		"""

		super().__init__(root, *args, **kwargs)
		self.quit_program_function = quit_program_fn

		main_menu_page = MainMenuPage(self, self.on_calendar_loaded, quit_program_fn)
		self.switch_to_page(main_menu_page)
	
	def on_calendar_loaded(self, calendar, calendar_save_function):
		""" Is called once the main menu has loaded, will switch to the browse page view
		Parameters 
		----------
		calendar : my_calendar.Calendar
			The calendar which should be passed to browse page

		calendar_save_function :
			Should be a function that takes no arguments and returns None which saves the calendar that was passed to this on_calendar_loaded_function
		"""
		self.switch_to_page(BrowsePage(self, calendar, calendar_save_function, self.on_exit_browse_page))
		
	
	def on_exit_browse_page(self):
		""" Is called once the browse page exits. Will make the program return to the main menu """
		self.switch_to_page(MainMenuPage(self, self.on_calendar_loaded, self.quit_program_function))
		
	

