from enum import Enum
from typing import Tuple
import tkinter as tk
from tkinter import messagebox
from gui.date_time_selection_page import SelectDateTimeFrame
from my_calendar.my_calendar import Calendar
from my_calendar.note import Note
import tkcalendar as tkcal
from gui.multipage_frame import MultipageFrame
import datetime as dt

from time_utils import strip_seconds

class AddNotePage(MultipageFrame):
	""" A Page where the user can create notes. The result (Note|None) is passed as an argument to the callback function """

	def __init__(self, root: tk.Frame, callback, preset: Note|None = None):
		super().__init__(root)
		self.callback = callback

		if preset == None:
			now = strip_seconds(dt.datetime.now())
			preset = Note(now, now + dt.timedelta(hours=1), "")

		self.create_main_page(preset)
		self.switch_to_page(self.main_page)

	def create_main_page(self, preset: Note):
		self.main_page = tk.Frame(self)

		self.start_datetime = preset.start_datetime
		self.end_datetime = preset.end_datetime

		start_datetime_frame = tk.Frame(self.main_page)
		end_datetime_frame = tk.Frame(self.main_page)

		self.start_datetime_label = tk.Label(start_datetime_frame)
		self.end_datetime_label = tk.Label(end_datetime_frame)

		change_start_datetime_button = tk.Button(start_datetime_frame, text="Ändra", 
																					 command=lambda: self.switch_to_page(SelectDateTimeFrame(self, self.on_user_input_start_time, self.start_datetime)))

		change_end_datetime_button = tk.Button(end_datetime_frame, text="Ändra", 
																				 command=lambda: self.switch_to_page(SelectDateTimeFrame(self, self.on_user_input_end_time, self.end_datetime)))

		self.start_datetime_label.pack(side=tk.LEFT)
		change_start_datetime_button.pack(side=tk.LEFT)

		self.end_datetime_label.pack(side=tk.LEFT)
		change_end_datetime_button.pack(side=tk.LEFT)

		self.note_text = tk.StringVar()
		note_text_entry = tk.Entry(self.main_page, textvariable=self.note_text)
		self.note_text.set(preset.text)
		self.update_datetime_labels()

		done_button = tk.Button(self.main_page, command=self.done, text="Spara")
		cancel_button = tk.Button(self.main_page, command=self.cancel, text="Radera och Avbryt")

		self.start_datetime_label.pack(side=tk.LEFT)
		change_start_datetime_button.pack(side=tk.LEFT)

		self.end_datetime_label.pack()
		change_end_datetime_button.pack(side=tk.LEFT)

		start_datetime_frame.pack()
		end_datetime_frame.pack()
		note_text_entry.pack(fill=tk.BOTH, padx=50)

		done_button.pack()
		cancel_button.pack()

	def cancel(self):
		self.callback(None)
	
	def done(self):
		if self.note_text.get() == "":
			messagebox.WARNING("Felaktig inmatning", "Du måste skriva något i anteckningarna")
			return

		note = Note(self.start_datetime, self.end_datetime, self.note_text.get())
		self.callback(note)
	

	def switch_to_date_time_selection(self, callback):
		""" Will show the user a page where they can select a date and a time """
		self.switch_to_page(SelectDateTimeFrame(self,callback))
		
	def on_user_input_start_time(self, new_time):
		self.switch_to_page(self.main_page)
		self.start_datetime = new_time

		if self.end_datetime < self.start_datetime:
			self.end_datetime = self.start_datetime + dt.timedelta(hours=1)

		self.update_datetime_labels()

	def on_user_input_end_time(self, new_time):
		self.switch_to_page(self.main_page)
		self.end_datetime = new_time

		if self.start_datetime > self.end_datetime:
			self.start_datetime = self.end_datetime - dt.timedelta(hours=1)

		self.update_datetime_labels()
	
	def update_datetime_labels(self):
		DATE_FORMAT = "%d/%m-%Y %H:%M"
		start_text = f'Start tid: {self.start_datetime.strftime(DATE_FORMAT)}'
		self.start_datetime_label.config(text=start_text)

		end_text = f'Slut tid: {self.end_datetime.strftime(DATE_FORMAT)}'
		self.end_datetime_label.config(text=end_text)
