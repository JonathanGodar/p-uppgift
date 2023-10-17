from enum import Enum
import datetime as dt
from note import Note
from bisect import bisect_left


class AddNoteResult(Enum):
	Ok = 0
	DateOverlap = 1

class RemoveNoteResult(Enum):
	Ok = 0
	NoteNotFound = 1


# class CalendarException(Exception):
# 	def __init__(self, variant: CalendarExceptionVariant) -> None:
# 		super().__init__(variant)
# 		self.type = variant

# class CalendarCursor:
# 	def __init__(self, constrain_index_to_bounds: ) -> None:
# 		self.cursor = 0
	
# 	def move_left():
	
	# def add_note(self, note):
	# 	add_result = self.calendar.add_note(note)
	# 	if add_result == AddNoteResult.Ok:
	# 		if self.calendar.find_note_by_date(note) <= self.cursor:
	# 			self.move_forwards()
	
	# Possibly None
	# def get_selected_note(self):
	# 	return self.calendar.get_note_by_idx(self.cursor)
	
	# def delete_selected_note(self):
	# 	delete_result = self.calendar.delete_note_by_idx(self.cursor)
	# 	self.__constrain_cursor_to_bounds()
	# 	return delete_result

	# def __constrain_cursor_to_bounds(self):
	# 	new_idx = min(max(self.cursor, 0), self.calendar.get_note_count())
	# 	self.cursor = new_idx

	# def move_forwards(self):
	# 	self.cursor += 1
	# 	self.__constrain_cursor_to_bounds()

	# def move_backwars(self):
	# 	self.cursor -= 1
	# 	self.__constrain_cursor_to_bounds

class Calendar:
	def __init__(self):
		self.__notes = []

	def add_note(self, note: Note) -> AddNoteResult:
		self.find_note_by_date(note.start_date)
		if insert_position > 0:
			return AddNoteResult.DateOverlap
		
		self.__notes.insert(insert_position, note)
		return AddNoteResult.Ok
	
	def constrain_int_to_notes_idx_bounds(self, idx: int) -> int:
		return min(max(idx, 0), self.get_note_count() - 1)
	
	def get_previews(self, max_char_count_per_note: int):
		previews = list(map(lambda note: note.get_preview(max_char_count_per_note), self.__notes))
		return previews
	
	def get_note_count(self):
		return len(self.__notes)
	
	# None if idx is out of bounds 
	def get_note_by_idx(self, index: int):
		if index < 0 or index >= len(self.__notes):
			return None

		return self.__notes[index]
	

	def delete_note_by_date(self, date: dt.date) -> RemoveNoteResult:
		try:
				idx = self.find_note_by_date(date)
				return self.delete_note_by_idx(idx)
		except:
			return RemoveNoteResult.NoteNotFound

	def delete_note_by_idx(self, index: int) -> RemoveNoteResult:
		if index < 0 or index >= len(self.__notes):
			return RemoveNoteResult.NoteNotFound

		return RemoveNoteResult.Ok
		
	
	def date_overlap(self, date_to_search):
		try:
			self.find_note_by_date(date_to_search)
			return True
		except:
			return False

	# Returns the index of the note if found, returns the compliment of the last searched index otherwise(a negative number)
	def find_note_by_date(self, date_to_search: dt.date):
		note_dates_only = list(map(lambda note: note.start_date, self.__notes))

		# https://docs.python.org/3/library/bisect.html
		index = bisect_left(note_dates_only, date_to_search) 

		if index == len(note_dates_only) or note_dates_only[index] != date_to_search:
			raise ValueError

		return index
	

	
class DirectoryCalendarSaver:
	@staticmethod
	def load(path: str): # type: ignore
		pass 

	@staticmethod
	def save(calendar: Calendar, path: str): # type: ignore
		pass


class SingleFileCalendarSaver:
	@staticmethod
	def load(path: str): # type: ignore
		pass 

	@staticmethod
	def save(calendar: Calendar, path: str): 
		pass
		# with open()
		# 	calendar.serialize()

	@staticmethod
	def __serialize_calendar(calendar: Calendar): 
		# We escape the $ symbol with as $$ such that the program can deserialize the file unambiguesly
		notes_escaped = map(lambda note: note.serialize().replace('$', '$$'), calendar.__notes)
		notes_formatted = map(lambda escaped: '$' + escaped, notes_escaped)
		
		return '\n'.join(notes_formatted)

