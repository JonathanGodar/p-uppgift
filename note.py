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
	def __init__(self, start_datetime: dt.datetime, end_datetime: dt.datetime,  note_text: str):
		note_text = note_text.strip()

		self.start_datetime = start_datetime 
		self.end_datetime = end_datetime 
		self.text = note_text
		
	def __str__(self):
		return f'{self.start_datetime.strftime("%Y-%m-%d %H:%M")}-{self.end_datetime.strftime("%H:%M")}: {self.text}'
	
	def get_preview(self, max_char_count: int, elipson = "..."):
		preview = f'{str(self.start_datetime)}: '
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
		raise Exception("TODO")
		return f'{str(self.start_date)}: {self.text}'
