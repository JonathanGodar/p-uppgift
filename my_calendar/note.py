import datetime as dt
from enum import Enum

class Note():
	""" A class which stores a single line of text that is bound to a start time and an end time """
	def __init__(self, start_datetime: dt.datetime, end_datetime: dt.datetime,  note_text: str):
		""" Validates that start_datetime < end_datetime. The note text is stripped and then checked that it does not contain any new lines
		Parameters
		----------
		start_datetime : datetime.datetime
			The start time of the note
		end_datetime : datetime.datetime
			The end time of the note
		note_text : The line of 

		Raises
		------
		Exception :
			If the Note text contains new lines
			Or if the start_datetime is greater then the end_datetime
		"""

		if start_datetime > end_datetime:
			raise Exception('Could not initialize because the start datetime was after the end datetime')

		note_text = note_text.strip()
		if '\n' in note_text:
			raise Exception('Notes can only be one line. No newlines permitted')

		self.start_datetime = start_datetime 
		self.end_datetime = end_datetime 
		self.text = note_text
		
	def __str__(self):
		""" 
		Returns : 
			The note formated as a string. Note that the formating is "smart", if the end date time is more than a date after the start datetime then the
			the end datetime will be formated so that it includes day and year as well the hours and minutes it always contains. 
		"""

		TIME_FORMAT = "%Y-%m-%d %H:%M"
		
		# If the note spans more than a day we have to be more specifik about when the note ends
		end_datetime_format = "%H:%M" if self.end_datetime - self.start_datetime < dt.timedelta(days=1) else TIME_FORMAT 
		return f'{self.start_datetime.strftime(TIME_FORMAT)}-{self.end_datetime.strftime(end_datetime_format)}: {self.text}'
	
	def get_preview(self, max_char_count: int, ellipsis = "..."):
		"""
		Parameters 
		----------
		max_char_count : int
			The maximum ammount of characters that the preview may contain
		elipsis : str = "..."
			If max_chars is less than the lenght of the preview the preview will be cut down and the elipsis will be added.
		Returns
		-------
		str : 
			The preview 
		"""

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
		""" 
		Returns
		-------
		str : 
			The note serialized
		"""
		start_ser = self.start_datetime.strftime(Note.DATETIME_SERIALIZATION_FORMAT)
		end_ser = self.end_datetime.strftime(Note.DATETIME_SERIALIZATION_FORMAT)
		return f'{start_ser}-{end_ser}: {self.text}'
	
	@staticmethod
	def deserialize(serialized: str):
		""" 
		Parameters 
		----------
		serialized : 
			A serialized version of a note. See Note.serialize()

		Returns
		-------
		Note : 
			A note which was deserialized from the parameter 'serialized' 
		"""

		[start_datetime, rest] = serialized.split('-', 1)
		start_datetime = dt.datetime.strptime(start_datetime, Note.DATETIME_SERIALIZATION_FORMAT)
		[end_datetime, text] = rest.split(': ', 1)
		end_datetime = dt.datetime.strptime(end_datetime, Note.DATETIME_SERIALIZATION_FORMAT)

		return Note(start_datetime, end_datetime, text)