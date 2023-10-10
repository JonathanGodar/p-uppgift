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
		self.notes = []

	def add_note(self, note: Note) -> AddNoteResult:
		insert_position = self.find_note_by_date(note.start_date)
		if insert_position > 0:
			return AddNoteResult.DateOverlap
		
		self.notes.insert(insert_position, note)
		return AddNoteResult.Ok
	
	def constrain_int_to_notes_idx_bounds(self, idx: int) -> int:
		return min(max(idx, 0), self.get_note_count() - 1)
	
	def get_previews(self, max_char_count_per_note: int):
		previews = list(map(lambda note: note.get_preview(max_char_count_per_note), self.notes))
		return previews
	
	def get_note_count(self):
		return len(self.notes)
	
	# None if idx is out of bounds 
	def get_note_by_idx(self, index: int):
		if index < 0 or index >= len(self.notes):
			return None

		return self.notes[index]
	

	def delete_note_by_date(self, date: dt.date) -> RemoveNoteResult:
		idx = self.find_note_by_date(date)
		if idx < 0:
			return RemoveNoteResult.NoteNotFound
		return self.delete_note_by_idx(idx)

	def delete_note_by_idx(self, index: int) -> RemoveNoteResult:
		if index < 0 or index >= len(self.notes):
			return RemoveNoteResult.NoteNotFound

		return RemoveNoteResult.Ok
		
	# Returns the index of the note if found, returns the compliment of the last searched index otherwise(a negative number)
	def find_note_by_date(self, date_to_search: dt.date):
		if len(self.notes) == 0:
			return ~0

		note_dates_only = list(map(lambda note: note.start_date, self.notes))
		index = bisect_left(note_dates_only, date_to_search) 
		if note_dates_only[index] == date_to_search:
			return index
		return ~index
	
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
		notes_escaped = map(lambda note: note.serialize().replace('$', '$$'), calendar.notes)
		notes_formatted = map(lambda escaped: '$' + escaped, notes_escaped)
		
		return '\n'.join(notes_formatted)

