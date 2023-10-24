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
		files = glob.glob(f'*.{DirectoryCalendarSaver.NOTE_FILE_EXTENSION}', root_dir=path) 

		notes = []
		for file in files:
			notes += SingleFileCalendarSaver.load_notes(os_path.join(path, file))
		
		return Calendar(notes)
		
	@staticmethod
	def save(calendar: Calendar, path: str): 
		# Clear any old files so that removed entries are permanently removed
		files = glob.glob(f'*.{DirectoryCalendarSaver.NOTE_FILE_EXTENSION}', root_dir=path)
		for file in files:
			os.remove(os_path.join(path,file))

		notes = calendar.get_all_notes()
		if len(notes) == 0:
			return

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
		return f'filofax-{date.strftime(DirectoryCalendarSaver.NOTE_FILE_NAME_FORMAT)}.{DirectoryCalendarSaver.NOTE_FILE_EXTENSION}'