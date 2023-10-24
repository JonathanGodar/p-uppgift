from enum import Enum
from typing import Tuple
import tkinter as tk
from tkinter import messagebox
from my_calendar.my_calendar import Calendar
from my_calendar.note import Note
import tkcalendar as tkcal
from gui.multipage_frame import MultipageFrame
import datetime as dt

from time_utils import strip_seconds

class AddNotePage(MultipageFrame):
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

		self.start_datetime_label.pack(side=tk.LEFT)
		change_start_datetime_button.pack(side=tk.LEFT)

		self.end_datetime_label.pack()
		change_end_datetime_button.pack(side=tk.LEFT)

		start_datetime_frame.pack()
		end_datetime_frame.pack()
		note_text_entry.pack(fill=tk.BOTH, padx=50)
		done_button.pack()
	
	def done(self):
		note = Note(self.start_datetime, self.end_datetime, self.note_text.get())
		self.callback(note)
	

	def switch_to_date_time_selection(self, callback):
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

class SelectDateTimeFrame(tk.Frame):
	def __init__(self, root: tk.Frame, callback, preset: dt.datetime = dt.datetime.now()):
		super().__init__(root)
		self.callback = callback

		preset = strip_seconds(preset)
		self.calendar = tkcal.Calendar(self)
		self.calendar.selection_set(preset.date())

		self.time_str = tk.StringVar() 
		time_label = tk.Label(self, text='Tid(HH:MM):)')
		time_entry = tk.Entry(self, textvariable=self.time_str)
		self.time_str.set(preset.strftime('%H:%M'))

		done_button = tk.Button(self, text='Klar', command=self.done)

		self.calendar.pack()
		time_label.pack(side=tk.LEFT)
		time_entry.pack(side=tk.LEFT)
		done_button.pack()
	
	def done(self):
		time_parsed = self.try_parse_time_entry()

		if time_parsed == None:
			messagebox.showerror("Felaktig inmatning", "Tiden i tid rutan måste vara i formatet 00:00, (TIMME:MINUT)")
			return
		
		selected_date = self.calendar.selection_get()
		if selected_date == None:
			messagebox.showerror("Inget datum valt", "Du måste välja ett datum i kalendern för att kunna gå vidare")
			return
		
		# https://stackoverflow.com/questions/1937622/convert-date-to-datetime-in-python
		date_time = dt.datetime(year=selected_date.year, month=selected_date.month, day=selected_date.day, hour=time_parsed[0], minute=time_parsed[1])
		self.callback(date_time)
	
	def try_parse_time_entry(self) -> None | Tuple[int, int]:
		try: 
			[hour_str, minute_str]= self.time_str.get().split(":")
			hour = int(hour_str)
			min = int(minute_str)

			if hour < 0 or hour > 23 or min < 0 or min > 59:
				return None			

			return (hour, min)
		except:
			pass
	# def display_invalid_time_input_messagebox(self):