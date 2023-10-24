from my_calendar.my_calendar import Calendar
from my_calendar.note import Note


class SingleFileCalendarSaver:
	@staticmethod
	def load(path: str): # type: ignore
		notes = SingleFileCalendarSaver.load_notes(path)
		return Calendar(notes)

	@staticmethod
	def load_notes(path: str):
		with open(path, 'r', encoding='utf-8') as file:
			return list(map(Note.deserialize, file.readlines()))
		

	@staticmethod
	def save(calendar: Calendar, path: str): 
		SingleFileCalendarSaver.save_notes(calendar.get_all_notes(), path)
	
	@staticmethod
	def save_notes(notes: [Note], path: str):
		with open(path, 'w', encoding='utf-8') as file:
			notes_serialized = map(lambda note: f'{note.serialize()}\n', notes)
			file.writelines(notes_serialized)