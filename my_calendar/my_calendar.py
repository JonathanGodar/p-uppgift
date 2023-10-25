from enum import Enum
import datetime as dt
from my_calendar.note import Note
from bisect import bisect_left, bisect_right, insort
from dateutil.relativedelta import relativedelta

from time_utils import date_to_year_month_tuple, strip_days


class AddNoteResult(Enum):
	""" A return type for functions in Calendar which add notes. Ok if the addition was  successful, something else otherwise"""
	Ok = 0
	DateOverlap = 1

class RemoveNoteResult(Enum):
	""" A return type for functions in Calendar which remove notes. Ok if the removal was successful, something else otherwise"""
	Ok = 0
	NoteNotFound = 1

class Calendar:
	""" The calendar stores a list of notes. The notes cannot overlap and are constantly sorted by start_datetime """
	def __init__(self, notes:[Note]=[]):
		""" Init the calendar 
		Parameters
		----------
		notes: [Notes]
			A list of notes that should be stored
		
		Raises
		------
		Excpetion 
			If if there are overlapping notes
		"""
		self.notes = Calendar.validate_and_sort_notes(notes)

	@staticmethod
	def validate_and_sort_notes(notes: [Note]) -> [Note]:
		""" Sorts the given notes by start time and makes sure that there are no overlapping notes
		Parameters
		----------
		notes : [Note]
			The list of notes that should be added
	
		Returns
		-------
		[Note] : 
			Sorted and validated notes
		
		"""
		notes.sort(key=lambda note: note.start_datetime)

		if len(notes) == 0:
			return []

		# Check for overlaps
		prev_note = notes[0]
		for note in notes[1:]:
			if prev_note.end_datetime > note.start_datetime:
				#									"Could not create the calendare since 												and													are overlapping"
				raise Exception(f'Kunde inte skapa kalender eftersom {prev_note.get_preview(50)} och {note.get_preview(50)} överlappar')
			prev_note = note
		
		return notes

	def try_add_note(self, note: Note) -> AddNoteResult:
		""" Tries to add a note to the calendar. Adds it in sorted order
		Parameters
		----------
		note : Note
			The note to add

		Returns
		-------
		AddNoteResult :
			AddNoteResult.Ok if the note was sucessfully added. Otherwise other variant of AddNoteResult
		"""
		if self.get_overlapping_notes(note) != []:
			return AddNoteResult.DateOverlap
		
		insort(self.notes, note, key=lambda note: note.start_datetime)
		
		return AddNoteResult.Ok
	
	def get_all_notes(self) -> [Note]:
		"""
		Returns
		-------
		[Note] : 
			A list of all notes
		"""
		return self.notes
	
	def get_notes_in_interval(self, interval_start: dt.datetime, interval_end: dt.datetime):
		""" That start before interval_end and ends after interval_start
		Parameters
		----------
		interval_start : datetime.datetime
		interval_end : datetime.datetime
		"""
		left_bound = bisect_right(self.notes, interval_start, key=lambda note: note.end_datetime)
		right_bound = bisect_left(self.notes, interval_end, key=lambda note: note.start_datetime)

		if left_bound > right_bound:
			return [self.notes[right_bound]]

		return self.notes[left_bound:right_bound]
	
	def get_notes_starting_in_interval(self, interval_start: dt.datetime, interval_end: dt.datetime):
		""" Returns all notes that start after (inclusive) interval_start but strictly before interval_end
		Parameters
		----------
		interval_start : datetime.datetime
		interval_end : datetime.datetime
		"""
		
		left_bound = bisect_left(self.notes, interval_start, key=lambda note: note.start_datetime)
		right_bound = bisect_left(self.notes, interval_end, key=lambda note: note.start_datetime)

		if left_bound > right_bound:
			return []
		
		return self.notes[left_bound:right_bound]
	
	def get_notes_for_month(self, date: dt.datetime):
		""" Returns all notes that start in the given month
		date : datetime.datetime
			A date in the wanted month
		"""
		search_start = strip_days(date)
		search_end = search_start + relativedelta(months=1)
		
		return self.get_notes_starting_in_interval(search_start, search_end)
	
	def get_notes_for_date(self, date: dt.date):
		""" Returns all notes that start on the given date 
		date : datetime.datetime
			The date which all notes should be retrieved for
		"""

		interval_start = dt.datetime.combine(date, dt.time(0, 0))
		interval_end = interval_start + relativedelta(days=1)

		return self.get_notes_starting_in_interval(interval_start, interval_end)
	
	# None if idx is out of bounds 
	def get_note_by_idx(self, index: int):
		""" Retrieves a note at a specified index
		Parameters
		----------
		index: int
		"""

		if index < 0 or index >= len(self.notes):
			return None

		return self.notes[index]

	def delete_note_by_start_datetime(self, date: dt.datetime) -> RemoveNoteResult:
		""" Deletes a note by the start datetime O(log(n))
		Parameters
		----------
		date : datetime.datetime
			The datetime for the note that should be deleted
		
		Returns
		-------
		RemoveNoteResult
			Ok if the removal was successfull. Other variants of RemoveNoteResult otherwise
		"""

		idx = self.find_note_by_start_datetime(date)
		if idx < 0:
			return RemoveNoteResult.NoteNotFound

		return self.delete_note_by_idx(idx)

	def delete_note_by_idx(self, index: int) -> RemoveNoteResult:
		""" Deletes a note by the index in the notes list
		Parameters
		----------
		index : int
		
		Returns
		-------
		RemoveNoteResult
			Ok if the removal was successfull. Other variants of RemoveNoteResult otherwise
		"""
		if index < 0 or index >= len(self.notes):
			return RemoveNoteResult.NoteNotFound
		
		del self.notes[index]

		return RemoveNoteResult.Ok
	
	def get_overlapping_notes(self, note) -> [Note]:
		""" Gets all notes that overlap with the given note
		Parameters
		----------
		note : Note
			The note for which the overlap of notes should be checked

		Returns
		-------
		[Note] :
			A list of notes that overlap with the given note
		"""
		return self.get_notes_in_interval(note.start_datetime, note.end_datetime)

	def get_first_note_after(self, after: dt.datetime) -> Note | None:
		""" Retrieves the first note that starts after the specified datetime
		Parameters
		----------
		after : datetime.datetime
		"""
		for note in self.notes:
			if note.start_datetime > after:
				return note 
		
		return None

	def get_first_note_before(self, before: dt.datetime) -> Note:
		""" Retrieves the first note that ends before the specified datetime
		Parameters
		----------
		after : datetime.datetime
		"""
		note_idx = bisect_right(self.notes, before, key=lambda note: note.end_datetime) - 1
		if note_idx < 0:
			return None

		return self.notes[note_idx]

	def find_note_by_start_datetime(self, date_to_search: dt.datetime):
		""" 
		Parameters
		----------
		date_to_search : datetime.datetime

		Returns
		-------
		int : 
			The index of the note if it is found, other wise it returns the compliment of the last searched(binary search) position (always negative) 
		
		"""

		# https://docs.python.org/3/library/bisect.html
		index = bisect_left(self.notes, date_to_search, key=lambda note: note.start_datetime) 

		if index == len(self.notes) or self.notes[index].start_datetime != date_to_search:
			return ~index 

		return index