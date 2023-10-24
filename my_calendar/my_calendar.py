from enum import Enum
import datetime as dt
from my_calendar.note import Note
from bisect import bisect_left, bisect_right, insort
from dateutil.relativedelta import relativedelta

from time_utils import date_to_year_month_tuple, strip_days


class AddNoteResult(Enum):
	Ok = 0
	DateOverlap = 1

class RemoveNoteResult(Enum):
	Ok = 0
	NoteNotFound = 1

class Calendar:
	def __init__(self, notes:[Note]=[]):
		self.notes = Calendar.validate_and_sort_notes(notes)

	@staticmethod
	def validate_and_sort_notes(notes: [Note]) -> [Note]:
		notes.sort(key=lambda note: note.start_datetime)

		if len(notes) == 0:
			return []

		prev_note = notes[0]
		for note in notes[1:]:
			if prev_note.end_datetime > note.start_datetime:
				raise Exception(f'Kunde inte skapa kalender eftersom {prev_note.get_preview(50)} och {note.get_preview(50)} överlappar')
			
			prev_note = note
		
		return notes

	def try_add_note(self, note: Note) -> AddNoteResult:
		if self.get_overlapping_notes(note) != []:
			return AddNoteResult.DateOverlap
		
		insort(self.notes, note, key=lambda note: note.start_datetime)
		
		return AddNoteResult.Ok
	
	def get_all_notes(self) -> [Note]:
		return self.notes
	
	def get_notes_in_interval(self, interval_start: dt.datetime, interval_end: dt.datetime):
		""" Retrieves all notes that are active in a given interaval """
		left_bound = bisect_right(self.notes, interval_start, key=lambda note: note.end_datetime)
		right_bound = bisect_left(self.notes, interval_end, key=lambda note: note.start_datetime)

		if left_bound > right_bound:
			return [self.notes[right_bound]]

		return self.notes[left_bound:right_bound]
	
	def get_notes_for_month(self, date: dt.datetime):
		""" Returns all notes that start in the given month """
		search_start = strip_days(date)
		search_end = search_start + relativedelta(months=1)
		
		return self.get_notes_in_interval(search_start, search_end)
	
	def get_notes_for_date(self, date: dt.date):
		""" Returns all notes that start on the given date """
		extract_note_date_fn = lambda note: note.start_datetime.date()
		begin_index = bisect_left(self.notes, date, key=extract_note_date_fn)
		end_index = bisect_left(self.notes, date + dt.timedelta(days=1), key= extract_note_date_fn)

		return self.notes[begin_index:end_index]
	
	def constrain_int_to_notes_idx_bounds(self, idx: int) -> int:
		""" Takes an int and clamps it between 0 and len(self.notes) """
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

	def delete_note_by_start_datetime(self, date: dt.datetime) -> RemoveNoteResult:
		idx = self.find_note_by_start_datetime(date)
		if idx < 0:
			return RemoveNoteResult.NoteNotFound

		return self.delete_note_by_idx(idx)

	def delete_note_by_idx(self, index: int) -> RemoveNoteResult:
		if index < 0 or index >= len(self.notes):
			return RemoveNoteResult.NoteNotFound
		
		del self.notes[index]

		return RemoveNoteResult.Ok
	
	def get_overlapping_notes(self, note) -> [Note]:
		return self.get_notes_in_interval(note.start_datetime, note.end_datetime)

	def get_first_note_after(self, after: dt.datetime) -> Note | None:
		for note in self.notes:
			if note.start_datetime > after:
				return note 
		
		return None

	def get_first_note_before(self, before: dt.datetime) -> Note:
		note_idx = bisect_right(self.notes, before, key=lambda note: note.end_datetime) - 1
		if note_idx < 0:
			return None

		return self.notes[note_idx]

	# Returns the index of the note if it is found, other wise it returns the compliment of the last searched position (always negative)
	def find_note_by_start_datetime(self, date_to_search: dt.datetime):
		# https://docs.python.org/3/library/bisect.html
		index = bisect_left(self.notes, date_to_search, key=lambda note: note.start_datetime) 

		if index == len(self.notes) or self.notes[index].start_datetime != date_to_search:
			return ~index 

		return index
	

	



