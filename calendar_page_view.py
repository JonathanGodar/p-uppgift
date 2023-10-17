from my_calendar import Calendar
from user_input_utils import get_alternative_from_user
import os

def calendar_page_view(calendar: Calendar, note_idx = 0):
	os.system('cls') # Credit for this line of code: ChatGPT
	note = calendar.get_note_by_idx(note_idx)
	if note == None:
		print("Det finns inga antecknignar att visa")
		return
	
	print(note)
	user_choice = get_alternative_from_user("1 - Bakåt, 2 - Frammåt, 3 - Ta bort nuvarande", ["1", "2", "3"])
	if user_choice == "1":
		note_idx -= 1 
	elif user_choice == "2":
		note_idx += 1
	elif user_choice == "3":
		calendar.delete_note_by_idx(note_idx)


	note_idx = calendar.constrain_int_to_notes_idx_bounds(note_idx)
	calendar_page_view(calendar, note_idx)