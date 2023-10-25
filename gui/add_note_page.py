# Niklasson Godar, Jonathan | jonathan.godar@ug.kth.se

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
	""" A Page where the user can create notes. NOTE: The note will have start time and end time be at the start of a minute (see date_time_selection_page). The result (Note|None) is passed as an argument to the callback function """

	def __init__(self, root: tk.Frame, callback, preset: Note|None = None):
		""" Performs setup of UI
		Parameters
		----------
		root : tkinter.Frame
			The frame to which this frame shall bind
		callback : function(Note|None) -> None
			The function that will be called once the user has selected a note. The argument will be of type None if the user choose to cancel
		preset : Note|None
			Will be the start values when this frame is opened.
			If None then preset will be Note(datetime.now(), datetime.now() + timedelata(hours=1), "")
		"""
		super().__init__(root)
		self.callback = callback

		if preset == None:
			now = strip_seconds(dt.datetime.now())
			preset = Note(now, now + dt.timedelta(hours=1), "")

		self.create_main_page(preset)
		self.switch_to_page(self.main_page)

	def create_main_page(self, preset: Note):
		""" Creates the main note creation page (Where the user can choose to edit star/end time and input the text that the note should contain)
		Parameters
		----------
		preset : Note
			The preset of the frame. See self.__init__()
		
		Additions to self
		-----------------
			main_page: tkinter.Frame
			start_datetime_label: tkinter.Label
			start_datetime: datetime.datetime
			end_datetime_label: tkinter.Label
			end_datetime: datetime.datetime
			note_text_entry: tkinkinter.Entry
			note_text: tkinter.StringVar
		"""
		self.main_page = tk.Frame(self)

		self.start_datetime = preset.start_datetime
		self.end_datetime = preset.end_datetime

		start_datetime_frame = tk.Frame(self.main_page)
		end_datetime_frame = tk.Frame(self.main_page)

		self.start_datetime_label = tk.Label(start_datetime_frame)
		self.end_datetime_label = tk.Label(end_datetime_frame)

		#																																		"Change"
		change_start_datetime_button = tk.Button(start_datetime_frame, text="Ändra", 
																					 command=lambda: self.switch_to_page(SelectDateTimeFrame(self, self.on_user_input_start_time, self.start_datetime)))

		#																																"Change"
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

		#																																"Save"
		done_button = tk.Button(self.main_page, command=self.done, text="Spara")

		#																																		"Delete and cancel"
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
		""" Cancels the creation of a note. Called when the user presses __init__.cancel_button"""
		self.callback(None)
	
	def done(self):
		""" Performas validation of the user inputed note and calls callback with the created not if validations pass """
		if self.note_text.get() == "":
			#										"Bad input",					"You have to write something in your note"
			messagebox.WARNING("Felaktig inmatning", "Du måste skriva något i anteckningarna")
			return

		note = Note(self.start_datetime, self.end_datetime, self.note_text.get())
		self.callback(note)
	

	def switch_to_date_time_selection(self, callback):
		""" Will show the user a page where they can select a date and a time
		Parameters
		----------
		callback : function(datetime) -> None
			Will be called once the user has selected a note
		"""
		self.switch_to_page(SelectDateTimeFrame(self,callback))
		
	def on_user_input_start_time(self, new_time: dt.datetime):
		""" Changes the page back to self.main page and sets the self.start_datetime to the new time. Performs some validatoins
		Parameters:
		new_time : datetime.datetime
			The new start_datetime which should be set
		"""
		self.switch_to_page(self.main_page)
		self.start_datetime = new_time

		# Move the end_time forward if it is before the start_time
		if self.end_datetime < self.start_datetime:
			self.end_datetime = self.start_datetime + dt.timedelta(hours=1)

		self.update_datetime_labels()

	def on_user_input_end_time(self, new_time: dt.datetime):
		""" Changes the page back to self.main page and sets the self.end_datetime to the new time. Performs some validatoins
		Parameters:
		new_time : datetime.datetime
			The new end_datetime which should be set
		"""
		self.switch_to_page(self.main_page)
		self.end_datetime = new_time

		# Move the start_time backwards if it is after the end_time
		if self.start_datetime > self.end_datetime:
			self.start_datetime = self.end_datetime - dt.timedelta(hours=1)

		self.update_datetime_labels()
	
	def update_datetime_labels(self):
		""" Updates the labels which shows the user which start_datetime and end_datetime are selected"""
		DATE_FORMAT = "%d/%m-%Y %H:%M"
		# 							"Start time:"
		start_text = f'Start tid: {self.start_datetime.strftime(DATE_FORMAT)}'
		self.start_datetime_label.config(text=start_text)

		# 					"End time:"
		end_text = f'Slut tid: {self.end_datetime.strftime(DATE_FORMAT)}'
		self.end_datetime_label.config(text=end_text)
