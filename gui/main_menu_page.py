import os
from my_calendar.my_calendar import Calendar
import tkinter as tk
from tkinter import filedialog, messagebox

from my_calendar.savers.single_file_calendar_saver import SingleFileCalendarSaver
from my_calendar.savers.directory_calendar_saver import DirectoryCalendarSaver

class MainMenuPage(tk.Frame):
	""" A page that lets the user to choose where to load the calendar from. It can be either a directory or a file """
	def __init__(self, root: tk.Frame, callback, exit_fn):
		""" Constructs the interface and sets up callbacks and bindings 
		Parameters:
		----------
		root : tkinter.Frame
			The frame to which this frame should bind to
		callback : function(my_calendar.Calendar, calendar_save_function: (function() -> None)) -> None
			A callback which will be called once the user has selected a calendar file/directory to load
			The calendar_save_function is a function that will save the my_calendar.Calendar which was passed as the first
			argument to the callback.
		"""
		super().__init__(root)
		self.callback = callback

		load_from_dir_frame = tk.Frame(self)
		tk.Label(load_from_dir_frame, text="Läs in (eller skapa) en kalender från en mapp").pack(side=tk.LEFT)
		tk.Button(load_from_dir_frame, text="Välj mapp", command=self.load_calendar_from_directory).pack(side=tk.LEFT)

		load_from_file_frame = tk.Frame(self)
		tk.Label(load_from_file_frame, text="Läs in en kalender från en fil").pack(side=tk.LEFT)
		tk.Button(load_from_file_frame, text="Välj fil", command=self.load_calendar_from_file).pack(side=tk.LEFT)

		create_file_frame = tk.Frame(self)
		tk.Label(create_file_frame, text="Skapa en ny kalender i en fil").pack(side=tk.LEFT)
		tk.Button(create_file_frame, text="Välj fil", command=self.create_single_file_calendar).pack(side=tk.LEFT)



		load_from_dir_frame.pack()
		load_from_file_frame.pack()

		create_file_frame.pack()
		tk.Button(self, text="Avsluta programmet", command=exit_fn).pack()

	def create_single_file_calendar(self):
		""" Prompts the user for a new file in which a calendar should be created. And calls self.callback function once the file is created"""
		file_name = filedialog.asksaveasfilename()
		
		calendar = Calendar()
		save_function = MainMenuPage.create_save_function_for_file_calendar(calendar, file_name)
		self.callback(calendar, save_function)

	def load_calendar_from_directory(self):
		""" Prompts the user for a directory from where a calendar should be loaded/created. Calls self.callback once the calendar is set up """
		directory = filedialog.askdirectory()

		try:
			calendar = DirectoryCalendarSaver.load(directory)

			save_function = MainMenuPage.create_save_function_for_directory_calendar(calendar, directory)
			self.callback(calendar, save_function)
		except Exception as e:
			# 									"Could not load the folder"
			messagebox.showerror("Kunde inte ladda mappen", str(e))

		

	def load_calendar_from_file(self):
		""" Prompt the user for a file which contains a my_calendar.Calendar which has been serialized using SingleFileCalendarSaver
		Will deserialize the calendar in that file and call self.callback
		
		"""
		file_name = filedialog.askopenfilename()
		try:
			calendar = SingleFileCalendarSaver.load(file_name)
			self.callback(calendar, MainMenuPage.create_save_function_for_file_calendar(calendar, file_name))
		except Exception as e:
			#										" Could not load the file",   "Validate the filecontents"
			messagebox.showerror("Kunde inte ladda in filen", "Kontrollera filinnehållet")
	
	@staticmethod
	def create_save_function_for_file_calendar(calendar, path):
		""" Constructs a save function for a calendar that will be saved in a single file by SingeleFileCalendarSaver
		Parameters
		----------
		calendar : my_calendar.Calendar
			The calendar which should be saved by the returned save function
		path : str
			The path to the save file of the calendar
		
		Returns
		-------
		function() -> None : 
			A function which will save the calendar to the given path when called
		"""

		def calendar_saver():
			""" Saveds a calendar"""
			SingleFileCalendarSaver.save(calendar, path)
		return  calendar_saver

	@staticmethod
	def create_save_function_for_directory_calendar(calendar, directory_path, ):
		""" Constructs a save function for a calendar that will be saved in a directory by DirectoryCalendarSaver
		Parameters
		----------
		calendar : my_calendar.Calendar
			The calendar which should be saved by the returned save function
		path : str
			The path to the save directory of the calendar
		
		Returns
		-------
		function() -> None : 
			A function which will save the calendar to the given path when called
		"""

		def calendar_saver():
			DirectoryCalendarSaver.save(calendar, directory_path)
		return calendar_saver