import os
from my_calendar.my_calendar import Calendar
import tkinter as tk
from tkinter import filedialog, messagebox

from my_calendar.single_file_calendar_saver import SingleFileCalendarSaver
from my_calendar.directory_calendar_saver import DirectoryCalendarSaver

class LoadCalendarPage(tk.Frame):
	def __init__(self, root: tk.Frame, callback):
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

	
	# def create_directory_calendar(self):
	# 	directory_path = filedialog.askdirectory()

	# 	(calendar,  = Calendar()
	# 	save_function = LoadCalendarPage.create_save_method_for(calendar, directory_path, 'directory')

	# 	self.callback(calendar, save_function)

	def create_single_file_calendar(self):
		file_name = filedialog.asksaveasfilename()
		
		# with open(file_name, 'w', encoding='utf-8') as file:
		# 	file.write("")
		
		calendar = Calendar()
		save_function = LoadCalendarPage.create_save_method_for_file_calendar(calendar, file_name, 'file')
		self.callback(calendar, save_function)

	def load_calendar_from_directory(self):
		directory = filedialog.askdirectory()

		try:
			(calendar, included_files) = DirectoryCalendarSaver.load(directory)

			save_function = LoadCalendarPage.create_save_method_for_directory_calendar(calendar, included_files, directory)
			self.callback(calendar, save_function)
		except Exception as e:
			messagebox.showerror("Kunde inte ladda mappen", str(e))

		

	def load_calendar_from_file(self):
		file_name = filedialog.askopenfilename()
		try:
			calendar = SingleFileCalendarSaver.load(file_name)
			self.callback(calendar, LoadCalendarPage.create_save_method_for(calendar, file_name, 'file'))
		except Exception as e:
			messagebox.showerror("Kunde inte ladda in filen", str(e))
	
	@staticmethod
	def create_save_method_for_file_calendar(calendar, path):
		def calendar_saver():
			SingleFileCalendarSaver.save(calendar, path)
		return  calendar_saver

	@staticmethod
	def create_save_method_for_directory_calendar(calendar, includec_files, directory_path, ):
		def calendar_saver():
			# Clear any old saves so that removed entries are not accidentally still saved 
			try:
				for file in includec_files:
					os.remove(file)
			except:
				pass
			
			DirectoryCalendarSaver.save(calendar, directory_path)
		return calendar_saver