# Niklasson Godar, Jonathan | jonathan.godar@ug.kth.se

import os
from my_calendar.my_calendar import Calendar
from my_calendar.note import Note
from my_calendar.savers.single_file_calendar_saver import SingleFileCalendarSaver
import glob
import os.path as os_path
import datetime as dt

class DirectoryCalendarSaver:
	""" Saves a Calendar in a directory. Notes that begin on the same day get saved in the same file """

	@staticmethod
	def load(path: str) -> Calendar:
		""" Loads(deserializes) a calendar that has been saved using DirectoryCalendarSaver.save 
		Parameters
		----------
		path : str
			Where the serialized calendars root dir is
		
		Returns
		-------
		my_calendar.Calendar : 
			The deserialized calendar
		"""
		# Find all files that have the .kal extension
		files = glob.glob(f'*.{DirectoryCalendarSaver.NOTE_FILE_EXTENSION}', root_dir=path) 

		# Load the notes contained in each file
		notes = []
		for file in files:
			notes += SingleFileCalendarSaver.load_notes(os_path.join(path, file))
		
		return Calendar(notes)
		
	@staticmethod
	def save(calendar: Calendar, path: str): 
		""" Saves(serializes) a calendar into a directory. It will create a file for each day that contains notes and will also save all the notes that start on that day into the created file
		Parameters 
		----------
		calendar : my_calendar.Calendar
			The calendar to save
		path : str
			The directory to where the calendar should be saved
		"""

		# Clear any old files so that removed entries are permanently removed
		files = glob.glob(f'*.{DirectoryCalendarSaver.NOTE_FILE_EXTENSION}', root_dir=path)
		for file in files:
			os.remove(os_path.join(path,file))

		notes = calendar.get_all_notes()
		if len(notes) == 0:
			return

		# Save all notes from the same day into the same file
		note = notes[0]
		while note != None:
			note_for_this_date = calendar.get_notes_for_date(note.start_datetime.date())
			save_path = os_path.join(path, DirectoryCalendarSaver.get_filename_for_date(note.start_datetime))
			SingleFileCalendarSaver.save_notes(note_for_this_date, save_path)
			note = calendar.get_first_note_after(note_for_this_date[-1].start_datetime)


	NOTE_FILE_NAME_FORMAT = "%Y_%m_%d"
	NOTE_FILE_EXTENSION="kal"
	@staticmethod
	def get_filename_for_date(date: dt.date):
		""" Gets the filename to which a note from a spacified date should be saved  to
		Parameters
		----------
		date: date_time.date
			The date to generate the filename for
		"""
		return f'filofax-{date.strftime(DirectoryCalendarSaver.NOTE_FILE_NAME_FORMAT)}.{DirectoryCalendarSaver.NOTE_FILE_EXTENSION}'