import datetime as dt
from enum import Enum

class NoteCreationExceptionVariant(Enum):
	# end_time_before_start_time = 0
	bad_data_type_input = 1
	empty_note_text = 2

class NoteCreationException(Exception):
	def __init__(self, variant: NoteCreationExceptionVariant) -> None:
		super().__init__(variant)
		self.type = variant
	
class Note():
	def __init__(self, date: dt.date,  note_text: str):
		if not isinstance(date, dt.date) or not isinstance(note_text, str):
			raise NoteCreationException(NoteCreationExceptionVariant.bad_data_type_input)

		note_text = note_text.strip()

		if note_text == "":
			raise NoteCreationException(NoteCreationExceptionVariant.empty_note_text)

		self.start_date = date
		self.text = note_text
	
	def __str__(self):
		return f'{self.start_date.strftime("%Y-%m-%d")}: {self.text}'
	
	def get_preview(self, max_char_count: int, elipson = "..."):
		preview = f'{str(self.start_date)}: '
		if len(preview) > max_char_count:
			return preview[:max_char_count-1]
		
		
		should_have_elipson = False
		for word_to_append in self.text.split():
			# The last 1 is to account for the space that we have to add back 
			if len(word_to_append) + len(preview) + len(elipson) + 1 > max_char_count:
				should_have_elipson = True
				break

			preview += word_to_append + " "
		
		if should_have_elipson:
			preview += elipson
		return preview

	
	def serialize(self):
		return f'{str(self.start_date)}: {self.text}'
