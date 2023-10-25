from typing import Tuple
import tkinter as tk
import datetime as dt
import tkcalendar as tkcal
from tkinter import messagebox

from time_utils import strip_seconds

class SelectDateTimeFrame(tk.Frame):
	""" A page where the user can input date and time(HH:MM no seconds or millis). The result is passed as an argument to the "callback" function"""

	def __init__(self, root: tk.Frame, callback, preset: dt.datetime = dt.datetime.now()):
		""" Sets up the UI, callbacks and binds 
		Parameters
		----------
		root : tk.Frame:
			The parent frame which this frame should attach to
		callback : function(datetime) -> None
			Will be called once the user has selected a date and a time. NOTE: This class always leaves the seconds and miliseconds to zero
		preset : datetime
			The datetime should be selected once the frame opens. Defaults datetime.now()
		"""

		super().__init__(root)
		self.callback = callback

		preset = strip_seconds(preset)
		self.calendar = tkcal.Calendar(self)
		self.calendar.selection_set(preset.date())

		self.time_str = tk.StringVar() 
		
		#																	"Time(HH:MM)"
		time_label = tk.Label(self, text='Tid(HH:MM):)')
		time_entry = tk.Entry(self, textvariable=self.time_str)
		self.time_str.set(preset.strftime('%H:%M'))

		#																	"Done"
		done_button = tk.Button(self, text='Klar', command=self.done)

		self.calendar.pack()
		time_label.pack(side=tk.LEFT)
		time_entry.pack(side=tk.LEFT)
		done_button.pack()
	
	def done(self):
		""" Called when the user presses the "done" button. If validation checks are passed this function will call self.callback"""
		
		# Perform validation of input
		time_parsed = self.try_parse_time_entry()

		if time_parsed == None:
			#										"Bad input", 						"Time time in the box should be in the format 00:00 (HOUR:MINUTE)"
			messagebox.showerror("Felaktig inmatning", "Tiden i tid rutan måste vara i formatet 00:00, (TIMME:MINUT)")
			return
		
		selected_date = self.calendar.selection_get()
		if selected_date == None:
			#											"No date selected", "You have to choose a date in the calendar to proceed"
			messagebox.showerror("Inget datum valt", "Du måste välja ett datum i kalendern för att kunna gå vidare")
			return
		
		# https://stackoverflow.com/questions/1937622/convert-date-to-datetime-in-python
		date_time = dt.datetime(year=selected_date.year, month=selected_date.month, day=selected_date.day, hour=time_parsed[0], minute=time_parsed[1])
		self.callback(date_time)
	
	def try_parse_time_entry(self) -> None | Tuple[int, int]:
		""" Tries to parse the hour and minute that the user has entered in self.time_entry 
		Returns:
		None : 
			If the user has not entered a correct date and time
		Tuple[int, int] :
			If the user has entered a correct date and time. The first int is the hour and the second the minutes

		"""

		try: 
			[hour_str, minute_str]= self.time_str.get().split(":")
			hour = int(hour_str)
			min = int(minute_str)

			if hour < 0 or hour > 23 or min < 0 or min > 59:
				return None			

			return (hour, min)
		except:
			return None