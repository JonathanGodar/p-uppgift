from my_calendar.my_calendar import Calendar
import tkinter as tk
from tkinter import filedialog, messagebox

from my_calendar.savers.single_file_calendar_saver import SingleFileCalendarSaver
from my_calendar.my_calendar import DirectoryCalendarSaver

class LoadCalendarPage(tk.Frame):
	def __init__(self, root: tk.Frame, callback):
		super().__init__(root)
		self.callback = callback

		load_from_dir_frame = tk.Frame(self)
		tk.Label(load_from_dir_frame, text="Läs in en kalender från en mapp").pack(side=tk.LEFT)
		tk.Button(load_from_dir_frame, text="Välj mapp", command=self.load_calendar_from_directory).pack(side=tk.LEFT)

		load_from_file_frame = tk.Frame(self)
		tk.Label(load_from_file_frame, text="Läs in en kalender från en fil").pack(side=tk.LEFT)
		tk.Button(load_from_file_frame, text="Välj fil", command=self.load_calendar_from_file).pack(side=tk.LEFT)

		create_dir_frame = tk.Frame(self)
		tk.Label(create_dir_frame, text="Skapa en ny kalender i mapp").pack(side=tk.LEFT)
		tk.Button(create_dir_frame, text="Välj mapp", command=self.create_directory_calendar).pack(side=tk.LEFT)

		create_file_frame = tk.Frame(self)
		tk.Label(create_file_frame, text="Skapa en ny kalender i en fil").pack(side=tk.LEFT)
		tk.Button(create_file_frame, text="Välj fil", command=self.create_single_file_calendar).pack(side=tk.LEFT)

		load_from_dir_frame.pack()
		load_from_file_frame.pack()

		create_dir_frame.pack()
		create_file_frame.pack()

	
	def create_directory_calendar(self):
		pass

	def create_single_file_calendar(self):
		file_name = filedialog.asksaveasfilename()
		
		with open(file_name, 'w', encoding='utf-8') as file:
			file.write("")
		
		calendar = Calendar()
		self.callback(calendar, LoadCalendarPage.create_save_method_for(calendar, file_name, 'file'))

	def load_calendar_from_directory(self):
		directory = filedialog.askdirectory()
		

	def load_calendar_from_file(self):
		file_name = filedialog.askopenfilename()
		try:
			calendar = SingleFileCalendarSaver.load(file_name)
			self.callback(calendar, LoadCalendarPage.create_save_method_for(calendar, file_name, 'file'))
		except Exception as e:
			messagebox.showerror("Kunde inte ladda in filen", str(e))
	
	@staticmethod
	def create_save_method_for(calendar, path, type):
		if type == 'file':
			def calendar_saver():
				SingleFileCalendarSaver.save(calendar, path)
			return  calendar_saver
		if type == 'directory':
			def calendar_saver():
				DirectoryCalendarSaver.save(calendar, path)