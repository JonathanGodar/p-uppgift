from my_calendar.my_calendar import Calendar
from my_calendar.note import Note


class SingleFileCalendarSaver:
	""" Saves an entire calendar into a file """
	@staticmethod
	def load(path: str) -> Calendar: 
		""" Loads (deserializes) a calendar that has been serialized with SingelFileCalendarSaver.save
		Parameters
		----------
		path : str
			The path where the file that contains the serialized calendar is located


		Returns
		my_calendar.Calendar:
			The deserialized calendar
		"""
		notes = SingleFileCalendarSaver.load_notes(path)
		return Calendar(notes)

	@staticmethod
	def load_notes(path: str) -> [Note]:
		""" Loads (deserializes) a list of notes that has been serialized with SingelFileCalendarSaver.save_notes
		Parameters
		----------
		path : str
			The path where the file that contains the serialized notes is located


		Returns
		[Note]:
			The deserialized notes 
		"""
		with open(path, 'r', encoding='utf-8') as file:
			return list(map(Note.deserialize, file.readlines()))
		

	@staticmethod
	def save(calendar: Calendar, path: str): 
		""" Saves a calender to a path
		Parameters
		----------
		calendar : my_calendar.Calendar
			The calendar to serialize
		path : str
			The path to where the serialized calendar should be saved
		"""
		SingleFileCalendarSaver.save_notes(calendar.get_all_notes(), path)
	
	@staticmethod
	def save_notes(notes: [Note], path: str):
		""" Saves a lsit of notes to a path
		Parameters
		----------
		notes : [Note]
			The notes to serialize
		path : str
			The path to where the serialized notes should be saved
		"""
		with open(path, 'w', encoding='utf-8') as file:
			notes_serialized = map(lambda note: f'{note.serialize()}\n', notes)
			file.writelines(notes_serialized)