import os
from my_calendar.my_calendar import Calendar
import tkinter as tk
from tkinter import filedialog, messagebox

from my_calendar.savers.single_file_calendar_saver import SingleFileCalendarSaver
from my_calendar.savers.directory_calendar_saver import DirectoryCalendarSaver

class LoadCalendarPage(tk.Frame):
	""" A page that lets the user to choose where to load the calendar from. It can be either a directory or a file """
	def __init__(self, root: tk.Frame, callback, exit_fn):
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
		file_name = filedialog.asksaveasfilename()
		
		calendar = Calendar()
		save_function = LoadCalendarPage.create_save_function_for_file_calendar(calendar, file_name)
		self.callback(calendar, save_function)

	def load_calendar_from_directory(self):
		directory = filedialog.askdirectory()

		try:
			calendar = DirectoryCalendarSaver.load(directory)

			save_function = LoadCalendarPage.create_save_function_for_directory_calendar(calendar, directory)
			self.callback(calendar, save_function)
		except Exception as e:
			messagebox.showerror("Kunde inte ladda mappen", str(e))

		

	def load_calendar_from_file(self):
		file_name = filedialog.askopenfilename()
		try:
			calendar = SingleFileCalendarSaver.load(file_name)
			self.callback(calendar, LoadCalendarPage.create_save_function_for_file_calendar(calendar, file_name))
		except Exception as e:
			messagebox.showerror("Kunde inte ladda in filen", "Kontrollera filinnehållet")
	
	@staticmethod
	def create_save_function_for_file_calendar(calendar, path):
		def calendar_saver():
			SingleFileCalendarSaver.save(calendar, path)
		return  calendar_saver

	@staticmethod
	def create_save_function_for_directory_calendar(calendar, directory_path, ):
		def calendar_saver():
			DirectoryCalendarSaver.save(calendar, directory_path)
		return calendar_saver