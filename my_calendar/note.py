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
		if start_datetime > end_datetime:
			raise Exception('Could not initialize because the start datetime was after the end datetime')

		note_text = note_text.strip()

		self.start_datetime = start_datetime 
		self.end_datetime = end_datetime 
		self.text = note_text
		
	def __str__(self):
		TIME_FORMAT = "%Y-%m-%d %H:%M"
		
		# If the note spans more than a day we have to be more specifik about when the note ends
		end_datetime_format = "%H:%M" if self.end_datetime - self.start_datetime < dt.timedelta(days=1) else TIME_FORMAT 
		return f'{self.start_datetime.strftime(TIME_FORMAT)}-{self.end_datetime.strftime(end_datetime_format)}: {self.text}'
	
	def get_preview(self, max_char_count: int, ellipsis = "..."):
		preview = f'{self.start_datetime.strftime("%y-%m-%d %H:%M")}: '
		if len(preview) > max_char_count:
			return preview[:max_char_count-1]
		
		
		should_have_ellipsis = False
		for word_to_append in self.text.split():
			# The last 1 is to account for the space that we have to add back 
			if len(word_to_append) + len(preview) + len(ellipsis) + 1 > max_char_count:
				should_have_ellipsis = True
				break

			preview += word_to_append + " "
		
		if should_have_ellipsis:
			preview += ellipsis
		return preview

	DATETIME_SERIALIZATION_FORMAT = "%Y/%m/%d %H:%M"
	def serialize(self) -> str:
		start_ser = self.start_datetime.strftime(Note.DATETIME_SERIALIZATION_FORMAT)
		end_ser = self.end_datetime.strftime(Note.DATETIME_SERIALIZATION_FORMAT)
		return f'{start_ser}-{end_ser}: {self.text}'
	
	@staticmethod
	def deserialize(serialized: str):
		[start_datetime, rest] = serialized.split('-', 1)
		start_datetime = dt.datetime.strptime(start_datetime, Note.DATETIME_SERIALIZATION_FORMAT)
		[end_datetime, text] = rest.split(': ', 1)
		end_datetime = dt.datetime.strptime(end_datetime, Note.DATETIME_SERIALIZATION_FORMAT)

		return Note(start_datetime, end_datetime, text)