
from enum import Enum


class NotesViewWidth(Enum):
	"""An enum that describes how "wide" the notes view should be. 

	Eg. it describes if you should see one day at a time or an entire month"""

	DAY = 0
	MONTH = 1
	ALL_PAGES = 2